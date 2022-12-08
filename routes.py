from flask import request
from app import api, db
from models import *

@api.route("/new", methods=["POST"])
def new():
    answer = request.json

    annonce = Annonce(
        price = answer["price"],
        description = answer["description"],
        space =  answer["space"],
        phone =  answer["phone"],
        email =  answer["email"],
        localisation = answer["localisation"],
        type = answer["type"],
    )
    try:
        db.session.add(annonce)
        db.session.commit()
        return {"ok":1}
    except:
        return {"ok":0}

    

@api.route("/delete", methods=["POST"])
def delete():
    concerned = Annonce.query.filter_by(price=1200).first()#
    if(concerned is not None):
        try:
            db.session.delete(concerned)
            db.session.commit()
            return {"ok":1}
        except:
            return {"ok":0}
    return {"ok":0}

@api.route("/search", methods=["GET"])
def search():
    pass    
    
    

@api.route("/")
def test():
    r = {
        "key":"value",
    }

    return r