from app import db


class Annonce(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scraped = db.Column(db.Boolean, default=False)
    price = db.Column(db.Integer)
    description = db.Column(db.String)
    space =  db.Column(db.String)
    phone =  db.Column(db.String)
    email =  db.Column(db.String)
    localisation = db.Column(db.String)
    type = db.Column(db.String)
    

     

