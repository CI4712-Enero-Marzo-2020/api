import sys, os, tempfile, pytest, json
import app
import apps.projects.services as services
from apps.stories.models import Story, StoryPriority
from apps.user.models import UserA as User


def test_stories_work():
    assert(True)


def test_add_story(client, init_database):
    rv = client.post('/stories/add', 
        data = dict(
            description = 'Test description',
            project_id = 1,
            epic = False,
            priority = 'high'
        )
    )
    response_json = json.loads(rv.data.decode('utf-8'))
    new_story = Story.query.get(response_json['id'])
    
    assert new_story.description == 'Test description'
    assert new_story.priority == StoryPriority.high
    app.db.session.commit()

def test_delete_story(client, init_database):

    rv = client.post('/stories/add', 
        data = dict(
            description = 'Test description1',
            project_id = 1,
            epic = False,
            priority = 'high'
        )
    )
    response_json = json.loads(rv.data.decode('utf-8'))
    new_story_id = response_json['id']
    rv = client.delete("/stories/delete/" + str(new_story_id))
    deleted_story = Story.query.get(new_story_id)

    assert deleted_story is None
    app.db.session.commit()


def test_change_story_epicness(client, init_database):

    rv = client.post('/stories/add', 
        data = dict(
            description = 'Test description1',
            project_id = 1,
            epic = False,
            priority = 'high'
        )
    )

    response_json = json.loads(rv.data.decode('utf-8'))
    new_story_id = response_json['id']
    rv = client.patch("/stories/classification/" + str(new_story_id))

    response_json = json.loads(rv.data.decode('utf-8'))
    modified_story = Story.query.get(response_json['id'])
    
    assert modified_story.epic == True
    app.db.session.commit()


def test_update_story(client, init_database):

    rv = client.post('/stories/add', 
        data = dict(
            description = 'Test description1',
            project_id = 1,
            epic = False,
            priority = 'high'
        )
    )

    response_json = json.loads(rv.data.decode('utf-8'))
    new_story_id = response_json['id']
    rv = client.put("/stories/update/" + str(new_story_id),
        data = dict(
            description = 'Modified description',
            project_id = 2,
        )
    )

    response_json = json.loads(rv.data.decode('utf-8'))
    modified_story = Story.query.get(response_json['id'])
    
    assert modified_story.description == 'Modified description'
    assert modified_story.project_id == 2
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

    app.db.session.add(user1)
    app.db.session.add(user2)

    app.db.session.commit()

    yield app.db

    app.db.drop_all()