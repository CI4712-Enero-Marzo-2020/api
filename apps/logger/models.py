import os, enum
from app import db
from apps.user.models import UserA
from datetime import datetime


class LoggerEvents(enum.Enum):
    add_project = "Agregar Proyecto"
    update_project = "Modificar Proyecto"
    activate_project = "Activar Proyecto"
    pause_project = "Pausar Proyecto"
    delete_project = "Eliminar Proyecto"
    search_project = "Buscar Proyecto"
    user_register = "Registro"
    user_login = "Inicio de Sesion"
    user_role_assign = "Rol Asignado"

class Logger(db.Model):
    __tablename__ = 'logger'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('userA.id'))
    event = db.Column(
        db.Enum(LoggerEvents), 
        default= LoggerEvents.user_login,
        nullable=False
    )
    date = db.Column(db.DateTime, default=datetime.utcnow)
    loged_module = db.Column(db.String(100), nullable=False)


    def __init__(self, user, event, loged_module):
        self.user = user
        self.event = event
        self.loged_module = loged_module

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'user': UserA.query.get_or_404(self.user).username,
            'event': self.event.value,
            'date':self.date,
            'loged_module':self.loged_module
        }