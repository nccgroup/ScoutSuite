from sqlitedict import SqliteDict
import cherrypy
import cherrypy_cors

import re

count_re = re.compile(r".*_count$")


class Server(object):
    """
    Boots a server that serves the result of the report for the user. This is still a proof of concept,
    but will eventually be used to serve data when it exceeds 400mb.
    """
    def __init__(self, filename):
        """
        Constructor of the server object. Should not be called directly outside the class.

        :param filename:                Name of the file to write data to.
        :return:                        The server object.
        """
        self.results = SqliteDict(filename)

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def summary(self):
        """
        Returns the stripped down data of the results that doesn't scale up when using a lot of resources,
        used to render the summary.
        Should be the first call from the server.
        Can be found at GET /api/summary

        :return:                        The summary data of the report.
        """
        data = dict(self.results)
        services = data.get('services')
        stripped_services = {}
        for k1, v1 in services.items():
            service = {}
            for k2, v2 in v1.items():
                if k2 == 'findings' or k2 == 'filters' or count_re.match(k2):
                    service[k2] = v2
            stripped_services[k1] = service
        data['services'] = stripped_services
        return {'data': data}

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def data(self, key=None):
        """
        Return the data at the requested key. Doesn't returns nested dictionaries and lists.
        If one of the value is a dictionary, it will return {'type': 'dict', 'keys': <Array of all the keys>}
        If one of the value is a list, it will return {'type': 'list', 'count': <number of elements in the list>}

        Can be found at GET /api/data?key=<KEY>
        :param key:                     Key of the requested information, separated by the character '¤'.
        :return:                        The data at the requested location stripped of its nested data.
        """
        result = self.get_item(self.results, key)
        # Returns only indexes or length if it's a complex type
        if isinstance(result, dict) or isinstance(result, SqliteDict):
            result = {'type': 'dict', 'keys': list(result.keys())}
        elif isinstance(result, list):
            result = {'type': 'list', 'length': len(result)}
        return {'data': result}

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def full(self, key=None):
        """
        Return the data at the requested key. Returns all the nested data.
        Be sure not to use it on a key that may contains a lot of data, as the request won't be answered
        if it's too large(generally 3mb).

        Can be found at GET /api/full?key=<KEY>
        :param key:                     Key of the requested information, separated by the character '¤'.
        :return:                        The data at the requested location.
        """
        result = self.get_item(self.results, key)
        if isinstance(result, str) or isinstance(result, int):
            return {'data': result}
        return {'data': dict(result)}

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def page(self, key=None, page=None, pagesize=None):
        """
        Return a page of the data at the requested key. Doesn't returns nested dictionaries and lists.
        For example, if you set pagesize=10 and page=2, it should return element 10-19
        If one of the value is a dictionary, it will return {'type': 'dict', 'keys': <Array of all the keys>}
        If one of the value is a list, it will return {'type': 'list', 'count': <number of elements in the list>}

        Can be found at GET /api/page?key=<KEY>&page=<PAGE>&pagesize=<PAGESIZE>
        :param key:                     Key of the requested information, separated by the character '¤'.
        :param page:                    The number of the page you request.
        :param pagesize:                The size of the page you request.
        :return:                        A subset of the data at the requested location.
        """
        result = self.get_item(self.results, key)

        page = int(page)
        pagesize = int(pagesize)

        start = page * pagesize
        end = min((page + 1) * pagesize, len(result))

        if isinstance(result, dict) or isinstance(result, SqliteDict):
            page = {k: result.get(k) for k in sorted(list(result))[start:end]}
        if isinstance(result, list):
            page = result[start:end]

        return {'data': self.strip_nested_data(page)}

    @staticmethod
    def init(database_filename, host, port):
        """
        Configure and starts the server.

        :param database_filename:       Location of the database file.
        :param host:                    Address on which to listen.
        :param port:                    Port on which to listen.
        """
        cherrypy_cors.install()
        config = {
            '/': {
                'cors.expose.on': True,
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            },
        }
        cherrypy.config.update({
                'server.socket_host': host,
                'server.socket_port': port,
        })
        cherrypy.quickstart(Server(database_filename), "/api", config=config)

    @staticmethod
    def get_item(data, key):
        """
        Get a specific information from its key.

        :param data:                    The dictionary in which the information is stored.
        :param host:                    The key where the information is located.
        :return:                        The nested data at the requested location.
        """
        if not key:
            return data

        keyparts = key.split('¤')
        for k in keyparts:
            if isinstance(data, dict) or isinstance(data, SqliteDict):
                data = data.get(k)
            elif isinstance(data, list):
                data = data[int(k)]
        return data

    @staticmethod
    def strip_nested_data(data):
        """
        Strip nested lists and dictionaries from the provided object to reduce its size.

        :param data:                    The object to strip.
        :return:                        The input data stripped of its nested lists and dictionaries.
        """
        if not isinstance(data, dict):
            return data

        result = {}
        for k, v in data.items():
            if isinstance(v, dict):
                result[k] = {'type': 'dict', 'keys': list(v.keys())}
            elif isinstance(v, list):
                result[k] = {'type': 'list', 'length': len(v)}
        return result

