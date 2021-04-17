import RPi.GPIO as GPIO 
import time
import threading

buttonPin = 17
ledPin = 27

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(ledPin,GPIO.OUT)
GPIO.output(ledPin,GPIO.LOW)

pressTime = time.time()

thread = "over"
pill2kill = ""
speed = 0.5

def button_call(channel):
    global buttonPin
    GPIO.remove_event_detect(buttonPin)
    pressTime = time.time()
    while GPIO.input(buttonPin) == 0:
        newTime = time.time()
        if newTime - pressTime > 0.8:
            print("longPress")
            LongPress()

            while GPIO.input(buttonPin) == 0:
                continue

            GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=button_call, bouncetime=300)
            return
    print("short press")
    ShortPress()
    GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=button_call, bouncetime=300)
    
def ShortPress():
    global speed
    if(thread != "over"):
        speed = 0.5
        EndBlink()
        return
    ToggleLed()

def LongPress():
    global speed
    if thread == "over":
        StartBlink(speed)
    else:
        speed = speed - 0.2
        EndBlink()
        StartBlink(speed)
    

#region BLINKING
def StartBlink(speed):
    global pill2kill
    global thread
    pill2kill = threading.Event()
    thread = threading.Thread(target=Blink, args=(pill2kill, speed))
    thread.start()

def EndBlink():
    global pill2kill
    global thread
    global speed
    pill2kill.set()
    thread.join()
    thread = "over"
    LedOff()

def Blink(pill, speed):
    while not pill.wait(speed):
        ToggleLed()
    print("stopping blink")
#endregion

#region LED CONTROL
def ToggleLed():
    global led
    if led:
        LedOff()  
    else:
        LedOn()
        
def LedOn():
    global led
    global ledPin
    GPIO.output(ledPin,GPIO.HIGH)
    led = True

def LedOff():
    global led
    global ledPin
    GPIO.output(ledPin,GPIO.LOW)
    led = False
#endregion

def StartButton():
    global led
    led = False
    GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=button_call, bouncetime=300)
    while True:
        continue

