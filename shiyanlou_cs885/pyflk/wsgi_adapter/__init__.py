from werkzeug.wrappers import Request

# WSGI dispatch framework entrance
def wsgi_app(app, environ, start_response):
    '''
        first parameter is app
        second parameter is transfer request from server
        third parameter is response body. its never use, just transfer result to server
    '''

    # analysis request header
    request = Request(environ)

    # from request route and handle, then achieve result
    response = app.dispatch_request(request)

    # return to server
    return response(environ, start_response)
