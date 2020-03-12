
import os
from .models import *
from apps.logger.models import Logger, LoggerEvents
from apps.logger.services import add_event_logger
from apps.projects.models import Project 
from app import db, app
from flask import  request, jsonify


MODULE = 'Reunion'


