from pyflk import PyFlk
from pyflk.view import Controller

from core.base_view import BaseView

class Index(BaseView):
    def get(self, request):
        return 'Hello, World!'

class Test(Index):
    def post(self, request):
        return 'This is a POST request!'

app = PyFlk()

py_url_map = [
    {
        'url': '/index',
        'view': Index,
        'endpoint': 'index'
    },
    {
        'url': '/test',
        'view': Test,
        'endpoint': 'test'
    }
]

index_controller = Controller('index', py_url_map)
app.load_controller(index_controller)

app.run()
