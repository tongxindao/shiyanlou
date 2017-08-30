from pyflk.view import Controller
from pyflk.session import session
from pyflk import PyFlk, simple_template, redirect, render_json, render_file

from core.base_view import BaseView, SessionView

class Download(BaseView):
    def get(self, request):
        return render_file("main.py")

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
        return simple_template('login.html')

    def post(self, request):

        # gets user parameter's value from the POST request
        user = request.form['user']

        # user save to current Session
        session.push(request, 'user', user)

        # return login success prompt and index link
        return redirect("/")

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
    }
]

app = PyFlk()

index_controller = Controller('index', py_url_map)
app.load_controller(index_controller)

app.run()
