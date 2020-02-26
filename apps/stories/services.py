import os, sys
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

''' Agregar historia '''
@app.route("/stories/add",methods=['POST'])
def add_story():
    if request.method == 'POST':
        description=request.form.get('description')
        project_id=request.form.get('project_id')
        priority=request.form.get('priority')
        #epic=request.form.get('epic')
        try:
            story = Story(
                project_id = project_id,
                description=description,
                priority = priority,
                epic = False,
            )
            db.session.add(story)
            db.session.commit()

            ###########Agregando evento al logger#######################
            # add_event_logger(user_id, LoggerEvents.add_project, MODULE)
            ############################################################

            return jsonify(story.serialize())
        except Exception as e:
            print(e)            
            return jsonify({'server': 'ERROR'})


''' Prioridad Hight a la Historia '''
@app.route("/stories/hight/<int:id_>",methods= ['PATCH'])
def hight_story(id_):
    if request.method == 'PATCH':
        try:
            story= Story.query.get_or_404(id_)
            story.priority=StoryPriority.hight
            db.session.commit()

            user_id=story.user_id
            ###########Agregando evento al logger##########################
            add_event_logger(user_id, LoggerEvents.hight_story, MODULE)
            ###############################################################

            return jsonify(project.serialize())
        except:
            return jsonify({'server': 'ERROR'})

''' Prioridad Medium a la Historia '''
@app.route("/stories/medium/<int:id_>",methods= ['PATCH'])
def medium_story(id_):
    if request.method == 'PATCH':
        try:
            story= Story.query.get_or_404(id_)
            story.priority=StoryPriority.medium
            db.session.commit()

            user_id=story.user_id
            ###########Agregando evento al logger##########################
            add_event_logger(user_id, LoggerEvents.medium_story, MODULE)
            ###############################################################

            return jsonify(project.serialize())
        except:
            return jsonify({'server': 'ERROR'})


''' Prioridad Low a la Historia '''
@app.route("/stories/low/<int:id_>",methods= ['PATCH'])
def low_story(id_):
    if request.method == 'PATCH':
        try:
            story= Story.query.get_or_404(id_)
            story.priority=StoryPriority.low
            db.session.commit()

            user_id=story.user_id
            ###########Agregando evento al logger##########################
            add_event_logger(user_id, LoggerEvents.low_story, MODULE)
            ###############################################################

            return jsonify(project.serialize())
        except:
            return jsonify({'server': 'ERROR'})





''' Eliminar una historia '''
@app.route("/stories/delete/<int:id_>",methods= ['DELETE'])
def delete_story(id_):
    if request.method == 'DELETE':
        story = Story.query.get_or_404(id_)
        try:
            project_id=story.project_id
            db.session.delete(story)
            db.session.commit()

            ###########Agregando evento al logger###########################
            #add_event_logger(user_id, LoggerEvents.delete_project, MODULE)
            ################################################################

            return jsonify({'server': '200'})
        except:
            return jsonify({'server': 'ERROR'})


'''Buscar un proyecto por su id'''
@app.route("/stories/search/<int:id_>")
def search_story(id_):
    try:
        story= Story.query.get_or_404(id_)

        project_id=story.project_id
        ###########Agregando evento al logger###########################
        #add_event_logger(user_id, LoggerEvents.search_project, MODULE)
        ################################################################

        return  jsonify([story.serialize()])
    except:
         return jsonify({'server': 'ERROR'})


''' Modificar una historia '''
@app.route("/stories/update/<int:id_>",methods= ['PUT'])
def update_story(id_):
    if request.method == 'PUT':
        story = Story.query.get_or_404(id_)
        description=request.form.get('description')
        project_id=request.form.get('project_id')

        story.description=description
        story.project_id=project_id
        try:
            db.session.commit()

            ###########Agregando evento al logger##########################
            #add_event_logger(user_id, LoggerEvents.update_project, MODULE)
            ###############################################################

            return jsonify(story.serialize())
        except Exception as e:
            print(e)
            return jsonify({'server': 'ERROR'})