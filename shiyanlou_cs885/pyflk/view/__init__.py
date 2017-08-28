class View:
    '''
    view base class
    '''

    # support request method
    methods = None

    # request handle function mapping
    methods_meta = None

    # view handle function call entrance
    def dispatch_request(self, request, *args, **option):
        raise NotImplementedError

    # generate view handle function, parameter name is endpoint name
    @classmethod
    def get_func(cls, name):

        # define handle function
        def func(*args, **kwargs):

            # handle function internal instance view object
            obj = func.view_class()

            # through view object call handle function entrance, return view handle function
            return obj.dispatch_request(*args, **kwargs)

        # for handle function bind attribute
        func.view_class = cls
        func.__name__ = name
        func.__doc__ = cls.__doc__
        func.__module__ = cls.__module__
        func.methods = cls.methods

        # return handle function
        return func

class Controller:
    '''
    controller class
    '''

    def __init__(self, name, url_map):

        # store mapping relation, the one is Dict's List
        self.url_map = url_map

        # controller name when generate endpoint is use
        self.name = name

    def __name__(self):

        # return controller name
        return self.name
