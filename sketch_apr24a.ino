
#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <PubSubClient.h>

#define SS_PIN 5
#define RST_PIN 27

MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
MFRC522::MIFARE_Key key;
byte nuidPICC[4];

const char* ssid = "TP-Link_2AD8";
const char* password = "14730078";
const char* mqtt_server = "192.168.0.121";

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

void setup() {
  Serial.begin(115200);
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522

  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  Serial.println();
  Serial.print(F("Reader: "));
  rfid.PCD_DumpVersionToSerial();

  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }

  Serial.println();
  Serial.println(F("This code scans the MIFARE Classic NUID."));
  Serial.print(F("Using the following key:"));
  printHex(key.keyByte, MFRC522::MF_KEY_SIZE);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  if (!rfid.PICC_IsNewCardPresent())
    return;

  if (!rfid.PICC_ReadCardSerial())
    return;

  Serial.print(F("PICC type: "));
  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
  Serial.println(rfid.PICC_GetTypeName(piccType));

  if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&
      piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
      piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
    Serial.println(F("Your tag is not of type MIFARE Classic."));
    return;
  }

  if (rfid.uid.uidByte[0] != nuidPICC[0] ||
      rfid.uid.uidByte[1] != nuidPICC[1] ||
      rfid.uid.uidByte[2] != nuidPICC[2] ||
      rfid.uid.uidByte[3] != nuidPICC[3]) {
    Serial.println(F("A new card has been detected."));
    for (byte i = 0; i < 4; i++) {
      nuidPICC[i] = rfid.uid.uidByte[i];
    }
    Serial.println(F("The NUID tag is:"));
    Serial.print(F("In hex: "));
    printHex(rfid.uid.uidByte, rfid.uid.size);
    Serial.println();
    Serial.print(F("In dec: "));
    printDec(rfid.uid.uidByte, rfid.uid.size);
    Serial.println();

    // Publish RFID tag data to MQTT topic
    String rfidData = "";
    for (byte i = 0; i < rfid.uid.size; i++) {
      rfidData += String(rfid.uid.uidByte[i], HEX);
    }
    client.publish("IoTlab/RFIDTag", rfidData.c_str());
  } else {
    Serial.println(F("Card read previously."));
  }

  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();

  send_light(); // Call the function to fetch and send light intensity

  delay(5000);
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
      delay(3000);
    }
  }
}

void send_light() {
  int lightIntensity = analogRead(photoresistorPin);
  client.publish("IoTlab/LightIntensity", String(lightIntensity).c_str());
}

void printHex(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}

void printDec(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], DEC);
  }
}