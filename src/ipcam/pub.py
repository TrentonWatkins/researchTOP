import paho.mqtt.publish as publish
MQTT_SERVER = "mqtt.eclipseprojects.io"  #Write Server IP Address
MQTT_PATH = "Image"

f=open("image_test.jpg", "rb") #3.7kiB in same folder
fileContent = f.read()
byteArr = bytearray(fileContent)


publish.single(MQTT_PATH, byteArr, hostname=MQTT_SERVER)
