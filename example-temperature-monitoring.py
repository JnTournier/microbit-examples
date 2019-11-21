from microbit import *

m = 14
c = 66

while True:
    reading = pin0.read_analog()
    temperature = int((reading - c) / m)
    if temperature < 10:
        display.show(str(temperature))
    else:
        display.scroll(str(temperature))
    sleep(500)
    display.clear()
