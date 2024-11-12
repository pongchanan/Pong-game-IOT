import time
import RPi.GPIO as GPIO

# Define the GPIO pin for the buzzer
BUZZER_PIN = 18

# Set up the GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def beep():
    # Turn the buzzer on
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(0.1)  # Beep for 0.1 seconds
    # Turn the buzzer off
    GPIO.output(BUZZER_PIN, GPIO.LOW)