import os

from werkzeug.wrappers import Response
from werkzeug.serving import run_simple

from pyflk.route import Route
from pyflk.wsgi_adapter import wsgi_app
from pyflk.helper import parse_static_key
from pyflk.template_engine import replace_template
from pyflk.session import create_session_id, session

import pyflk.exceptions as exceptions

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

    # class attribute, template file local store folder
    template_folder = None

    def __init__(self, static_folder='static', template_folder='template', session_path='.session'):
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

        # template file local store path, default app/template
        self.template_folder = template_folder

        # class's template_folder init, replace template engine call it
        PyFlk.template_folder = self.template_folder

        # route decorator
        self.route = Route(self)

        # Session record default save to .session folder same path to app
        self.session_path = session_path

    def bind_view(self, url, view_class, endpoint):
        '''
        add view rule
        '''
        self.add_url_rule(url, func=view_class.get_func(endpoint), func_type='view')

    def load_controller(self, controller):
        '''
        load controller
        '''
        
        # gets controller name
        name = controller.__name__()

        # ergodic controller's `url_map` member
        for rule in controller.url_map:

            # bind URL and view object, final endpoint name format is `controller name` + "." + define endpoint name
            self.bind_view(rule['url'], rule['view'], name + '.' + rule['endpoint'])

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

        # gets Cookie from the request
        cookies = request.cookies

        # if key `session_id` not in cookies, then notice client set Cookie
        if 'session_id' not in cookies:
            headers = {
            
                # define Set-Cookie attribute, notice client record Cookie, create_session_id is generate a ruleless only string method
                'Set-Cookie': 'session_id=%s' % create_session_id(),

                # define response header's Server attribute
                'Server': 'PyFlk Web Framework 0.1'
            }
        else:
            
            # define response header's Server attribute
            headers = {
                'Server': 'PyFlk Web Framework 0.1'
            }

        # through URL find endpoint
        if url.find(self.static_folder) == 1 and url.index(self.static_folder) == 1:
            
            # if URL use static resource catalog name define first folder, then resource is static resource, endpoint is static
            endpoint = 'static'
            url = url[1:]
        else:
    
            # if static not first, then from the URL and endpoint mapping table gets endpoint
            endpoint = self.url_map.get(url, None)

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

        # decide if return value is a Response type, then direct return
        if isinstance(rep, Response):
            return rep

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

        # if Session record storage path not exist then create it
        if not os.path.exists(self.session_path):
            os.mkdir(self.session_path)

        # set Session record storage path
        session.set_storage_path(self.session_path)

        # load local cache Session record
        # session.load_local_session()        

        # transfer parameter to werkzeug's run_simple
        run_simple(hostname=self.host, port=self.port, application=self)

    def __call__(self, environ, start_response):
        '''
        framework call WSGI entrance's method
        '''
        
        return wsgi_app(self, environ, start_response)

def redirect(url, status_code=302):
    ''' URL redirect method '''

    # define a response body
    response = Response('', status=status_code)

    # response body header Location parameter and URL bind, notice client auto skip
    response.headers['Location'] = url

    # return response body
    return response

def simple_template(path, **options):
    return replace_template(PyFlk, path, **options)
