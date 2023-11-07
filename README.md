# I-SAT Prototype-v1

![Media Player 07-11-2023 13_13_03](https://github.com/Aerosat-Launch-Program/Prototype-v1/assets/76823828/0b895ff9-559f-4c5a-9299-9d79bf965064)

ISAT-8266 is first version of our prototype or satellite series **ISAT**. The purpose behind this prototype to create a foundation of ISAT, to understand
the complexity and working of satellite communication and data visualization.

ISAT-8266 is based on MCU- **ESP32** which was previously designed on **ESP8266**. The sensors installed are
- MPU6050 (GYROSCOPE, ACCELERATION)
- BMP180  (Pressure, Temperature, Altitude)

Other Electronics installed are for indication purposes..

Data communication is done over wifi, the ESP32 act as server.

# How to setup
> Power ISAT-8266

> When powered the will be one beep sound and green-red leds will start blinking. This indiactes the hardware is powered and all the sensor connections are successsfull.

> If indication are not as above, then do check the sensor connection properly.

> Next Connect with WIFI **ISAT_8266** from your system and open the software/GUI in the system

> It will automatically connect and start visualizing data.

> if not check the sensor connection and follow the indication.


Repository contains the first version of the I-SAT satellite wrapping the software and hardware details.
This prototype contains the basic detail about data commmunication and data visualization - integration of hardware and software.

Refer to the code and make necessary change if needed!!
