import os, enum
from datetime import datetime
from app import db
from apps.stories.models import *
from apps.user.models import *
from apps.sprints.models import *
from sqlalchemy.orm import relationship


class TaskType(enum.Enum):
    develop = "Desarrollo"
    design = "Diseño"
    fix = "Reparar"
    refact = "Refactor"


class TaskStatus(enum.Enum):
    new = "Nueva"
    init = "Iniciada"
    to_test = "Lista para Pruebas"
    ended = "Culminada"


class TaskClass(enum.Enum):
    easy = "Sencilla"
    middle = "Media"
    hard = "Compleja"

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    #relacion one task - one story OBLIGATORIO
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=False)
    #relacion one task - one sprint OBLIGATORIO
    sprint_id = db.Column(db.Integer, db.ForeignKey('sprints.id'), nullable=False)
    task_type = db.Column(
        db.Enum(TaskType), 
        default= TaskType.develop,
        nullable=False
    )
    task_status = db.Column(
        db.Enum(TaskStatus), 
        default= TaskStatus.new,
        nullable=False
    )
    task_class = db.Column(
        db.Enum(TaskClass), 
        default= TaskClass.easy,
        nullable=False
    )
    init_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    est_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('userA.id'))


    def __init__(self, description,story_id,sprint_id,task_type,task_status,task_class,init_date,end_date,est_time,user_id, duration):
        self.description =description
        self.story_id = story_id
        self.sprint_id = sprint_id
        self.task_type = task_type
        self.task_status = task_status
        self.task_class = task_class
        self.init_date = init_date
        self.end_date = end_date
        self.est_time = est_time
        self.user_id = user_id
        self.duration = duration

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        users = []
        try:
            assign=assign.query.filter(task_id=self.id)
            for i in assign:
                users.append(i.user_id)
        except:
            pass
        
        return{
            'description': self.description,
            'story_id': self.story_id,
            'sprint_id': self.sprint_id,
            'task_type': self.task_type,
            'task_status': self.task_status,
            'task_class' : self.task_class,
            'init_date' : self.init_date,
            'end_date' : self.end_date,
            'est_time' : self.est_time,
            'user_id' : self.user_id,
            'users' : users 
        }
