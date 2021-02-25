from flask import Flask, request, jsonify
from flask_cors import CORS
from ScoutSuite.utils import format_service_name

import json # TO REMOVE

scout_suite_directory = '/Users/noboruyoshida/code/ScoutSuite'

with open(f'{scout_suite_directory}/scoutsuite-report/scoutsuite-results/scoutsuite_results_aws-186023717850.json') as json_file:
    results = json.load(json_file)

# def start_api(results):
app = Flask(__name__)
CORS(app)
# app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>SCOUT SUITE WEB APP</h1>
        '''

@app.route('/api', methods=['GET'])
def api():
    return jsonify(results)

@app.route('/api/services/<service>/findings', methods=['GET'])
def get_findings(service):
    findings = results['services'][service]['findings']
    for finding in findings: findings[finding]['name'] = finding
    
    return jsonify(list(findings.values()))

@app.route('/api/services/<service>/findings/<finding>/items', methods=['GET'])
def get_items(service, finding):
    item_list = []
    finding = results['services'][service]['findings'][finding]

    if not finding['items']:
        item_list = []
    else:
        path = finding['display_path'] if 'display_path' in finding else finding['path']
        attributes = get_attributes_from_path(path) # [regions, vpcs]

        for item_path in finding['items']:
            item_object = {}
            words = item_path.split('.') # [ec2, regions, us-east-1, vpcs, vpc-0190d8398f12f0340, security_groups, sg-0e584bf4e7793ea2a, default_in_use]
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
                attribute_id = ''
                attribute_path = []
                for idx, word in enumerate(words):
                    if word == attribute:
                        attribute_path = words[:idx + 2]
                attribute_path_with_brackets = results['services']
                for idx in range(len(attribute_path)):
                    attribute_path_with_brackets = attribute_path_with_brackets[attribute_path[idx]]
                attribute_object = {
                    'id': attribute_path_with_brackets['id'],
                    'name': attribute_path_with_brackets['name'],
                    'path': '.'.join(attribute_path)
                }
                item_object[attribute] = attribute_object
            
            item_list.append(item_object)

    return jsonify(item_list)

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


@app.route('/api/raw/<path:path_to_element>', methods=['GET'])
def get_raw_info(path_to_element):
    words = path_to_element.split('/')
    path_to_elemnt_in_brackets = results

    for idx in range(len(words)):
        path_to_elemnt_in_brackets = path_to_elemnt_in_brackets[words[idx]]

    return jsonify(path_to_elemnt_in_brackets)

def get_attributes_from_path(path):
    attributes = []
    words = path.split('.')
    for idx, word in enumerate(words):
        if word == 'id':
            attributes.append(words[idx-1])

    return attributes[:-1]

def format_title(title):
    return title[0].upper() + ' '.join(title[1:].lower().split('_'))

# /services/{service}/findings/{finding}/items/{itemID}?path=ec2.regions.{region}.vpcs.{vpc}.security_groups.{sg_id}
# /services


app.run()
