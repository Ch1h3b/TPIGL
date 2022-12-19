from flask import request
from app import api, db
from models import *
from script import getAll
from datetime import datetime
from hashlib import md5
from flask_jwt_extended import create_access_token, unset_jwt_cookies, get_jwt_identity, jwt_required
from json import dumps


# ================= Annonce Routes ================= #
def add(answer, scrapped=False):
    annonce = Annonce(

        userId = answer["userId"],
        
        title = answer["title"],
        description = answer["description"],

        type = answer["type"],
        category = answer["category"],

        price = answer["price"],        
        space =  answer["space"],

        phone =  answer["phone"],
        email =  answer["email"],
        
        localisation = answer["localisation"],
        scrapped = scrapped
    )
    try:
        db.session.add(annonce)
        db.session.commit()
        return {"ok":1}
    except Exception as e:
        return {"ok":str(e)}

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
 
    
@api.route("/scrap", methods=["GET"])
def scrap():
    lastscrap = open(".lastcrap", 'r').read() # Need to handle last scrapping in a better way x)
    c=0
    try:
        #result = getAll(l=lastscrap) add it
        result = getAll()
    except:
        return {"ok":0}
    for entry in result:
        entry["userId"]=-1 # Ouedkniss User Id
        a=add(entry, True)
        c+=a["ok"]
        
    open(".lastscrap", "w").write(str(datetime.now())[:10])
    return {"ok":1,"added":c}

# ================= Search && filters ================ #

@api.route("/search", methods=["GET"])
def search():
    keywords = request.json["keywords"].split(" ")
    res = []
    for A in Annonce.query.all():
        if any(keyword in A.description + A.title for keyword in keywords):
            res.append(A)
    return {"data":[r.brief() for r in res]} 


# Should we resend the keywords ??
# Suppose the json request body looks like this
# {"keywords":keywords, "type":type or "", "wilaya":wilaya or ""....}
@api.route("/filter", methods=["GET"])
def filter():
    rjson = request.json
    keywords = rjson["keywords"].split(" ")
    res = []
    for A in Annonce.query.all():
        if any(keyword.lower() in (A.description + A.title).lower() for keyword in keywords)\
            and rjson["type"] == A.type\
            and rjson["wilaya"].lower() in A.location.lower()\
            and rjson["commune"].lower() in A.location.lower()\
            and "time"=="time": #change this
            res.append(A)
    return {"data":[r.brief() for r in res]}


# ================= Favourite Routes ================= #

@api.route("/getfavourite", methods=["GET"])
def getfav():
    pass


@api.route("/setfavourite", methods=["GET"])
def setfav():
    pass




# ================= User Routes ================= #

@api.route("/register", methods = ["POST"])
def register():
    answer = request.json
    # we can do an email verification here
    if len(User.query.filter_by(email = answer["email"])) > 0:
        return {"ok":0, "msg":"Email already in use!"}
    
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
    
    if user is None:
        return {"msg": "Bad username or password"}
    access_token = create_access_token(identity=answer["email"])
    return access_token

@api.route("/logout", methods=["POST"])
def logout():
    response = {"msg":"logout successful"}
    unset_jwt_cookies(response)
    return response





def refresh(request):
    refresh_token = request.GET['refresh_token']

    data = {
        'refresh_token': refresh_token,
        'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY, # client ID
        'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET, # client secret
        'grant_type': 'refresh_token'
    }

    response = requests.post('https://oauth2.googleapis.com/token', data=data)

    return JsonResponse(response.json(), status=200)

# =============== Messages routes ================= #
@api.route("/sendmsg", methods=["POST"])
def sendmsg():
    try:
        answer = request.json
        message = Message(
            senderid = answer["senderid"],
            receiverid = answer["reveiverid"],
            annonceid = answer["annonceid"],
            content = answer["content"]
        )
        db.session.add(message)
        db.session.commit()
        return {"ok":1}
    except:
        return {"ok":0}

@api.route("/getmessages")
def getmessages():
    all = Annonce.query.filter_by(receiverid=request.json["reveiverid"])
    return { [ a.details() for a in all ] }
    

@api.route("/")
@jwt_required()
def test():
    
    current_user = get_jwt_identity()
    r = {
        "user":current_user,
    }

    return r