from flask import Flask
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object('config')
UPLOAD_FOLDER = 'D:/Desktop/FlaskProg/app/static/files'
MAX_FILE_SIZE = 1024 * 1024 + 1
from app import views