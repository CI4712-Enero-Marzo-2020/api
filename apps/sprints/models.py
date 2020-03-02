import os, enum
from datetime import datetime
from app import db
from apps.user.models import UserA
from apps.projects.models import *
from apps.stories.models import *

class Sprint(db.Model):
    __tablename__ = 'sprints'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('userA.id'))
    #relacion one sprint - one project OBLIGATORIO
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    #relacion many stories - one sprint
    stories = db.relationship('Story', backref='sprints', lazy=True, post_update=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    closed = db.Column(db.Boolean)

    def __init__(self, user_id, description, project_id, closed):
        self.user_id = user_id
        self.description = description
        self.project_id = project_id
        self.closed = closed

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        user = UserA.query.get_or_404(self.user_id)
        return {
            'id': self.id, 
            'description': self.description,
            'user': {
                'id':user.id,
                'username':user.username
            },
            'date_created':self.date_created,
            'closed':self.closed
        }


class AcceptanceCriteria(db.Model):
    __tablename__ = 'acceptcriteria'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    # relacion one criteria - one project OBLIGATORIO
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('userA.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean)

    def __init__(self, user_id, description, story_id, approved):
        self.user_id = user_id
        self.description = description
        self.story_id = story_id
        self.approved = approved

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        story = Story.query.get_or_404(self.story_id)
        user = UserA.query.get_or_404(self.user_id)
        return {
            'id': self.id, 
            'description': self.description,
            'user': {
                'id':user.id,
                'username':user.username
            },
            'date_created':self.date_created,
            'story':{
                'id':story.id,
                'description':story.description
            },
            'approved':self.approved
        }

class AcceptanceTest(db.Model):
    __tablename__ = 'accepttests'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    # relacion one test - one project OBLIGATORIO
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('userA.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean)

    def __init__(self, user_id, description, story_id, approved):
        self.user_id = user_id
        self.description = description
        self.story_id = story_id
        self.approved = approved

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        story = Story.query.get_or_404(self.story_id)
        user = UserA.query.get_or_404(self.user_id)
        return {
            'id': self.id, 
            'description': self.description,
            'user': {
                'id':user.id,
                'username':user.username
            },
            'date_created':self.date_created,
            'story':{
                'id':story.id,
                'description':story.description
            },
            'approved':self.approved
        }