from werkzeug.serving import run_simple
from werkzeug.wrappers import Response
from pyflk.wsgi_adapter import wsgi_app

class PyFlk:
    def __init__(self):
        '''
        instance method
        '''

        # default host
        self.host = '127.0.0.1' 
        
        # default port
        self.port = 8086        

    def dispatch_request(self, request):
        '''
        route
        '''

        # define HTTP status code 200, its means request success
        status = 200

        # define response header's Server attribute
        headers = {
            'Server': 'PyFlk Framework'
        }

        # return implement WSGI standard response body to WSGI module
        return Response('<h1>Hello, PyFlk</h1>', 
                    content_type='text/html', 
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

        # transfer parameter to werkzeug's run_simple
        run_simple(hostname=self.host, port=self.port, application=self, **options) 

    def __call__(self, environ, start_response):
        '''
        framework call WSGI entrance's method
        '''
        
        return wsgi_app(self, environ, start_response)
