import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = '\xf7\xe9)q\n\xb5W\xed\xed\xd4:L:\xb7\\\xf3K\xf0\x00\x93\x7f\x19\xb8L\xd2\xbabR\xf6%\x02'
