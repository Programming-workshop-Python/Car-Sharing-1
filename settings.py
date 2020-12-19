from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

def create_app():
    app = Flask(__name__)
    return app

def create_config(app):
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:12345@localhost/Data'
    db = SQLAlchemy(app)
    return db

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s - %(message)s')
    file_handler = logging.FileHandler(filename='app.log', mode='w')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

app = create_app()
db = create_config(app)
logger = setup_logger()





