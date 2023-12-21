# pip install paho-mqtt
import paho.mqtt.client as paho_mqtt
import json
import threading

# MQTT broker
# prod
broker_address = "121.40.124.59"
broker_port = 1883
user = "mqtt"
passwd = "mqtt@123"
# test
# broker_address = "localhost"
# broker_port = 1883
# user = "user"
# passwd = "password"


'''
    send mqtt message to topic
'''
def send_message(topic, message):
    client = paho_mqtt.Client()
    client.username_pw_set(user, passwd)
    client.connect(broker_address, broker_port)

    info = client.publish(topic, message, qos=1)
    print(f"[mqtt] Send message to topic={topic}, msg={message}")    
    # TODO
    info.wait_for_publish(1)
    print(info.is_published())
    
    client.disconnect()

'''
    send mqtt message to one user by username
'''
def send_message_to_user(username, message):
    client = paho_mqtt.Client()
    client.username_pw_set(user, passwd)
    client.connect(broker_address, broker_port)

    info = client.publish('topic/user/{}'.format(username), message, qos=2)
    print(info.is_published())
    # info.wait_for_publish()
    print(f"[mqtt] Sent message to user={username}, msg={message}")
    
    client.disconnect()

'''
    send mqtt message to all users
'''
def send_message_to_all(message):
    client = paho_mqtt.Client()
    client.username_pw_set(user, passwd)
    client.connect(broker_address, broker_port)

    info = client.publish('topic/user/all', message, qos=2)
    print(f"[mqtt] Sent message to all users, msg={message}")
    print(info.is_published())
    # info.wait_for_publish()
    
    client.disconnect()


# MQTT message handler/router
def handler(payload):
    print(f"Received message: {payload}")
    # do some script
    print("some script done")
    # send message to mobile
    print("send back message done")

mqtt_router = {
    "/data/flow": handler
}

'''
    function to receive mqtt message for outside-service
'''
def outside_service_receive_message():
    client = paho_mqtt.Client(client_id='outside-service', clean_session=False)
    client.username_pw_set(user, passwd)
    client.connect(broker_address, broker_port)

    def on_message(client, userdata, msg):
        try:
            # decode msg to json, dispatch by url
            payload = json.loads(msg.payload.decode())
            handler = mqtt_router[payload['url']]
            handler(payload)
        except Exception as e:
            print("[error] parse mqtt message: {} {} {}".format(client, userdata, msg))
            print(e)
    client.on_message = on_message
    client.subscribe("topic/outside-service", qos=2)

    print("*** [mqtt] is listening at topic: [topic/outside-service]")
    client.loop_forever()    
    # client.disconnect()


# test
if __name__ == "__main__":    
    outside_service_receive_message()

