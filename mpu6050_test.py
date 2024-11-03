import time
from mpu6050 import mpu6050
import sys

def test_sensor(address):
    """Test a single MPU6050 sensor"""
    try:
        print(f"\nTesting MPU6050 at address 0x{address:02x}")
        sensor = mpu6050(address)
        
        # Test temperature reading
        temp = sensor.get_temp()
        print(f"Temperature: {temp:.2f}°C")
        
        # Test accelerometer
        print("\nTesting accelerometer - move the sensor...")
        for _ in range(5):
            accel_data = sensor.get_accel_data()
            print(f"X: {accel_data['x']:.2f}, Y: {accel_data['y']:.2f}, Z: {accel_data['z']:.2f}")
            time.sleep(0.5)
            
        # Test gyroscope
        print("\nTesting gyroscope - rotate the sensor...")
        for _ in range(5):
            gyro_data = sensor.get_gyro_data()
            print(f"X: {gyro_data['x']:.2f}, Y: {gyro_data['y']:.2f}, Z: {gyro_data['z']:.2f}")
            time.sleep(0.5)
            
        print("\nSensor test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error testing sensor at 0x{address:02x}: {str(e)}")
        return False

def main():
    print("MPU6050 Diagnostic Test")
    print("======================")
    
    # Test both possible addresses
    success_68 = test_sensor(0x68)
    success_69 = test_sensor(0x69)
    
    print("\nTest Summary:")
    print(f"Sensor at 0x68: {'WORKING' if success_68 else 'NOT FOUND/ERROR'}")
    print(f"Sensor at 0x69: {'WORKING' if success_69 else 'NOT FOUND/ERROR'}")
    
    if not success_69:
        print("\nTroubleshooting steps for second sensor (0x69):")
        print("1. Check physical connections:")
        print("   - VCC to 3.3V")
        print("   - GND to GND")
        print("   - SDA to GPIO 2")
        print("   - SCL to GPIO 3")
        print("   - AD0 to 3.3V (This is crucial for setting address to 0x69)")
        print("2. Verify the AD0 pin is properly connected to 3.3V")
        print("3. Try disconnecting and reconnecting the sensor")
        print("4. Check for any bent pins or loose connections")
        print("5. Try swapping the sensors to verify hardware functionality")

if __name__ == "__main__":
    main()