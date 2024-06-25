import paho.mqtt.client as mqtt

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,"T")

def on_publish(client, userdata, mid):
    print(f"Message published! by {client._client_id.decode()}")

# client.on_connect = on_connect
client.on_publish = on_publish
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe("audit_request")


client.loop_start()
def receive_client():
    return client