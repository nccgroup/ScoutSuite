from flask import Flask, request, Response, make_response, jsonify, abort
from flask_cors import CORS
from ScoutSuite.utils import format_service_name

import csv, io, json

def start_api(results, exceptions=None):
    app = Flask(__name__, 
            static_url_path='', 
            static_folder='../web_report')
    CORS(app)

    @app.route('/', methods=['GET'])
    def home():
        return app.send_static_file('index.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return app.send_static_file('index.html')

    @app.route('/api', methods=['GET'])
    def api():
        return jsonify(results)

    @app.route('/api/services/<service>/findings', methods=['GET'])
    def get_findings(service):
        if service not in results['services']:
            return Response('Pro feature', status=402)
        findings = results['services'][service]['findings']
        for finding in findings:
            findings[finding]['name'] = finding
            if findings[finding]['dashboard_name'] == 'Password policy':
                findings[finding]['redirect_to'] = '/services/iam/password_policy'
        
        return jsonify(list(findings.values()))

    # Paginated
    @app.route('/api/services/<service>/findings/<finding>/items', methods=['GET'])
    def get_items(service, finding):
        item_list = get_all_items_in_finding(service, finding, results)

        return jsonify(process_results(item_list))

    @app.route('/api/services/<service>/findings/<finding>/items/options/<attribute>')
    def get_findings_items_attribute_options(service, finding, attribute):
        item_list = get_all_items_in_finding(service, finding, results)
        
        return get_attribute_options(attribute, item_list, results)

    @app.route('/api/services/<service>/findings/<finding>/items/<item_id>', methods=['GET'])
    def get_issue_paths(service, finding, item_id):
        path = request.args.get('path')
        items = results['services'][service]['findings'][finding]['items']
        issue_paths = []
        for item_path in items:
            if (path == item_path):
                issue_paths.append('ALL')
            if (path in item_path):
                issue_path = item_path.split(path)[1][1:]
                issue_paths.append(issue_path)

        words = path.split('.')
        item_path_with_brackets = results['services']
        for idx in range(len(words)):
            item_path_with_brackets = item_path_with_brackets[words[idx]]

        issue_paths_and_item = {
            'path_to_issues': issue_paths,
            'item': item_path_with_brackets,
        }

        return jsonify(issue_paths_and_item)

    @app.route('/api/services/', methods=['GET'])
    def get_services():
        metadata = results['metadata']
        category_list = []

        for category in metadata:
            services = metadata[category]
            service_list = []
            category_dashboard = []
            for service in services:
                resource_list = []
                if service == 'summaries':
                    for dashboard_type in services[service]:
                        category_dashboard.append(dashboard_type)
                else:
                    service_id = service
                    dashboard = ['findings']

                    if 'resources' in services[service]:
                        resources = services[service]['resources']
                        for resource in resources:
                            count = None if 'count' not in services[service]['resources'][resource] else services[service]['resources'][resource]['count']
                            resource_info = {
                                'id': resource,
                                'name': format_title(resource),
                                'count': count
                            }
                            resource_list.append(resource_info)

                    if 'summaries' in services[service]:
                        dashboard_types = services[service]['summaries']
                        for dashboard_type in dashboard_types:
                            dashboard.append(dashboard_type)

                    service_info = {
                        'id': service,
                        'name': format_service_name(service),
                        'dashboards': dashboard,
                        'resources': resource_list
                    }
                    service_list.append(service_info)
                
            category_info = {
                'id': category,
                'name': category[0].upper() + category[1:],
                'services': service_list
            }
            if category_dashboard: category_info['dashboard'] = category_dashboard
            category_list.append(category_info)
        
        return jsonify(category_list)

    @app.route('/api/provider', methods=['GET'])
    def get_provider():
        provider_info = {
            'account_id':results['account_id'],
            'environment':results['environment'],
            'provider_code':results['provider_code'],
            'provider_name': results['provider_name']
        }
        return jsonify(provider_info)

    @app.route('/api/execution-details', methods=['GET'])
    def get_execution_details():
        execution_details = {
            'provider_name': results['provider_name'],
            'time': results['last_run']['time'],
            'version': results['last_run']['version'],
            "ruleset_about": results['last_run']['ruleset_about'],
            "ruleset_name": results['last_run']['ruleset_name']
        }
        return jsonify(execution_details)

    @app.route('/api/dashboard', methods=['GET'])
    def get_dashboard():
        summary = results['last_run']['summary']
        service_list = []
        for summary_service in summary:
            issues = {
                'Critical': 0,
                'High': 0,
                'Medium': 0,
                'Low': 0,
                'Good': 0
            }
            findings = results['services'][summary_service]['findings']
            for rule in findings:
                if findings[rule]['items']:
                    issue_level = findings[rule]['level']
                    if issue_level == 'danger': issues['High'] += 1
                    if issue_level == 'warning': issues['Medium'] += 1
                else:
                    issues['Good'] += 1

            summary_service_object = summary[summary_service]
            service_info = {
                'id': summary_service,
                'name': format_service_name(summary_service),
                'issues': issues,
                'resources': summary_service_object['resources_count'],
                'rules': summary_service_object['rules_count'],
                'flagged-items': summary_service_object['flagged_items']
            }
            service_list.append(service_info)

        return jsonify(service_list)

    # Paginated
    @app.route('/api/services/<service>/resources/<resource>')
    def get_resources(service, resource):
        all_resources, resource_path = get_all_resources(service, resource, results)
        resource_list = [list(fetched_resource.values())[0] for fetched_resource in all_resources]
        for resource_data in resource_list: resource_data['display_path'] = resource_path

        return jsonify(process_results(resource_list))

    @app.route('/api/services/<service>/resources/<resource>/options/<attribute>')
    def get_resources_attribute_options(service, resource, attribute):
        all_resources, resource_path = get_all_resources(service, resource, results)
        resource_list = [list(fetched_resource.values())[0] for fetched_resource in all_resources]
        
        return get_attribute_options(attribute, resource_list, results)

    @app.route('/api/services/<service>/resources/<resource>/<resource_id>')
    def get_resource(service, resource, resource_id):
        all_resources = get_all_resources(service,resource, results)[0]
        for retrieved_resource in all_resources:
            if list(retrieved_resource.keys())[0] == resource_id:
                if not list(retrieved_resource.values())[0]['id']:
                    retrieved_resource.values()[0]['id'] = resource_id
                return jsonify(list(retrieved_resource.values())[0])
        return {}

    @app.route('/api/services/<service>/resources/<resource>/download')
    def download_resource(service, resource):
        resource_list = [list(fetched_resource.values())[0] for fetched_resource in get_all_resources(service, resource, results)[0]]
        response = download_filtered_elements(resource_list, f'{resource}')

        return response

    @app.route('/api/services/<service>/findings/<finding>/items/download')
    def download_items(service, finding):
        item_list = get_all_items_in_finding(service, finding, results)
        response = download_filtered_elements(item_list, f'{finding}_items')

        return response

    @app.route('/api/categories/<category>/<policy_type>')
    def get_category_policy_type(category, policy_type):
        metadata = results['metadata']
        if policy_type == 'external_attack_surface': policy_type = 'external attack surface'

        for category_metadata in metadata:
            if category_metadata == category:
                summaries = metadata[category]['summaries']
                policy_path = summaries[policy_type]['path']

                return get_element_from_path(policy_path, results)

    @app.route('/api/services/<service>/<policy_type>')
    def get_service_policy_type(service, policy_type):
        metadata = results['metadata']
        if policy_type == 'external_attack_surface': policy_type = 'external attack surface'

        for category in metadata:
            services = metadata[category]
            for service_metadata in services:
                if service_metadata == service:
                    summaries = services[service]['summaries']
                    policy_path = summaries[policy_type]['path']

                    return get_element_from_path(policy_path, results)

    @app.route('/api/exceptions')
    def get_exceptions():
        if not exceptions: return {}
        return exceptions

    @app.route('/api/raw/<path:path_to_element>', methods=['GET'])
    def get_raw_info(path_to_element):
        words = path_to_element.split('/')
        path_to_elemnt_in_brackets = results

        for idx in range(len(words)):
            path_to_elemnt_in_brackets = path_to_elemnt_in_brackets[words[idx]]

        return jsonify(path_to_elemnt_in_brackets)

    @app.route('/health', methods=['GET'])
    def check_server_health():
        return 'OK'

    app.run()

def get_attributes_from_path(path):
    attributes = []
    words = path.split('.')
    for idx, word in enumerate(words):
        if word == 'id':
            attributes.append(words[idx-1])

    return attributes

def get_all_items_in_finding(service, finding, results):
    item_list = []
    finding = results['services'][service]['findings'][finding]

    if not finding['items']:
        return jsonify([])

    path = finding['display_path'] if 'display_path' in finding else finding['path'] # storageaccounts.subscriptions.id.storage_accounts.id
    attributes = get_attributes_from_path(path)[:-1] # ['subscriptions']

    for item_path in finding['items']:
        item_path_kw = item_path.split('.') # [storageaccounts, subscriptions, c4596cb7-805b-49aa-9a04-ed74e9f5c789, storage_accounts, e21374e58a7142b3bc563467ac097f66345454fd, blob_containers, test, public_access_allowed]
        if 'id_suffix' in finding and item_path_kw[-1] == finding['id_suffix']: item_path_kw = item_path_kw[:-1]

        item_to_display = get_element_from_path_kw(item_path_kw[:len(path.split('.'))], results['services'])
        item = {
            'name': item_to_display['name'],
            'display_path': '.'.join(item_path_kw[:len(path.split('.'))])
        }
        if 'id' in item_to_display: item['id'] = item_to_display['id']
    
        for attribute in attributes:
            attribute_idx = item_path_kw.index(attribute)
            item[attribute[:-1]] = item_path_kw[attribute_idx + 1]
        
        item_list.append(item)

    return item_list

def get_all_elements_from_path(path, report_location):
    path_keywords = path.split('.')
    element_path_with_brackets = report_location
    element_list = []
    subelement_list = []

    id_locations = [id_index for id_index, x in enumerate(path_keywords) if x == 'id'] # [3, 5]

    if not id_locations:
        elements = get_element_from_path(path, report_location)
        for element in elements:
            new_element = {element: elements[element]}
            new_element[element]['path'] = path + f'.{element}'
            element_list.append(new_element)
        return element_list

    for id_idx in range(len(id_locations)):
        subelement_list.append([])
        if id_idx == 0:
            path_to_element = path_keywords[:id_locations[id_idx]]
            element = get_element_from_path_kw(path_to_element, report_location)
            for subelement in element:
                if element[subelement]:
                    subelement_list[id_idx].append(element[subelement])
                    subelement_list[id_idx][-1]['path'] = path_keywords[0:id_locations[id_idx]] + [subelement]

        else:
            for idx, element in enumerate(subelement_list[id_idx - 1]):
                path_to_element = path_keywords[id_locations[id_idx - 1] + 1:id_locations[id_idx]]
                new_element = get_element_from_path_kw(path_to_element, element)
                for element_dict in new_element: new_element[element_dict]['path'] = subelement_list[id_idx - 1][idx]['path'] + path_to_element
                subelement_list[id_idx - 1][idx] = new_element

                for subelement in subelement_list[id_idx - 1][idx]:
                    if subelement_list[id_idx - 1][idx][subelement]:
                        subelement_list[id_idx].append(subelement_list[id_idx - 1][idx][subelement])
                        subelement_list[id_idx][-1]['path'] = subelement_list[id_idx - 1][idx][subelement]['path'] + [subelement]

        if id_idx == len(id_locations) - 1:
            for subelement in subelement_list[id_idx]:
                path_to_element = path_keywords[id_locations[id_idx] + 1:len(path_keywords)]
                element = get_element_from_path_kw(path_to_element, subelement)
                if element: 
                    if len(element) > 1:
                        for individual_element in element:
                            element_list.append({individual_element: element[individual_element]})
                            element_list[-1][individual_element]['path'] = '.'.join(subelement['path'] + path_to_element + [individual_element])
                    else:
                        element_list.append(element)
                        for element_dict in element:
                            element_list[-1][element_dict]['path'] = '.'.join(subelement['path'] + path_to_element + [element_dict])
    
    return element_list

def get_all_resources(service, resource, results):
    metadata = results['metadata']

    for category in metadata:
        services = metadata[category]
        for service_metadata in services:
            if service_metadata == service:
                resources = services[service]['resources']
                for resource_metadata in resources:
                    if resource_metadata == resource:
                        resource_path = resources[resource]['path']
                        return (get_all_elements_from_path(resource_path, results), resource_path)
    return []

def download_filtered_elements(element_list, filename):
    download_type = request.args.get('type') if request.args.get('type') else 'json'
    filtered_list = filter_results(element_list)
    searched_list = search_results(filtered_list)
    
    data = (dict_to_csv(searched_list), 'csv', 'text/csv') if download_type == 'csv' else (jsonify(searched_list), 'json', 'application/json')
    response = make_response(data[0])
    response.headers['Content-Disposition'] = f'attachment; filename={filename}.{data[1]}'
    response.mimetype = data[2]

    return response

def format_title(title):
    return title[0].upper() + ' '.join(title[1:].lower().split('_'))

def dict_to_csv(dict_list):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(dict_list[0].keys()), delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    writer.writerows(dict_list)
    
    return output.getvalue()

def get_element_from_path(path, report_location):
    return get_element_from_path_kw(path.split('.'), report_location)

def get_element_from_path_kw(path, report_location):
    element = report_location
    for idx in range(len(path)):
        element = element[path[idx]]
    
    return element

def get_attribute_options(attribute, items, results):
    option_list = []
    for item in items:
        if attribute in item and item[attribute] not in option_list:
            option_list.append(item[attribute])

    return jsonify(option_list)

def filter_results(results):
    filter_by = json.loads(dict(request.args)['filter_by']) if request.args.get('filter_by') else {}
    if not filter_by: return results

    filtered_results = []
    for element in results:
        shared_items = {filter_param: filter_by[filter_param] for filter_param in filter_by if filter_param in element and filter_by[filter_param] == element[filter_param]}
        if shared_items == filter_by: filtered_results.append(element)

    return filtered_results

def search_results(results):
    search_kw = request.args.get('search') if request.args.get('search') else ''
    if not search_kw: return results

    search_properties = ['name', 'id']
    search_results = []
    for element in results:
        for search_property in search_properties:
            if search_property in element and search_kw in element[search_property]:
                search_results.append(element)
                break

    return search_results

def sort_results(results):
    sort_by = request.args.get('sort_by') if request.args.get('sort_by') else 'name'
    order_by = request.args.get('order_by') if request.args.get('order_by') else 'asc'

    return sorted(results, key=lambda k: k[sort_by], reverse=(order_by=='desc'))

def paginate_results(results):
    items_per_page = int(request.args.get('limit')) if request.args.get('limit') else 10
    current_page = int(request.args.get('current_page')) if request.args.get('current_page') else 1

    paginated_results = [results[i:i + items_per_page] for i in range(0, len(results), items_per_page)]
    page_results = {
        'meta': {
            'current_page': current_page,
            'next_page': current_page + 1 if current_page < len(paginated_results) else None,
            'prev_page': current_page - 1 if current_page > 1 else None,
            'total_pages': len(paginated_results),
            'limit': items_per_page
        },
        'results': paginated_results[current_page - 1] if paginated_results else []
    }

    return page_results

def process_results(results):
    filtered_results = filter_results(results)
    searched_results = search_results(filtered_results)
    sorted_results = sort_results(searched_results)
    paginated_results = paginate_results(sorted_results)

    return paginated_results
