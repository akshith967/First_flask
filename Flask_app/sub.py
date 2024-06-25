from f import *

client2 = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,"T2")
client2.connect(MQTT_BROKER, MQTT_PORT, 60)
# db code

class Audits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return f'<audit {self.id}>'
with app.app_context():
    db.create_all()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to broker with client ID {client._client_id.decode()}")  
    else:
        print(f"Failed to connect with result code {rc}")

def on_message(client, userdata, message):
    try:
        # write code to add the received data to db
   
        # Create a new audit record
        with app.app_context():
            new_audit = Audits(msg=message.payload.decode())
            db.session.add(new_audit)
            db.session.commit()
        print(f"Received message: {message.payload.decode()}")
    except Exception as e: 
        print(e)

# Assign event callbacks
client2.on_connect = on_connect
client2.on_message = on_message
client2.subscribe("audit_request")
# Ready to receive message as soon as they are published 
client2.loop_start() 
while True:
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")
        client.loop_stop()
        client.disconnect()


