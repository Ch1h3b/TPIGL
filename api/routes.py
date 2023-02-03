from flask import request,redirect,session,url_for, send_from_directory
from app import api, db
from os import environ, path, getcwd
from models import *
from script import getAll
from datetime import datetime,timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from pip._vendor import cachecontrol
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests
import requests
import google_auth_oauthlib
import random
import string


CLIENT_ID=environ.get("CLIENT_ID")

SCOPES = [
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
        "https://www.googleapis.com/auth/drive.metadata.readonly"
    ]
CLIENT_SECRETS_FILE = "client_secrets.json"

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    SCOPES,
    redirect_uri="http://localhost:5000/oauth2callback")


# ================= User Routes ================= #

@api.route("/login", methods=["GET"])
@jwt_required()
def login():
    if request.headers.get("Authorization"):
        jwtr = request.headers.get("Authorization").split(" ")[1]

    user = User.query.filter_by(id = get_jwt_identity()).first()
    return {"name":user.name,"picture":user.picture,"token":jwtr}


@api.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    response = {"ok":1,"msg":"logout successful"}
    session.clear()
    return response


@api.route("/auth/google")
def loginauth(): 
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true')
    session['state'] = state
    url_for("oauth2callback")
    return redirect(authorization_url)
     

@api.route('/oauth2callback')
def oauth2callback():
  if not session['state'] == request.args['state']:
        ConnectionAbortedError(500)
  state = session['state']
  print(state)

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES,state=state)

  flow.redirect_uri = url_for('oauth2callback', _external=True)
  
  
  flow.fetch_token(authorization_response=request.url)

  credentials = flow.credentials
  request_session = requests.session()
  cached_session = cachecontrol.CacheControl(request_session)
  token_request = google.auth.transport.requests.Request(session=cached_session)
  
  idinfo = id_token.verify_oauth2_token(id_token= credentials._id_token,request=token_request ,audience= CLIENT_ID)
  

  del idinfo['aud']
  if len(User.query.filter_by(email = idinfo.get("email")).all()) == 0:
    newuser = User(
        name=idinfo.get("name"),
        email = idinfo.get("email"),
        picture = idinfo.get("picture"),
    ) 
    
    db.session.add(newuser)
    db.session.commit()
  userId = User.query.filter_by(email = idinfo.get("email")).first().id
    
  access_token = create_access_token(identity=userId,expires_delta=timedelta(days=7))
  return redirect(f"http://localhost:3000/?jwt={access_token}")


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
        livesin = answer["livesin"],

        localisation = answer["localisation"],
        pics= answer["pics"],
        scraped = scraped,
        date=date,
        
    )
    
    try:
        db.session.add(annonce)
        db.session.commit()
        return annonce
    except Exception as e:
        return {"ok":0}


@api.route("/getMine", methods=["GET"])
@jwt_required()
def getMesAnn():
    myAnnonces = [a.brief() for a in  Annonce.query.filter_by(userId=get_jwt_identity()).all()]
    return {"data":myAnnonces}

@api.route("/images/<pic>")
def getimage(pic):
    return send_from_directory(api.config["UPLOAD_FOLDER"], pic)


def upload(images):
    list = []
    for image in images:
        if not (image.filename.endswith("jpg") or image.filename.endswith("png")):continue
        rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7)) + ".{ext}".format(ext=image.filename.split(".")[-1])
        image.save(path.join(getcwd(),api.config["UPLOAD_FOLDER"] ,rand))
        list.append(rand)
    
    return ",".join(list) if len(list)>0 else ","

@api.route("/new", methods=["POST"])
@jwt_required()
def new():
    
    r=request.form
    print(r.keys())
    
    answer={
        "title":r.get("title"),
        "description":r.get("description"),
        "type":r.get("type"),
        "category":r.get("category"),
        "price":r.get("price"),
        "space":r.get("space"),
        "phone":r.get("phone"),
        "localisation": ",".join([r.get("wilaya"),r.get("commune"),r.get("addresse")]),
        "userId":get_jwt_identity(),
        "pics":upload(request.files.getlist('images')),
        "email":User.query.filter_by(id=get_jwt_identity()).first().email,
        "livesin":r.get("myaddresse")
    }
    
    
    print(answer)
    return add(answer=answer).details()


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
            return {"ok":1,"id":request.json["id"]}
        except:
            pass
    return {"ok":0}

@api.route("/getai/<int:id>", methods=["GET"])
@jwt_required()
def getDetail(id):
    print(id)
    detailed = Annonce.query.filter_by(id=id).first()
    if detailed is None:
        return {"ok":0}
    
    return detailed.details()

# ================= Admin ================ #
@api.route("/getAll", methods=["GET"])
@jwt_required()
def getAllAnnonces():
    if get_jwt_identity() != api.config["adminid"]:return {"ok":0, "msg":"Tresspassing detected"}
    allAnnonces = Annonce.query.all()
    return [a.brief() for a in allAnnonces] 

@api.route("/scrap", methods=["GET"])
@jwt_required()
def scrap():
    if get_jwt_identity() != api.config["adminid"]:return {"ok":0, "msg":"Tresspassing detected"}
    lastscrap = api.config["last_scrap"]
    added=[]
    
    try:
        result = getAll(l=lastscrap) # add it
        
    except:
        return {"ok":0}
    for entry in result:
        
        entry["userId"]=-1 # Ouedkniss User Id
        entry["livesin"]=""
        
        a=add(entry, True, datetime.strptime(entry["createdAt"], "%Y-%m-%d") )
        added.append(a)
        print(a)
    
    api.config["last_scrap"] = str(datetime.now())[:10]
    return {"ok":1, "data":[a.brief() for a in added]}

# ================= Search && filters ================ #

@api.route("/search", methods=["POST"])
@jwt_required()
def search():
    keywords = request.json["keywords"]
    res = []
    for A in Annonce.query.all():
        if any(keyword.lower() in (A.description+ " " + A.title).lower().split(' ') for keyword in keywords):
            res.append(A)
    res = sorted(res)
    return {"data":[r.brief() for r in res]}





# =============== Messages routes ================= #

@api.route("/sendmsg", methods=["POST"])
@jwt_required()
def sendmsg():
    try:
        answer = request.json
        message = Message(
            senderid = get_jwt_identity(),
            receiverid = Annonce.query.filter_by(id=answer["annonceid"]).first().userId,
            annonceid = answer["annonceid"],
            content = answer["content"],
            date=datetime.now()
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
    return { "data": [ m.details() for m in all ] }
    


# ================= Favourite Routes ================= #

@api.route("/getfav", methods=["GET"])
@jwt_required()
def getfav():
    user = User.query.filter_by(id = get_jwt_identity()).first()
    if (user):
        fav=[]
        if (user.favourite!=","):
            fav = [Annonce.query.filter_by(id=int(i)).first().brief() for i in user.favourite.split(",") ]
            return {"data":fav}
    return {"ok":0,"data":fav}

@api.route("/setfav", methods=["POST"])
@jwt_required()
def setfav():
    user = User.query.filter_by(id = get_jwt_identity()).first()
    if user.favourite==",":fav=[]
    else:
        fav = user.favourite.split(",")
        if "" in fav:fav.remove("")
    if request.json["id"] not in fav:
        fav.append(str(request.json["id"]))
        user.favourite = ",".join(fav)
        db.session.commit()
        fav = Annonce.query.filter_by(id=int(request.json["id"])).first().brief()
        return {"ok":1,"fav":fav}
    return {"ok":0,"fav":{}}

@api.route("/unsetfav", methods=["POST"])
@jwt_required()
def unsetfav():
    user = User.query.filter_by(id = get_jwt_identity()).first()
    fav = user.favourite.split(",") 
    fav.remove(str(request.json["id"]))
    user.favourite = ",".join(fav)
    db.session.commit()
    return {"ok":1,"id":request.json["id"]} 

# =================== Static ====================== #
@api.route("/wilaya", methods=["GET"])
def wilaya():    
    return eval(open("new_wilayas.json").read())

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
    # User.query.delete()
    # Message.query.delete()
    Annonce.query.delete()
    db.session.commit()
    return {"ok":1}

@api.route("/all", methods=["GET"])
def allusers():
    return {
        "users": [(u.email,u.name,u.picture,u.favourite,u.id) for u in User.query.all()],
        "annonces": [a.details() for a in Annonce.query.all()],
        "messages": [m.details() for m in Message.query.all() ],
    }


@api.route("/logintest", methods=["POST"])
def logintest():
    answer = request.json
    user = User.query.filter_by(email = answer["email"]).first()
    
    if user is None:
        return {"ok":0,"msg": "Bad username or password"}
    access_token = create_access_token(identity=user.id)
    return access_token




