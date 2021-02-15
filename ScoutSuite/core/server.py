import flask

from flask import request, jsonify

def start_api(results):
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    @app.route('/', methods=['GET'])
    def home():
        return '''<h1>SCOUT SUITE WEB APP</h1>
            '''

    @app.route('/api', methods=['GET'])
    def api():
        return jsonify(results)

    app.run()
