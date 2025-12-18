from flask_mysqldb import MySQL

mysql = MySQL()

def init_db(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'db_passport'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    app.config['MYSQL_PORT'] = 3336

    mysql.init_app(app)