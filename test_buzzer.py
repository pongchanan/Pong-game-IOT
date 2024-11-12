import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
BUZZER_PIN = 19
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Test the buzzer
try:
    print("Testing buzzer...")
    
    # Turn the buzzer on for 1 second
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    print("Buzzer on")
    time.sleep(1)
    
    # Turn the buzzer off
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    print("Buzzer off")

except KeyboardInterrupt:
    # Clean up GPIO on Ctrl+C
    GPIO.cleanup()
    print("\nExiting...")
