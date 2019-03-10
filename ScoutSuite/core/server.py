from ScoutSuite.core.sqlite import SQLConnection
import cherrypy


class Server(object):
    def __init__(self, filename):
        self.results = SQLConnection(filename)

    @cherrypy.expose(['data'])
    def get(self, key=None):
        return self.results.get(key)

    @staticmethod
    def init(database_filename, host, port):
        cherrypy.config.update({
                'server.socket_host': host,
                'server.socket_port': port,
            })
        cherrypy.quickstart(Server(database_filename), "/api")


if __name__ == "__main__":
    Server.init("/tmp/sqltest1.db", '127.0.0.1', 8000)
