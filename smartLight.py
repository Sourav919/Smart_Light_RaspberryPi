import RPi.GPIO as GPIO
import time


LDR_PIN = 17  
TRIGGER_PIN = 23  
ECHO_PIN = 24  
LED_PIN = 18  

GPIO.setmode(GPIO.BCM)
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)



def measure_distance():
    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150 
    return distance

try:
    is_led_on = False

    while True:
        ldr_value = GPIO.input(LDR_PIN)
        print(ldr_value)

        distance = measure_distance()
        print(f"Distance: {distance} cm")

        if ldr_value == 0 and distance < 50 and not is_led_on:
            GPIO.output(LED_PIN, GPIO.HIGH)

            time.sleep(0.2)
            is_led_on = True
        elif (ldr_value == 1 or distance >= 50) and is_led_on:
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(0.2)
            is_led_on = False

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program terminated by user")
finally:
    GPIO.cleanup()
