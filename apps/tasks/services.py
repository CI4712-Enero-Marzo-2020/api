import os
from .models import *
from app import db, app
from flask import  request, jsonify,make_response
from datetime import datetime
from apps.sprints.models import *
from apps.user.models import *

Module = 'Task'

@app.route("task/getbystory/<story_id>")
    tasks = Task.query.filter_by(story_id=story_id)
    if tasks.count() >0:
        return  jsonify([c.serialize() for c in tasks])
    else: 
         return jsonify({'server': 'NO_CONTENT'})

@app.route("/task/delete/<task_id>",methods=['POST'])
def delete_task(task_id):
    try:
        task=Task.query.filter_by(id=task_id).delete()
        db.session.commit()
        return jsonify(task), 200
    except Exception as e:
	    return(str(e))

@app.route("/tasks/add",methods=['POST'])
def add_tasks():
    if request.method == 'POST':
        description=request.json.get('description')
        story_id=request.json.get('story_id')
        sprint_id=request.json.get('sprint_id')
        task_type = request.json.get('task_type')
        task_status = request.json.get('task_status')
        task_class = request.json.get('task_class')
        if request.json.get('init_date'):
            init_date = request.json.get('init_date')
        end_date = request.json.get('end_date')
        duration = (end_date - init_date).days
        est_time = request.json.get('est_time')

        #usuario que crea la tarea
        user_id = request.json.get('user_id')
        user_creator = UserA.query.get_or_404(user_id)
        if user.role not in ['Scrum Master', 'Scrum Team']:
            return jsonify({'server': 'Debe ser parte del equipo'}), 405

        #usuarios a los que se las asignan
        users = []
        if len(request.json.get('users'))>2:
            return make_response(jsonify('maximo 2 usuarios permitidos'), 404)
        elif len(request.json.get('users'))=0:
            pass
        else:    
            for i in request.json.get('users'):
                user = UserA.query.get_or_404(i)
                users.append(user)
        try:
            task = Task(
                        description= description,
                        story_id= story_id,
                        sprint_id=sprint_id,
                        task_type= task_type,
                        task_status= task_status,
                        task_class= task_class,
                        init_date= init_date,
                        end_date= end_date,
                        duration= duration,
                        est_time= est_time,
                        users= users,
                        user_id = user_id
            )
            db.session.add(task)
            db.session.commit()

            ###########Agregando evento al logger#######################
            add_event_logger(user_id, LoggerEvents.add_task, MODULE)
            ############################################################

            return jsonify(task.serialize())
        except Exception as e:
            print(e)            
            return jsonify({'server': 'ERROR'})