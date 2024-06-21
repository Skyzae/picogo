from machine import Pin, PWM
from micropython_servo_pdm_360 import ServoPDM360
from buzzer_music import music
from utime import sleep, sleep_us, ticks_us
from Motor import PicoGo

# Different songs
song = '0 E5 1 11;2 C5 1 11;4 E5 1 11;6 C5 1 11;8 D#5 1 11;12 E4 1 10;16 E5 1 11;18 C5 1 11;20 E5 1 11;22 C5 1 11;24 F5 1 11;28 F4 1 10;12 G#4 1 10;12 B4 1 10;28 A4 1 10;28 C5 1 10;32 E5 1 11;34 C5 1 11;36 E5 1 11;38 C5 1 11;44 F#5 3 9;48 F5 4.5 9;54 E4 1 10;54 G#4 1 10;54 B4 1 10;56 F4 1 10;56 A4 1 10;56 C5 1 10;58 G#4 1 10;58 B4 1 10;58 E4 1 10;60 D#4 1 10;60 G4 1 10;60 A#4 1 10;62 D4 1 10;62 F#4 1 10;62 A4 1 10;40 G5 3 9'
song2 = '0 E5 1 13;1 C5 1 13;2 E5 1 13;3 C5 1 13;4 E5 1 13;5 C5 1 13;6 E5 1 13;7 C5 1 13;8 D#5 1 13;9 B4 1 13;10 D#5 1 13;11 B4 1 13;12 D#5 1 13;13 B4 1 13;14 D#5 1 13;15 B4 1 13;16 D5 1 13;17 A#4 1 13;18 D5 1 13;19 A#4 1 13;20 D5 1 13;21 A#4 1 13;22 D5 1 13;23 A#4 1 13;24 C#5 1 13;25 A4 1 13;26 C#5 1 13;27 A4 1 13;28 C#5 1 13;29 A4 1 13;30 C#5 1 13;31 A4 1 13;0 C4 4 14;0 A3 4 14;8 B3 4 14;8 G#3 4 14;16 A#3 4 14;24 A3 4 14;16 G3 4 14;24 F#3 4 14;4 C4 4 14;4 A3 4 14;12 B3 4 14;12 G#3 4 14;20 A#3 4 14;28 A3 4 14;20 G3 4 14;28 F#3 4 14;32 E5 1 13;33 C5 1 13;34 E5 1 13;35 C5 1 13;36 E5 1 13;37 C5 1 13;38 E5 1 13;39 C5 1 13;40 D#5 1 13;41 B4 1 13;42 D#5 1 13;43 B4 1 13;44 D#5 1 13;45 B4 1 13;32 C4 4 14;32 A3 4 14;40 B3 4 14;40 G#3 4 14;48 A#3 4 14;56 B3 4 14;48 G3 4 14;56 G#3 4 14;36 C4 4 14;36 A3 4 14;44 B3 4 14;44 G#3 4 14;52 A#3 4 14;60 B3 4 14;52 G3 4 14;60 G#3 4 14;46 B5 1 13;47 E5 1 13;48 A5 1 13;49 E5 1 13;50 A5 1 13;51 E5 1 13;52 A5 1 13;53 E5 1 13;54 A5 1 13;55 E5 1 13;56 G#5 1 13;57 E5 1 13;58 G#5 1 13;59 E5 1 13;60 G#5 1 13;61 E5 1 13;62 D5 1 13;63 B4 1 13;64 E5 1 13;65 C5 1 13;66 E5 1 13;67 C5 1 13;68 E5 1 13;69 C5 1 13;70 E5 1 13;71 C5 1 13;72 D#5 1 13;73 B4 1 13;74 D#5 1 13;75 B4 1 13;76 D#5 1 13;77 B4 1 13;78 D#5 1 13;79 B4 1 13;80 D5 1 13;81 A#4 1 13;82 D5 1 13;83 A#4 1 13;84 D5 1 13;85 A#4 1 13;86 D5 1 13;87 A#4 1 13;88 C#5 1 13;89 A4 1 13;90 C#5 1 13;91 A4 1 13;92 C#5 1 13;93 A4 1 13;94 C#5 1 13;95 A4 1 13;64 C4 4 14;64 A3 4 14;72 B3 4 14;72 G#3 4 14;80 A#3 4 14;88 A3 4 14;80 G3 4 14;88 F#3 4 14;68 C4 4 14;68 A3 4 14;76 B3 4 14;76 G#3 4 14;84 A#3 4 14;92 A3 4 14;84 G3 4 14;92 F#3 4 14;66 E6 1 7;68 A6 1 7;70 E7 1 7;72 D#7 1 7;76 B6 1 7;84 D7 1 7;88 C#7 1 7;92 A6 1 7;98 E6 1 7;100 A6 1 7;102 E7 1 7;104 D#7 1 7;108 B7 1 7;112 A7 1 7;120 G#7 1 7;124 E7 1 7;96 E5 1 13;97 C5 1 13;98 E5 1 13;99 C5 1 13;100 E5 1 13;101 C5 1 13;102 E5 1 13;103 C5 1 13;104 D#5 1 13;105 B4 1 13;106 D#5 1 13;107 B4 1 13;108 D#5 1 13;109 B4 1 13;110 D#5 1 13;111 B4 1 13;112 D5 1 13;113 A#4 1 13;114 D5 1 13;115 A#4 1 13;116 D5 1 13;117 A#4 1 13;118 D5 1 13;119 A#4 1 13;120 C#5 1 13;121 A4 1 13;122 C#5 1 13;123 A4 1 13;124 C#5 1 13;125 A4 1 13;126 C#5 1 13;127 A4 1 13;96 C4 4 14;96 A3 4 14;104 B3 4 14;104 G#3 4 14;112 A#3 4 14;120 A3 4 14;112 G3 4 14;120 F#3 4 14;100 C4 4 14;100 A3 4 14;108 B3 4 14;108 G#3 4 14;116 A#3 4 14;124 A3 4 14;116 G3 4 14;124 F#3 4 14;122 F7 1 7'

#One buzzer on pin 4
mySong = music(song2, pins=[Pin(4)])
led_pin = Pin(8, Pin.OUT)

# create a counter for the LED
counter = 0

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
    while True:
        picoGo.forward(100)
        mySong.tick()
        counter += 1
        print(counter)
        
        # turn counter-clockwise with a force of 50
        servo.turn_ccv(50)
        
        if counter >= 250:
            servo.stop()
            mySong.stop()
            led_pin.value(0)
            break
        else :
            if counter % 4 == 0:
                led_pin.value(not led_pin.value())
            if counter % 2 == 0:
                picoGo.left(100)
            else:
                picoGo.right(100)

        sleep(0.05)
    servo.deinit()
    
while True:
    distance = dist()
    print(distance)
    if distance < 10:
        picoGo.backward(50)
        sleep(0.5)
        picoGo.left(100)
        sleep(0.5)
        picoGo.stop()
        escape()
    sleep(1)
