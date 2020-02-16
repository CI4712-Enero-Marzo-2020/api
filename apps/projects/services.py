
import os
from .models import Project,ProjectStatus 
from apps.logger.models import Logger, LoggerEvents
from apps.logger.services import add_event_logger
from app import db, app
from flask import  request, jsonify


MODULE = 'Proyecto'

''' Listar todos los proyectos de un usuario '''
@app.route("/projects/getall/<int:user_id>")
def get_all_by_user(user_id):
    projects = Project.query.filter_by(user_id=user_id)
    if projects.count() >0:
        return  jsonify([project.serialize() for project in projects])
    else: 
        return(str(Exception))

''' Agregar un proyecto '''
@app.route("/projects/add",methods=['POST'])
def add_project():
    if request.method == 'POST':
        description=request.form.get('description')
        user_id=request.form.get('user_id')
        try:
            project= Project(
                description=description,
                user_id=user_id,
                status= ProjectStatus.active
            )
            db.session.add(project)
            db.session.commit()

            ###########Agregando evento al logger#######################
            add_event_logger(user_id, LoggerEvents.add_project, MODULE)
            ############################################################

            return jsonify(project.serialize())
        except Exception as e:
            return(str(e))

''' Pausar un proyecto '''
@app.route("/projects/pause/<int:id_>")
def pause_project(id_):
    try:
        project= Project.query.get_or_404(id_)
        project.status=ProjectStatus.paused
        db.session.commit()

        #user_id=request.form.get('user_id')
        ###########Agregando evento al logger##########################
        #add_event_logger(user_id, LoggerEvents.pause_project, MODULE)
        ###############################################################

        return "Project status modified to paused. Project id={}".format(project.id)
    except Exception as e:
	    return(str(e))

''' Activar nuevamente un proyecto '''
@app.route("/projects/reactivate/<int:id_>")
def reactivate_project(id_):
    try:
        project= Project.query.get_or_404(id_)
        project.status=ProjectStatus.active
        db.session.commit()

        #user_id=request.form.get('user_id')
        ###########Agregando evento al logger#############################
        #add_event_logger(user_id, LoggerEvents.activate_project, MODULE)
        ##################################################################

        return "Project status modified to active. Project id={}".format(project.id)
    except Exception as e:
	    return(str(e))

''' Eliminar un proyecto '''
@app.route("/projects/delete/<int:id_>")
def delete_project(id_):
    project = Project.query.get_or_404(id_)
    try:
        db.session.delete(project)
        db.session.commit()

        #user_id=request.form.get('user_id')
        ###########Agregando evento al logger###########################
        #add_event_logger(user_id, LoggerEvents.delete_project, MODULE)
        ################################################################

        return "Project Deleted. Project id={}".format(project.id)
    except Exception as e:
        return(str(e))

''' Modificar un proyecto '''
@app.route("/projects/update/<int:id_>",methods= ['PUT'])
def update_project(id_):
    if request.method == 'PUT':
        project = Project.query.get_or_404(id_)
        description=request.form.get('description')
        user_id=request.form.get('user_id')

        project.description=description
        project.user_id=user_id
        try:
            db.session.commit()

            ###########Agregando evento al logger##########################
            add_event_logger(user_id, LoggerEvents.update_project, MODULE)
            ###############################################################

            return jsonify(project.serialize())
        except Exception as e:
            return(str(e))






