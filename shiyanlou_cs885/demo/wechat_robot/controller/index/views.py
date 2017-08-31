from pyflk import simple_template
from pyflk.session import session

from core.base_view import SessionView

class Index(SessionView):
    def get(self):
        user = session.get(self.request, 'user')
        return simple_template('index.html', message='current user', user=user)
