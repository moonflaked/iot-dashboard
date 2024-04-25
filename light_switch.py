import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
led_output_pin = 35  # This would be physical pin 35 that is the gpio19
GPIO.setup(led_output_pin, GPIO.OUT)
GPIO.output(led_output_pin, GPIO.LOW)

def switch_state(led_state):
    GPIO.output(led_output_pin, led_state)
    return led_state

def turn_on():
    GPIO.output(led_output_pin, GPIO.HIGH)
def turn_off():
    GPIO.output(led_output_pin, GPIO.LOW)
