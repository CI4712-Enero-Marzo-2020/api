
import os
from .models import *
from apps.sprints.models import *
from app import db, app
from flask import request, jsonify
from apps.logger.models import Logger, LoggerEvents
from apps.logger.services import add_event_logger
from flask_cors import CORS, cross_origin

MODULE = 'Reunion'


''' Retorna fecha de reunion de planning y lista de resultados de un sprint '''
@app.route("/meetings/plannings/<int:sprint_id>",methods=['GET'])
def get_planning_by_sprint(sprint_id):
    if request.method == 'GET':
        planning = Planning.get_or_404(sprint_id=sprint_id)
        dic = [planning.serialize()]
        results = PlanningResults.query.filter_by(planning_id=planning.id)
        if results.count() > 0:
            dic.extend([result.serialize() for result in results])
        return jsonify(dic)


''' Agregar resultado de planning '''


''' Buscar resultado de planning '''


''' Modificar resultado de planning '''


''' Eliminar resultado de planning '''


''' Listar todas las reuniones de retrospectiva de un sprint '''
@app.route("/meetings/retrospectives/<int:sprint_id>",methods=['GET'])
def get_retrospectives_by_sprint(sprint_id):
    if request.method == 'GET':
        meetings = Retrospective.query.filter_by(sprint_id=sprint_id)
        if meetings.count() > 0:
            return jsonify([meeting.serialize() for meeting in meetings])
        else:
            return jsonify({'server': 'NO_CONTENT'})


''' Agregar  reunion de retrospectiva '''


''' Buscar reunion de retrospectiva '''


''' Modificar reunion de retrospectiva '''


''' Eliminar reunion de retrospectiva '''


''' Listar todos los dailies de un sprint '''
@app.route("/meetings/dailies/<int:sprint_id>",methods=['GET'])
def get_dailies_by_sprint(sprint_id):
    if request.method == 'GET':
        meetings = Daily.query.filter_by(sprint_id=sprint_id)
        if meetings.count() > 0:
            return jsonify([meeting.serialize() for meeting in meetings])
        else:
            return jsonify({'server': 'NO_CONTENT'})


''' Agregar daily '''
@app.route("/meetings/dailies/add", methods=['POST'])
def add_daily():
    if request.method == 'POST':
        date = request.form.get('date')
        report = request.form.get('report')
        sprint_id = request.form.get('sprint_id')

        try:
            daily = Daily(
                date=date,
                report=report,
                sprint_id=sprint_id,
            )
            db.session.add(daily)
            db.session.commit()

            ###########Agregando evento al logger#######################
            #add_event_logger(sprint_id, LoggerEvents.add_daily, MODULE)
            ############################################################
            return jsonify(daily.serialize())
        except:
            return jsonify({'ERROR':'500_INTERNAL_SERVER_ERROR'})


''' Buscar daily '''
@app.route("/meetings/dailies/search/<int:id_>",methods=['GET'])
def search_daily(id_):
    if request.method == 'GET':
        daily= Daily.query.get_or_404(id_)
        ###########Agregando evento al logger###########################
        #add_event_logger(daily_id, LoggerEvents.search_daily, MODULE)
        ################################################################
        return  jsonify(daily.serialize())


''' Modificar daily '''
@app.route("/meetings/dailies/<id_>", methods=['PUT'])
def update_daily(id_):
    if request.method == 'PUT':
        daily = Daily.query.get_or_404(id_)
        date = request.form.get('date')
        report = request.form.get('report')
        sprint_id = request.form.get('sprint_id')

        daily.date = date
        daily.report = report
        daily.sprint_id = sprint_id

        db.session.commit()

        ###########Agregando evento al logger##########################
        #add_event_logger(
        #daily.daily_id, LoggerEvents.update_daily, MODULE)
        ###############################################################

        return jsonify(daily.serialize())


''' Eliminar daily '''
@app.route("/meetings/dailies/delete/<id_>", methods= ['DELETE'])
def delete_daily(id_):
   if request.method == 'DELETE':
        daily = Daily.query.get_or_404(id_)
        try:
            db.session.delete(daily)
            db.session.commit()

            ###########Agregando evento al logger###########################
            #add_event_logger(user_id, LoggerEvents.delete_daily, MODULE)
            ################################################################

            return jsonify({'server': '200'})
        except:
            return jsonify({'server': 'ERROR'})
