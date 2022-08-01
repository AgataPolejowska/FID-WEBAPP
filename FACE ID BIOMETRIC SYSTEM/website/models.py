from website import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(20), nullable=False)
    w1 = db.Column(db.Integer)
    w2 = db.Column(db.Integer)
    w3 = db.Column(db.Integer)
    w4 = db.Column(db.Integer)
    w5 = db.Column(db.Integer)
    w6 = db.Column(db.Integer)
    w7 = db.Column(db.Integer)

class FaceImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(60), nullable=False)
    