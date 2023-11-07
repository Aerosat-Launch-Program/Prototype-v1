#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP085.h>
#include <WiFi.h>

// Replace with your network credentials
const char *ssid = "iSat-8266";
const char *password = "isat@8266";

WiFiServer server(80);

// Set up the MPU6050 sensor
Adafruit_MPU6050 mpu;

// Set up the BMP180 sensor
Adafruit_BMP085 bmp;

// Define LED and Buzzer pins
const int redLedPin = 13;   // Change to your desired pin number
const int greenLedPin = 12; // Change to your desired pin number
const int buzzerPin = 14;   // Change to your desired pin number

void setup()
{
  Serial.begin(115200);
  delay(1000);

  // Initialize LEDs and buzzer pins
  pinMode(redLedPin, OUTPUT);
  pinMode(greenLedPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  // Turn on the red LED and beep the buzzer on power-up
  digitalWrite(redLedPin, HIGH);
  digitalWrite(buzzerPin, HIGH);
  delay(500);
  digitalWrite(redLedPin, LOW);
  digitalWrite(buzzerPin, LOW);

  // Connect to Wi-Fi
  WiFi.softAP(ssid, password);
  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);

  // Create a server and listen for incoming connections
  server.begin();
  Serial.println("Server started");

  // Initialize the I2C communication
  Wire.begin();

  // Initialize the MPU6050 sensor
  if (!mpu.begin())
  {
    Serial.println("Failed to find MPU6050 sensor.");
    while (1)
      ;
  }

  // Initialize the BMP180 sensor
  if (!bmp.begin())
  {
    Serial.println("Failed to find BMP180 sensor.");
    while (1)
      ;
  }
}
// Function to toggle the red and green LEDs
void toggleLEDs()
{
  static bool toggleState = false;
  digitalWrite(redLedPin, toggleState ? HIGH : LOW);
  digitalWrite(greenLedPin, toggleState ? LOW : HIGH);
  toggleState = !toggleState;
}

// Function to beep the buzzer
void beepBuzzer()
{
  digitalWrite(buzzerPin, HIGH);
  delay(100); // Adjust this delay for the desired beep duration
  digitalWrite(buzzerPin, LOW);
}

void loop()
{
  // Wait for a client to connect
  WiFiClient client = server.available();
  if (!client)
  {
    // If no client is connected, toggle the red and green LEDs
    toggleLEDs();
    delay(500);
    return;
  }

  // If a client is connected, turn on both LEDs
  digitalWrite(redLedPin, HIGH);
  digitalWrite(greenLedPin, HIGH);

  Serial.println("Client connected");

  while (client.connected())
  {
    // Read sensor data from MPU6050
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    // Read pressure data from BMP180
    float pressure = bmp.readPressure() / 100.0F; // Convert Pa to hPa

    // Read altitude data from BMP180
    float altitude = bmp.readAltitude(1013.25); // Use your local pressure for more accurate results

    // Format sensor data as a string
    String sensorData = String(a.acceleration.x) + "," +
                        String(a.acceleration.y) + "," +
                        String(a.acceleration.z) + "," +
                        String(g.gyro.x) + "," +
                        String(g.gyro.y) + "," +
                        String(g.gyro.z) + "," +
                        String(pressure) + "," +
                        String(altitude) + "," +
                        String(temp.temperature);

    // Send sensor data to the client (Python GUI)
    client.println(sensorData);

    // Beep the buzzer after each data is sent
    beepBuzzer();

    // Wait for a moment before sending more data
    delay(1000);
  }

  // Client disconnected
  Serial.println("Client disconnected");
}
