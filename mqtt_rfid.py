import paho.mqtt.client as mqtt
import setup_db as db
rfid_data = None
name = None
humidity_threshold = None
temperature_threshold = None
light_intensity_threshold = None
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("IoTlab/RFIDTag")

def on_message(client, userdata, msg):
    global rfid_data
    rfid_data = msg.payload.decode()
    print("Received RFID tag data: " + rfid_data)
    rfid_db_row = db.select_user_threshold_by_rfid("dashboard.db", rfid_data)
    name = rfid_db_row[0][1]
    name = rfid_db_row[0][2]
    name = rfid_db_row[0][3]
    name = rfid_db_row[0][4]
    name = rfid_db_row[0][5]
    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.121", 1883, 60)

client.loop_start()
