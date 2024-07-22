
def test_api2(client,dbsession):
    import pytest
    from unittest.mock import patch, MagicMock
    import json
    from Employee.models import Employees
    from Projects.models import Projects

    response = client[0].get("/")
    assert response.status_code ==200

    response = client[0].post("/employees/", json={"name": "test", "department": "test"})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Published for creation'}
#
    response = client[0].put("/employees/1", json={"department": "test"})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Published for update'}
#
    response = client[0].delete("/employees/1")
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Published for deletion'}
#
    response = client[0].post("/projects/", json={"name": "test", "department": "test"})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Published for creation'}

    response = client[0].put("/projects/1", json={"department": "test"})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Published for update'}

    response = client[0].delete("/projects/1")
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Published for deletion'}
# # testing the Employees get
    e1 = Employees(name="t1", department="t1")
    e2 = Employees(name="t2", department="t2")
    dbsession.add(e1)
    dbsession.add(e2)
    dbsession.commit()
    with patch('app.db.session', new=dbsession):
        response = client[0].get('/employees/')
    data = response.get_json()
    assert data[0]["name"] == "t1"
    assert data[0]["department"] == "t1"
    assert data[1]["name"] == "t2"
    assert data[1]["department"] == "t2"
# Testing the projects get
    p1 = Projects(name="t1")
    p2 = Projects(name="t2")
    dbsession.add(p1)
    dbsession.add(p2)
    dbsession.commit()
    with patch('app.db.session', new=dbsession):
        response = client[0].get('/projects/')
    data = response.get_json()
    assert data[0]["name"] == "t1"
    assert data[1]["name"] == "t2"
# Testing the project get
    with patch('app.db.session', new=dbsession):
        response = client[0].get('/projects/1')
    data = response.get_json()
    print(data)
    assert data["project_id"]==1
    assert data["project_name"] == "t1"

    client[1].publish.side_effect = RuntimeError("Mqtt client is down")
    with patch('app.db.session', new=dbsession):
        response = client[0].get('/employees/')
    assert response.status_code == 400
    res = client[0].post("/employees/", json={"name": "test", "department": "test"})
    assert res.status_code == 400
    obj = json.loads(res.data)
    assert obj['message'] == "Failed to create employee"
    res = client[0].put("/employees/1", json={"department": "test"})
    assert res.status_code == 400
    obj = json.loads(res.data)
    assert obj['message'] == 'Failed to update employee'
    #
    response = client[0].delete("/employees/1")
    assert response.status_code == 400
    obj = json.loads(response.data)
    assert obj['message'] == "Failed to delete employee"

    with patch('app.db.session', new=dbsession):
        response = client[0].get('/projects/')
    assert response.status_code == 400
    with patch('app.db.session', new=dbsession):
        response = client[0].get('/projects/3')
    assert response.status_code == 404

    with patch('app.db.session', return_value=dbsession):
        response = client[0].get('/projects/1')
    assert response.status_code == 400

    response = client[0].post("/projects/", json={"name": "test"})
    assert response.status_code == 400
    obj = json.loads(response.data)
    assert obj['message'] == 'Failed to create project'

    response = client[0].put("/projects/1", json={"name": "test"})
    assert response.status_code == 400
    obj = json.loads(response.data)
    assert obj['message'] == 'Failed to update project'
    response = client[0].delete("/projects/1")
    assert response.status_code == 400
    obj = json.loads(response.data)
    assert obj['message'] == 'Failed to delete project'
def test_insert_table(dbsession,mock_app,mock_logger):
    import Employee.methods as e_methods
    import Projects.methods as p_methods
    from Employee.models import Employees
    from Projects.models import Projects
    from unittest.mock import patch, MagicMock
    import json
    client = MagicMock()
    message = MagicMock()
    message.payload.decode.return_value = json.dumps({'name': 'Alice', 'department': 'Engineering'})
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app), patch('app.logger', return_value = mock_logger):
        e_methods.insert_table(client, None, message)
    new_employee = dbsession.query(Employees).filter_by(name='Alice').first()
    assert new_employee.name == 'Alice'
    assert new_employee.department == 'Engineering'
    client.publish.assert_called_with("display_message", f"Employee created successfully with id: {new_employee.id}")
    message.payload.decode.return_value = json.dumps({'name': 'Alice'})
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app), patch('app.logger', return_value = mock_logger):
        e_methods.insert_table(client, None, message)
    client.publish.assert_called_with("display_message", f"Creation of employee failed")




def test_update_table(dbsession,mock_app,mock_logger):
    import Projects.methods as p_methods
    from Employee.models import Employees
    from Projects.models import Projects
    from unittest.mock import patch, MagicMock
    import json
    client = MagicMock()
    message = MagicMock()
    message.payload.decode.return_value = json.dumps({'name': 'Project'})
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app), patch('app.logger', return_value = mock_logger):
        p_methods.insert_table(client, None, message)

    import Employee.methods as e_methods
    import Projects.methods as p_methods
    from Employee.models import Employees
    from Projects.models import Projects
    from unittest.mock import patch, MagicMock
    import json
    client = MagicMock()
    message = MagicMock()


    # Insert a sample employee to update
    employee = Employees(name='Bob', department='HR')
    dbsession.add(employee)
    dbsession.commit()
    message.payload.decode.return_value = json.dumps({
        'e_id': employee.id,
        'user': {'name': 'Bob Updated', 'department': 'Finance', 'project_id': 1}
    })
    with patch('app.db.session', new = dbsession), patch('app.app', new=mock_app), patch('app.logger', return_value = mock_logger):
        e_methods.update_table(client, None, message)
    updated_employee = dbsession.query(Employees).filter_by(id=employee.id).one()
    assert updated_employee.name == 'Bob Updated'
    assert updated_employee.department == 'Finance'
    client.publish.assert_called_with("display_message", f"Employee updated successfully with id: {employee.id}")
    message.payload.decode.return_value = json.dumps({
        'e_id': 2,
        'user': {'name': 'Bob Updated', 'department': 'Finance','project_id': 1}
    })
#
    with patch('app.db.session', new = dbsession), patch('app.app', new=mock_app), patch('app.logger', return_value = mock_logger):
        e_methods.update_table(client, None, message)
    client.publish.assert_called_with("display_message", f"Updation of employee failed with id: 2")
#
def test_delete_record(dbsession, mock_app,mock_logger):
    import Employee.methods as e_methods
    import Projects.methods as p_methods
    from Employee.models import Employees
    from Projects.models import Projects
    from unittest.mock import patch, MagicMock
    import json
    client = MagicMock()
    message = MagicMock()
    # Insert a sample employee to delete
    employee = Employees(name='Charlie', department='IT')
    dbsession.add(employee)
    dbsession.commit()
    message.payload.decode.return_value = str(employee.id)
    with patch('app.db.session', new = dbsession), patch('app.app', new=mock_app), patch('app.logger', return_value = mock_logger):
        e_methods.delete_record(client, None, message)
    deleted_employee = dbsession.query(Employees).filter_by(id=employee.id).first()
    assert deleted_employee is None
    client.publish.assert_called_with("display_message", f"Employee deleted successfully with id: {employee.id}")

    message.payload.decode.return_value = 2
    with patch('app.db.session', new = dbsession), patch('app.app', new=mock_app), patch('app.logger', return_value = mock_logger):
        e_methods.delete_record(client, None, message)
    client.publish.assert_called_with("display_message", f"Deletion of employee failed with id: 2")
#
def test_insert_table_project(dbsession,mock_app,mock_logger):
    import Employee.methods as e_methods
    import Projects.methods as p_methods
    from Employee.models import Employees
    from Projects.models import Projects
    from unittest.mock import patch, MagicMock
    import json
    client = MagicMock()
    message = MagicMock()
    message.payload.decode.return_value = json.dumps({'name': 'Project'})
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app), patch('app.logger', return_value = mock_logger):
        p_methods.insert_table(client, None, message)
    new_project = dbsession.query(Projects).filter_by(name='Project').first()
    assert new_project.name == 'Project'
    client.publish.assert_called_with("display_message", f"Project created successfully with id: {new_project.id}")
    message.payload.decode.return_value = json.dumps({})
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app), patch('app.logger', return_value = mock_logger):
        p_methods.insert_table(client, None, message)
    client.publish.assert_called_with("display_message", f"Creation of Project failed")
#
def test_update_table_project(dbsession,mock_app,mock_logger):
    import Employee.methods as e_methods
    import Projects.methods as p_methods
    from Employee.models import Employees
    from Projects.models import Projects
    from unittest.mock import patch, MagicMock
    import json
    client = MagicMock()
    message = MagicMock()
    # Insert a sample employee to update
    project = Projects(name='Project')
    dbsession.add(project)
    dbsession.commit()
    message.payload.decode.return_value = json.dumps({
        'p_id': project.id,
        'project': {'name': 'P2','status':1}
    })
    with patch('app.db.session', new = dbsession), patch('app.app', new=mock_app), patch('app.logger', return_value = mock_logger):
        p_methods.update_table(client, None, message)
    updated_employee = dbsession.query(Projects).filter_by(id=project.id).one()
    assert updated_employee.name == 'P2'
    client.publish.assert_called_with("display_message", f"Project updated successfully with id: {updated_employee.id}")
    message.payload.decode.return_value = json.dumps({
        'p_id': 2,
        'project': {'name': 'P2'}
    })
    with patch('app.db.session', new = dbsession), patch('app.app', new=mock_app):
        p_methods.update_table(client, None, message)
    client.publish.assert_called_with("display_message", f"Updation of project failed with id: 2")

def test_delete_record_project(dbsession, mock_app,mock_logger):
    import Employee.methods as e_methods
    import Projects.methods as p_methods
    from Employee.models import Employees
    from Projects.models import Projects
    from unittest.mock import patch, MagicMock
    import json
    client = MagicMock()
    message = MagicMock()
    # Insert a sample employee to delete
    project = Projects(name='Project')
    dbsession.add(project)
    dbsession.commit()
    message.payload.decode.return_value = str(project.id)
    with patch('app.db.session', new = dbsession), patch('app.app', new=mock_app), patch('app.logger', return_value = mock_logger):
        p_methods.delete_record(client, None, message)
    deleted_employee = dbsession.query(Projects).filter_by(id=project.id).first()
    assert deleted_employee is None
    client.publish.assert_called_with("display_message", f"Employee deleted successfully with id: {project.id}")
    message.payload.decode.return_value = 2
    with patch('app.db.session', new = dbsession), patch('app.app', new=mock_app):
        p_methods.delete_record(client, None, message)
    client.publish.assert_called_with("display_message", f"Deletion of project failed with id: 2")

def test_mqtt_client_connect_publish():
    import paho.mqtt.client as mqtt
    import pytest
    from unittest.mock import MagicMock, patch
    import paho.mqtt.client as mqtt
    from app import logger
    # Mock the logger
    logger.info = MagicMock()
    logger.error = MagicMock()

    client = mqtt.Client()
    userdata = None
    flags = None
    rc = 0
    from m1 import on_connect, on_publish, subscriber

    with patch.object(client, 'subscribe') as mock_subscribe, patch.object(client, 'message_callback_add') as mock_callback_add:
        on_connect(client, userdata, flags, rc)
        logger.info.assert_called_with("Connected to broker")
        for key in subscriber.keys():
            mock_subscribe.assert_any_call(key)
            mock_callback_add.assert_any_call(key, subscriber[key])
    rc = 1
    with patch.object(client, 'subscribe') as mock_subscribe, patch.object(client, 'message_callback_add') as mock_callback_add:
        on_connect(client, userdata, flags, rc)
        logger.error.assert_called_with("Connection failed with code %d", rc)

    message = MagicMock()
    message.payload.decode.return_value = "Test message"
    with patch('app.logger') as mock_logger:
        on_publish(client, userdata, message)
        mock_logger.info.assert_called_with("Test message")


