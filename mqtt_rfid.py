import paho.mqtt.client as mqtt

rfid_data = None

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("IoTlab/RFIDTag")

def on_message(client, userdata, msg):
    global rfid_data
    rfid_data = msg.payload.decode()
    print("Received RFID tag data: " + rfid_data)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.121", 1883, 60)

client.loop_start()
