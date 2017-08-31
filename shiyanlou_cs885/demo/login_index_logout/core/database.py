from pyflk.dbconnector import BaseDB

# connect username
db_user = 'root'

# connect password
db_password = ''

# database name
db_database = 'db_demo'

# capture exception, because first connect database not exist, so program throw exception, after capture go to exception statement database init
try:
    
    # capture database connect object and appoint database name, if database not exist, throw exception
    dbconn = BaseDB(db_user, db_password, db_database)
except Exception as e:

    # capture exception code
    code, _ = e.args

    # if exception code is 1049 its means database not exist exception, then start create, otherwise unknown error, output information and quit
    if code == 1049:

        # create database table statement
        create_table = \
            '''CREATE TABLE user (
               id INT PRIMARY KEY AUTO_INCREMENT,
               f_name VARCHAR(50) UNIQUE
            ) CHARSET=utf8'''

        # gets a not appoint database connect object
        dbconn = BaseDB(db_user, db_password)

        # create database, return DBResult object
        ret = dbconn.create_db(db_database)

        # if create success, change to this database, then start create data table
        if ret.suc:

            # create database success, change to this database
            ret = dbconn.choose_db(db_database)

            # if change success, start create data table
            if ret.suc:
            
                # create data table
                ret = dbconn.execute(create_table)

        # if above operating anyone error, then drop database and before to create database status
        if not ret.suc:

            # drop database
            dbconn.drop_db(db_database)

            # output error information and quit
            print(ret.error.args)
            exit()
    else:

        # output error information and quit
        print(e)
        exit()
