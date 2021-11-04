from flask import Flask, Blueprint
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from authz.config import Config

apiv1_bp = Blueprint("apiv1_bp", __name__, url_prefix="/api/v1")
apiv1 = Api(apiv1_bp)

db = SQLAlchemy()
mg = Migrate()
ma = Marshmallow()

from authz import resource

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mg.init_app(app, db)
    ma.init_app(app)
    app.register_blueprint(apiv1_bp)
    return app
