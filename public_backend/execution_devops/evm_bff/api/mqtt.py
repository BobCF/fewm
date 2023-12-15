# pip install paho-mqtt
import paho.mqtt.client as paho_mqtt

# MQTT broker
broker_address = "121.40.124.59"
broker_port = 1883
user = "mqtt"
passwd = "mqtt@123"

'''
    function to send mqtt message
'''
def send_mqtt_message(topic, message):
    client = paho_mqtt.Client()
    client.username_pw_set(user, passwd)
    client.connect(broker_address, broker_port)

    client.publish(topic, message)
    print(f"[mqtt] Sent message: {message}")

# test
if __name__ == "__main__":
    topic = "myTopic/ClientID"
    message = "mqtt message"
    send_mqtt_message(topic, message)
