# pip install paho-mqtt
import uuid

import paho.mqtt.client as paho_mqtt
import json
import threading
import traceback

# MQTT broker
# aliyun rabbitmq prod
broker_address = "rabbitmq" # outside service inside docker along with rabbitmq
broker_port = 1883
user = "user"
pw = "password"

# topic for outside-serivce use
subscribe_topic = "topic/outside-serivce"

'''
    send mqtt message to asignee when task assigned
'''
def send_message_to_asignee(asignee=[], message=""):
    send_message('topic/mobile/user/<username>', {
            'id': str(uuid.uuid1()),
            'name':'inside-service',
            'url':'/notification/assign',
            'data': {
                "message": "task has been assigned to you.",
                "task": "task name",
            }
        })

'''
    general send mqtt message to topic
'''
def send_message(topic, message):
    client = paho_mqtt.Client()
    client.username_pw_set(user, pw)
    client.connect(broker_address, broker_port)

    info = client.publish(topic, json.dumps(message), qos=2)
    print(f"[mqtt] Sent message to topic={topic}, msg={message}")
    # print(info.is_published())
    info.wait_for_publish(1)
    
    client.disconnect()

"""
    MQTT message handler
"""
def default_handler(payload):
    print(f"Received message: {payload}")

"""
sync tasks Table data from intel into aliyun
"""
def tasks_handler(payload):
    print(f"Received message: {payload}")
    rows = payload['data']
    # sync to Task table
    from evm_bff.models.db_models import Task
    for row in rows:
        task, id_created = Task.objects.update_or_create(**row)
    # sync to TaskCache table

"""
sync userprofile Table data from intel into aliyun
"""
def userprofile_handler(payload):
    print(f"Received message: {payload}")
    rows = payload['data']
    # sync to UserProfile table
    from evm_bff.models.db_models import UserProfile
    for row in rows:
        userProfile, id_created = UserProfile.objects.update_or_create(**row)

"""
    mqtt router
"""
mqtt_router = {
    # /data
    "/data/tasks": tasks_handler,
    "/data/userprofile": userprofile_handler,
}

'''
    function to receive mqtt message for outside-service
'''
def outside_service_receive_message():
    client = paho_mqtt.Client(client_id='outside-service', clean_session=False)
    client.username_pw_set(user, pw)
    client.connect(broker_address, broker_port)

    def on_message(client, userdata, msg):
        try:
            # decode msg to json, dispatch by url
            payload = json.loads(msg.payload.decode())
            handler = mqtt_router.get(payload['url'], default_handler)
            handler(payload)
        except Exception as e:
            print("[error] parse mqtt message: {}".format(msg))
            traceback.print_exc()
    client.on_message = on_message
    client.subscribe("topic/outside-service", qos=2)

    print("*** [mqtt] is listening at topic: [topic/outside-service]")
    client.loop_forever()    
    # client.disconnect()

# test
if __name__ == "__main__":    
    outside_service_receive_message()
