# pip install paho-mqtt
import paho.mqtt.client as paho_mqtt

# MQTT broker
broker_address = "121.40.124.59"
broker_port = 1883
user = "mqtt"
passwd = "mqtt@123"

'''
    send mqtt message to one user by username
'''
def send_message_to_user(message, username):
    client = paho_mqtt.Client()
    client.username_pw_set(user, passwd)
    client.connect(broker_address, broker_port)

    client.publish('topic/user/{}'.format(username), message)
    print(f"[mqtt] Sent message to user={username}, msg={message}")
    
    client.disconnect()

'''
    send mqtt message to all users
'''
def send_message_to_all(message):
    client = paho_mqtt.Client()
    client.username_pw_set(user, passwd)
    client.connect(broker_address, broker_port)

    client.publish('topic/user/all', message)
    print(f"[mqtt] Sent message to all users, msg={message}")
    
    client.disconnect()

# test
if __name__ == "__main__":
    username = "xingyang"
    message = "mqtt message for user"
    send_message_to_user(message, username)
    
    message = "mqtt message for all"
    send_message_to_all(message)

