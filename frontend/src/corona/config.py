import os

### File Upload ###
UPLOAD_FOLDER_LOCATION = 'corona/static/csv'
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

### DB Connecion ###
mysql_config = {
	'host': os.environ.get('MYSQL_HOST', 'localhost'),
	'user': os.environ.get('MYSQL_USER', 'root'),
	'pass': os.environ.get('MYSQL_PASS', ''),
	'db':   os.environ.get('MYSQL_DB', ''),
}

def get_alchemy_uri():
    return 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (
            mysql_config['user'], mysql_config['pass'], mysql_config['host'], mysql_config['db']
    )

