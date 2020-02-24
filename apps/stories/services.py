
import os
from .models import *
from apps.projects.models import Project,ProjectStatus 
from apps.logger.models import Logger, LoggerEvents
from apps.logger.services import add_event_logger
from app import db, app
from flask import  request, jsonify


MODULE = 'Historia'

''' Listar todas las historias de un proyecto '''
@app.route("/stories/getall/<int:project_id>")
def get_all_by_project(project_id):
    stories = Story.query.filter_by(project_id=project_id)
    if stories.count() >0:
        return  jsonify([story.serialize() for story in stories])
    else: 
         return jsonify({'server': 'NO_CONTENT'})


''' Cambiar clasificacion de una historia '''
@app.route("/stories/classification/<int:id_>",methods= ['PATCH'])
def modify_class_story(id_):
    if request.method == 'PATCH':
        try:
            story= Story.query.get_or_404(id_)
            if story.epic == True :
                story.epic = False 
            else:
                story.epic = True
            db.session.commit()

            return jsonify(story.serialize())
        except:
            return jsonify({'server': 'ERROR'})

