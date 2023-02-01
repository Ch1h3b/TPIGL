from app import db


class Annonce(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    title = db.Column(db.String)
    description = db.Column(db.String)

    type = db.Column(db.String)
    category = db.Column(db.String)

    price = db.Column(db.Integer)
    space =  db.Column(db.String)
    phone =  db.Column(db.String)
    email =  db.Column(db.String)
    localisation = db.Column(db.String)
    
    date = db.Column(db.DateTime)
    scraped = db.Column(db.Boolean, default=False)

    pics = db.Column(db.String,default=",")
    livesin = db.Column(db.String)
    def details(self):
        return {
        "id":self.id, "title":self.title, "category":self.category,  "price":self.price, "description":self.description, "space":self.space,
        "phone":self.phone, "email":self.email, "localisation":self.localisation, "type":self.type, "userId":self.userId,
        "date":self.date, "pics":["/images/" + i for i in self.pics.split(",")], "livesin":self.livesin
        }
    def brief(self):
        return {"id":self.id,"userId":self.userId, "title":self.title, "category":self.category,  "price":self.price, "description":self.description, "space":self.space, "type":self.type, "localisation":self.localisation, "date":self.date, "pics":["/images/" + i for i in self.pics]}
    def __eq__(self, other):
        return self.date == other.date 

    def __lt__(self, other):
        return self.date < other.date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    favourite = db.Column(db.String, default=",")
    name = db.Column(db.String)
    favourite = db.Column(db.String, default=",")
    picture = db.Column(db.String,default="")

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senderid = db.Column(db.Integer)
    receiverid = db.Column(db.Integer)
    annonceid = db.Column(db.Integer)
    content = db.Column(db.String)
    date = db.Column(db.DateTime)
    def details(self):
        return {"senderid":self.senderid, "receiverid":self.receiverid, "content":self.content, "annonceid":self.annonceid, "date":self.date}



    

     

