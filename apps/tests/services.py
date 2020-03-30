import os, sys
from .models import *
from apps.tests.models import UITest, UnitTest
from apps.sprints.models import Sprint
from apps.logger.models import Logger, LoggerEvents
from apps.logger.services import add_event_logger
from app import db, app
from flask import request, jsonify

MODULE = "Prueba"


# Unitarias: Fecha, Modulo, Componente, Nombre, Cantidad, Sprint Id
# CRUD, Get by periodo. Get By Sprint. Get Sprint from. Actualizar cantidad


""" Retorna Lista de pruebas unitarias de un sprint """
@app.route("/tests/unit/<int:sprint_id>", methods=["GET"])
def get_unitTest_by_sprint(sprint_id):
    if request.method == "GET":
        tests = UnitTest.query.filter_by(sprint_id=sprint_id)
        if tests.count() > 0:
            return jsonify([test.serialize() for test in tests.all()])
        else:
            return jsonify({"server": "NO_CONTENT"})


""" Agregar prueba unitaria """
@app.route("/tests/unit/add", methods=["POST"])
def add_unitTest():
    if request.method == "POST":
        sprint_id = request.form.get("sprint_id")
        description = request.form.get("description")
        module = request.form.get("module")
        amount = request.form.get("amount")
        component = request.form.get("component")
        if component == 'vista':
            component = Component.vista
        elif component == 'modelo':
            component = Component.modelo 
        elif component == 'vista_modelo':
            component = Component.vista_modelo
        else :
            return jsonify({"server": "ERROR_COMPONENT_NOT_FOUND"})

        unit_test = UnitTest(
            sprint_id=sprint_id, 
            description = description,
            module = module,
            amount =  amount,
            component = component
        )
        db.session.add(unit_test)
        db.session.commit()
        return jsonify(unit_test.serialize())


""" Modificar prueba unitaria """
@app.route("/tests/unit/<int:_id>", methods=["PUT"])
def update_unitTest(_id):
    if request.method == "PUT":
        unit_test = UnitTest.query.get_or_404(_id)
        sprint_id = request.form.get("sprint_id")
        description = request.form.get("description")
        module = request.form.get("module")
        amount = request.form.get("amount")

        component = request.form.get("component")
        if component == 'vista':
            component = Component.vista
        elif component == 'modelo':
            component = Component.modelo 
        elif component == 'vista_modelo':
            component = Component.vista_modelo
        else :
            return jsonify({"server": "ERROR_COMPONENT_NOT_FOUND"})

        unit_test.sprint_id = sprint_id
        unit_test.description = description
        unit_test.module = module
        unit_test.amount = amount
        unit_test.component = component
        try:
            db.session.commit()
            return jsonify(unit_test.serialize())
        except:
            return jsonify({"server": "500_SERVER_ERROR"})


""" Eliminar prueba unitaria """
@app.route("/tests/unit/delete/<id_>", methods=["DELETE"])
def delete_unitTest(id_):
    if request.method == "DELETE":
        unit_test = UnitTest.query.get_or_404(id_)
        try:
            db.session.delete(unit_test)
            db.session.commit()

            return jsonify({"server": "200_OK"})
        except:
            return jsonify({"server": "500_SERVER_ERROR"})


# IU: Fecha, Funcionalidad
# CRUD, Get by Periodo. Get By Sprint. Get Sprint from


""" Retorna Lista de pruebas de interfaz de usuario de un sprint """
@app.route("/tests/user-interface/<int:sprint_id>", methods=["GET"])
def get_uiTest_by_sprint(sprint_id):
    if request.method == "GET":
        tests = UITest.query.filter_by(sprint_id=sprint_id)
        if tests.count() > 0:
            return jsonify([test.serialize() for test in tests.all()])
        else:
            return jsonify({"server": "NO_CONTENT"})


""" Agregar prueba de interfaz de usuario """
@app.route("/tests/user-interface/add", methods=["POST"])
def add_uiTest():
    if request.method == "POST":
        sprint_id = request.form.get("sprint_id")
        functionality = request.form.get("functionality")

        ui_test = UITest(
            sprint_id=sprint_id, 
            functionality = functionality
        )
        db.session.add(ui_test)
        db.session.commit()
        return jsonify(ui_test.serialize())


""" Modificar prueba de interfaz de usuario """
@app.route("/tests/user-interface/<int:_id>", methods=["PUT"])
def update_uiTest(_id):
    if request.method == "PUT":
        ui_test = UITest.query.get_or_404(_id)
        sprint_id = request.form.get("sprint_id")
        functionality = request.form.get("functionality")

        ui_test.sprint_id = sprint_id
        ui_test.functionality = functionality
        try:
            db.session.commit()
            return jsonify(ui_test.serialize())
        except:
            return jsonify({"server": "500_SERVER_ERROR"})


""" Eliminar prueba de interfaz de usuario """
@app.route("/tests/user-interface/delete/<id_>", methods=["DELETE"])
def delete_uiTest(id_):
    if request.method == "DELETE":
        ui_test = UITest.query.get_or_404(id_)
        try:
            db.session.delete(ui_test)
            db.session.commit()
            return jsonify({"server": "200_OK"})
        except:
            return jsonify({"server": "500_SERVER_ERROR"})