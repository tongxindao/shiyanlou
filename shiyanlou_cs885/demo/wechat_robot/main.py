import sys
sys.path.append('../..')

from pyflk import PyFlk
from controller import login, index, action, user

app = PyFlk()

app.load_controller(login.controller)
app.load_controller(index.controller)
app.load_controller(user.controller)
app.load_controller(action.controller)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090, threaded=True)
