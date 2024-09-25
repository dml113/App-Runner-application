from flask import Flask

def create_app():
    app = Flask(__name__)

    from application.api import bp as index_bp
    app.register_blueprint(index_bp)

    return app
