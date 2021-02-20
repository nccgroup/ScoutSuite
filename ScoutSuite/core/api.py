from flask import Blueprint, jsonify


scout_api = Blueprint('scout_api', __name__, url_prefix='/api')

@scout_api.route('/services/<service>/findings', methods=['GET'])
def getFindings(service):
    return '<h3>SUPERMAN</h3>'
    # return jsonify(results)




# /services/{service}/
# /services/{service}/findings/{finding}/items
# /services/{service}/findings/{finding}/items/{itemID}?path=ec2.regions.{region}.vpcs.{vpc}.security_groups.{sg_id}
# /services
