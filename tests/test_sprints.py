import sys, os, tempfile, pytest, json
import app
from mixer.backend.flask import mixer
from datetime import datetime

from apps.user.models import UserA as User
from apps.projects.models import *
from apps.stories.models import *
from apps.sprints.models import *

from mixer.backend.sqlalchemy import Mixer


# FUNCIONES DE APOYO
def add_temp_sprint(user, description, project, closed, end_date):
    try:

        sp_date = end_date.split('/')
        date = int(sp_date[0])
        mount = int(sp_date[1])
        year = int(sp_date[2])

        sprint = Sprint(
            user_id = user,
            description = description,
            project_id = project,
            closed = closed,
            end_date = datetime(year,mount,date)
        )
        db.session.add(sprint)
        db.session.commit()
        return [sprint.id, sprint.project_id, sprint.user_id]
    except Exception as e:
	    return(str(e))


def add_temp_story(description, project_id, priority, epic, sprint_id=None):
    try:
        story = Story(
            description = description,
            project_id = project_id,
            priority = priority,
            epic = epic,
            sprint_id = sprint_id
        )
        db.session.add(story)
        db.session.commit()
        return [story.id, sprint_id]

    except Exception as e:
        return(str(e))   

def add_temp_acceptcriteria(user_id, description, story_id, approved):
    try:
        a_criteria = AcceptanceCriteria(
            description = description,
            user_id = user_id,
            story_id = story_id,
            approved = approved
        )
        db.session.add(a_criteria)
        db.session.commit()
        return [a_criteria.id, story_id]

    except Exception as e:
        return(str(e)) 
        

def add_temp_accepttests(user_id, description, story_id, approved):
    try:
        accept_tests = AcceptanceTest(
            description = description,
            user_id = user_id,
            story_id = story_id,
            approved = approved
        )
        db.session.add(accept_tests)
        db.session.commit()
        return [accept_tests.id, story_id]

    except Exception as e:
        return(str(e)) 


def test_sprints_work():
    assert(True)


def test_get_sprints_by_project(client, init_database):
    # creando sprint temporal
    sprint0 = add_temp_sprint(1, 'test description', 1, False, '01/01/2020')
    sprint1 = add_temp_sprint(1, 'test description', 1, False, '01/01/2021')
    
    # tomamos el id del proyecto
    project_id = sprint0[1]

    # se llama al servicio
    rv = client.get("/sprint/getbyproject/"+str(project_id))

    # se deserializa el response
    sprint = json.loads(rv.data.decode('utf-8'))

    # se verifica numero de elementos y si los temporales estan entre ellos
    assert (sprint0[0] in [elem['id'] for elem in sprint]) and (sprint1[0] in [elem['id'] for elem in sprint])
    assert len(sprint) == 2
    app.db.session.commit()


def test_get_sprint_active_by_project(client, init_database):
    # creando sprint temporal
    sprint0 = add_temp_sprint(1, 'test description', 1, False, '01/01/2020')
    sprint1 = add_temp_sprint(1, 'test description', 2, False, '01/01/2021')
    
    # tomamos el id del proyecto
    project_id = sprint0[1]

    # se llama al servicio
    rv = client.get("/sprint/active/"+str(project_id))

    # se deserializa el response
    sprint = json.loads(rv.data.decode('utf-8'))

    # se verifica numero de elementos y si los temporales estan entre ellos
    assert (sprint0[0] in [elem['id'] for elem in sprint]) and not (sprint1[0] in [elem['id'] for elem in sprint])
    assert len(sprint) == 1
    app.db.session.commit()


def test_get_sprint(client, init_database):
    # creando sprint temporal
    sprint0 = add_temp_sprint(1, 'test description', 1, False, '01/01/2020')

    # se llama al servicio
    rv = client.get("/sprint/"+str(sprint0[0]))

    # se deserializa el response
    sprint = json.loads(rv.data.decode('utf-8'))

    # se verifica numero de elementos y si los temporales estan entre ellos
    assert (sprint0[0] in [elem['id'] for elem in sprint])
    assert len(sprint) == 1
    app.db.session.commit()


def test_get_stories_by_sprint(client, init_database):
    # creando sprint e historias temporales asociadas
    sprint0 = add_temp_sprint(1, 'test description', 1, False, '01/01/2020')
    
    story0 = add_temp_story('test_description', 1, StoryPriority.high,False,sprint0[0])
    story1 = add_temp_story('test_description', 1, StoryPriority.medium,False,sprint0[0])

    # se llama al servicio
    rv = client.get("/sprint/getstories/"+str(sprint0[0]))

    # se deserializa el response
    sprint_stories = json.loads(rv.data.decode('utf-8'))

    # se verifica numero de elementos y si los temporales estan entre ellos
    assert (story0[0] in [elem['id'] for elem in sprint_stories]) and (story1[0] in [elem['id'] for elem in sprint_stories])
    assert len(sprint_stories) == 2
    app.db.session.commit()


def test_get_criteria_by_story(client, init_database):
    # creando sprint e historias temporales asociadas
    story0 = add_temp_story('test_description', 1, StoryPriority.high,False)

    a_creiteria0 = add_temp_acceptcriteria(1,'Test description1',story0[0],False)
    a_creiteria1 = add_temp_acceptcriteria(1,'Test description2',story0[0],False)
    
    # se llama al servicio
    rv = client.get("/criteria/getbystory/"+str(story0[0]))

    # se deserializa el response
    sprint_stories = json.loads(rv.data.decode('utf-8'))

    # se verifica numero de elementos y si los temporales estan entre ellos
    assert (a_creiteria0[0] in [elem['id'] for elem in sprint_stories]) and (a_creiteria1[0] in [elem['id'] for elem in sprint_stories])
    assert len(sprint_stories) == 2
    app.db.session.commit()


def test_get_tests_by_story(client, init_database):
    # creando sprint e historias temporales asociadas
    story0 = add_temp_story('test_description', 1, StoryPriority.high,False)

    a_test0 = add_temp_accepttests(1,'Test description1',story0[0],False)
    a_test1 = add_temp_accepttests(1,'Test description2',story0[0],False)
    
    # se llama al servicio
    rv = client.get("/tests/getbystory/"+str(story0[0]))

    # se deserializa el response
    sprint_stories = json.loads(rv.data.decode('utf-8'))

    # se verifica numero de elementos y si los temporales estan entre ellos
    assert (a_test0[0] in [elem['id'] for elem in sprint_stories]) and (a_test1[0] in [elem['id'] for elem in sprint_stories])
    assert len(sprint_stories) == 2
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

    user1 = User('bob3','bob','dylan','emprendedor','123')
    user2 = User('bob4','bob','esponja','cocinero','123')

    project1 = Project('description1',1, ProjectStatus.active)
    project2 = Project('description2',1, ProjectStatus.active)

    app.db.session.add(user1)
    app.db.session.add(user2)
    app.db.session.add(project1)
    app.db.session.add(project2)

    app.db.session.commit()

    yield app.db

    app.db.drop_all()