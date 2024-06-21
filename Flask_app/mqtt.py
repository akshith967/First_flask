import paho.mqtt.client as mqtt

# Define MQTT broker and topic
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "test/topic"
MQTT_MESSAGE = "Hello, MQTT"

# Create an MQTT client instance
client = mqtt.Client()
# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)
# Publish a message to the specified topic
client.publish(MQTT_TOPIC, MQTT_MESSAGE)

# Disconnect from the broker
client.disconnect()
print("Message published!")



# @app.route('/publish', methods=['POST'])
# def publish_message():
#     content = request.json
#     topic = content['topic']
#     message = content['message']
#     mqtt_client.publish(topic, message)
#     return jsonify({"status": "Message sent"})