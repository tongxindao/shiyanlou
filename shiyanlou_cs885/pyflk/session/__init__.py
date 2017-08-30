import os
import json
import time
import base64

def create_session_id():
    '''
    create Session ID
    '''

    # first of all, get current time stamp and convert byte stream, in Base64 code, decode to string and put off Base64 code "=" symbol, get second to last bit, final reverse order array
    return base64.encodebytes(str(time.time()).encode()).decode().replace("=", "")[:-2][::-1]

def get_session_id(request):
    '''
    from request gets Session ID
    '''

    return request.cookies.get('session_id', '')

class Session:
    ''' 
    Session 
    '''

    # instance object
    __instance = None

    # init method
    def __init__(self):

        # session mapping table
        self.__session_map__ = {}

        # session local store folder
        self.__storage_path__ = None

    def set_storage_path(self, path):
        ''' set session storage path '''

        self.__storage_path__ = path

    def storage(self, session_id):
        ''' save session record to local '''

        # constructor Session local file path, file name is Session ID
        session_path = os.path.join(self.__storage_path__, session_id)

        # if already set Session storage path, then start cache to local
        if self.__storage_path__ is not None:
            with open(session_path, 'wb') as f:

                # convert session record to string
                content = json.dumps(self.__session_map__[session_id])

                # base64 code and write to file, prevent sone specified binary data cannot right write in
                f.write(base64.encodebytes(content.encode()))
    
    def __new__(cls, *args, **kwargs):
        ''' singleton, realization global public a Session instance object '''

        if cls.__instance is None:
            cls.__instance = super(Session, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def push(self, request, item, value):
        ''' update or add record '''

        # from request gets client's Session ID
        session_id = get_session_id(request)

        # if this Session ID exist in mapping table, then add new data key: value, if not, then first init a null dict, and add data key: value
        if session in self.__session_map__:

            # from current session add data
            self.__session_map__[get_session_id(request)][item] = value
        else:

            # init current session
            self.__session_map__[session_id] = {}

            # from current session add data
            self.__session_map__[session_id][item] = value

        # Session happen change, update cache to local
        self.storage(session_id)

    def pop(self, request, item, value=True):
        ''' delete current session's some item '''

        # gets current session
        session_id = get_session_id(request)
        current_session = self.__session_map__.get(session_id, {})

        # decide data item's key whether or not in current session, if yes then delete it
        if item in current_session:
            current_session.pop(item, value)

            # Session happen change, update cache to local
            self.storage(session_id)

    def load_local_session(self):
        ''' load local session '''

        # if already set Session storage path, then start load cache from local
        if self.__storage_path__ is not None:

            # from local storage folder get all of the Session record file list, file name is Session ID
            session_path_list = os.listdir(self.__storage_path__)

            # ergodic Session record file list
            for session_id in session_path_list:

                # constructor Session record file folder
                path = os.path.join(self.__storage_path__, session_id)

                # read file content
                with open(path, 'rb') as f:
                    content = f.read()

                # file content decode to base64
                content = base64.decodebytes(content)

                # Session ID content bind and add to Session mapping table
                self.__session_map__[session_id] = json.loads(content.decode())

    def map(self, request):
        ''' gets current Session record '''

        return self.__session_map__.get(get_session_id(request), {})

    def get(self, request, item):
        ''' gets current Session some item '''

        return self.__session_map__.get(get_session_id(request), {}).get(item, None)

class AuthSession:
    ''' Session verification decorator '''

    @classmethod
    def auth_session(cls, f, *args, **options):

        def decorator(obj, request):
            return f(obj, request) if cls.auth_logic(request, *args, **options) else cls.auth_fail_callback(request, *args, **options)

        return decorator

    @staticmethod
    def auth_logic(request, *args, **options):
        ''' verification logic interface, return a boolean '''

        raise NotImplementedError

    @staticmethod
    def auth_fail_callback(request, *args, **options):
        ''' verification fail callback interface '''

        raise NotImplementedError

# singleton global object
session = Session()
