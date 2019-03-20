from sqlitedict import SqliteDict
import cherrypy
import cherrypy_cors


class Server(object):
    def __init__(self, filename):
        self.results = SqliteDict(filename)

    @cherrypy.expose(['data'])
    def get(self, key=None):
        result = self.results
        keyparts = key.split('.')
        for k in keyparts:
            if isinstance(result, dict):
                result = result.get(k)
            elif isinstance(result, list):
                result = result[int(k)]
        return result

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


if __name__ == "__main__":
    Server.init("/tmp/sqltest1.db", '127.0.0.1', 8000)
