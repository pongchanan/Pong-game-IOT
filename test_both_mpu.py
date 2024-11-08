import smbus
import time
from mpu6050 import mpu6050

joy1 = mpu6050(0x68)
joy2 = mpu6050(0x69)

while True:
    print("joy 1 " + str(joy1.get_accel_data()))
    print("joy 2 " + str(joy2.get_accel_data()))
    time.sleep(0.5)