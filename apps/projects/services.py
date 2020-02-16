
import os
from .models import Project,ProjectStatus,User
from app import db, app
from flask import  request, jsonify

''' Agregar un usuario '''
@app.route("/users/add")
def add_user():
    name=request.args.get('name')
    try:
        user= User(
            name=name
        )
        db.session.add(user)
        db.session.commit()
        return "User added. User id={}".format(user.id)
    except Exception as e:
	     return jsonify({'server': 'ERROR'})

''' Listar todos los proyectos de un usuario '''
@app.route("/projects/getall/<int:user_id>")
def get_all_by_user(user_id):
    projects = Project.query.filter_by(user_id=user_id)
    if projects.count() >0:
        return  jsonify([project.serialize() for project in projects])
    else: 
         return jsonify({'server': 'ERROR'})

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
            return jsonify(project.serialize())
        except Exception as e:
             return jsonify({'server': 'ERROR'})

''' Pausar un proyecto '''
@app.route("/projects/pause/<int:id_>")
def pause_project(id_):
    try:
        project= Project.query.get_or_404(id_)
        project.status=ProjectStatus.paused
        db.session.commit()
        return jsonify({'server': '200'})
    except Exception as e:
	     return jsonify({'server': 'ERROR'})

''' Activar nuevamente un proyecto '''
@app.route("/projects/reactivate/<int:id_>")
def reactivate_project(id_):
    try:
        project= Project.query.get_or_404(id_)
        project.status=ProjectStatus.active
        db.session.commit()
        return jsonify({'server': '200'})
    except Exception as e:
	     return jsonify({'server': 'ERROR'})
''' Eliminar un proyecto '''
@app.route("/projects/delete/<int:id_>")
def delete_project(id_):
    project = Project.query.get_or_404(id_)
    try:
        db.session.delete(project)
        db.session.commit()
        return jsonify({'server': '200'})
    except Exception as e:
         return jsonify({'server': 'ERROR'})

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
            return jsonify(project.serialize())
        except Exception as e:
             return jsonify({'server': 'ERROR'})






