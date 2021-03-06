from authlib.flask.client import OAuth
from config import Config
from flask import Flask
from flask_login import LoginManager
from loginpass import create_flask_blueprint, GitHub


login_manager = LoginManager()
oauth = OAuth()

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    login_manager.init_app(app)
    oauth.init_app(app)

    # Hook in OAuth2 for GitHub. Key here, aside from some settings that flow
    # in via app.config, is that we point to app.main.handle_authorize(),
    # were we catch the result of authenticating, create a new User if
    # necessary, and peform the actual login_user().

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.auth.handlers import handle_authorize
    github_oauth_bp = create_flask_blueprint(GitHub, oauth, handle_authorize)
    app.register_blueprint(github_oauth_bp, url_prefix='/github')

    return app
