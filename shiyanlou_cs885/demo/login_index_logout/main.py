import sys
sys.path.append('../..')

from pyflk.view import Controller
from pyflk.session import session
from pyflk import PyFlk, simple_template, redirect, render_json, render_file, exceptions

from core.database import dbconn
from core.base_view import BaseView, SessionView

@exceptions.reload(404)
def test_reload():
    return '<h1>test reload 404 exception</h1>'

class Download(BaseView):
    '''
    it's a test for capture exception
    '''

    def get(self, request):
        return render_file('/etc/shadow')

class Register(BaseView):
    def get(self, request):

        # when get GET request through template return a register page
        return simple_template('layout.html', title='register', message='input register name')

    def post(self, request):

        # put user commit information for parameter, execute SQL INSERT statement put information save to database table
        ret = dbconn.insert('INSERT INTO user(f_name) VALUES (%(user)s)', request.form)

        # if insert success, its means register success, redirect to login page
        if ret.suc:
            return redirect('/login')
        else:
 
            # if fail, put error information for debug
            return render_json(ret.to_dict())

'''
class Download(BaseView):
    def get(self, request):
        return render_file("main.py")
'''

class API(BaseView):
    def get(self, request):
        data = {
            'name': 'user_001',
            'company': 'Google',
            'department': 'Research and Development Department'
        }
        return render_json(data)

class Index(SessionView):
    '''
    index view
    '''

    def get(self, request):

        # gets user's value from current Session
        user = session.get(request, 'user')

        # through template engine hold user's value exchange to page and return 
        return simple_template('index.html', user=user, message='Hi, World!')

class Login(BaseView):
    '''
    login view
    '''

    def get(self, request):

        # from GET request gets state parameter, if not exist then return default value 1
        state = request.args.get('state', '1')

        # through template return login page, when state isn't 1, page information return username error or not exist
        return simple_template('layout.html', title='login', message='input username' if state == '1' else 'username error or not exist, re-enter')

    def post(self, request):

        # put user commit information to database query
        ret = dbconn.execute('''SELECT * FROM user WHERE f_name = %(user)s''', request.form) 

        # if have match result the means its had register, otherwise redirect login page and put state=0, notice page show login error information
        if ret.rows == 1:

            # if matched, get first item data f_name field for username
            user = ret.get_first()['f_name'] 

            # put username to Session
            session.push(request, 'user', user)

            # Session check success, so redirect to index page
            return redirect('/') 
        return redirect('/login?state=0')

class Logout(SessionView):
    '''
    logout view
    '''

    def get(self, request):

        # delete user from current session
        session.pop(request, 'user')

        # return logout success prompt and index link
        return redirect("/")

py_url_map = [
    {
        'url': '/',
        'view': Index,
        'endpoint': 'index'
    },
    {
        'url': '/login',
        'view': Login,
        'endpoint': 'login'
    },
    {
        'url': '/logout',
        'view': Logout,
        'endpoint': 'logout'
    },
    {
        'url': '/api',
        'view': API,
        'endpoint': 'api'
    },
    {
        'url': '/download',
        'view': Download,
        'endpoint': 'download'
    },
    {
        'url': '/register',
        'view': Register,
        'endpoint': 'register'
    }
]

app = PyFlk()

index_controller = Controller('index', py_url_map)
app.load_controller(index_controller)

app.run()
