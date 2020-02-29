import os, enum
from datetime import datetime
from app import db
from apps.projects.models import Project

class Documentation(db.Model):
    __tablename__ = 'documentation'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    dev_met =  db.Column(db.Text, nullable=False)
    version = db.Column(db.Float, nullable=False)
    metaphor = db.Column(db.Text, nullable=True)
    project_id = db.Column(db.Integer, nullable=False)
    # project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    
    def __init__(self, name, dev_met, version, project_id, metaphor):
        self.name = name
        self.dev_met = dev_met
        self.version = version
        self.project_id = project_id
        self.metaphor = metaphor

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        # project = Project.query.get_or_404(self.project_id)
        return {
            'id': self.id, 
            'name': self.name,
            'project': {
                'id':self.project_id,
                'name':'Proyecto '+str(self.project_id)
            },
            'dev_met':self.dev_met,
            'version':self.version,
            'metaphor':self.metaphor
        }

class CopyRight(db.Model):
    __tablename__ = 'copyR'

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('documentation.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, content):
        self.doc_id = doc_id
        self.content = content

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        doc = Documentation.query.get_or_404(self.doc_id)
        return {
            'id': self.id, 
            'doc': {
                'id' : str(doc.id),
                'name':doc.name
            },
            'content':self.content
        }

class Intro(db.Model):
    __tablename__ = 'intro'

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('documentation.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, content):
        self.doc_id = doc_id
        self.content = content

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        doc = Documentation.query.get_or_404(self.doc_id)
        return {
            'id': self.id, 
            'doc': {
                'id' : str(doc.id),
                'name':doc.name
            },
            'content':self.content
        }

class Purpose(db.Model):
    __tablename__ = 'purpose'

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('documentation.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, content):
        self.doc_id = doc_id
        self.content = content

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        doc = Documentation.query.get_or_404(self.doc_id)
        return {
            'id': self.id, 
            'doc': {
                'id' : str(doc.id),
                'name':doc.name
            },
            'content':self.content
        }

class Motivation(db.Model):
    __tablename__ = 'motivation'

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('documentation.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, content):
        self.doc_id = doc_id
        self.content = content

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        doc = Documentation.query.get_or_404(self.doc_id)
        return {
            'id': self.id, 
            'doc': {
                'id' : str(doc.id),
                'name':doc.name
            },
            'content':self.content
        }

class Status(db.Model):
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('documentation.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, content):
        self.doc_id = doc_id
        self.content = content

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        doc = Documentation.query.get_or_404(self.doc_id)
        return {
            'id': self.id, 
            'doc': {
                'id' : str(doc.id),
                'name':doc.name
            },
            'content':self.content
        }

class Scope(db.Model):
    __tablename__ = 'scope'

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('documentation.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, content):
        self.doc_id = doc_id
        self.content = content

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        doc = Documentation.query.get_or_404(self.doc_id)
        return {
            'id': self.id, 
            'doc': {
                'id' : str(doc.id),
                'name':doc.name
            },
            'content':self.content
        }

class Arq(db.Model):
    __tablename__ = 'arq'

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('documentation.id'), nullable=False)
    path = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, path):
        self.doc_id = doc_id
        self.path = path

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        doc = Documentation.query.get_or_404(self.doc_id)
        return {
            'id': self.id, 
            'doc': {
                'id' : str(doc.id),
                'name':doc.name
            },
            'path':self.path
        }

class Diag(db.Model):
    __tablename__ = 'diag'

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('documentation.id'), nullable=False)
    path = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, path):
        self.doc_id = doc_id
        self.path = path

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        doc = Documentation.query.get_or_404(self.doc_id)
        return {
            'id': self.id, 
            'doc': {
                'id' : str(doc.id),
                'name':doc.name
            },
            'path':self.path
        }


class Foundation(db.Model):
    __tablename__ = 'foundation'

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('documentation.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, content):
        self.doc_id = doc_id
        self.content = content

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        doc = Documentation.query.get_or_404(self.doc_id)
        return {
            'id': self.id, 
            'doc': {
                'id' : str(doc.id),
                'name':doc.name
            },
            'content':self.content
        }

class Values(db.Model):
    __tablename__ = 'values'

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('documentation.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, content):
        self.doc_id = doc_id
        self.content = content

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        doc = Documentation.query.get_or_404(self.doc_id)
        return {
            'id': self.id, 
            'doc': {
                'id' : str(doc.id),
                'name':doc.name
            },
            'content':self.content
        }
