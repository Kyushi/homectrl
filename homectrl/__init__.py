from flask import Flask
from pathlib import Path

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='topsecret',
        DATABASE=str(Path(app.instance_path) / 'homectrl.sqlite')
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        ap.config.from_mapping(test_config)
    
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    
    @app.route('/test')
    def test():
        return "You found me!"
    
    from . import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')
    
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)

    from . import room
    app.register_blueprint(room.bp)

    from . import heater
    app.register_blueprint(heater.bp)

    return app

