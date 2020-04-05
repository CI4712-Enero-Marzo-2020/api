import os
from .models import *
from app import db, app
from datetime import datetime
from flask import  request, jsonify, json, url_for

@app.route('/docs/getall/team',methods=['GET'])
def getall_teams():
    try:
        teams = Team.query.all()
        return  jsonify([team.serialize() for team in teams])
    except Exception as e:
	    return(str(e))
    
@app.route('/docs/getall/team/test',methods=['GET'])
def teams_test():
    # Crea usuario
    # user = UserA('usuario','nombre','apellido','Project owner','clave')
    # db.session.add(user)
    # db.session.commit()
    user = UserA.query.filter_by(username='usuario').first()
    # Crea documento
    doc = Documentation('Documento','metodo',0.1,10,'metafora')
    db.session.add(doc)
    db.session.commit()
    # Crea equipo
    # team = Team('Equipo 1')
    # db.session.add(team)
    # db.session.commit()
    team = Team.query.filter_by(name='Equipo 2').first()
    # Mete equipo en documento
    doc.teams.append(team)
    db.session.add(doc)
    db.session.commit()
    # Mete usuario en equipo
    team.users.append(user)
    db.session.add(team)
    db.session.commit()

    try:
        teams = Team.query.all()
        return  jsonify([team.serialize() for team in teams])
    except Exception as e:
	    return(str(e))

@app.route('/docs/teamLeaders/<id>',methods=['GET'])
def get_doc_team_leaders(id):
    try:
        teams = TeamLeaders.query.all()
        return  jsonify([team.serialize() for team in teams])
    except Exception as e:
	    return(str(e))

@app.route('/docs/teams/<id>',methods=['POST'])
def add_team(id):
    try:   
        doc = Documentation.query.filter_by(project_id=id).first()
        pO = UserA.query.filter_by(username=request.json.get('product_owner')).first()
        sM = UserA.query.filter_by(username=request.json.get('scrum_master')).first()
        print(request.json.get('teams'))
        for team in request.json.get('teams'):
            team_temp = Team(name=team['name'])
            doc.teams.append(team_temp)
            db.session.add(doc)
            db.session.commit()
            for user in team['users']:
                user_temp = UserA.query.filter_by(username=user).first()
                team_temp.users.append(user_temp)
                db.session.add(team_temp)
                db.session.commit()

        doc = Documentation.query.filter_by(project_id=id).first()
        user1 = UserA.query.filter_by(username='usuario').first()
        user2 = UserA.query.filter_by(username='jguzman').first() 
        doc_leader = TeamLeaders(doc.id, user1.id, user2.id)
        # print(doc_leader.serialize())
        db.session.add(doc_leader)
        db.session.commit()
        data = doc_leader.serialize()
        data['teams'] = doc.serialize()['teams']
        return jsonify(data)
    except Exception as e:
	    return(str(e))


@app.route('/docs/teams/<id>',methods=['GET'])
def get_doc_team(id):
    try:
        doc = Documentation.query.filter_by(project_id=id).first()
        print(doc.serialize())
        data = doc.serialize()
        return  jsonify(data['teams'])
    except Exception as e:
	    return(str(e))

@app.route('/docs/revisions/<id>',methods=['GET'])
def get_doc_revisions(id):
    try:
        doc = Documentation.query.filter_by(project_id=id).first()
        revisions = Revisions.query.filter_by(doc_id=doc.id)
        return  jsonify([doc.serialize() for doc in revisions])
    except Exception as e:
	    return(str(e))

@app.route('/docs/getall')
def getall_docs():
    try:
        docs = Documentation.query.all()
        return  jsonify([doc.serialize() for doc in docs])
    except Exception as e:
	    return(str(e))

@app.route('/docs/getall/intro')
def getall_intro():
    try:
        docs = Intro.query.all()
        return  jsonify([doc.serialize() for doc in docs])
    except Exception as e:
	    return(str(e))



''' ELIMINAR ESTA PARTE '''
from apps.projects.models import Project,ProjectStatus 
@app.route("/projects/addd")
def add_projectt():

    project= Project(
        description='description',
        user_id=1,
        status= ProjectStatus.active
    )
    db.session.add(project)
    db.session.commit()
    db.reflect()
    db.drop_all()

    return jsonify(project.serialize())

# Create document
@app.route('/docs/add',methods=['POST'])
def add_doc():
    parameters = {'name':None,'dev_met':None,'version':None,'project_id':None}
    parameters = {param:request.form.to_dict().get(param, None) for param in parameters.keys()}
    
    for param, value in parameters.items():
        if not value:
            return jsonify({"msg": "Missing "+param+" parameter"}), 400
    
    
    if Documentation.query.filter_by(project_id=parameters['project_id']).first():
        return jsonify({"msg": "Documentation for 'Proyecto "+parameters['project_id']+"' already exist"}), 400

    if 'image' not in request.files:
        return jsonify({'message' : 'No file part in the request'}), 400
        
    image = request.files['image']
    upload_folder = os.path.join(app.root_path, 'uploads')
    image.save(os.path.join(upload_folder, image.filename))
    path = os.path.join(upload_folder, image.filename)

    try:
        doc = Documentation(name=parameters['name'],
                    dev_met=parameters['dev_met'],
                    version=parameters['version'],
                    project_id=parameters['project_id'],
                    metaphor=path)
        db.session.add(doc)
        db.session.commit()

        return jsonify(doc.serialize()), 200
    except Exception as e:
            return(str(e))

@app.route('/docs/add/copyright',methods=['POST'])
def add_copyright():
    parameters = {'doc_id':None,'content':None}
    parameters = {param:request.form.to_dict().get(param, None) for param in parameters.keys()}
    
    for param, value in parameters.items():
        if not value:
            return jsonify({"msg": "Missing "+param+" parameter"}), 400
    
    if not Documentation.query.filter_by(id=parameters['doc_id']).first():
        return jsonify({"msg": "'document "+parameters['doc_id']+"' does not exist"}), 400

    if CopyRight.query.filter_by(doc_id=parameters['doc_id']).first():
        return jsonify({"msg": "Copyright for 'document "+parameters['doc_id']+"' already exist"}), 400

    try:
        doc = CopyRight(doc_id=parameters['doc_id'],
                    content=parameters['content'])
        db.session.add(doc)
        db.session.commit()

        return jsonify(doc.serialize()), 200
    except Exception as e:
            return(str(e))

@app.route('/docs/add/intro',methods=['POST'])
def add_intro():
    parameters = {'doc_id':None,'content':None}
    parameters = {param:request.form.to_dict().get(param, None) for param in parameters.keys()}
    
    for param, value in parameters.items():
        if not value:
            return jsonify({"msg": "Missing "+param+" parameter"}), 400
    
    if not Documentation.query.filter_by(id=parameters['doc_id']).first():
        return jsonify({"msg": "'document "+parameters['doc_id']+"' does not exist"}), 400

    if Intro.query.filter_by(doc_id=parameters['doc_id']).first():
        return jsonify({"msg": "Introduction for 'document "+parameters['doc_id']+"' already exist"}), 400

    try:
        doc = Intro(doc_id=parameters['doc_id'],
                    content=parameters['content'])
        db.session.add(doc)
        db.session.commit()

        return jsonify(doc.serialize()), 200
    except Exception as e:
            return(str(e))

@app.route('/docs/add/purpose',methods=['POST'])
def add_purpose():
    parameters = {'doc_id':None,'content':None}
    parameters = {param:request.form.to_dict().get(param, None) for param in parameters.keys()}
    
    for param, value in parameters.items():
        if not value:
            return jsonify({"msg": "Missing "+param+" parameter"}), 400
    
    if not Documentation.query.filter_by(id=parameters['doc_id']).first():
        return jsonify({"msg": "'document "+parameters['doc_id']+"' does not exist"}), 400

    if Purpose.query.filter_by(doc_id=parameters['doc_id']).first():
        return jsonify({"msg": "Purpose for 'document "+parameters['doc_id']+"' already exist"}), 400

    try:
        doc = Purpose(doc_id=parameters['doc_id'],
                    content=parameters['content'])
        db.session.add(doc)
        db.session.commit()

        return jsonify(doc.serialize()), 200
    except Exception as e:
            return(str(e))

@app.route('/docs/add/motivation',methods=['POST'])
def add_motivation():
    parameters = {'doc_id':None,'content':None}
    parameters = {param:request.form.to_dict().get(param, None) for param in parameters.keys()}
    
    for param, value in parameters.items():
        if not value:
            return jsonify({"msg": "Missing "+param+" parameter"}), 400
    
    if not Documentation.query.filter_by(id=parameters['doc_id']).first():
        return jsonify({"msg": "'document "+parameters['doc_id']+"' does not exist"}), 400

    if Motivation.query.filter_by(doc_id=parameters['doc_id']).first():
        return jsonify({"msg": "Motivation for 'document "+parameters['doc_id']+"' already exist"}), 400

    try:
        doc = Motivation(doc_id=parameters['doc_id'],
                    content=parameters['content'])
        db.session.add(doc)
        db.session.commit()

        return jsonify(doc.serialize()), 200
    except Exception as e:
            return(str(e))

@app.route('/docs/add/status',methods=['POST'])
def add_status():
    parameters = {'doc_id':None,'content':None}
    parameters = {param:request.form.to_dict().get(param, None) for param in parameters.keys()}
    
    for param, value in parameters.items():
        if not value:
            return jsonify({"msg": "Missing "+param+" parameter"}), 400
    
    if not Documentation.query.filter_by(id=parameters['doc_id']).first():
        return jsonify({"msg": "'document "+parameters['doc_id']+"' does not exist"}), 400

    if Status.query.filter_by(doc_id=parameters['doc_id']).first():
        return jsonify({"msg": "Status for 'document "+parameters['doc_id']+"' already exist"}), 400

    try:
        doc = Status(doc_id=parameters['doc_id'],
                    content=parameters['content'])
        db.session.add(doc)
        db.session.commit()

        return jsonify(doc.serialize()), 200
    except Exception as e:
            return(str(e))

@app.route('/docs/add/scope',methods=['POST'])
def add_scope():
    parameters = {'doc_id':None,'content':None}
    parameters = {param:request.form.to_dict().get(param, None) for param in parameters.keys()}
    
    for param, value in parameters.items():
        if not value:
            return jsonify({"msg": "Missing "+param+" parameter"}), 400
    
    if not Documentation.query.filter_by(id=parameters['doc_id']).first():
        return jsonify({"msg": "'document "+parameters['doc_id']+"' does not exist"}), 400

    if Scope.query.filter_by(doc_id=parameters['doc_id']).first():
        return jsonify({"msg": "Scope for 'document "+parameters['doc_id']+"' already exist"}), 400

    try:
        doc = Scope(doc_id=parameters['doc_id'],
                    content=parameters['content'])
        db.session.add(doc)
        db.session.commit()

        return jsonify(doc.serialize()), 200
    except Exception as e:
            return(str(e))

@app.route('/docs/add/foundation',methods=['POST'])
def add_foundation():
    parameters = {'doc_id':None,'content':None}
    parameters = {param:request.form.to_dict().get(param, None) for param in parameters.keys()}
    
    for param, value in parameters.items():
        if not value:
            return jsonify({"msg": "Missing "+param+" parameter"}), 400
    
    if not Documentation.query.filter_by(id=parameters['doc_id']).first():
        return jsonify({"msg": "'document "+parameters['doc_id']+"' does not exist"}), 400

    if Foundation.query.filter_by(doc_id=parameters['doc_id']).first():
        return jsonify({"msg": "Foundation for 'document "+parameters['doc_id']+"' already exist"}), 400

    try:
        doc = Foundation(doc_id=parameters['doc_id'],
                    content=parameters['content'])
        db.session.add(doc)
        db.session.commit()

        return jsonify(doc.serialize()), 200
    except Exception as e:
            return(str(e))

@app.route('/docs/add/values',methods=['POST'])
def add_values():
    parameters = {'doc_id':None,'content':None}
    parameters = {param:request.form.to_dict().get(param, None) for param in parameters.keys()}
    
    for param, value in parameters.items():
        if not value:
            return jsonify({"msg": "Missing "+param+" parameter"}), 400
    
    if not Documentation.query.filter_by(id=parameters['doc_id']).first():
        return jsonify({"msg": "'document "+parameters['doc_id']+"' does not exist"}), 400

    if Values.query.filter_by(doc_id=parameters['doc_id']).first():
        return jsonify({"msg": "Values for 'document "+parameters['doc_id']+"' already exist"}), 400

    try:
        doc = Values(doc_id=parameters['doc_id'],
                    content=parameters['content'])
        db.session.add(doc)
        db.session.commit()

        return jsonify(doc.serialize()), 200
    except Exception as e:
            return(str(e))

@app.route('/docs/add/arq',methods=['POST'])
def add_arq():
    parameters = {'doc_id':None}
    parameters = {param:request.form.to_dict().get(param, None) for param in parameters.keys()}
    
    for param, value in parameters.items():
        if not value:
            return jsonify({"msg": "Missing "+param+" parameter"}), 400
    
    if not Documentation.query.filter_by(id=parameters['doc_id']).first():
        return jsonify({"msg": "'document "+parameters['doc_id']+"' does not exist"}), 400

    if Arq.query.filter_by(doc_id=parameters['doc_id']).first():
        return jsonify({"msg": "Arquitecture for 'document "+parameters['doc_id']+"' already exist"}), 400
    
    if 'image' not in request.files:
        return jsonify({'message' : 'No file part in the request'}), 400
        
    image = request.files['image']
    upload_folder = os.path.join(app.root_path, 'uploads')
    image.save(os.path.join(upload_folder, image.filename))
    parameters['path'] = os.path.join(upload_folder, image.filename)

    try:
        doc = Arq(doc_id=parameters['doc_id'],
                    path=parameters['path'])
        db.session.add(doc)
        db.session.commit()

        return jsonify(doc.serialize()), 200
    except Exception as e:
            return(str(e))

@app.route('/docs/add/diag',methods=['POST'])
def add_diag():
    parameters = {'doc_id':None}
    parameters = {param:request.form.to_dict().get(param, None) for param in parameters.keys()}
    
    for param, value in parameters.items():
        if not value:
            return jsonify({"msg": "Missing "+param+" parameter"}), 400
    
    if not Documentation.query.filter_by(id=parameters['doc_id']).first():
        return jsonify({"msg": "'document "+parameters['doc_id']+"' does not exist"}), 400

    if Diag.query.filter_by(doc_id=parameters['doc_id']).first():
        return jsonify({"msg": "Arquitecture for 'document "+parameters['doc_id']+"' already exist"}), 400
    
    if 'image' not in request.files:
        return jsonify({'message' : 'No file part in the request'}), 400
        
    image = request.files['image']
    upload_folder = os.path.join(app.root_path, 'uploads')
    image.save(os.path.join(upload_folder, image.filename))
    parameters['path'] = os.path.join(upload_folder, image.filename)

    try:
        doc = Diag(doc_id=parameters['doc_id'],
                    path=parameters['path'])
        db.session.add(doc)
        db.session.commit()

        return jsonify(doc.serialize()), 200
    except Exception as e:
            return(str(e))

# Delete document
@app.route("/docs/delete/<int:id_>",methods= ['DELETE'])
def delete_doc(id_):

    doc = Documentation.query.get_or_404(id_)
    # intro = Intro.query.filter_by(doc_id=doc.id).first()
    try:
        db.session.delete(doc)
        # db.session.delete(intro)
        db.session.commit()
        return jsonify({'server': '200'})
    except:
        return jsonify({'server': 'ERROR'})

@app.route('/docs/add/conclutions',methods=['POST'])
def add_conclutions():
    parameters = {'doc_id':None,'content':None}
    parameters = {param:request.form.to_dict().get(param, None) for param in parameters.keys()}
    
    for param, value in parameters.items():
        if not value:
            return jsonify({"msg": "Missing "+param+" parameter"}), 400
    
    if not Documentation.query.filter_by(id=parameters['doc_id']).first():
        return jsonify({"msg": "'document "+parameters['doc_id']+"' does not exist"}), 400

    if Conclutions.query.filter_by(doc_id=parameters['doc_id']).first():
        doc = Conclutions.query.filter_by(doc_id=parameters['doc_id']).first()
        # doc.content = doc.content + ' \n ' + parameters['content']
        doc.content = parameters['content']
        print(doc.content)
        db.session.commit()
        return jsonify(doc.serialize()), 200

    try:
        doc = Conclutions(doc_id=parameters['doc_id'],
                    content=parameters['content'])
        db.session.add(doc)
        db.session.commit()

        return jsonify(doc.serialize()), 200
    except Exception as e:
            return(str(e))

@app.route('/docs/add/thanks',methods=['POST'])
def add_thanks():
    parameters = {'doc_id':None,'content':None}
    parameters = {param:request.form.to_dict().get(param, None) for param in parameters.keys()}
    
    for param, value in parameters.items():
        if not value:
            return jsonify({"msg": "Missing "+param+" parameter"}), 400
    
    if not Documentation.query.filter_by(id=parameters['doc_id']).first():
        return jsonify({"msg": "'document "+parameters['doc_id']+"' does not exist"}), 400

    if Thanks.query.filter_by(doc_id=parameters['doc_id']).first():
        doc = Thanks.query.filter_by(doc_id=parameters['doc_id']).first()
        # doc.content = doc.content + ' \n ' + parameters['content']
        doc.content = parameters['content']
        print(doc.content)
        db.session.commit()
        return jsonify(doc.serialize()), 200

    try:
        doc = Thanks(doc_id=parameters['doc_id'],
                    content=parameters['content'])
        db.session.add(doc)
        db.session.commit()

        return jsonify(doc.serialize()), 200
    except Exception as e:
            return(str(e))

@app.route('/docs/add/recomendations',methods=['POST'])
def add_recomendations():
    parameters = {'doc_id':None,'content':None}
    parameters = {param:request.form.to_dict().get(param, None) for param in parameters.keys()}
    
    for param, value in parameters.items():
        if not value:
            return jsonify({"msg": "Missing "+param+" parameter"}), 400
    
    if not Documentation.query.filter_by(id=parameters['doc_id']).first():
        return jsonify({"msg": "'document "+parameters['doc_id']+"' does not exist"}), 400

    if Recomendations.query.filter_by(doc_id=parameters['doc_id']).first():
        doc = Recomendations.query.filter_by(doc_id=parameters['doc_id']).first()
        # doc.content = doc.content + ' \n ' + parameters['content']
        doc.content = parameters['content']
        print(doc.content)
        db.session.commit()
        return jsonify(doc.serialize()), 200

    try:
        doc = Recomendations(doc_id=parameters['doc_id'],
                            content=parameters['content'])
        db.session.add(doc)
        db.session.commit()

        return jsonify(doc.serialize()), 200
    except Exception as e:
            return(str(e))

@app.route('/docs/add/revisions',methods=['POST'])
def add_revitions():
    parameters = {'doc_id':None,'date':None,'version':None,'description':None,'teams':None}
    parameters = {param:request.form.to_dict().get(param, None) for param in parameters.keys()}
    
    for param, value in parameters.items():
        if not value:
            return jsonify({"msg": "Missing "+param+" parameter"}), 400
    
    if not Documentation.query.filter_by(id=parameters['doc_id']).first():
        return jsonify({"msg": "'document "+parameters['doc_id']+"' does not exist"}), 400

    if Revisions.query.filter_by(doc_id=parameters['doc_id'], version=float(parameters['version'])).first():
        doc = Revisions.query.filter_by(doc_id=parameters['doc_id'], version=float(parameters['version'])).first()
        # doc.content = doc.content + ' \n ' + parameters['content']
        doc.date = parameters['date']
        doc.version = parameters['version']
        doc.description = parameters['description']
        doc.teams = parameters['teams']
        db.session.commit()
        return jsonify(doc.serialize()), 200

    try:
        doc = Revisions(doc=parameters['doc_id'],
                        date = parameters['date'],
                        ver = parameters['version'],
                        desc = parameters['description'],
                        teams = parameters['teams'])
        db.session.add(doc)
        db.session.commit()

        return jsonify(doc.serialize()), 200
    except Exception as e:
            return(str(e))


