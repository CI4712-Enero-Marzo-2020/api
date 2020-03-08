import os, enum
from datetime import datetime
from app import db
from apps.stories.models import *
from apps.user.models import UserA
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
    users = relationship("UserA", secondary="assigns")



class Assign(BaseModel):
    __tablename__ = 'assigns'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userA.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))

    user = relationship(UserA, backref=backref("assigns", cascade="all, delete-orphan"))
    task = relationship(Task, backref=backref("assigns", cascade="all, delete-orphan"))



