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


if sys.argv[1]=="1":
    print("a???????????????????,")
    r=requests.post("http://127.0.0.1:5000/new", json=json)
    #print(r.text)
elif sys.argv[1]=="2":
    requests.post("http://127.0.0.1:5000/delete", json={"price":1200})
elif sys.argv[1]=="3":
    print("heaaaaaaaaaaaaaaaaa")
    r=requests.post("http://127.0.0.1:5000/login", json={"email":"ks_sbaa@esi.dz", "password":"123"})
    print(r.text)
elif sys.argv[1]=="4":
    r=requests.get("http://127.0.0.1:5000/",headers={"Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3MTAyODAwNywianRpIjoiYWJiZjUwOTctZTkzMi00ZGZiLTg3MjAtNDlhOWY5ZTVlOTk2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImtjX3lhaWNpQGVzaS5keiIsIm5iZiI6MTY3MTAyODAwNywiZXhwIjoxNjcxMDI4OTA3fQ.cCiQ8_dquizRpJxD1xQpgm1nsnMQQFkng2WFaLhY_ug"})
    print(r.text)
elif sys.argv[1]=="5":
    r=requests.post("http://127.0.0.1:5000/register", json={"email":"ks_sbaa@esi.dz", "password":"123"})
    print(r.text)
elif sys.argv[1]=="6":
    r=requests.get("http://127.0.0.1:5000/getai", json={"id":1})
    print(r.text)