from machine import Pin, PWM
from micropython_servo_pdm_360 import ServoPDM360
from buzzer_music import music
from utime import sleep, sleep_us, ticks_us
from Motor import PicoGo
from ws2812 import NeoPixel

# Different songs
song2 = '0 C5 1 0;4 E5 1 0;5 F5 1 0;6 G5 1 0;7 A5 2 0;9 E5 1 0;11 G5 1 0;13 G#5 1 0;14 A5 2 0;18 E5 1 0;19 F5 1 0;20 G5 1 0;21 A5 1 0;23 B5 1 0;25 B5 1 0;27 A#5 2 0;28 A5 2 0;33 D5 1 0;34 E5 1 0;35 F5 1 0;36 G5 2 0;38 D5 1 0;40 F5 1 0;42 F#5 1 0;43 G5 2 0;47 E5 1 0;46 D5 1 0;48 F5 1 0;49 G5 1 0;51 A5 1 0;53 A5 1 0;55 G#5 2 0;56 G5 2 0;61 E5 1 0;62 F5 1 0;63 G5 1 0;64 A5 2 0;66 E5 1 0;68 G5 1 0;70 G#5 1 0;71 A5 2 0;75 E5 1 0;76 F5 1 0;77 G5 1 0;78 A5 2 0;81 A5 2 0;86 A5 1 0;87 B5 1 0;88 C6 1 0;89 D6 2 0;92 A5 1 0;93 B5 1 0;94 C6 1 0;95 D6 2 0;98 C6 1 0;100 D6 1 0;104 E6 2 0;102 E6 2 0;106 C6 2 0;108 G5 1 0;110 B5 1 0;111 B5 1 0;114 A5 1 0;80 A#5 2 0;85 G5 1 0;118 A5 1 0;119 B5 1 0;120 C6 1 0;121 D6 2 0;117 G#5 1 0;123 A5 1 0;124 B5 1 0;125 C6 1 0;126 D6 2 0;129 E6 2 0;133 C6 2 0;136 G4 1 0;140 G4 1 0;143 G4 1 0;11 E5 1 8;13 E5 1 8;14 E5 1 8;23 F5 1 8;25 F5 1 8;27 F5 1 8;28 F5 1 8;40 D5 1 8;42 D5 1 8;43 D5 1 8;51 F5 1 8;53 F5 1 8;56 E5 1 8;68 E5 1 8;70 E5 1 8;71 E5 1 8;80 E5 1 8;81 F5 1 8;129 G5 1 8;133 G5 1 12;136 E4 1 8;140 E4 1 8;143 E4 1 8'

#One buzzer on pin 4
mySong = music(song2, pins=[Pin(4)])
mySong.stop()

led_pin = Pin(8, Pin.OUT)

# create a PWM servo controller (9 - pin Pico)
servo_pwm = PWM(Pin(9))

# Set the parameters of the servo pulses
freq = 50
min_us = 400
max_us = 2550
dead_zone_us = 150

# create a servo object
servo = ServoPDM360(pwm=servo_pwm, min_us=min_us, max_us=max_us, dead_zone_us=dead_zone_us, freq=freq)

picoGo = PicoGo()

Echo = Pin(15, Pin.IN)
Trig = Pin(14, Pin.OUT)
Trig.value(0)
Echo.value(0)

strip = NeoPixel()
strip.pixels_set(0, strip.BLACK)
strip.pixels_set(1, strip.BLACK)
strip.pixels_set(2, strip.BLACK)
strip.pixels_set(3, strip.BLACK)
strip.pixels_show()

def dist():
    Trig.value(1)
    sleep_us(10)
    Trig.value(0)
    while(Echo.value() == 0):
        pass
    ts=ticks_us()
    while(Echo.value() == 1):
        pass
    te=ticks_us()
    distance=((te-ts)*0.034)/2
    return distance


def escape():
    counter = 0
    mySong.resume()
    while True:
        mySong.tick()
        picoGo.forward(40)
        counter += 1        
        # turn counter-clockwise with a force of 50
        servo.turn_ccv(50)
        strip.pixels_set(0, strip.COLORS[counter % 8])
        strip.pixels_set(1, strip.COLORS[counter % 8])
        strip.pixels_set(2, strip.COLORS[counter % 8])
        strip.pixels_set(3, strip.COLORS[counter % 8])
        strip.pixels_show()
        
        distance = dist()
        if distance < 5:
            picoGo.backward(50)
            sleep(0.1)
            picoGo.left(40)
            sleep(0.3)
        
        if counter >= 80:
            servo.stop()
            led_pin.value(0)
            picoGo.stop()
            servo.deinit()
            mySong.stop()
            strip.pixels_set(0, strip.BLACK)
            strip.pixels_set(1, strip.BLACK)
            strip.pixels_set(2, strip.BLACK)
            strip.pixels_set(3, strip.BLACK)
            strip.pixels_show()
            break
        else :
            if counter % 4 == 0:
                led_pin.value(not led_pin.value())
                strip.pixels_set(0, strip.BLACK)
                strip.pixels_set(1, strip.BLACK)
                strip.pixels_set(2, strip.BLACK)
                strip.pixels_set(3, strip.BLACK)
                strip.pixels_show()
            if counter == 15:
                picoGo.left(40)
            elif counter == 36:
                picoGo.right(40)

        sleep(0.05)
    
while True:
    distance = dist()
    if distance < 10:
        picoGo.backward(50)
        sleep(0.3)
        picoGo.left(40)
        sleep(0.3)
        picoGo.stop()
        escape()