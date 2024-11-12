import smbus
import time
from mpu6050 import mpu6050

joy1 = mpu6050(0x68)

while True:
    print(joy1.get_accel_data())
    time.sleep(0.5)