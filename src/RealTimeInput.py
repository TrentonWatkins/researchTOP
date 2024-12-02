#Copyright Hayden Rose VMI CIS
import openai
from paho.mqtt import client as mqtt_client

broker = 'p85773ae.ala.us-east-1.emqxsl.com'
port = 8883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = 'Reader'
username = 'emqx'
password = '**********'
info = ""
openai.api_key = "API_KEY"




def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.tls_set(ca_certs='./server-ca.crt')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        info = (f" `{msg.payload.decode()}`   `{msg.topic}`")
        ai_response = send_to_openai(info)
        if ai_response:
            print(f"OpenAI Response: {ai_response}")
        else:
            print("Failed to get a response from OpenAI.")
    client.subscribe(topic)
    client.on_message = on_message
    
    

def send_to_openai(message):
    try:
        # Send the MQTT message to OpenAI for processing
        response = openai.Completion.create(engine="text-davinci-003",  # Replace with desired model
            prompt=f"Process this message: {message}",max_tokens=50)
        # Extract and return the generated response
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error interacting with OpenAI: {e}")
        return None

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    
if __name__ == '__main__':
    run()

