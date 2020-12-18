from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy.orm import sessionmaker

def create_app():
    app = Flask(__name__)
    return app

def create_config(app):
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:12345@localhost/Data'
    db = SQLAlchemy(app)
    return db

app = create_app()
db = create_config(app)




