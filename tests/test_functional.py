import json
from Employee.models import Employees
from Projects.models import Projects
from unittest.mock import patch, MagicMock
def test_api2(client):
    response = client[0].post("/employees/", json={"name": "test", "department": "test"})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Published for creation'}

    response = client[0].put("/employees/1", json={"department": "test"})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Published for update'}

    response = client[0].delete("/employees/1")
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Published for deletion'}

    response = client[0].post("/projects/", json={"name": "test", "department": "test"})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Published for creation'}

    response = client[0].put("/projects/1", json={"department": "test"})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Published for update'}

    response = client[0].delete("/projects/1")
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Published for deletion'}
    # down the mqtt client and test the exception
    client[1].publish.side_effect = RuntimeError("MQTT client is down")
    res = client[0].post("/employees/", json={"name": "test", "department": "test"})
    assert res.status_code == 400
    obj = json.loads(res.data)
    assert obj['message'] == "Failed to create employee"

    res = client[0].put("/employees/1", json={"department": "test"})
    assert res.status_code == 400
    obj = json.loads(res.data)
    assert obj['message'] == 'Failed to update employee'

    client[1].publish.side_effect = RuntimeError("MQTT client is down")
    response = client[0].delete("/employees/1")
    assert response.status_code == 400
    obj = json.loads(response.data)
    assert obj['message'] == "Failed to delete employee"

    response = client[0].post("/projects/", json={"name": "test", "department": "test"})
    assert response.status_code == 400
    obj = json.loads(response.data)
    assert obj['message'] == 'Failed to create project'

    response = client[0].put("/projects/1", json={"department": "test"})
    assert response.status_code == 400
    obj = json.loads(response.data)
    assert obj['message'] == 'Failed to update project'
    response = client[0].delete("/projects/1")
    assert response.status_code == 400
    obj = json.loads(response.data)
    assert obj['message'] == 'Failed to delete project'



import Employee.methods as e_methods
import Projects.methods as p_methods

def test_insert_table(dbsession,mock_app):
    client = MagicMock()
    message = MagicMock()
    message.payload.decode.return_value = json.dumps({'name': 'Alice', 'department': 'Engineering'})
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app):
        e_methods.insert_table(client, None, message)
    new_employee = dbsession.query(Employees).filter_by(name='Alice').first()
    assert new_employee.name == 'Alice'
    assert new_employee.department == 'Engineering'
    client.publish.assert_called_with("display_message", f"Employee created successfully with id: {new_employee.id}")
# #
def test_update_table(dbsession,mock_app):
    client = MagicMock()
    message = MagicMock()
    # Insert a sample employee to update
    employee = Employees(name='Bob', department='HR')
    dbsession.add(employee)
    dbsession.commit()
    message.payload.decode.return_value = json.dumps({
        'e_id': employee.id,
        'user': {'name': 'Bob Updated', 'department': 'Finance'}
    })
    with patch('app.db.session', new = dbsession), patch('app.app', new=mock_app):
        e_methods.update_table(client, None, message)
    updated_employee = dbsession.query(Employees).filter_by(id=employee.id).one()
    assert updated_employee.name == 'Bob Updated'
    assert updated_employee.department == 'Finance'
    client.publish.assert_called_with("display_message", f"Employee updated successfully with id: {employee.id}")

def test_delete_record(dbsession, mock_app):
    client = MagicMock()
    message = MagicMock()
    # Insert a sample employee to delete
    employee = Employees(name='Charlie', department='IT')
    dbsession.add(employee)
    dbsession.commit()
    message.payload.decode.return_value = str(employee.id)
    with patch('app.db.session', new = dbsession), patch('app.app', new=mock_app):
        e_methods.delete_record(client, None, message)
    deleted_employee = dbsession.query(Employees).filter_by(id=employee.id).first()
    assert deleted_employee is None
    client.publish.assert_called_with("display_message", f"Employee deleted successfully with id: {employee.id}")


def test_insert_table_project(dbsession,mock_app):
    client = MagicMock()
    message = MagicMock()
    message.payload.decode.return_value = json.dumps({'name': 'Project'})
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app):
        p_methods.insert_table(client, None, message)
    new_project = dbsession.query(Projects).filter_by(name='Project').first()
    assert new_project.name == 'Project'
    client.publish.assert_called_with("display_message", f"Project created successfully with id: {new_project.id}")
# #
def test_update_table_project(dbsession,mock_app):
    client = MagicMock()
    message = MagicMock()
    # Insert a sample employee to update
    project = Projects(name='Project')
    dbsession.add(project)
    dbsession.commit()
    message.payload.decode.return_value = json.dumps({
        'p_id': project.id,
        'project': {'name': 'P2'}
    })
    with patch('app.db.session', new = dbsession), patch('app.app', new=mock_app):
        p_methods.update_table(client, None, message)
    updated_employee = dbsession.query(Projects).filter_by(id=project.id).one()
    assert updated_employee.name == 'P2'
    # assert updated_employee.department == 'Finance'
    client.publish.assert_called_with("display_message", f"Project updated successfully with id: {updated_employee.id}")

def test_delete_record_project(dbsession, mock_app):
    client = MagicMock()
    message = MagicMock()
    # Insert a sample employee to delete
    project = Projects(name='Project')
    dbsession.add(project)
    dbsession.commit()
    message.payload.decode.return_value = str(project.id)
    with patch('app.db.session', new = dbsession), patch('app.app', new=mock_app):
        p_methods.delete_record(client, None, message)
    deleted_employee = dbsession.query(Projects).filter_by(id=project.id).first()
    assert deleted_employee is None
    client.publish.assert_called_with("display_message", f"Employee deleted successfully with id: {project.id}")
