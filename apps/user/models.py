import os
from app import db

class UserA(db.Model):
    __tablename__ = 'userA'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self,username,first_name,last_name,role,password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'username': self.username,
            'firs_name': self.first_name,
            'last_name':self.last_name,
            'role':self.role
        }