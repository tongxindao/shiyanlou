from flask import Flask
from flask import flash
from flask import redirect
from flask import request
from flask import url_for
from flask import render_template

app = Flask(__name__)
app.secret_key = '\x8d\xb2\xb2dd\xfa\ta\xa4\xa3\x10\xbc\x82]\xd8W\x8cS\xb5x\xfdWL'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
            request.form['password'] != 'admin':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    return render_template('login1.html', error=error)

if __name__ == "__main__":
    app.run(debug=True)
