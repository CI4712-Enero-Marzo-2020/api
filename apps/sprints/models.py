import os, enum
from datetime import datetime
from app import db
from apps.user.models import *
from apps.projects.models import *
from apps.stories.models import *


class Sprint(db.Model):
    __tablename__ = "sprints"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('userA.id'))
    #relacion one sprint - one project OBLIGATORIO
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    #relacion many stories - one sprint
    stories = db.relationship('Story', backref='sprints', lazy=True, post_update=True)
    burn_up = db.relationship('BurnUp', backref='sprints', lazy=True, post_update=True)
    burn_down = db.relationship('BurnDown', backref='sprints', lazy=True, post_update=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    closed = db.Column(db.Boolean)
    tasks = db.relationship("Task", backref="sprints", lazy=True)
    init_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    duration = db.Column(db.Integer, default=0)
    est_time = db.Column(db.Integer, default=0)

    def __init__(self, user_id, description, project_id, closed, end_date):
        self.user_id = user_id
        self.description = description
        self.project_id = project_id
        self.closed = closed
        self.end_date = end_date

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        user = UserA.query.get_or_404(self.user_id)
        return {
            "id": self.id,
            "description": self.description,
            "user": {"id": user.id, "username": user.username},
            "project_id": self.project_id,
            "date_created": self.date_created,
            "init_date": self.init_date,
            "end_date": self.end_date,
            "duration": self.duration,
            "est_time": self.est_time,
            "closed": self.closed,
        }


class AcceptanceCriteria(db.Model):
    __tablename__ = "acceptcriteria"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    # relacion one criteria - one project OBLIGATORIO
    story_id = db.Column(db.Integer, db.ForeignKey("stories.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("userA.id"))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean)

    def __init__(self, user_id, description, story_id, approved):
        self.user_id = user_id
        self.description = description
        self.story_id = story_id
        self.approved = approved

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        story = Story.query.get_or_404(self.story_id)
        user = UserA.query.get_or_404(self.user_id)
        return {
            "id": self.id,
            "description": self.description,
            "user": {"id": user.id, "username": user.username},
            "date_created": self.date_created,
            "story": {"id": story.id, "description": story.description},
            "approved": self.approved,
        }


class AcceptanceTest(db.Model):
    __tablename__ = "accepttests"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    # relacion one test - one project OBLIGATORIO
    story_id = db.Column(db.Integer, db.ForeignKey("stories.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("userA.id"))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean)

    def __init__(self, user_id, description, story_id, approved):
        self.user_id = user_id
        self.description = description
        self.story_id = story_id
        self.approved = approved

    def __repr__(self):
        return "<id {}>".format(self.id)

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


class BurnUp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # relacion many BurnUp - one sprint OBLIGATORIO
    sprint_id = db.Column(db.Integer, db.ForeignKey('sprints.id'), nullable=False)
    dia = db.Column(db.Integer)
    realizados = db.Column(db.Integer)
    necesarios = db.Column(db.Integer)
    estimados = db.Column(db.Integer)

    def __init__(self, sprint_id, dia, realizados, necesarios, estimados):
        self.sprint_id = sprint_id
        self.dia = dia
        self.realizados = realizados
        self.necesarios = necesarios
        self.estimados = estimados

    def serialize(self):
        sprint = Sprint.query.get_or_404(self.sprint_id)
        return {
            'id': self.id, 
            'sprint':sprint.id,
            'dia': self.dia,
            'realizados': self.realizados,
            'necesarios': self.necesarios,
            'estimados': self.estimados,
        }


class BurnDown(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # relacion many BurnDown - one sprint OBLIGATORIO
    sprint_id = db.Column(db.Integer, db.ForeignKey('sprints.id'), nullable=False)
    dia = db.Column(db.Integer)
    trabajo = db.Column(db.Integer)
    disponible = db.Column(db.Integer)

    def __init__(self, sprint_id, dia, trabajo, disponible):
        self.sprint_id = sprint_id
        self.dia = dia
        self.trabajo = trabajo
        self.disponible = disponible

    def serialize(self):
        sprint = Sprint.query.get_or_404(self.sprint_id)
        return {
            'id': self.id, 
            'sprint':sprint.id,
            'dia': self.dia,
            'trabajo': self.trabajo,
            'disponible': self.disponible,
        }
