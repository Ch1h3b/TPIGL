
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_jwt_extended import JWTManager
from flask_cors import CORS

api = Flask(__name__)
api.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
api.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(api)
CORS(api,resources={r"/*": {"origins": "*"}})

api.config['Access-Control-Allow-Origin'] = '*'
api.config["Access-Control-Allow-Headers"]="Content-Type"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api.config["JWT_SECRET_KEY"] = "aaaa"  # Change this!
jwt = JWTManager(api)

from routes import *



with api.app_context():
    print("creating db :================================)")
    db.create_all()
    
if __name__=="__main__":
    api.run()
    
    

