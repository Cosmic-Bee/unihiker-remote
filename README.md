# Unihiker Remote

This project uses the [Unihiker (affiliate link)](https://www.dfrobot.com/product-2691.html?tracking=Abxl41KH0gYXMiwPMWR8KfrR2xHcVGPklsPZMCdpxU6kcAylDPqgIkd9tpqCto1b) as a remote control for a [Adeept 4WD Omni-directional Mecanum Wheels Robotic Car Kit for ESP32-S3](https://www.adeept.com/adeept-4wd-omni-directional-mecanum-wheels-robotic-car-kit-for-esp32-s3-banana-pi-picow-s3-diy-stem-remote-controlled-educational-robot-kit_p0406_s0086.html).

The omni-directional robotic car kit from Adeept comes with Circuit Python installed. This repository contains a script for the car to run with an access point allowing for remote control. This script communicates with a provided socket to send commands to the car.  

## Setup

### Omni-Directional Car

Several libraries will need to be installed to get the car fully running. This script assumes you have setup the wifi control related logic as part of the setup flow. There are several scripts from the car bundle that are used by this script.

The associated zip file from the car tutorial set includes the needed libraries but they include: `adafruit_ht16k33`, `avoid_obstacles`, `line_tracking`, `BPI_PicoW_S3_Car` with the latter three available as part of that bundle.

For the `BPI_PicoW_S3_Car` file I needed to make a change to the LCD for the logic to run (it expected the i2c to be provided):
```py
class LCD1602:
    def __init__(self):
        self.i2c = busio.I2C(board.GP21, board.GP20)
        self.lcd = LCD(I2CPCF8574Interface(self.i2c, 0X27), num_rows=2, num_cols=16)
    def cleanup(self):
        self.I2C.deinit()
```

Once the associated libraries have been added update the code.py file to reflect the one from this repository. Do not include the `unihiker_remote.py` file as it should be used with the Unihiker.

### Unihiker

With the car setup the Unihiker can be updated to run the associated script. This process 