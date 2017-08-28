import os

from werkzeug.wrappers import Response
from werkzeug.serving import run_simple

import pyflk.exceptions as exceptions
from pyflk.route import Route
from pyflk.wsgi_adapter import wsgi_app
from pyflk.helper import parse_static_key

# define common service exception's response body
ERROR_MAP = {
    '401': Response('<h1>401 Unknown or unsupported method</h1>', content_type='text/html; charset=UTF-8', status=401),
    '404': Response('<h1>404 Resource Not Found</h1>', content_type='text/html; charset=UTF-8', status=404),
    '503': Response('<h1>503 Unknown function type</h1>', content_type='text/html; charset=UTF-8', status=503)
}

# define file type
TYPE_MAP = {
    'css': 'text/css',
    'js': 'text/js',
    'png': 'image/png',
    'jpg': 'image/jpg',
    'jpeg': 'image/jpeg'
}

class ExecFunc:
    '''
    handle function data structure
    '''

    def __init__(self, func, func_type, **options):
        # handle function
        self.func = func
        
        # incidental arguments
        self.options = options

        # function type
        self.func_type = func_type

class PyFlk:
    '''
    Framework name
    '''

    def __init__(self, static_folder='static'):
        '''
        instance method
        '''

        # default host
        self.host = '127.0.0.1' 
        
        # default port
        self.port = 8086        

        # store URL and Endpoint mapping
        self.url_map = {}

        # store URL and static resource mapping
        self.static_map = {}

        # store Endpoint and request function mapping
        self.function_map = {}

        # static resource local store path, default path is app/static folder
        self.static_folder = static_folder

        # route decorator
        self.route = Route(self)

    def add_url_rule(self, url, func, func_type, endpoint=None, **options):
        '''
        add url rule
        '''
        
        # if endpoint unnaming, use handle function's name
        if endpoint is None:
            endpoint = func.__name__

        # throw URL exist exceptions
        if url in self.url_map:
            raise exceptions.URLExistError

        # if type isn't static resource and endpoint exist, then throw EndpointExistsError
        if endpoint in self.function_map and func_type != 'static':
            raise exceptions.EndpointExistsError

        # add URL and endpoint mapping
        self.url_map[url] = endpoint

        # add endpoint and request handle function mapping
        self.function_map[endpoint] = ExecFunc(func, func_type, **options)

    def dispatch_static(self, static_path):
        '''
        dispatch static resource route
        '''

        # if resource file not in static resource rule, return 404 status page
        if os.path.exists(static_path):
            
            # gets resource file suffix
            key = parse_static_key(static_path)

            # gets file type
            doc_type = TYPE_MAP.get(key, 'text/plain')

            # gets file content
            with open(static_path, 'rb') as f:
                rep = f.read()

            # package and return response body
            return Response(rep, content_type=doc_type)
        else:
            
            # if not found response body for it, return 404 page
            return ERROR_MAP['404']

    def dispatch_request(self, request):
        '''
        dispatch route
        '''

        # extract path/file from the domain, eg http://xxx.com/path/file?xx=xx
        url = "/" + "/".join(request.url.split("/")[3:]).split("?")[0]

        # through URL find endpoint
        if url.find(self.static_folder) == 1 and url.index(self.static_folder) == 1:
            
            # if URL use static resource catalog name define first folder, then resource is static resource, endpoint is static
            endpoint = 'static'
            url = url[1:]
        else:
    
            # if static not first, then from the URL and endpoint mapping table gets endpoint
            endpoint = self.url_map.get(url, None)

        # define response header
        headers = {
            'Server': 'PyFlk Web Framework 0.1'
        }

        # if endpoint is none, return 404
        if endpoint is None:
            return ERROR_MAP['404']

        # gets endpoint's execute function
        exec_function = self.function_map[endpoint]

        # decide excute function type
        if exec_function.func_type == 'route':

            ''' route handle '''
            
            # decide request method whether or not support
            if request.method in exec_function.options.get('methods'):

                ''' route handle result '''

                # decide route's excute function whether or not need request body conduct internal processing
                argcount = exec_function.func.__code__.co_argcount

                if argcount > 0:

                    # need in passing request body conduct result handle
                    rep = exec_function.func(request)
                else:

                    # not need in passing request body conduct result handle
                    rep = exec_function.func()
            else:
                ''' unkown request method '''

                # return 401 error response body
                return ERROR_MAP['401']
        elif exec_function.func_type == 'view':

            ''' view handle result '''

            # all of the view handle function needs in passing request body gets handle result
            rep = exec_function.func(request)
        elif exec_function.func_type == 'static':

            ''' static logic handle '''

            # static resource return packaged response body
            return exec_function.func(url)
        else:

            ''' unknown type handle '''

            # return 503 error response body
            return ERROR_MAP['503']
       
        # define HTTP status code 200, its means request success
        status = 200

        # define response body type
        content_type = 'text/html'

        # return response body
        return Response(rep, 
                    content_type='%s; charset=UTF-8' % content_type, 
                    headers=headers, 
                    status=status)

    def run(self, host=None, port=None, **options):
        '''
        run entrance
        '''
        
        # if input parameter isn't null, then assign it a value
        for key, value in options.items(): 
            if value is not None:
                self.__setattr__(key, value)

        # if host isn't null, replace self.host
        if host: 
            self.host = host

        # if port isn't null, replace self.port
        if port: 
            self.port = port
        
        # mapping static resource handle function, all of the static resource handle function is static resource
        self.function_map['static'] = ExecFunc(func=self.dispatch_static, func_type='static')

        # transfer parameter to werkzeug's run_simple
        run_simple(hostname=self.host, port=self.port, application=self, **options)

    def __call__(self, environ, start_response):
        '''
        framework call WSGI entrance's method
        '''
        
        return wsgi_app(self, environ, start_response)
