from flask import Flask, request, Response, make_response, jsonify, abort
from flask_restx import Api, Resource as RestxResource
from flask_cors import CORS
from ScoutSuite.utils import format_service_name

import csv, io, json, logging, sys

def start_api(results, exceptions=None):
    app = Flask(__name__, 
            static_url_path='', 
            static_folder='../web_report')
    api = Api(app, title='ScoutSuite API', description='Documentation for ScoutSuite API',doc='/api-docs')
    CORS(app)

    # Comment out the following 5 lines to view server requests in shell
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    app.logger.disabled = True
    log = logging.getLogger('werkzeug')
    log.disabled = True

    @app.route('/', methods=['GET'])
    def home():
        return app.send_static_file('index.html')

    # For all 404 paths, if it starts with /api/ return 404
    # Else let the front-end display its own 404 page
    @app.errorhandler(404)
    def page_not_found(e):
        if request.path.startswith('/api/'): return Response('Not found', status=404)
        return app.send_static_file('index.html')

    @api.route('/api')
    @api.doc(
        description='Return the whole report as JSON object.')
    class API(RestxResource):  
        def get(self):
            return jsonify(results)

    @api.route('/api/services/<service>/findings')
    @api.doc(
        params={
            'service': {
                'description': 'A provider service',
                'example':'ec2'}},
        description='Return the list of findings for a specific service.')
    class Findings(RestxResource):
        def get(self, service):
            findings = results['services'][service]['findings']
            for finding in findings:
                findings[finding]['name'] = finding
                # Password_policy needs to be redirected to its partial
                if findings[finding]['dashboard_name'] == 'Password policy':
                    findings[finding]['redirect_to'] = '/services/iam/password_policy'
            
            return jsonify(list(findings.values()))

    @api.route('/api/services/<service>/findings/<finding>/items')
    @api.doc(
        params={
            'service': {
                'description': 'A provider service',
                'example':'ec2'},
            'finding': {
                'description': 'A service finding',
                'example':'ec2-security-group-opens-all-ports'}},
        description='Return the list of items for a specific finding of a specific service.')
    class Items(RestxResource):
        def get(self, service, finding):
            item_list = get_all_items_in_finding(service, finding, results)

            return jsonify(process_results(item_list))

    @api.route('/api/services/<service>/findings/<finding>/items/options/<attribute>')
    @api.doc(
        params={
            'service': {
                'description': 'A provider service',
                'example':'rds'},
            'finding': {
                'description': 'A service finding',
                'example':'rds-instance-single-az'},
            'attribute': {
                'description': 'An attribute contained in item',
                'example':'vpc'}},
        description='Return a list of values an attribute can take for a specific finding of a specific service.')
    class ItemsAttributeOptions(RestxResource):
        def get(self, service, finding, attribute):
            item_list = get_all_items_in_finding(service, finding, results)
            
            return get_attribute_options(attribute, item_list, results)

    @api.route('/api/services/<service>/findings/<finding>/items/<item_id>')
    @api.doc(
        params={
            'service': {
                'description': 'A provider service',
                'example':'ec2'},
            'finding': {
                'description': 'A service finding',
                'example':'ec2-security-group-opens-all-ports'},
            'item_id': {
                'description': 'The ID of an item',
                'example':'ec2.regions.ap-northeast-1.vpcs.vpc-edd0d68a.security_groups.sg-495d7a3b.rules.ingress.protocols.ALL.ports.1-65535'}},
        description='Return a specific item of a specific finding of a specific service.')
    class Item(RestxResource):
        def get(self, service, finding, item_id):
            element_path = request.args.get('path')
            items = results['services'][service]['findings'][finding]['items']
            issue_paths = []
            for item_path in items:
                # If the element path is the whole item path, send 'ALL'
                if (element_path == item_path):
                    issue_paths.append('ALL')
                # If the element path is a substring of the item path, send the tail of the item path
                if (element_path in item_path):
                    issue_path = item_path.split(element_path)[1][1:]
                    issue_paths.append(issue_path)

            issue_paths_and_item = {
                'path_to_issues': issue_paths,
                'item': get_element_from_path(element_path, results['services'])
            }

            return jsonify(issue_paths_and_item)

    @api.route('/api/services')
    @api.doc(
        description='Return the list of service categories and each of their services with information\
            extracted from the metadata object of the report.')
    class Services(RestxResource):
        def get(self):
            metadata = results['metadata']
            category_list = []

            for category in metadata:
                services = metadata[category]
                service_list = []
                category_dashboard = []
                for service in services:
                    resource_list = []
                    # If a dashboard exists in a specific category, append all dashboard types to category_dashboard
                    if service == 'summaries':
                        for dashboard_type in services['summaries']:
                            category_dashboard.append(dashboard_type)
                    else:
                        # The 'findings' dashboard is included for all services
                        service_dashboard = ['findings']

                        # Get each resource's information and append to resource_list
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

                        # If a dashboard exists in a specific service, append all dashboard types to category_dashboard
                        if 'summaries' in services[service]:
                            for dashboard_type in services[service]['summaries']:
                                service_dashboard.append(dashboard_type)
                        
                        pro_feature = service not in results['services']
                        
                        service_info = {
                            'id': service,
                            'name': format_service_name(service),
                            'dashboards': service_dashboard,
                            'resources': resource_list,
                            'pro_feature': pro_feature
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

    @api.route('/api/provider')
    @api.doc(description='Return provider information.')
    class Provider(RestxResource):
        def get(self):
            provider_info = {
                'account_id':results['account_id'],
                'environment':results['environment'],
                'provider_code':results['provider_code'],
                'provider_name': results['provider_name']
            }
            return jsonify(provider_info)

    @api.route('/api/execution-details')
    @api.doc(description='Return report''s execution details.')
    class ExecutionDetails(RestxResource):
        def get(self):
            execution_details = {
                'provider_name': results['provider_name'],
                'time': results['last_run']['time'],
                'version': results['last_run']['version'],
                "ruleset_about": results['last_run']['ruleset_about'],
                "ruleset_name": results['last_run']['ruleset_name']
            }
            return jsonify(execution_details)

    @api.route('/api/dashboard')
    @api.doc(
        description='Return information used in the main dashboard such as the breakdown of\
            the issues based on their level of risk.')
    class Dashboard(RestxResource):
        def get(self):
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
                
                # For every finding where there's at least one item, add it to 'issues'
                # with its corresponding issue level
                findings = results['services'][summary_service]['findings']
                for finding in findings:
                    if findings[finding]['items']:
                        issue_level = findings[finding]['level']
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

    @api.route('/api/services/<service>/resources/<resource>')
    @api.doc(
    params={
            'service': {
                'description': 'A provider service',
                'example':'ec2'},
            'resource': {
                'description': 'A resource of a service',
                'example':'volumes'},
            'limit': {
                'description': 'Number of resources to return',
                'example': 5,
                'default': 10},
            'current_page': {
                'description': 'Page number if return results have multiple pages',
                'example': 3,
                'default': 1},
            'sort_by': {
                'description': 'Property of the resource to sort by',
                'example':'id',
                'default':'name'},
            'order_by': {
                'description': 'Sort results in ascending or descending order (asc or desc)',
                'example': 'desc',
                'default':'asc'},
            'search': {
                'description': 'Search in name or id properties',
                'example':'test'},
            'filter_by': {
                'description': 'Return results containing a specific property value',
                'example':'{"region":"us-east-1"}'}
            },
    description='Return a list of resources of a specific resource type of a specific service.')
    class Resources(RestxResource):
        def get(self, service, resource):
            all_resources, resource_path = get_all_resources(service, resource, results)
            resource_list = [list(fetched_resource.values())[0] for fetched_resource in all_resources]
            for resource_data in resource_list: resource_data['display_path'] = resource_path

            return jsonify(process_results(resource_list))

    @api.route('/api/services/<service>/resources/<resource>/options/<attribute>')
    @api.doc(
        params={
            'service': {
                'description': 'A provider service',
                'example':'ec2'},
            'resource': {
                'description': 'A resource of a service',
                'example':'instances'},
            'attribute': {
                'description': 'An attribute contained in item',
                'example':'SubnetId'}},
        description='Return a list of values an attribute can take for a specific resource of a specific service.')
    class ResourcesAttributeOptions(RestxResource):
        def get(self, service, resource, attribute):
            all_resources, resource_path = get_all_resources(service, resource, results)
            resource_list = [list(fetched_resource.values())[0] for fetched_resource in all_resources]
            
            return get_attribute_options(attribute, resource_list, results)

    @api.route('/api/services/<service>/resources/<resource>/<resource_id>')
    @api.doc(
        params={
            'service': {
                'description': 'A provider service',
                'example':'ec2'},
            'resource': {
                'description': 'A resource of a service',
                'example':'instances'},
            'resource_id': {
                'description': 'The ID of a resource',
                'example':'i-0253e40e53cd800a1'}},
        description='Return the details of a specific resource of a specific service.')
    class Resource(RestxResource):
        def get(self, service, resource, resource_id):
            all_resources = get_all_resources(service,resource, results)[0]
            for retrieved_resource in all_resources:
                if list(retrieved_resource.keys())[0] == resource_id:
                    if not list(retrieved_resource.values())[0]['id']:
                        retrieved_resource.values()[0]['id'] = resource_id
                    return jsonify(list(retrieved_resource.values())[0])
            return {}

    @api.route('/api/services/<service>/resources/<resource>/download')
    @api.doc(
        params={
            'service': {
                'description': 'A provider service',
                'example':'ec2'},
            'resource': {
                'description': 'A resource of a service',
                'example':'security_groups'},
            'type': {
                'description': 'Download type (CSV or JSON)',
                'example': 'csv',
                'default': 'json'},
            'search': {
                'description': 'Search in name or id properties',
                'example':'test'},
            'filter_by': {
                'description': 'Return results containing a specific property value',
                'example':'{"region":"us-east-1"}'}},
        description='Download a list of resources of a specific resource type of a specific service.')
    class DownloadResource(RestxResource):
        def get(self, service, resource):
            resource_list = [list(fetched_resource.values())[0] for fetched_resource in get_all_resources(service, resource, results)[0]]
            response = download_filtered_elements(resource_list, f'{resource}')

            return response

    @api.route('/api/services/<service>/findings/<finding>/items/download')
    @api.doc(
        params={
            'service': {
                'description': 'A provider service',
                'example':'ec2'},
            'finding': {
                'description': 'A service finding',
                'example':'ec2-security-group-opens-all-ports'},
            'type': {
                'description': 'Download type (CSV or JSON)',
                'example': 'csv',
                'default': 'json'},
            'search': {
                'description': 'Search in name or id properties',
                'example':'test'},
            'filter_by': {
                'description': 'Return results containing a specific property value',
                'example':'{"region":"us-east-1"}'}},
        description='Download the list of items for a specific finding of a specific service.')
    class DownloadItems(RestxResource):
        def get(self, service, finding):
            item_list = get_all_items_in_finding(service, finding, results)
            response = download_filtered_elements(item_list, f'{finding}_items')

            return response

    @api.route('/api/categories/<category>/<policy_type>')
    @api.doc(
        params={
            'category': {
                'description': 'A service category',
                'example':'compute'},
            'policy_type': {
                'description': 'A vulnerability policy type',
                'example':'external_attack_surface'}},
        description='Return information about a policy type for a specific service category.')
    class CategoryPolicyType(RestxResource):
        def get(self, category, policy_type):
            metadata = results['metadata']
            if policy_type == 'external_attack_surface': policy_type = 'external attack surface'

            for category_metadata in metadata:
                if category_metadata == category:
                    summaries = metadata[category]['summaries']
                    policy_path = summaries[policy_type]['path']

                    return get_element_from_path(policy_path, results)

    @api.route('/api/services/<service>/<policy_type>')
    @api.doc(
        params={
            'service': {
                'description': 'A provider service',
                'example':'ec2'},
            'policy_type': {
                'description': 'A vulnerability policy type',
                'example':'external_attack_surface'}},
        description='Return information about a policy type for a specific service.')
    class ServicePolicyType(RestxResource):
        def get(self, service, policy_type):
            metadata = results['metadata']
            if policy_type == 'external_attack_surface': policy_type = 'external attack surface'

            for category in metadata:
                services = metadata[category]
                for service_metadata in services:
                    if service_metadata == service:
                        summaries = services[service]['summaries']
                        policy_path = summaries[policy_type]['path']

                        return get_element_from_path(policy_path, results)

    @api.route('/api/exceptions')
    @api.doc(
        description='Return the exceptions file used to run the report.')
    class Exception(RestxResource):
        def get(self):
            if not exceptions: return {}
            return exceptions

    @api.route('/api/raw/<path:path_to_element>')
    @api.doc(
        params={
            'path_to_element': {
                'description': 'A path to specific element in JSON object',
                'example':'last_run/time'}},
        description='Return a specific element in the JSON file based on path.')
    class Raw(RestxResource):
        def get(self, path_to_element):
            new_path = path_to_element.replace('/', '.')
            return jsonify(get_element_from_path(new_path, results))

    @api.route('/health')
    @api.doc(
        description='Return the string "OK" if server is up.')
    class ServerHealth(RestxResource):
        def get(self):
            return 'OK'

    app.run()

def get_attributes_from_path(path):
    attributes = []
    elements = path.split('.')
    for idx, word in enumerate(elements):
        if word == 'id':
            attributes.append(elements[idx-1])

    return attributes

def get_all_items_in_finding(service, finding, results):
    item_list = []
    finding = results['services'][service]['findings'][finding]
    
    # If there is no items, return an empty array
    if not finding['items']:
        return jsonify([])

    # Use display path if possible, if not use path
    path = finding['display_path'] if 'display_path' in finding else finding['path']
    attributes = get_attributes_from_path(path)[:-1]

    for item_path in finding['items']:
        item_path_kw = item_path.split('.')

        # Remove the item's tail if it's the id_suffix
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

    # List of all the positions of 'id' in path
    id_indexes = [id_index for id_index, x in enumerate(path_keywords) if x == 'id']

    # If there is no 'id', return the only element from path
    if not id_indexes:
        elements = get_element_from_path(path, report_location)
        for element in elements:
            new_element = {element: elements[element]}
            new_element[element]['path'] = path + f'.{element}'
            element_list.append(new_element)
        return element_list

    # Loop through each of the attributes = same number as the number of 'id' in path
    for id_idx in range(len(id_indexes)):
        subelement_list.append([])

        # First attribute
        if id_idx == 0:
            path_to_element = path_keywords[:id_indexes[id_idx]]
            element = get_element_from_path_kw(path_to_element, report_location)
            
            # Add the attribute to subelement_list[0]
            for subelement in element:
                if element[subelement]:
                    subelement_list[0].append(element[subelement])
                    subelement_list[0][-1]['path'] = path_keywords[0:id_indexes[0]] + [subelement]

        # Non-first, non-last attributes at position id_idx = new attribute
        else:

            # Loop through all of the attributes of the previous level
            for idx, element in enumerate(subelement_list[id_idx - 1]):
                path_to_element = path_keywords[id_indexes[id_idx - 1] + 1:id_indexes[id_idx]]
                new_element = get_element_from_path_kw(path_to_element, element)

                # Update the path to new attribute in subelement_list
                for element_dict in new_element: new_element[element_dict]['path'] = subelement_list[id_idx - 1][idx]['path'] + path_to_element
                subelement_list[id_idx - 1][idx] = new_element

                # Add the new attribute to subelement_list[id_idx]
                for subelement in subelement_list[id_idx - 1][idx]:
                    if subelement_list[id_idx - 1][idx][subelement]:
                        subelement_list[id_idx].append(subelement_list[id_idx - 1][idx][subelement])
                        subelement_list[id_idx][-1]['path'] = subelement_list[id_idx - 1][idx][subelement]['path'] + [subelement]

        # Last attribute
        if id_idx == len(id_indexes) - 1:

            # Loop through all of the attributes of the previous level
            for subelement in subelement_list[id_idx]:
                path_to_element = path_keywords[id_indexes[id_idx] + 1:len(path_keywords)]
                element = get_element_from_path_kw(path_to_element, subelement)

                # If element is a list with more than one element, append each of them as dict in element_list
                if element: 
                    if len(element) > 1:
                        for individual_element in element:
                            element_list.append({individual_element: element[individual_element]})
                            element_list[-1][individual_element]['path'] = '.'.join(subelement['path'] + path_to_element + [individual_element])

                    # If there is only one element, append to element_list
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
