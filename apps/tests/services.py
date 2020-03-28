import os, sys
from .models import *
from apps.tests.models import UITest, UnitTest
from apps.sprints.models import Sprint
from apps.logger.models import Logger, LoggerEvents
from apps.logger.services import add_event_logger
from app import db, app
from flask import request, jsonify

# Unitarias: Fecha, Modulo, Componente, Nombre, Cantidad, Sprint Id
# CRUD, Get by periodo. Get By Sprint. Get Sprint from. Actualizar cantidad

# IU: Fecha, Funcionalidad
# CRUD, Get by Periodo. Get By Sprint. Get Sprint from
