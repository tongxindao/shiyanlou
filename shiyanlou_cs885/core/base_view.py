from pyflk.view import View

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
