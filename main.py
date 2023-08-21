from machine import Pin, PWM
import utime

freq=1500
speed=18000
f=1

led = Pin("LED", Pin.OUT)
beep= Pin(7,Pin.OUT)
SR = Pin(3,Pin.IN, Pin.PULL_UP)
SM = Pin(4,Pin.IN, Pin.PULL_UP)
SL = Pin(5,Pin.IN, Pin.PULL_UP)


#define Motor 1        
M1_cw=PWM(Pin(16,Pin.OUT))
M1_ccw=PWM(Pin(17,Pin.OUT))        
M1_cw.freq(freq)
M1_ccw.freq(freq)

#define Motor 2        
M2_cw=PWM(Pin(18,Pin.OUT))
M2_ccw=PWM(Pin(19,Pin.OUT))        
M2_cw.freq(freq)
M2_ccw.freq(freq)

#define Motor 3        
M3_cw=PWM(Pin(13,Pin.OUT))
M3_ccw=PWM(Pin(12,Pin.OUT))        
M3_cw.freq(freq)
M3_ccw.freq(freq)

#define Motor 4        
M4_cw=PWM(Pin(14,Pin.OUT))
M4_ccw=PWM(Pin(15,Pin.OUT))        
M4_cw.freq(freq)
M4_ccw.freq(freq)



# Create a Pin object for the onboard LED, configure it as an output

# Initialize the LED state to 0 (off)
led_state = 0
beep_state = 0
old_con_state=False
MStatus=False
counter=0
debounce_time=0
count_old = 0

def button_isr(pin):
    global MStatus, counter, debounce_time
    if (utime.ticks_ms() - debounce_time) > 800:
        if SM.value()==1:
            counter = counter +1 
            print("ISR durchlaufen MStatus=True", counter)
            MStatus=True
        debounce_time=utime.ticks_ms()

SM.irq(trigger=Pin.IRQ_FALLING,handler=button_isr)




def Beep():
    beep.on()
    utime.sleep_ms(50)
    beep.off()



# Beep short if connetced
def Beeper(x):
    global old_con_state
    if x== old_con_state:
        return
    if x==True:
        m=1
        old_con_state = x
    if x==False:
        m=2
        old_con_state = x
    for i in range(0,m,1):
        beep.on()
        utime.sleep_ms(m*50)
        beep.off()
        utime.sleep_ms(50)

# Define a callback function to handle received data
'''
def on_rx(data):
    #print(SL.value(), SM.value(), SR.value())  
    print("Data received: ", data)  # Print the received data
    global led_state, beep_state  # Access the global variable led_state
    
    
    if data == b'LED\r':  # Check if the received data is "toggle"
        led.value(not led_state)  # Toggle the LED state (on/off)
        led_state = 1 - led_state  # Update the LED state
    if data == b'Beep\r':  # Check if the received data is "toggle"
        beep.value(not beep_state)  # Toggle the LED state (on/off)
        beep_state = 1 - beep_state  # Update the LED state    

    decode(data)


def decode(para):
    if para==b'v\r':
        go(speed)
    if para==b's\r':
        go(0)
    if para==b'b\r':
        go(-speed)
    if para==b'l\r':
        turn(-(int(speed/2)))    
    if para==b'r\r':
        turn(int(speed/2))    
'''

def stop():
    M1(0)
    M2(0)
    M3(0)
    M4(0)
    
def turn(s):
    M1(s/f)
    M2(-s)
    M4(s/f)
    M3(-s)
    
    
def Uturn():
    global MStatus, counter
    print("Wende")
    counter=0
    while counter<= 2:
        turn(speed)
        utime.sleep_ms(300)
    stop()
    counter=0
    utime.sleep_ms(1000)
    print("Wenden beendet")
    MStatus=False

def go(s):
    M1(s)
    M2(s)
    M4(s)
    M3(s)

def M1(s):
    if s==0:
        M1_cw.duty_u16(0)
        M1_ccw.duty_u16(0)
    if s > 0:
        M1_cw.duty_u16(int(s*f))
        #print("M1 Vorwärts " +str(M1_cw.duty_u16()))
    if s < 0:
        M1_ccw.duty_u16(int(abs(s)*f))
        #print("M1 Rückwärts " +str(M1_ccw.duty_u16()))
        
def M2(s):
    if s==0:
        M2_cw.duty_u16(0)
        M2_ccw.duty_u16(0)
    if s > 0:
        M2_cw.duty_u16(s)
        #print("M2 Vorwärts " +str(M2_cw.duty_u16()))
    if s < 0:
        M2_ccw.duty_u16(abs(s))
        #print("M2 Rückwärts " +str(M2_ccw.duty_u16()))

def M3(s):
    if s==0:
        M3_cw.duty_u16(0)
        M3_ccw.duty_u16(0)
    if s > 0:
        M3_cw.duty_u16(int(s))
        #print("M3 Vorwärts " +str(M3_cw.duty_u16()))
    if s < 0:
        M3_ccw.duty_u16(abs(s))
        #print("M3 Rückwärts " +str(M3_ccw.duty_u16()))

def M4(s):
    if s==0:
        M4_cw.duty_u16(0)
        M4_ccw.duty_u16(0)
    if s > 0:
        M4_cw.duty_u16(int(s*f))
        #print("M4 Vorwärts " +str(M4_cw.duty_u16()))
    if s < 0:
        M4_ccw.duty_u16(int(abs(s)*f))
        #print("M4 Rückwärts " +str(M4_ccw.duty_u16()))
        
       
stop()
Beep()
#M4(speed)
utime.sleep_ms(1000)
stop()


# Start an infinite loop
'''
while True:

    if sp.is_connected():  # Check if a BLE connection is established
        Beeper(True)
        sp.on_write(on_rx)  # Set the callback function for data reception
        print(SL.value(), SM.value(), SR.value())  
    else:
        led.value(0)
        beep.value(0)
        led_state = 0
        beep_state = 0
        stop()
        Beeper(False)
    utime.sleep_ms(20)  
'''        
oldcorL=0
oldcorR=0
oldcorM=0
i=0
#go(speed)
try:
    while True:
        MStatus=False
        zeit=utime.time()       
        corL = SR.value()
        corR = SL.value()
        corM = SM.value()
        if corL == 1 and corR==1 and corM==1:
            Beep()
            stop()
            oldcorL=corL
            oldcorR=corR
            print("Stop")
            utime.sleep_ms(2000)
            MStatus=False
            counter=0
            Uturn()
        #print(corL, oldcorL, corR, oldcorR, corM, oldcorM)
        if corL!=oldcorL or corR!=oldcorR: # or corM != oldcorM:
            #print(corL, corM, corR)
            if corL==1:
                i=0
                stop()
                turn(speed)
            elif corR==1:
                i=0
                stop()
                turn(-speed)
            if corL == 0 and corR==0 :
                i=0
                stop()
                go(speed)
        
        oldcorL=corL
        oldcorR=corR
        oldcorM=corM
        utime.sleep_ms(100)
        
finally:
    stop()
