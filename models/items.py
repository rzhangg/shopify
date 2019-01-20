import os
from server import db, ma

class Item(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title= db.Column(db.String(124), unique=True)
    price= db.Column(db.Integer)
    units= db.Column(db.Integer)

    def __init__(self, title, price, units):
        self.title = title
        self.price = price
        self.units = units

class ItemSchema(ma.Schema):
    class Meta:
        """
        Expose these fields in json
        """
        fields= ('title', 'price', 'units')




