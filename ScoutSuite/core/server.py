from sqlitedict import SqliteDict
import cherrypy
import cherrypy_cors


class Server(object):
    def __init__(self, filename):
        self.results = SqliteDict(filename)

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def data(self, key=None):
        result = self.get_item(self.results, key)
        # Returns only indexes or length if it's a complex type
        if isinstance(result, dict) or isinstance(result, SqliteDict):
            result = list(result.keys())
        elif isinstance(result, list):
            result = len(result)
        return {'data': result}

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def page(self, key=None, page=None, pagesize=None):
        result = self.get_item(self.results, key)

        page = int(page)
        pagesize = int(pagesize)

        start = page * pagesize
        end = min((page + 1) * pagesize, len(result))

        if isinstance(result, dict) or isinstance(result, SqliteDict):
            page = {k: result.get(k) for k in list(result)[start:end]}
        if isinstance(result, list):
            page = result[start:end]

        return {'data': page}

    @staticmethod
    def init(database_filename, host, port):
        cherrypy_cors.install()
        config = {
            '/': {
                'cors.expose.on': True,
            },
        }
        cherrypy.config.update({
                'server.socket_host': host,
                'server.socket_port': port,
        })
        cherrypy.quickstart(Server(database_filename), "/api", config=config)

    @staticmethod
    def get_item(data, key):
        if not key:
            return data

        keyparts = key.split('.')
        for k in keyparts:
            if isinstance(data, dict) or isinstance(data, SqliteDict):
                data = data.get(k)
            elif isinstance(data, list):
                data = data[int(k)]
        return data


if __name__ == "__main__":
    Server.init("/tmp/sqltest1.db", '127.0.0.1', 8000)
