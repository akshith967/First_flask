import paho.mqtt.client as mqtt
import json

def setup_mqtt(app, db, logger,Employees):
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,"T")

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("connected")
            logger.info("Connected to broker")
            mqtt_client.subscribe("display_message")
            mqtt_client.subscribe("insert")
            mqtt_client.subscribe("update")
            mqtt_client.subscribe("delete")
        else:
            logger.error("Connection failed with code %d", rc)

    def insert_table(client, userdata, message):
        with app.app_context():
            try:
                data = json.loads(message.payload.decode())
                new_employee = Employees(name=data['name'], department=data['department'])
                db.session.add(new_employee)
                db.session.commit()
                client.publish("display_message", f"Employee created successfully with id: {new_employee.id}")
            except Exception as e:
                client.publish("display_message", "Creation of employee failed")
                logger.error(f"Failed to create employee: {e}")

    def update_table(client, userdata, message):
        with app.app_context():
            try:
                data = json.loads(message.payload.decode())
                employee = Employees.query.get_or_404(data['e_id'])
                employee.name = data['user']['name']
                employee.department = data['user']['department']
                db.session.commit()
                client.publish("display_message", f"Employee updated successfully with id: {data['e_id']}")
            except Exception as e:
                client.publish("display_message", f"Updation of employee failed with id: {data['e_id']}")
                logger.error(f"Failed to update employee: {e}")

    def delete_record(client, userdata, message):
        with app.app_context():
            try:
                employee_id = int(message.payload.decode())
                employee = Employees.query.get_or_404(employee_id)
                db.session.delete(employee)
                db.session.commit()
                client.publish("display_message", f"Employee deleted successfully with id: {employee_id}")
            except Exception as e:
                client.publish("display_message", f"Deletion of employee failed with id: {employee_id}")
                logger.error(f"Failed to delete employee: {e}")

    def on_publish(client, userdata, message):
        logger.info(message.payload.decode())

    mqtt_client.on_connect = on_connect
    mqtt_client.message_callback_add("insert", insert_table)
    mqtt_client.message_callback_add("update", update_table)
    mqtt_client.message_callback_add("delete", delete_record)
    mqtt_client.message_callback_add("dislay_message", on_publish)
    mqtt_client.connect("127.0.0.1", 1883, 60)
    mqtt_client.loop_start()
    return mqtt_client
