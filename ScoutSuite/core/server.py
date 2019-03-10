from flask import Flask, request, _app_ctx_stack

from ScoutSuite.core.sqlite import SQLConnection

app = Flask(__name__)

database_filename = None


@app.route('/api/data', methods=['GET'])
def data():
    key = request.args.get('key')
    return SQLConnection(database_filename).get_value(key)


def start(filename):
    global database_filename
    database_filename = filename
    app.run()


if __name__ == "__main__":
    start("/tmp/sqltest1.db")
