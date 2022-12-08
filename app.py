from flask import Flask
from flask_sqlalchemy import SQLAlchemy

api = Flask(__name__)
api.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
api.config['SECRET_KEY'] = "allouma"
db = SQLAlchemy(api)

from routes import *


if __name__ == '__main__':
    with api.app_context():db.create_all()
    api.run()
    
    

