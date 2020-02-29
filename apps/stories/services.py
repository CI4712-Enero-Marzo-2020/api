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


'''Agrega historia a una epica'''
@app.route("/stories/add_to_epic/<int:story_id>/<int:epic_id>",methods= ['PUT'])
def add_to_epic(story_id, epic_id):
    if request.method == 'PUT':
        try:
            story= Story.query.get_or_404(story_id)
            new_parent = Story.query.get_or_404(epic_id)

            if new_parent.epic:
                new_parent.children.append(story)
                story.parent_id = new_parent.id
            else:
                return jsonify({'server': 'ERROR: Parent is not epic'})

            ###########Agregando evento al logger###########################
            #add_event_logger(user_id, LoggerEvents.search_project, MODULE)
            ################################################################

            return jsonify([new_parent.serialize()])
        except Exception as e:
            print(e)
            return jsonify({'server': 'ERROR'})

'''Elimina historia de su epica'''
@app.route("/stories/remove_from_epic/<int:story_id>/",methods=['DELETE'])
def remove_from_epic(story_id):
    if request.method == 'DELETE':
        try:
            story = Story.query.get_or_404(story_id)
            parent = Story.query.get_or_404(story.parent_id)
            if parent.epic:
               parent.children.remove(story_id)
               story.parent_id = None
            else:
                return jsonify({'server': 'ERROR: Parent is not epic'})
            
            ###########Agregando evento al logger###########################
            #add_event_logger(user_id, LoggerEvents.search_project, MODULE)
            ################################################################

            return  jsonify([parent.serialize()])
        except Exception as e:
            print(e)
            return jsonify({'server': 'ERROR'})


'''Retorna historias de una epica'''
@app.route("/stories/get_children/<int:id_>")
def get_children_from_epic(id_):
    try:
        parent= Story.query.get_or_404(id_)

        ###########Agregando evento al logger###########################
        #add_event_logger(user_id, LoggerEvents.search_project, MODULE)
        ################################################################

        return  jsonify([child.serialize() for child in parent.children])
    except Exception as e:
        print(e)
        return jsonify({'server': 'ERROR'})

'''Retorna historias de una epica'''
@app.route("/stories/get_parent/<int:id_>")
def get_parent_from_story(id_):
    try:
        story= Story.query.get_or_404(id_)

        ###########Agregando evento al logger###########################
        #add_event_logger(user_id, LoggerEvents.search_project, MODULE)
        ################################################################
        parent = Story.query.get_or_404(story.parent_id)

        return  jsonify(parent.serialize())
    except Exception as e:
        print(e)
        return jsonify({'server': 'ERROR'})