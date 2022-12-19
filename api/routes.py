from flask import request
from app import api, db
from models import *
from script import getAll
from datetime import datetime
from hashlib import md5
from flask_jwt_extended import create_access_token, unset_jwt_cookies, get_jwt_identity, jwt_required
from datetime import datetime
import requests

import google.oauth2.credentials
from google_auth_oauthlib.flow import Flow
SCOPES = ["https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email"]
CLIENT_SECRETS_FILE = "client_secret.json"



@api.route("/auth/google", methods=["POST"])
def login(request):
    auth_code = request.GET['code']
    flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    SCOPES)

    
    
    flow.fetch_token(code=auth_code)

    # You can use flow.credentials, or you can just get a requests session
    # using flow.authorized_session.
    session = flow.authorized_session()
    print(session.get('https://www.googleapis.com/userinfo/v2/me').json())
    return {"data":session.get('https://www.googleapis.com/userinfo/v2/me').json()}
    
# ================= Annonce Routes ================= #
def add(answer, scraped=False, date=datetime.now()):
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
        scraped = scraped,
        date=date,
    )
    try:
        db.session.add(annonce)
        db.session.commit()
        return {"ok":1}
    except Exception as e:
        return {"ok":0, "msg":str(e)}


@api.route("/new", methods=["POST"])
@jwt_required()
def new():
    answer = request.json
    answer["userId"]= get_jwt_identity()
    return add(answer=answer)


@api.route("/delete", methods=["POST"])
@jwt_required()
def delete():
    concerned = Annonce.query.filter_by(id=request.json["id"]).first()
    if get_jwt_identity() != concerned.userId:
        return {"ok":0, "msg":"Tresspassing detected"}
    
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
    detailed = Annonce.query.filter_by(id=id).first()
    if detailed is None:
        return {"ok":0}
    
    return detailed.details()
 

@api.route("/scrap", methods=["GET"])
def scrap():
    lastscrap = open(".lastscrap", 'r').read() # Need to handle last scrapping in a better way x)
    c=0
    try:
        #result = getAll(l=lastscrap) add it
        result = getAll()
    except:
        return {"ok":0}
    for entry in result:
        entry["userId"]=-1 # Ouedkniss User Id
        a=add(entry, True, datetime.strptime(entry["createdAt"], "%Y-%m-%d") )
        c+=a["ok"]
        
    open(".lastscrap", "w").write(str(datetime.now())[:10])
    return {"ok":1,"added":c}

# ================= Search && filters ================ #

@api.route("/search", methods=["GET"])
def search():
    keywords = request.json["keywords"].split(" ")
    res = []
    for A in Annonce.query.all():
        if any(keyword.lower() in (A.description + A.title).lower() for keyword in keywords):
            res.append(A)
    res = sorted(res)
    return {"data":[r.brief() for r in res]}



# The react app should keep the keywords and send them again
@api.route("/filter", methods=["GET"])
def filter():
    rjson = request.json
    keywords = rjson["keywords"].split(" ")
    res = []
    for A in Annonce.query.all():
        if any(keyword.lower() in (A.description + A.title).lower() for keyword in keywords)\
            and rjson["type"].lower() in A.typ.lower()\
            and rjson["wilaya"].lower() in A.localisation.lower()\
            and rjson["commune"].lower() in A.localisation.lower()\
            and datetime.strptime(rjson["fdate"], "%Y-%m-%d") <= A.date  <= datetime.strptime(rjson["ldate"], "%Y-%m-%d") : #change this
            res.append(A)
    res = sorted(res)
    return {"data":[r.brief() for r in res]}




# ================= User Routes ================= #

@api.route("/register", methods = ["POST"])
def register():
    answer = request.json
    # we can do an email verification here
    if len(User.query.filter_by(email = answer["email"]).all()) > 0:
        return {"ok":0, "msg":"Email already in use!"}
    

    
    newuser = User(
        email = answer["email"],
        password = md5(answer["password"].encode()).hexdigest(),
    )

    db.session.add(newuser)
    db.session.commit()
    return {"ok":1}

@api.route("/login", methods=["POST"])
def login():
    answer = request.json
    user = User.query.filter_by(email = answer["email"], password=md5(answer["password"].encode()).hexdigest()).first()
    
    if user is None:
        return {"ok":0,"msg": "Bad username or password"}
    access_token = create_access_token(identity=user.id)
    return access_token

@api.route("/logout", methods=["POST"])
def logout():
    response = {"ok":1,"msg":"logout successful"}
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
@jwt_required()
def sendmsg():
    try:
        answer = request.json
        senderid = get_jwt_identity()
        receiverid= Annonce.query.filter_by(id=answer["annonceid"]).first().userId
        message = Message(
            senderid = senderid,
            receiverid = receiverid,
            annonceid = answer["annonceid"],
            content = answer["content"]
        )
        db.session.add(message)
        db.session.commit()
        return {"ok":1}
    except:
        return {"ok":0}

@api.route("/getmessages")
@jwt_required()
def getmessages():
    all = Message.query.filter_by(receiverid=get_jwt_identity()).all()
    print(all)
    return { "data": [ m.details() for m in all ] }
    


# ================= Favourite Routes ================= #

@api.route("/getfav", methods=["GET"])
@jwt_required()
def getfav():
    user = User.query.filter_by(id = get_jwt_identity()).first()
    fav = user.favourite.split(",") 
    return {"data":fav}


@api.route("/setfav", methods=["POST"])
@jwt_required()
def setfav():
    user = User.query.filter_by(id = get_jwt_identity()).first()
    fav = user.favourite.split(","); fav.remove("")
    if request.json["id"] not in fav:fav.append(str(request.json["id"]))
    user.favourite = ",".join(fav)
    
    db.session.commit()
    return {"ok":1}

@api.route("/unsetfav", methods=["POST"])
@jwt_required()
def unsetfav():
    user = User.query.filter_by(id = get_jwt_identity()).first()
    fav = user.favourite.split(",") 
    fav.remove(str(request.json["id"]))
    user.favourite = ",".join(fav)
    db.session.commit()
    return {"ok":1}


# ================ Tests_only ===================== #
@api.route("/")
@jwt_required()
def test():
    
    current_user_id = get_jwt_identity()
    r = {
        "user":current_user_id,
    }

    return r

@api.route("/dropdb")
def drop():
    User.query.delete()
    Message.query.delete()
    Annonce.query.delete()
    return {"ok":1}

@api.route("/all", methods=["GET"])
def allusers():
    print("hello")
    return {
        "users": [(u.id,u.email) for u in User.query.all()],
        "annonces": [a.details() for a in Annonce.query.all()],
        "messages": [m.details() for m in Message.query.all() ],
    }
    