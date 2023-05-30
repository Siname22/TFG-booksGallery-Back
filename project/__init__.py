import os
import datetime
from flask_cors import CORS
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from project.config import *

# instantiate the db
db = SQLAlchemy()

def create_app():

    # instantiate the app
    app = Flask(__name__)

    #set config
    #app_settings = os.getenv('APP_SETTINGS')
    app_settings = DevelopmentConfig
    app.config.from_object(app_settings)

    

    # setup extensions
    db.init_app(app)
    
    from project.api.operations.base import ops_all
    app.register_blueprint(ops_all)
    CORS(app)
    

    app.shell_context_processor({'app': app, 'db': db})
    
    
    return app