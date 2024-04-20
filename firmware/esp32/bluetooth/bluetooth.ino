#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

//BLE server name
#define bleServerName "Haptic Definition: Right Hand"

// Timer variables
unsigned long lastTime = 0;
unsigned long timerDelay = 30000;

bool deviceConnected = false;

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/
#define SERVICE_UUID "91bad492-b950-4226-aa2b-4ede9fa42f59"


BLECharacteristic bleTestCharacteristics("cba1d466-344c-4be3-ab3f-189f80dd7518", BLECharacteristic::PROPERTY_NOTIFY);
BLEDescriptor bleTestDescriptor(BLEUUID((uint16_t)0x2902));


//Setup callbacks onConnect and onDisconnect
class MyServerCallbacks: public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) {
    Serial.println("Successfully connected!");
    deviceConnected = true;
  };
  void onDisconnect(BLEServer* pServer) {
    deviceConnected = false;
  }
};

void setup() {
  // Start serial communication 
  Serial.begin(115200);

  Serial.println("Beginning");

  // Create the BLE Device
  BLEDevice::init(bleServerName);

  Serial.println("Initalized bluetooth");

  // Create the BLE Server
  BLEServer *pServer = BLEDevice::createServer();
  Serial.println("Created bluetooth server");
  pServer->setCallbacks(new MyServerCallbacks());

  // Create the BLE Service
  Serial.println("Created bluetooth service");
  BLEService *bleService = pServer->createService(SERVICE_UUID);

  Serial.println("Starting service");
  // Start the service
  bleService->start();

  // Start advertising
  Serial.println("Starting advertising");
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pServer->getAdvertising()->start();
}

void loop() {
  Serial.print(".");
  delay(1000);
}