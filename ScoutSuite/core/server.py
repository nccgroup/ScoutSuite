from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from ScoutSuite.utils import format_service_name

import json # TO REMOVE

# ROUTES TO REPORT
scout_suite_directory = '/Users/noboruyoshida/code/ScoutSuite'
aws = '/scoutsuite-report/scoutsuite-results/scoutsuite_results_aws-635327450130.json'
azure = '/scoutsuite-report/scoutsuite-results/scoutsuite_results_azure-tenant-0cc90829-0d8e-40d6-ba9c-aea092ba7de5.json'
gcp = '/scoutsuite-report/scoutsuite-results/scoutsuite_results_gcp-poly-project-1.json'

# REPORT (aws, azure or gcp)
provider = aws

with open(f'{scout_suite_directory}{provider}') as json_file:
    results = json.load(json_file)

# def start_api(results):
app = Flask(__name__)
CORS(app)
# app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>SCOUT SUITE WEB APP</h1>'''

@app.route('/api', methods=['GET'])
def api():
    return jsonify(results)

@app.route('/api/services/<service>/findings', methods=['GET'])
def get_findings(service):
    findings = results['services'][service]['findings']
    for finding in findings: findings[finding]['name'] = finding
    
    return jsonify(list(findings.values()))

# Paginated
@app.route('/api/services/<service>/findings/<finding>/items', methods=['GET'])
def get_items(service, finding):
    item_list = []
    finding = results['services'][service]['findings'][finding]

    if not finding['items']:
        return jsonify([])

    path = finding['display_path'] if 'display_path' in finding else finding['path'] # storageaccounts.subscriptions.id.storage_accounts.id
    attributes = get_attributes_from_path(path)[:-1] # ['subscriptions']

    for item_path in finding['items']:
        item_object = {}
        words = item_path.split('.') # [storageaccounts, subscriptions, c4596cb7-805b-49aa-9a04-ed74e9f5c789, storage_accounts, e21374e58a7142b3bc563467ac097f66345454fd, blob_containers, test, public_access_allowed]
        words = words[:-1] if 'id_suffix' in finding and words[-1] == finding['id_suffix'] else words
        item_path_with_brackets = results['services']

        for idx in range(len(path.split('.'))):
            item_path_with_brackets = item_path_with_brackets[words[idx]]
        item = {
            'id': item_path_with_brackets['id'],
            'name': item_path_with_brackets['name'],
            'display_path': '.'.join(words[:len(path.split('.'))])
        }
        item_object['item'] = item
    
        for attribute in attributes: # regions
            attribute_path = []
            for idx, word in enumerate(words):
                if word == attribute:
                    attribute_path = words[:idx + 2]
            attribute_path_with_brackets = results['services']
            for idx in range(len(attribute_path)):
                attribute_path_with_brackets = attribute_path_with_brackets[attribute_path[idx]]
            attribute_object = {
                'path': '.'.join(attribute_path)
            }
            if 'id' in attribute_path_with_brackets: attribute_object['id'] = attribute_path_with_brackets['id']
            if 'name' in attribute_path_with_brackets: attribute_object['name'] = attribute_path_with_brackets['name']
            item_object[attribute] = attribute_object
        
        item_list.append(item_object)

    sort_by = request.args.get('sort_by') if request.args.get('sort_by') else 'name'
    direction = request.args.get('direction') if request.args.get('direction') else 'asc'
    items_per_page = int(request.args.get('items_per_page')) if request.args.get('items_per_page') else 10
    current_page = int(request.args.get('current_page')) if request.args.get('current_page') else 1

    # filtered_results = filter_results(item_list, filter_keywords)
    sorted_results = sort_results(item_list, sort_by, direction)
    paginated_results = paginate_results(sorted_results, items_per_page, current_page)
    return jsonify(paginated_results)

@app.route('/api/services/<service>/findings/<finding>/items/<item_id>', methods=['GET'])
def get_issue_paths(service, finding, item_id):
    path = request.args.get('path')
    items = results['services'][service]['findings'][finding]['items']
    issue_paths = []
    for item_path in items:
        if (path == item_path):
            issue_paths.append('THE WHOLE PATH')
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

@app.route('/api/services/<service>/resources/<resource>')
def get_resource(service, resource):
    metadata = results['metadata']

    for category in metadata:
        services = metadata[category]
        for service_metadata in services:
            if service_metadata == service:
                resources = services[service]['resources']
                for resource_metadata in resources:
                    if resource_metadata == resource:
                        resource_path = resources[resource]['path']
                        
                        sort_by = request.args.get('sort_by') if request.args.get('sort_by') else 'name'
                        direction = request.args.get('direction') if request.args.get('direction') else 'asc'
                        items_per_page = int(request.args.get('items_per_page')) if request.args.get('items_per_page') else 10
                        current_page = int(request.args.get('current_page')) if request.args.get('current_page') else 1

                        # filtered_results = filter_results(item_list, filter_keywords)
                        sorted_results = sort_results(get_all_elements_from_path(resource_path), sort_by, direction)
                        paginated_results = paginate_results(sorted_results, items_per_page, current_page)

                        return jsonify(paginated_results)
    return {}

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

def get_attributes_from_path(path):
    attributes = []
    words = path.split('.')
    for idx, word in enumerate(words):
        if word == 'id':
            attributes.append(words[idx-1])

    return attributes

def get_all_elements_from_path(path, report_location = results):
    path_keywords = path.split('.')
    element_path_with_brackets = report_location
    element_list = []
    subelement_list = []

    id_locations = [id_index for id_index, x in enumerate(path_keywords) if x == 'id'] # [3, 5]

    for id_idx in range(len(id_locations)):
        subelement_list.append([])
        if id_idx == 0:
            for path_keyword_idx in range(id_locations[id_idx]):
                element_path_with_brackets = element_path_with_brackets[path_keywords[path_keyword_idx]] # [services, ec2, regions]
            for subelement in element_path_with_brackets:
                if element_path_with_brackets[subelement]:
                    subelement_list[id_idx].append(element_path_with_brackets[subelement])

        else:
            for idx, element in enumerate(subelement_list[id_idx - 1]):
                for path_keyword_idx in range(id_locations[id_idx - 1] + 1, id_locations[id_idx]):
                    subelement_list[id_idx - 1][idx] = element[path_keywords[path_keyword_idx]]
                for subelement in subelement_list[id_idx - 1][idx]:
                    if subelement_list[id_idx - 1][idx][subelement]:
                        subelement_list[id_idx].append(subelement_list[id_idx - 1][idx][subelement])

        if id_idx == len(id_locations) - 1:
            for subelement in subelement_list[id_idx]:
                element = subelement
                for path_keyword_idx in range(id_locations[id_idx] + 1, len(path_keywords)):
                    element = element[path_keywords[path_keyword_idx]]
                if element: element_list.append(element)
    
    return element_list

def format_title(title):
    return title[0].upper() + ' '.join(title[1:].lower().split('_'))

def get_element_from_path(path, report_location = results):
    path_keywords = path.split('.')
    element_path_with_brackets = report_location

    for idx in range(len(path_keywords)):
        element_path_with_brackets = element_path_with_brackets[path_keywords[idx]]
    
    return element_path_with_brackets

def filter_results(results, filter_keyword):
    return results

def sort_results(results, sort_by, direction):
    descending = direction == 'desc'
    return sorted(results, reverse=descending) if not sort_by else sorted(results, key=lambda k: k['item'][sort_by], reverse=descending)

def paginate_results(results, elements_per_page, page_number):
    paginated_results = [results[i:i+elements_per_page] for i in range(0, len(results), elements_per_page)]
    page_results = {
        'meta': {
            'current_page': page_number,
            'next_page': page_number + 1 if page_number < len(paginated_results) else None,
            'prev_page': page_number - 1 if page_number > 1 else None,
            'total_pages': len(paginated_results),
        },
        'results': paginated_results[page_number - 1] if paginated_results else []
    }

    return page_results

app.run()
