from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from scales import settings

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY if settings.SECRET_KEY else 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + settings.DATABASE_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

csrf = CSRFProtect(app)

login = LoginManager(app)
login.login_message = 'Please log in to access this page'
login.session_protection = 'strong'
login.login_view = 'login'

from scales import routes, models  # noqa: E402, F401
