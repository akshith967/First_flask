def test_app_get(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Hello World" in response.data
def test_app_post(test_client, mqtt_client):

    response = test_client.post("/employees/", json = {"name" : "test", "department":"test"})
    assert response.status_code == 200

