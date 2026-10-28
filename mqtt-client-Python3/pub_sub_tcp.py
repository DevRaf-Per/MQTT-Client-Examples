import json
import random
import time

import paho.mqtt.client as mqtt_client
from paho.mqtt.enums import CallbackAPIVersion

from logger_setup import get_logger

logger = get_logger()

# BROKER = "broker.emqx.io"
BROKER = "localhost"
PORT = 1883
TOPIC = "python-mqtt/tcp"
# generate client ID with pub prefix randomly
CLIENT_ID = f"python-mqtt-tcp-pub-sub-{random.randint(1000,9999)}"
# USERNAME = "emqx"
# PASSWORD = "public"
USERNAME = "sntest"
PASSWORD = "testpassword1"

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

FLAG_EXIT = False


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0 and client.is_connected():
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC)
    else:
        print(f"Failed to connect, return code {reason_code}")


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    logger.info("Disconnected with reason code: %s", reason_code)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logger.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logger.info("Reconnected successfully!")
            return
        except OSError as err:
            logger.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logger.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)
    global FLAG_EXIT
    FLAG_EXIT = True


def on_message(client, userdata, msg):
    print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")


def connect_mqtt():
    client = mqtt_client.Client(
        callback_api_version=CallbackAPIVersion.VERSION2, client_id=CLIENT_ID
    )
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=120)
    client.on_disconnect = on_disconnect
    return client


def publish(client):
    msg_count = 0
    while not FLAG_EXIT:
        msg_dict = {"msg": msg_count}
        msg = json.dumps(msg_dict)
        if not client.is_connected():
            logger.error("publish: MQTT client is not connected!")
            time.sleep(1)
            continue
        result = client.publish(TOPIC, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Sent '{msg}' to topic '{TOPIC}'")
        else:
            print(f"Failed to send message to topic {TOPIC}")
        msg_count += 1
        time.sleep(1)


def run():
    client = connect_mqtt()
    client.loop_start()
    time.sleep(1)
    if client.is_connected():
        publish(client)
    else:
        client.loop_stop()


if __name__ == "__main__":
    run()
