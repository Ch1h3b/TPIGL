from flask import request
from app import api, db
from models import *
from script import getAll
from datetime import datetime
from hashlib import md5
from flask_jwt_extended import create_access_token, unset_jwt_cookies, get_jwt_identity, jwt_required
from json import dumps

# ================= Annonce Routes ================= #

@api.route("/new", methods=["POST"])
def new():
    answer = request.json
    return add(answer=answer)

    

@api.route("/delete", methods=["POST"])
def delete():
    concerned = Annonce.query.filter_by(price=1200).first()
    if(concerned is not None):
        try:
            db.session.delete(concerned)
            db.session.commit()
            return {"ok":1}
        except:
            pass
    return {"ok":0}

@api.route("/getai", methods=["GET"])
def getDetail():
    id = request.json["id"]
    #detailed = Annonce.query.filter_by(id=id).first()
    detailed = Annonce.query.filter_by(price=1200).first()
    if detailed is None:
        return {"ok":0}
    
    return detailed.details()


@api.route("/search", methods=["POST"])
def search():
    pass    
    
    
@api.route("/scrap", methods=["GET"])
def scrap():
    lastscrap = open(".lastcrap", 'r').read() # Need to handle last scrapping in a better way x)
    c=0
    try:
        result = getAll()
    except:
        return {"ok":0}
    for entry in result:
        a=add(entry)
        c+=a["ok"]
        
    open(".lastscrap", "w").write(str(datetime.now())[:10])
    return {"ok":1,"added":c}








# ================= User Routes ================= #

@api.route("/register", methods = ["POST"])
def register():
    answer = request.json
    # we can do an email verification here
    newuser = User(
        email = answer["email"],
        password = md5(answer["password"].encode()).hexdigest()
    )

    db.session.add(newuser)
    db.session.commit()
    return {"ok":1}

@api.route("/login", methods=["POST"])
def login():
    answer = request.json
    #db.session.query()
    user = User.query.filter_by(email = answer["email"], password=md5(answer["password"].encode()).hexdigest()).first()
    print(user)
    if user is None:
        return {"msg": "Bad username or password"}
    access_token = create_access_token(identity=answer["email"])
    return access_token

@api.route("/logout", methods=["POST"])
def logout():
    response = {"msg":"logout successful"}
    unset_jwt_cookies(response)
    return response




@api.route("/")
@jwt_required()
def test():
    
    current_user = get_jwt_identity()
    r = {
        "user":current_user,
    }

    return r