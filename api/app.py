
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from os import environ

api = Flask(__name__)

api.config['SECRET_KEY'] = environ.get('SECRET_KEY')
api.config["JWT_SECRET_KEY"] = "aaaa"  # Change this!
api.config["last_scrap"] = "2022-12-15" # probably this too
api.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
api.config['Access-Control-Allow-Origin'] = '*'
api.config["Access-Control-Allow-Headers"]="Content-Type"

jwt = JWTManager(api)
db = SQLAlchemy(api)
CORS(api)

from routes import *

with api.app_context():
    print("creating db :================================)")
    db.create_all()
    
if __name__=="__main__":
    api.run()
    
    

