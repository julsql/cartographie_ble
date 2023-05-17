# Fichier led.py --> Allumer la led de la ESP32-S3

import machine
import neopixel
import time

print("Allumer la LED")

# Configuration de la broche de la bande de LEDs
led_pin = machine.Pin(48, machine.Pin.OUT)

# Configuration du nombre de LEDs dans la bande
num_leds = 1

# Création d'un objet "NeoPixel" avec la configuration de la bande de LEDs
leds = neopixel.NeoPixel(led_pin, num_leds)

# Activer la LED avec une couleur spécifique (ici, rouge)
leds[0] = (255, 0, 0)
leds.write()
time.sleep(3)
leds[0] = (0, 0, 0)
leds.write()