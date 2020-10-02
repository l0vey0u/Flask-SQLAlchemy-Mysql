from flask import Flask

app = Flask(__name__)

from corona import config
app.config['UPLOAD_FOLDER_LOCATION'] = config.UPLOAD_FOLDER_LOCATION
from corona import routes
