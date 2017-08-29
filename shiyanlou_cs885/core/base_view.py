from pyflk import redirect
from pyflk.view import View
from pyflk.session import AuthSession, session

class BaseView(View):

    # define support request method, default support GET and POST method
    methods = ['GET, POST']

    # POST request handle function
    def post(self, request, *args, **kwargs):
        pass

    # GET request handle function
    def get(self, request, *args, **kwargs):
        pass

    # view handle function call entrance
    def dispatch_request(self, request, *args, **options):

        # define request method and handle function mapping
        methods_meta = {
            'GET': self.get,
            'POST': self.post,
        }

        # decide that view whether or not support this request method, if yes then return function handle result, if not return error information
        if request.method in methods_meta:
            return methods_meta[request.method](request, *args, **options)
        else:
            return '<h1>Unknown or unsupported require method</h1>'

class AuthLogin(AuthSession):
    '''
    login verification class
    '''

    @staticmethod
    def auth_fail_callback(request, *args, **options):
        ''' if auth fail, then return a lick, click it skip to login page '''

        return redirect("/login")

    @staticmethod
    def auth_logic(request, *args, **options):
        ''' verification logic, if user key not in Session, then auth fail, if not be success '''

        if 'user' in session.map(request):
            return True
        return False

class SessionView(BaseView):
    '''
    Session view base class
    '''

    @AuthLogin.auth_session
    def dispatch_request(self, request, *args, **options):
        ''' verification class decorator '''

        # combination decorator internal logic, call inherit subclass dispatch_request method
        return super(SessionView, self).dispatch_request(request, *args, **options) 
