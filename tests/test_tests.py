import sys, os, tempfile, pytest, json

import app
import apps.projects.services as services
from apps.projects.models import Project, ProjectStatus
from apps.tests.models import UITest, UnitTest
from apps.user.models import UserA as User


def test_tests_work():

    assert True


def test_tests_add_unittest(client, init_database):

    data = dict(
        sprint_id="1",
        description="Test description",
        module="Test Module",
        amount="2",
        component="vista",
    )

    rv = client.post("/tests/unit/add", data=data)
    print(rv.data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_unittest = UnitTest.query.get(response_json["id"])

    assert new_unittest.description == "Test description"
    app.db.session.commit()


def test_tests_get_unittest_by_sprint(client, init_database):

    data = dict(
        sprint_id="15",
        description="Test description",
        module="Test Module",
        amount="2",
        component="vista",
    )

    rv = client.post("/tests/unit/add", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_unittest = UnitTest.query.get(response_json["id"])

    rv = client.get("/tests/unit/15")
    response_json = json.loads(rv.data.decode("utf-8"))

    assert new_unittest.description == response_json[0]["description"]
    app.db.session.commit()


def test_tests_update_unittest(client, init_database):

    data = dict(
        sprint_id="1",
        description="Test description",
        module="Test Module",
        amount="2",
        component="vista",
    )

    rv = client.post("/tests/unit/add", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_unittest = UnitTest.query.get(response_json["id"])

    data = dict(
        sprint_id="2",
        description="New description",
        module="Test Module",
        amount="2",
        component="vista",
    )
    rv = client.put("/tests/unit/" + str(new_unittest.id), data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    updated_unittest = UnitTest.query.get(response_json["id"])

    assert updated_unittest.description == "New description"
    app.db.session.commit()


def test_tests_delete_unittest(client, init_database):

    data = dict(
        sprint_id="1",
        description="Test description",
        module="Test Module",
        amount="2",
        component="vista",
    )

    rv = client.post("/tests/unit/add", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_unittest = UnitTest.query.get(response_json["id"])

    rv = client.delete("/tests/unit/delete/" + str(new_unittest.id))
    response_json = json.loads(rv.data.decode("utf-8"))
    deleted_unittest = UnitTest.query.get(new_unittest.id)

    assert deleted_unittest is None
    app.db.session.commit()


def test_tests_add_uitest(client, init_database):

    data = dict(sprint_id="1", functionality="Test description",)

    rv = client.post("/tests/user-interface/add", data=data)
    print(rv.data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_uitest = UITest.query.get(response_json["id"])

    assert new_uitest.functionality == "Test description"
    app.db.session.commit()


def test_tests_get_uitest_by_sprint(client, init_database):

    data = dict(sprint_id="16", functionality="Test description",)

    rv = client.post("/tests/user-interface/add", data=data)
    print(rv.data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_uitest = UITest.query.get(response_json["id"])

    rv = client.get("/tests/user-interface/16")
    response_json = json.loads(rv.data.decode("utf-8"))

    assert new_uitest.functionality == response_json[0]["functionality"]
    app.db.session.commit()


def test_tests_update_uitest(client, init_database):

    data = dict(sprint_id="1", functionality="Test description",)

    rv = client.post("/tests/user-interface/add", data=data)
    print(rv.data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_uitest = UITest.query.get(response_json["id"])

    data = dict(sprint_id="1", functionality="New description",)

    rv = client.put("/tests/user-interface/" + str(new_uitest.id), data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    updated_uitest = UITest.query.get(response_json["id"])

    assert updated_uitest.functionality == "New description"
    app.db.session.commit()


def test_tests_delete_uitest(client, init_database):

    data = dict(sprint_id="1", functionality="Test description",)

    rv = client.post("/tests/user-interface/add", data=data)
    print(rv.data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_uitest = UITest.query.get(response_json["id"])

    rv = client.delete("/tests/user-interface/delete/" + str(new_uitest.id))
    response_json = json.loads(rv.data.decode("utf-8"))
    deleted_uitest = UITest.query.get(new_uitest.id)

    assert deleted_uitest is None
    app.db.session.commit()


@pytest.fixture
def client():
    db_fd, app.app.config["DATABASE"] = tempfile.mkstemp()
    app.app.config["TESTING"] = True

    with app.app.test_client() as client:
        with app.app.app_context():
            yield client

    os.close(db_fd)
    os.unlink(app.app.config["DATABASE"])


@pytest.fixture
def init_database():
    app.db.create_all()

    user1 = User("bob1", "bob", "dylan", "emprendedor", "123")
    user2 = User("bob2", "bob", "esponja", "cocinero", "123")

    app.db.session.add(user1)
    app.db.session.add(user2)

    app.db.session.commit()

    yield app.db

    app.db.drop_all()
