from machine import Pin
from time import sleep_ms

class LedController:

    DOT = "."
    DASH = "-"

    UNIT = 200  # Morse-Zeiteinheit in ms

    def __init__(self, led_pin_num):
        self.led = Pin(led_pin_num, Pin.OUT, value=0)

    def signal(self, duration):
        self.led.value(1)
        sleep_ms(duration * self.UNIT)
        self.led.value(0)
        sleep_ms(self.UNIT)

    def switch(self, code):
        for char in code:
            if char == self.DOT:
                self.signal(1)

            elif char == self.DASH:
                self.signal(3)

            else:
                pass