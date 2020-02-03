import os
from app import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    author = db.Column(db.String())
    published = db.Column(db.String())
    hola = db.Column(db.String())

    def __init__(self, name, author, published, hola):
        self.name = name
        self.author = author
        self.published = published
        self.hola = hola

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'author': self.author,
            'published':self.published,
            'hola':self.hola
        }