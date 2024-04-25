#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "BELL5153";
const char* password = "hello123";
const char* mqtt_server = "192.168.2.36";

WiFiClient espClient;
PubSubClient client(espClient);

const int photoresistorPin = 34; // Analog pin connected to the photoresistor

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP32 IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messagein;
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messagein += (char)message[i];
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 3 seconds");
      // Wait 3 seconds before retrying
      delay(3000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void send_light() {
  
  int lightIntensity = analogRead(photoresistorPin); // Read analog value from photoresistor

  client.publish("IoTlab/LightIntensity", String(lightIntensity).c_str());
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  send_light(); // Call the function to fetch and send light intensity

  delay(5000);
}
