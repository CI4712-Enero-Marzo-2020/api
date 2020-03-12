
import os
from .models import *
from apps.sprints.models import *
from app import db, app
from flask import  request, jsonify


MODULE = 'Reunion'


''' Retorna fecha de reunion de planning y lista de resultados de un sprint '''
@app.route("/meetings/plannings/<int:sprint_id>")
def get_planning_by_sprint(sprint_id):
    planning = Planning.get_or_404(sprint_id=sprint_id)
    dic = [planning.serialize()]
    results = PlanningResults.query.filter_by(planning_id=planning.id)
    if results.count() >0:
        dic.extend([result.serialize() for result in results])
    return  jsonify(dic)


''' Agregar resultado de planning '''


''' Buscar resultado de planning '''


''' Modificar resultado de planning '''



''' Eliminar resultado de planning '''


''' Listar todas las reuniones de retrospectiva de un sprint '''
@app.route("/meetings/retrospectives/<int:sprint_id>")
def get_retrospectives_by_sprint(sprint_id):
    meetings = Retrospective.query.filter_by(sprint_id=sprint_id)
    if meetings.count() >0:
        return  jsonify([meeting.serialize() for meeting in meetings])
    else: 
         return jsonify({'server': 'NO_CONTENT'})


''' Agregar  reunion de retrospectiva '''


''' Buscar reunion de retrospectiva '''


''' Modificar reunion de retrospectiva '''


''' Eliminar reunion de retrospectiva '''


''' Listar todos los dailies de un sprint '''
@app.route("/meetings/dailies/<int:sprint_id>")
def get_dailies_by_sprint(sprint_id): 
    meetings = Daily.query.filter_by(sprint_id=sprint_id)
    if meetings.count() >0:
        return  jsonify([meeting.serialize() for meeting in meetings])
    else: 
         return jsonify({'server': 'NO_CONTENT'})


''' Agregar daily '''


''' Buscar daily '''


''' Modificar daily '''


''' Eliminar daily '''


