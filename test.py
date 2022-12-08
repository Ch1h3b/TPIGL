import requests
import sys
json = {
    "price":1200,
    "description":"Ahhhh",
    "space":"30 m2",
    "phone":"0782220894", 
    "email":"kc_yaici@esi.dz",
    "localisation":"localisation",
    "type":"location",

}


if sys.argv[1]==1:
    requests.post("http://127.0.0.1:5000/new", json=json)
elif sys.argv[1]==2:
    requests.post("http://127.0.0.1:5000/delete", json={"price":1200})
