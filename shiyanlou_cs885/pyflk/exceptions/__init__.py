from werkzeug.wrappers import Response

# define common headers parameter Content-Type
content_type = 'text/html; charset=UTF-8'

# define common service exception's response body
ERROR_MAP = {
    '2': Response('<h1>E2 Not Found File</h1>', content_type=content_type, status=500),
    '13': Response('<h1>E13 No Read Permission</h1>', content_type=content_type, status=500),
    '401': Response('<h1>401 Unknown or unsupported method</h1>', content_type=content_type, status=401),
    '404': Response('<h1>404 Resource Not Found</h1>', content_type=content_type, status=404),
    '503': Response('<h1>503 Unknown function type</h1>', content_type=content_type, status=503)
}


class PyFlkException(Exception):
    '''
    Framework exception base class
    '''

    def __init__(self, code='', message='Error'):

        # exceptions number
        self.code = code

        # exceptions message
        self.message = message

    def __str__(self):

        # returns the exception information when used as a string
        return self.message

class EndpointExistsError(PyFlkException):
    '''
    endpoint exist error
    '''

    def __init__(self, message='Endpoint exists'):
        super(EndpointExistError, self).__init__(message)

class URLExistsError(PyFlkException):
    '''
    URL exist error
    '''

    def __init__(self, message='URL exists'):
        super(URLExistError, self).__init__(message)

class FileNotExistsError(PyFlkException):
    '''
    file not found
    '''

    def __init__(self, code='2', message='File not found'):
        super(FileNotExistsError, self).__init__(code, message)

class RequireReadPermissionError(PyFlkException):
    '''
    insufficient permission
    '''

    def __init__(self, code='13', message='Require read permission'):
        super(RequireReadPermissionError, self).__init__(code, message)

class InvalidRequestMethodError(PyFlkException):
    '''
    not support request method
    '''

    def __init__(self, code='402', message='Unknown or unsupported request method'):
        super(InvalidRequestMethodError, self).__init__(code, message)

class PageNotFoundError(PyFlkException):
    '''
    page not found
    '''

    def __init__(self, code='404', message='Source not found'):
        super(PageNotFoundError, self).__init__(code, message)

class UnknownFuncError(PyFlkException):
    '''
    unknown deal with type
    '''

    def __init__(self, code='503', message='Unknown function type'):
        super(UnknownFuncError, self).__init__(code, message)

def capture(f):
    ''' exception capture'''

    def decorator(*args, **options):

        # start capture exception
        try:

            # try execute function
            rep = f(*args, **options)
        except PyFlkException as e:

            # when capture PyFlkException this classification exception, decide exception code, if not none and in ERROR_MAP, then deal with it, otherwise throw
            if e.code in ERROR_MAP and ERROR_MAP[e.code]:

                # gets exception result
                rep = ERROR_MAP[e.code]

                # if exception code less than 100, response code common set 500 internal server error
                status = int(e.code) if int(e.code) >= 100 else 500

                # decide result whether or not is a repsonse body, if not then its a customize exception handle function, call it and return package response body
                return rep if isinstance(rep, Response) or rep is None else Response(rep(), content_type=content_type, status=status)
            else:

                # throw not handle's exception
                raise e

        # return result for function execute normal
        return rep

    # return decorator
    return decorator

def reload(code):
    ''' exception handle reload decorator, parameter is exception number, define it integer'''

    def decorator(f):
        ''' replace ERROR_MAP value to function '''

        # if set code str then execute ./main.py test_reload
        ERROR_MAP[str(code)] = f

        # if set code integer then execute ERROR_MAP code
        # ERROR_MAP[int(code)] = f

    # return decorator
    return decorator
