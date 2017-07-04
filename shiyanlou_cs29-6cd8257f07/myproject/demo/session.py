# _*_coding:UTF-8 _*_
from flask import Flask
from flask import session
from flask import redirect
from flask import url_for
from flask import escape
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
             <p>Username:<input type=text name=username></p>
             <p><input type=submit value=Login></p>
        </form>
    '''

@app.route('/logout')
def logout():
    # 如果用户名存在，则从会话中移除该用户名
    session.pop('username', None)
    return redirect(url_for('index'))

# 设置密钥，保证会话安全
app.secret_key = '\x8d\xb2\xb2dd\xfa\ta\xa4\xa3\x10\xbc\x82]\xd8W\x8cS\xb5x\xfdWL'

if __name__ == '__main__':
    app.run(debug=True)
