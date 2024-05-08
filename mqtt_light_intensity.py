
import paho.mqtt.client as mqtt
curr_light_intensity = None

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("IoTlab/LightIntensity")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global curr_light_intensity
    curr_light_intensity = str(int(msg.payload))
    print(curr_light_intensity)

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("172.20.10.2", 1883, 60)


mqttc.loop_start()




