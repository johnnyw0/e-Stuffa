import re
import time
import paho.mqtt.client as mqtt
import random

from multiprocessing import Process, Value

SEND = Value('b', False)
INTERVAL = Value('i', 5)

client = mqtt.Client()
client.connect("mosquitto", 1883, 60)

def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic}| Payload: {str(msg.payload)}")
    match = re.search(r"[@](.+)[|](.+)'", str(msg.payload)) 
    command = match.group(1) 
    value = match.group(2) 

    
    if command == "switch":
        if SEND.value == False:
            SEND.value = True
            client.publish('ul/4jggokgpepnvsb2uv4s40d59ov/device001/attrs', "switch_status|OK")
            client.publish('ul/4jggokgpepnvsb2uv4s40d59ov/device001/attrs', "switch_info|Started sending data")
        elif SEND.value == True:
            SEND.value = False
            client.publish('ul/4jggokgpepnvsb2uv4s40d59ov/device001/attrs', "switch_status|OK")
            client.publish('ul/4jggokgpepnvsb2uv4s40d59ov/device001/attrs', "switch_info|Stopped sending data")
    elif command == "interval":
        try:
            INTERVAL.value = int(value)
        except:
            INTERVAL.value = 5
        client.publish('ul/4jggokgpepnvsb2uv4s40d59ov/device001/attrs', "interval_status|OK")
        client.publish('ul/4jggokgpepnvsb2uv4s40d59ov/device001/attrs', f"interval_info|Interval set to {INTERVAL.value}")

def run_mqtt(client):
    client.on_message = on_message

    client.subscribe("/4jggokgpepnvsb2uv4s40d59ov/device001/cmd")

    client.loop_forever()

def send_data(client):
    while True:
        if SEND.value:
            temperature = round(random.uniform(30, 40), 2)
            humidity = round(random.uniform(0, 100), 2)

            client.publish('ul/4jggokgpepnvsb2uv4s40d59ov/device001/attrs', f"t|{temperature}")
            client.publish('ul/4jggokgpepnvsb2uv4s40d59ov/device001/attrs', f"rh|{humidity}")

        time.sleep(INTERVAL.value)


if __name__ == "__main__":
    client
    p = Process(target=run_mqtt, args=(client,))
    p.start()
    
    p = Process(target=send_data, args=(client,))
    p.start()
    