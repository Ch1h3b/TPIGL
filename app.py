
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_jwt_extended import JWTManager


api = Flask(__name__)
api.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
api.config['SECRET_KEY'] = environ.get('SECRET_KEY')
db = SQLAlchemy(api)

api.config["JWT_SECRET_KEY"] = "aaaa"  # Change this!
jwt = JWTManager(api)

from routes import *



with api.app_context():
    print("creating db :================================)")
    db.create_all()
#api.run()
    
    

