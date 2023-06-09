# Import required modules
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

# Set the view function for the login page
login.login_view = 'auth.signin'
#display message on the login page and message type
login.login_message = "Please Login"
login.login_message_category = "warning"

# Import blueprints
from app.blueprints.auth import bp as auth_bp
from app.blueprints.main import bp as main_bp
from app.blueprints.social import bp as social_bp
from app.blueprints.api import bp as api_bp

# Register the blueprints with Flask
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(social_bp)
app.register_blueprint(api_bp)


from app import models