from flask import request,redirect,session,url_for
from app import api, db
from os import environ
from models import *
from script import getAll
from datetime import datetime
from hashlib import md5
from flask.wrappers import  Response
from flask_jwt_extended import create_access_token, unset_jwt_cookies, get_jwt_identity, jwt_required
import json
import requests
from authlib.integrations.flask_client import OAuth

CLIENT_ID=environ.get("CLIENT_ID")
import google_auth_oauthlib
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests
from pip._vendor import cachecontrol

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

# oauth = OAuth(api)

@api.route('/')
def index():
    return "You are logged out <a href='/auth/google'><button>Login</button></a>"

# @api.route('/google')
# def google():
#     GOOGLE_CLIENT_ID = environ.get('CLIENT_ID')
#     GOOGLE_CLIENT_SECRET = environ.get('CLIENT_SECRET')
     
#     CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
#     oauth.register(
#         name='google',
#         client_id=GOOGLE_CLIENT_ID,
#         client_secret=GOOGLE_CLIENT_SECRET,
#         server_metadata_url=CONF_URL,
#         client_kwargs={
#             'scope': 'openid email profile'
#         }
#     )
     
#     redirect_uri = url_for('google_auth', _external=True)
#     return oauth.google.authorize_redirect(redirect_uri)
 
# @api.route('/google/auth')
# def google_auth():
#     token = oauth.google.authorize_access_token()
#     # user = oauth.google.parse_id_token(token)
    # userinfo = token['userinfo']
#     return redirect('/')

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
    session.clear()
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


@api.route("/auth/google")
def loginauth(): 
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true')
    session['state'] = state
    print(state)
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
  userid = idinfo['sub']
  
  session["google_id"] = userid
  del idinfo['aud']
#   session['credentials'] = credentials_to_dict(credentials)
  if len(User.query.filter_by(email = idinfo.get("email")).all()) == 0:
    newuser = User(
        name=idinfo.get("name"),
        email = idinfo.get("email"),
        picture = idinfo.get("picture"),
    ) 

    db.session.add(newuser)
    db.session.commit()
  
  access_token = create_access_token(identity=userid)
  
  return redirect(f"http://localhost:3000/?jwt={access_token}")
#   return json.dumps({"user":idinfo,"message":"ok"})

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





# =============== Messages routes ================= #

@api.route("/sendmsg", methods=["POST"])
# @jwt_required()
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
        "users": [(u.email,u.name,u.picture) for u in User.query.all()],
        "annonces": [a.details() for a in Annonce.query.all()],
        "messages": [m.details() for m in Message.query.all() ],
    }


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}