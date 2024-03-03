import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
led_output_pin = 17
GPIO.setup(led_output_pin, GPIO.OUT)
GPIO.output(led_output_pin, GPIO.LOW)

def switch_state(led_state):
    GPIO.output(led_output_pin, led_state)
    return led_state
    
    