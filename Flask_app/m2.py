import paho.mqtt.client as mqtt

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "test"
MQTT_MESSAGE = "Hello, MQTT"

# Creating mqtt clients
client2 = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,"T2")

# Connect to the MQTT broker
client2.connect(MQTT_BROKER, MQTT_PORT, 60)

# Callback when the client receives a CONNACK response from the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to broker with client ID {client._client_id.decode()}")
    else:
        print(f"Failed to connect with result code {rc}")
# Callback when a message is published
def on_publish(client, userdata, mid):
    print(f"Message published! by {client._client_id.decode()}")

# Callback when a message is received
def on_message(client, userdata, msg):
    try:
        print(f"Received message: {msg.payload.decode()}; on topic {msg.topic}")
    except Exception as e: 
        print(e)

# Assign event callbacks

client2.on_connect = on_connect
client2.on_publish = on_publish
client2.on_message = on_message



# Publish a message to the specified topic
client2.subscribe(MQTT_TOPIC)
client2.loop_forever()
client2.disconnect()
