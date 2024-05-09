import paho.mqtt.client as mqtt
import setup_db as db
rfid_tag = ""
name = ""
humidity_threshold = None
temperature_threshold = None
light_intensity_threshold = None
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("IoTlab/RFIDTag")

def on_message(client, userdata, msg):
    global rfid_data
    global name
    global humidity_threshold
    global light_intensity_threshold
    global temperature_threshold
    global rfid_tag
    rfid_data = msg.payload.decode()
    rfid_db_row = db.select_user_threshold_by_rfid("dashboard.db", rfid_data)
    
    name = rfid_db_row[0][1]
    temperature_threshold = rfid_db_row[0][2]
    humidity_threshold = rfid_db_row[0][3]
    light_intensity_threshold = rfid_db_row[0][4]
    rfid_tag = rfid_db_row[0][5]
    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("172.20.10.2", 1883, 60)

client.loop_start()
