import json
def test_api(client):
    response = client[0].post("/employees/", json = {"name":"test", "department":"test"})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Published for creation'}

    response = client[0].put("/employees/1", json={"department": "test"})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Published for update'}

    response = client[0].delete("/employees/1")
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Published for deletion'}

    response = client[0].post("/projects/", json = {"name":"test", "department":"test"})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Published for creation'}

    response = client[0].put("/projects/1", json = {"department":"test"})
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






