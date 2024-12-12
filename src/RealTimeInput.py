import os
import openai
import paho.mqtt.client as mqtt
from PIL import Image
import cv2
import numpy as np


MQTT_SERVER = "mqtt.eclipseprojects.io"
MQTT_PATH = "Image"

# Securely set the OpenAI API key
openai.api_key = "Enter API key here"

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
def detect_people(image_path):
    # Load the pre-trained MobileNet SSD model
    prototxt_path = 'deploy.prototxt'
    caffe_model_path = 'mobilenet_iter_73000.caffemodel'

    class_labels = [
        'background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 
        'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 
        'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor'
    ]

    net = cv2.dnn.readNetFromCaffe(prototxt_path, caffe_model_path)

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Error loading image")

    height, width = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 0.007843, (300, 300), (127.5, 127.5, 127.5), swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward()

    person_count = 0
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:
            class_id = int(detections[0, 0, i, 1])
            if class_labels[class_id] == 'person':
                person_count += 1
                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

    return person_count, image
    print("There are " + person_count + " Located in this image")	

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
    if msg.topic == MQTT_PATH:
        try:
            # Save received image to a file
            with open('output.jpg', 'wb') as f:
                f.write(msg.payload)
            print("Image Received")

            # Process image with `people.detect_people`
            person_count = detect_people('output.jpg')

            # Send result to OpenAI for response
            response = send_to_openai(f"Detected {person_count} people in the image.")

            # Save response to a file
            with open('chatgpt_response.txt', 'w') as response_file:
                response_file.write(response)
            
            # Print response for debugging/logging
            print(response)

        except Exception as e:
            print(f"Error processing message: {e}")
    else:
        print(f"Unexpected topic: {msg.topic}")

# Create MQTT client and set callbacks
client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT server and start loop
try:
    client.connect(MQTT_SERVER, 1883, 60)
    client.loop_forever()
except Exception as e:
    print(f"Error connecting to MQTT server: {e}")
