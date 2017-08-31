import pymysql

class DBResult:
    '''
    database return result object
    '''

    # execute success or fail
    suc = False

    # execute result, usually is querry set, is a list nesting dict structure
    result = None

    # error information
    error = None

    # effect row number
    rows = None

    def index_of(self, index):
        ''' return appoint location a data in result set '''

        # decide if or not execute success, if yes then decide index whether or not is a integer, if yes final decide index whether or not in effective range
        if self.suc and isinstance(index, int) and self.rows > index >= -self.rows:

            # condition establish, return subscript of result
            return self.result[index]

        return None

    def get_first(self):
        ''' return first of data in result set '''

        return self.index_of(0)

    def get_last(self):
        ''' return last of data in result set '''

        return self.index_of(-1)

    @staticmethod
    def handler(func):
        ''' exception capture decorator '''

        def decorator(*args, **options):

            # instantiation
            ret = DBResult()

            # capture exception
            try:

                # assignment for DBResult object's member rows and result
                ret.rows, ret.result = func(*args, **options)

                # modify execute status is True, it means success
                ret.suc = True
            except Exception as e:

                # if capture exception, put it on the DBResult object's error attribute
                ret.error = e

            # return DBResult object
            return ret

        # return decorator method, its amount to return DBResult object
        return decorator

    def to_dict(self):
        ''' structure four attribute component dict '''

        return {
            'suc': self.suc,
            'result': self.result,
            'error': self.error,
            'rows': self.rows
        }

class BaseDB:
    '''
    database module
    '''

    # instance object init method
    def __init__(self, user, password, database='', host='127.0.0.1', port=3306, charset='utf8', cursor_class=pymysql.cursors.DictCursor):
    
        # connect user
        self.user = user

        # connect user password
        self.password = password

        # select database
        self.database = database

        # hostname, default 127.0.0.1
        self.host = host

        # port, default 3306
        self.port = port

        # database charset, default UTF-8
        self.charset = charset

        # database cursor type, default DictCursor, return every row data set all of the dict
        self.cursor_class = cursor_class

        # database connect object
        self.conn = self.connect()

    def connect(self):
        ''' create connect '''

        # return a database connect object
        return pymysql.connect(host=self.host, user=self.user, port=self.port,
                                passwd=self.password, db=self.database,
                                charset=self.charset, cursorclass=self.cursor_class)

    def close(self):
        ''' close connect '''

        # close database connect
        self.conn.close()

    @DBResult.handler
    def execute(self, sql, params=None):
        ''' SQL statement execute method, data operating, add, delete, modify, query '''

        # gets database connect object context
        with self.conn as cursor:

            # if parameter not none and its Dict type, SQL statement and parameter incoming execute call, otherwise direct calll execute
            
            # execute statement and gets effect item number
            rows = cursor.execute(sql, params) if params and isinstance(params, dict) else cursor.execute(sql)

            # gets execute result
            result = cursor.fetchall()

        # return effect item number and execute result
        return rows, result

    def insert(self, sql, params=None):
        ''' insert data and gets last insert data indentified, its the Primary key index field '''

        # gets after SQL statement execute DBResult object
        ret = self.execute(sql, params)

        # DBResult object's result attribute again assignment for insert data's ID
        ret.result = self.conn.insert_id()
    
        # return DBResult object
        return ret

    @DBResult.handler
    def process(self, func, params=None):
        ''' storage process call '''

        # gets database connect object context
        with self.conn as cursor:
     
            # if parameter not none and its Dict type, put storage process name and parameter incoming callproc call, otherwise direct call callproc
            rows = cursor.callproc(func, params) if params and isinstance(params, dict) else cursor.callproc(func)

            # gets storage process execute result
            result = cursor.fetchall()
        return rows, result

    def create_db(self, db_name, db_charset='utf8'):
        ''' create database '''

        return self.execute('CREATE DATABASE %s DEFAULT CHARACTER SET %s' % (db_name, db_charset))

    def drop_db(self, db_name):
        ''' drop database '''

        return self.execute('DROP DATABASE %s' % db_name)

    @DBResult.handler
    def choose_db(self, db_name):
        ''' choose database '''

        # call PyMySQL select_db method select database
        self.conn.select_db(db_name)

        # because correct execute, no effect item and execute result, so return two None
        return None, None
