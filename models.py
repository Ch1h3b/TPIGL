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
    
    scraped = db.Column(db.Boolean, default=False)
    def details(self):
        return {"id":self.id, "title":self.title, "category":self.category,  "price":self.price, "description":self.description, "space":self.space,
        "phone":self.phone, "email":self.email, "localisation":self.localisation, "type":self.type, "userId":self.userId}
    def brief(self):
        return {"id":self.id, "title":self.title, "category":self.category,  "price":self.price, "description":self.description, "space":self.space, "localisation":self.localisation}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    favoris = db.Column(db.ARRAY(db.Integer))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senderid = db.Column(db.Integer)
    receiverid = db.Column(db.Integer)
    annonceid = db.Column(db.Integer)
    content = db.Column(db.String)
    def details(self):
        return {"senderid":self.senderid, "content":self.content, "annonceid":self.annonceid}



    

     

