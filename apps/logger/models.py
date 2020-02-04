import os
from app import db

class Logger(db.Model):
    __tablename__ = 'logger'

    id = db.Column(db.Integer, primary_key=True)
    #user = db.Column(db.Integer, ForeignKey('user.user_id'))
    event = db.Column(db.String())
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, use=None, event, date):
        self.user = user
        self.event = event
        self.date = date

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'user': self.user,
            'event': self.event,
            'date':self.date
        }