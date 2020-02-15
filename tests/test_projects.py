import sys, os, tempfile, pytest, json

import app
import apps.projects.services as services
from apps.projects.models import User, Project, ProjectStatus


def test_projects_work():
    
    assert(True)

def test_add_user(client, init_database):
    rv = client.get('/users/add')
    new_user = User.query.get(3)
    
    assert rv.data != None
    assert new_user != None
    assert new_user.id == int(new_user.id)
    app.db.session.commit()

def test_add_project(client, init_database):
    rv = client.post('/projects/add', 
        data = dict(
            description = 'Test description',
            user_id = 1,
            status = ProjectStatus.active
        )
    )
    response_json = json.loads(rv.data.decode('utf-8'))
    new_project = Project.query.get(response_json['id'])
    
    assert new_project.description == 'Test description'
    assert new_project.status == ProjectStatus.active
    app.db.session.commit()

def test_get_all_by_user(client, init_database):
    test_user_id = 4
    rv = client.post('/projects/add', 
        data = dict(
            description = 'Test description1',
            user_id = test_user_id,
        )
    )
    rv = client.post('/projects/add', 
        data = dict(
            description = 'Test description2',
            user_id = test_user_id,
        )
    )    
    rv = client.get('/projects/getall/'+ str(test_user_id))        
    response_json = json.loads(rv.data.decode('utf-8'))
    new_projects = [Project.query.get(element['id']) for element in response_json]
    
    assert len(new_projects) == 2
    assert new_projects[0].description == 'Test description1'
    assert new_projects[1].description == 'Test description2'
    app.db.session.commit()

def test_pause_project(client, init_database):

    rv = client.post('/projects/add', 
        data = dict(
            description = 'Test description1',
            user_id = 1,
            status = ProjectStatus.active
        )
    )
    response_json = json.loads(rv.data.decode('utf-8'))
    new_project_id = response_json['id']
    rv = client.get('/projects/pause/' + str(new_project_id))
    paused_project = Project.query.get(new_project_id)
    
    assert paused_project.status == ProjectStatus.paused
    app.db.session.commit()

def test_reactivate_project(client, init_database):

    rv = client.post('/projects/add', 
        data = dict(
            description = 'Test description1',
            user_id = 1,
            status = ProjectStatus.active
        )
    )
    response_json = json.loads(rv.data.decode('utf-8'))
    new_project_id = response_json['id']
    rv = client.get('/projects/pause/' + str(new_project_id))
    rv = client.get('/projects/reactivate/' + str(new_project_id))
    reactivated_project = Project.query.get(new_project_id)
    
    assert reactivated_project.status == ProjectStatus.active
    app.db.session.commit()

def test_delete_project(client, init_database):

    rv = client.post('/projects/add', 
        data = dict(
            description = 'Test description1',
            user_id = 1,
            status = ProjectStatus.active
        )
    )
    response_json = json.loads(rv.data.decode('utf-8'))
    new_project_id = response_json['id']
    rv = client.get("/projects/delete/" + str(new_project_id))
    deleted_project = Project.query.get(new_project_id)

    assert deleted_project is None
    app.db.session.commit()

def test_update_project(client, init_database):

    rv = client.post('/projects/add', 
        data = dict(
            description = 'Test description1',
            user_id = 1,
            status = ProjectStatus.active
        )
    )
    response_json = json.loads(rv.data.decode('utf-8'))
    new_project_id = response_json['id']
    rv = client.put("/projects/update/" + str(new_project_id),
        data = dict(
            description = 'Modified description',
            user_id = 2,
        )
    )

    response_json = json.loads(rv.data.decode('utf-8'))
    modified_project = Project.query.get(response_json['id'])
    
    assert modified_project.description == 'Modified description'
    assert modified_project.user_id == 2
    app.db.session.commit()

@pytest.fixture
def client():
    db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
    app.app.config['TESTING'] = True

    with app.app.test_client() as client:
        with app.app.app_context():
            yield client

    os.close(db_fd)
    os.unlink(app.app.config['DATABASE'])

@pytest.fixture
def init_database():
    app.db.create_all()

    user1 = User()
    user2 = User()

    app.db.session.add(user1)
    app.db.session.add(user2)

    app.db.session.commit()

    yield app.db

    app.db.drop_all()