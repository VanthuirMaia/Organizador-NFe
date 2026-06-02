from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = 'organizador-nfe-dev-key'

    from .routes.main import bp
    app.register_blueprint(bp)

    return app
