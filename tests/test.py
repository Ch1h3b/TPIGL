#!/usr/bin/python3
import requests
import sys
import random

random_json = {
    "title": random.choice(["maison f chbab", "Dar chaba", "Terrain 9owa"]),
    "price":random.choice([120000, 99999, 133337]),
    "description":"key word key word",
    "space":random.choice(["30 m2", "400 m2", "0 m2"]),
    "phone":"0782220894", 
    "email":random.choice(["kc_yaici@esi.dz", "ka_atoui@esi.dz" ]),
    "localisation":"Alger, bachdjerah, lamontagne",
    "type":random.choice(["terrain", "appartement", "maison", "villa"]),
    "category":random.choice([ "location", "echange", "vente"])
}
h={"Authorization":"Bearer " + open(".tmpauth").read()}
authj={"email":"kb_arab@esi.dz", "password":"123", "name":"bilal", "lname":"chabi"}
if len(sys.argv)<2:
    print("Usage: python test.py <function>")
    exit(0)
elif sys.argv[1]=="register":
    r=requests.post("http://127.0.0.1:5000/register", json=authj)
    print(r.text)
elif sys.argv[1]=="login":
    r=requests.post("http://127.0.0.1:5000/login", json=authj)
    print(r.text)
    open(".tmpauth","w").write(r.text)
elif sys.argv[1]=="login":
    r=requests.post("http://127.0.0.1:5000/logout")
    print(r.text)
elif sys.argv[1]=="new":
    r=requests.post("http://127.0.0.1:5000/new", json=random_json, headers=h)
    print(r.text)
elif sys.argv[1]=="delete":
    r=requests.post("http://127.0.0.1:5000/delete", json={"id":"1"}, headers=h)
    print(r.text)
elif sys.argv[1]=="getuid":
    r=requests.get("http://127.0.0.1:5000/",headers=h)
    print(r.text)
elif sys.argv[1]=="getannonce":
    r=requests.get("http://127.0.0.1:5000/getai", json={"id":1})
    print(r.text)
elif sys.argv[1]=="dropdb":
    r=requests.get("http://127.0.0.1:5000/dropdb")
    print(r.text)
elif sys.argv[1]=="all":
    r=requests.get("http://127.0.0.1:5000/all")
    print(r.text)
elif sys.argv[1]=="sendmsg":
    r=requests.post("http://127.0.0.1:5000/sendmsg", headers=h, json={"annonceid":1, "content":"Toujours dispo ?? :)"})
    print(r.text)
elif sys.argv[1]=="getmymsg":
    r=requests.get("http://127.0.0.1:5000/getmessages", headers=h)
    print(r.text)
elif sys.argv[1]=="search":
    r=requests.get("http://127.0.0.1:5000/search", json={"keywords":""})
    print(r.text)

elif sys.argv[1]=="filter":
    json={
        "keywords":"",
        "type":"pfff", #maison
        "wilaya":"", #spain
        "commune":"", # ?
        "fdate":"2022-12-14",
        "ldate":"2022-12-16",
    }
    print(requests.get("http://127.0.0.1:5000/filter", json=json).text)

elif sys.argv[1]=="setf":
    print(requests.post("http://127.0.0.1:5000/setfav", headers=h, json={"id":1}).text)
elif sys.argv[1]=="unsetf":
    print(requests.post("http://127.0.0.1:5000/unsetfav", headers=h, json={"id":1}).text)
elif sys.argv[1]=="getf":
    print(requests.get("http://127.0.0.1:5000/getfav", headers=h).text)
elif sys.argv[1]=="scrap":
    print(requests.get("http://127.0.0.1:5000/scrap").text)