from flask import Flask
from flask import abort
from flask import redirect
from flask import url_for
from flask import render_template
from flask import make_response

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(404)
    this_is_never_executed()

@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('page_not_found.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

if __name__ == '__main__':
    app.run(debug=True)
