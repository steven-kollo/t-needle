#include <Wire.h>
#include <LSM303.h>
#include <SoftwareSerial.h>
#define SPTR_SIZE 20
char *sPtr[SPTR_SIZE];
LSM303 compass;
SoftwareSerial link(2, 3); // Rx, Tx
char cString[40];
byte chPos = 0;
byte ch = 0;
char dataStr[6];

int defineInstructionPosition(char tag)
{
    switch (tag)
    {
    case 't':
        return 0;
    case 'r':
        return 1;
    case 'p':
        return 2;
    case 'y':
        return 3;
    case 'f':
        return 4;
    default:
        return -1;
    }
}

long *parseInstructionString(String str)
{
    static long instructions[5] = {0, 0, 0, 0, 0};
    int N = separate(str, sPtr, SPTR_SIZE);

    for (int n = 0; n < N; n++)
    {
        int position = defineInstructionPosition(sPtr[n][0]);
        String instruction = String(sPtr[n]);
        instruction.remove(0, 1);
        long value = String(instruction).toInt();
        instructions[position] = value;
    }
    return instructions;
}

int separate(String str, char **p, int size)
{
    int n;
    char s[100];
    // Serial.println(str);
    strcpy(s, str.c_str());
    *p++ = strtok(s, " ");
    for (n = 1; NULL != (*p++ = strtok(NULL, " ")); n++)
        if (size == n)
            break;
    return n;
}

void processInstructions()
{
    while (link.available())
    {
        ch = link.read();
        cString[chPos] = ch;
        chPos++;
    }
    cString[chPos] = 0;
    chPos = 0;
    Serial.print("Instructions: ");
    Serial.println(cString);
    long *instructions;
    instructions = parseInstructionString(cString);
    // Uncomment to pass instructions into flight-controller
    // analogWrite(5, instructions[0]); // THROTTLE
    // analogWrite(6, instructions[0]); // ROLL
    // analogWrite(9, instructions[0]); // PITCH
    // analogWrite(10, instructions[0]); // YAW
    // analogWrite(11, instructions[0]); // FLIGHT_MODE
}

void writeSensorValues()
{
    compass.read();
    String sensorValues = "h" + String(int(compass.heading())) + " ax" + String(compass.a.x) + " ay" + String(compass.a.y) + " az" + String(compass.a.z) + " mx" + String(compass.m.x) + " my" + String(compass.m.y) + " mz" + String(compass.m.z);
    Serial.println("Sensors: " + sensorValues);
    link.println(sensorValues);
}

void setup()
{
    Serial.println("Setup..");
    link.begin(9600);
    Serial.begin(9600);

    Wire.begin();
    compass.init();
    compass.enableDefault();
    compass.m_min = (LSM303::vector<int16_t>){-32767, -32767, -32767};
    compass.m_max = (LSM303::vector<int16_t>){+32767, +32767, +32767};

    Serial.println("Setup complete...");
}

void loop()
{
    processInstructions();
    writeSensorValues();
    delay(100);
}