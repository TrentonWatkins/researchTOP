import os

import openai
import paho.mqtt.client as mqtt
from PIL import Image

import people  # Ensure people.py exists and is importable

MQTT_SERVER = "mqtt.eclipseprojects.io"
MQTT_PATH = "Image"


# Securely set the OpenAI API key
openai.api_key = "API Key"

def send_to_openai(message):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Process this message: {message}",
            max_tokens=50
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error interacting with OpenAI: {e}")
        return None

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
    if msg.topic == MQTT_PATH:
        try:
            with open('output.jpg', 'wb') as f:
                f.write(msg.payload)
            print("Image Received")
            image = Image.open('output.jpg')
            message = people.people(image)  # Ensure `people.people()` can handle an image object
            response = send_to_openai(message)
            print(response)
        except Exception as e:
            print(f"Error processing message: {e}")
    else:
        print(f"Unexpected topic: {msg.topic}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(MQTT_SERVER, 1883, 60)
    client.loop_forever()
except Exception as e:
    print(f"Error connecting to MQTT server: {e}")
