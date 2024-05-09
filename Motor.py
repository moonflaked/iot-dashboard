import RPi.GPIO as GPIO
Motor1 = 15  # Enable Pin, GPIO 22
Motor2 = 13  # Input Pin, GPIO 27
Motor3 = 22  # Input Pin, GPIO 25

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(Motor1,GPIO.OUT)
GPIO.setup(Motor2,GPIO.OUT)
GPIO.setup(Motor3,GPIO.OUT)

# GPIO.output(Motor1,GPIO.HIGH)
# GPIO.output(Motor2,GPIO.LOW)
# GPIO.output(Motor3,GPIO.HIGH)
# print("hello")
# time.sleep(5)

# GPIO.output(Motor1,GPIO.HIGH)
# GPIO.output(Motor2,GPIO.HIGH)
# GPIO.output(Motor3,GPIO.LOW)
def turn_on():
    GPIO.output(Motor2, GPIO.HIGH)
    GPIO.output(Motor1, GPIO.HIGH)
    GPIO.output(Motor3, GPIO.LOW)
def turn_off():
    GPIO.output(Motor1, GPIO.LOW)

# time.sleep(5)
#GPIO.cleanup()
turn_on();
# GPIO.setup(Motor1, GPIO.OUT)
# GPIO.setup(Motor2, GPIO.OUT)
# GPIO.setup(Motor3, GPIO.OUT)


