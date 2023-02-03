
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from os import environ

environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


api = Flask(__name__)

api.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
api.config['Access-Control-Allow-Origin'] = '*'
api.config["Access-Control-Allow-Headers"]="Content-Type"
api.config["UPLOAD_FOLDER"]="images"
# to change:
api.config['SECRET_KEY'] = "secret_key" 
api.config["JWT_SECRET_KEY"] = "secret_key_jwt"  
api.config["last_scrap"] = "2023-01-01" 
api.config["adminid"] = 2

jwt = JWTManager(api)
db = SQLAlchemy(api)
CORS(api)

from routes import *

with api.app_context():
    print("creating db :================================)")
    db.create_all()
    
if __name__=="__main__":
    api.run()
    
    

