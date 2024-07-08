from Employee.models import Employees
import pytest
import paho.mqtt.client as mqtt
messages = []
@pytest.fixture(scope = "module")
def new_employee():
    return Employees(name="test",department = "IT")

@pytest.fixture(scope="module")
def test_client():
    from app import app
    with app.test_client() as test_client:
        yield test_client
@pytest.fixture(scope="module")
def mqtt_client():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "T1")

    def mess(client, userdata, msg):
        print(msg.payload.decode())
    def on_connect(client, userdata, flags, rc):
        client.subscribe("employee/insert")
        client.message_callback_add("employee/insert", mess)


    client.on_connect = on_connect
    client.connect('localhost', 1883, 60)
    client.loop_start()
    yield client
    client.loop_stop()
