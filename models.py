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

    def details(self):
        return {"id":self.id, "price":self.price, "description":self.description, "space":self.space,   }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)


def add(answer):
    annonce = Annonce(
        price = answer["price"],
        description = answer["description"],
        space =  answer["space"],
        phone =  answer["phone"],
        email =  answer["email"],
        localisation = answer["localisation"],
        type = answer["type"],
    )
    try:
        db.session.add(annonce)
        db.session.commit()
        return {"ok":1}
    except Exception as e:
        return {"ok":str(e)}
    

     

