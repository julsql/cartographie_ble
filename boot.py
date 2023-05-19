import machine
import neopixel

num_leds = 1

led_pin = machine.Pin(48, machine.Pin.OUT)
leds = neopixel.NeoPixel(led_pin, num_leds)

leds[0] = (0, 0, 0)
leds.write()