import os, enum
from datetime import datetime
from app import db
from apps.user.models import UserA
from apps.projects.models import *


class StoryPriority(enum.Enum):
    high = 'high'
    medium = 'medium'
    low = 'low'


class Story(db.Model):
    __tablename__ = 'stories'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    priority = db.Column(
        db.Enum(StoryPriority), 
        default= StoryPriority.high,
        nullable=False
    )
    epic = db.Column(db.Boolean)
    done = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    parent_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    children = db.relationship('Story', lazy='joined')
    
    def __init__(self,project_id,description,priority,epic):
        self.description = description
        self.project_id = project_id
        self.priority =  priority
        self.epic = epic
        self.done = False  

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'description': self.description,
            'project_id': self.project_id,
            'priority':self.priority.value,
            'epic':self.epic,
            'done':self.done,
            'date_created':self.date_created,
            'parent_id':self.parent_id
        }



