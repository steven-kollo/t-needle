#include <Wire.h>
#include <LSM303.h>
LSM303 compass;
char report[80];

#include <SoftwareSerial.h>
SoftwareSerial link(2, 3); // Rx, Tx

byte greenLED = 12;
char cString[20];
byte chPos = 0;
byte ch = 0;
char dataStr[6];

void setup()
{
    link.begin(9600);
    Serial.begin(9600);
    Serial.println("Setup..");
    Wire.begin();
    compass.init();
    compass.enableDefault();

    Serial.println("Setup complete...");
    compass.m_min = (LSM303::vector<int16_t>){-32767, -32767, -32767};
    compass.m_max = (LSM303::vector<int16_t>){+32767, +32767, +32767};
}

void loop()
{

    while (link.available())
    {
        // read incoming char by char:
        ch = link.read();
        cString[chPos] = ch;
        chPos++;
    }
    cString[chPos] = 0; // terminate cString
    chPos = 0;
    // Serial.println(link.available());
    link.println("Works");
    compass.read();

    float heading = compass.heading();
    link.print("Heading:  ");
    link.println(heading);
    Serial.print("Heading:  ");
    Serial.println(heading);

    snprintf(report, sizeof(report), "A: %6d %6d %6d    M: %6d %6d %6d",
             compass.a.x, compass.a.y, compass.a.z,
             compass.m.x, compass.m.y, compass.m.z);
    // link.println(report);
    // Serial.println(report);
    delay(200);
}