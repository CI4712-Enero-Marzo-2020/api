import os, enum
from datetime import datetime
from app import db
from apps.sprints.models import *

# Unitarias: Fecha, Modulo, Componente, Nombre, Cantidad, Sprint Id
# CRUD, Get by periodo. Get By Sprint. Get Sprint from. Actualizar cantidad

# IU: Fecha, Funcionalidad
# CRUD, Get by Periodo. Get By Sprint. Get Sprint from


class Component(enum.Enum):
    vista = "vista"
    modelo = "modelo"
    vista_modelo = "vista/modelo"


class UnitTest(db.Model):
    __tablename__ = "unittests"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    module = db.Column(db.Text)
    sprint_id = db.Column(db.Integer, db.ForeignKey("sprints.id"))
    component = db.Column(db.Enum(Component), default=Component.vista, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Integer)

    def __init__(self, sprint_id, description, component, amount, module):
        self.sprint_id = sprint_id
        self.description = description
        self.component = component
        self.amount = amount
        self.module = module

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "sprint_id": self.sprint_id,
            "description": self.description,
            "module": self.module,
            "component": self.component.value,
            "date_created": self.date_created,
            "amount": self.amount,
        }


class UITest(db.Model):
    __tablename__ = "uitests"

    id = db.Column(db.Integer, primary_key=True)
    functionality = db.Column(db.Text)
    sprint_id = db.Column(db.Integer, db.ForeignKey("sprints.id"))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, sprint_id, functionality):
        self.sprint_id = sprint_id
        self.functionality = functionality

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "sprint_id": self.sprint_id,
            "functionality": self.functionality,
            "date_created": self.date_created,
        }
