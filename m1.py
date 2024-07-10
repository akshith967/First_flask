import paho.mqtt.client as mqtt

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,"T")
from Employee import methods as e_methods
from Projects import methods as p_methods


def on_publish(client, userdata, message):
    from app import logger
    logger.info(message.payload.decode())

subscriber = {
    "display_message" : on_publish,
    "employee/insert" : e_methods.insert_table,
    "employee/update" : e_methods.update_table,
    "employee/delete" : e_methods.delete_record,
    "projects/insert" : p_methods.insert_table,
    "projects/update" : p_methods.update_table,
    "projects/delete" : p_methods.delete_record
}
def on_connect(client, userdata, flags, rc):
    from app import logger
    if rc == 0:
        print("connected")

        logger.info("Connected to broker")
        for key, value in subscriber.items():
            client.subscribe(key)
            client.message_callback_add(key, value)
    else:
        logger.error("Connection failed with code %d", rc)

mqtt_client.on_connect = on_connect
mqtt_client.connect("127.0.0.1", 1883, 60)
mqtt_client.loop_start()

