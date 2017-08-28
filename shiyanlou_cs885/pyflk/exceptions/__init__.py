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
