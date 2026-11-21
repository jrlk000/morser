from machine import Pin
from time import sleep_ms

class LedController:

    DOT = "."
    DASH = "-"

    UNIT = 200  # Morse-Zeiteinheit in ms
    FAKTOR_DASH = 6
    FAKTOR_DOT = 3
    FAKTOR_LETTERS = 9
    FAKTOR_LETTER = 2

    def __init__(self, led_pin_num):
        self.led = Pin(led_pin_num, Pin.OUT, value=0)

    def signal(self, duration):
        self.led.value(1)
        sleep_ms(duration * self.UNIT)
        self.led.value(0)
        sleep_ms(self.UNIT*self.FAKTOR_LETTER)

    def switch(self, code_wort, durchläufe):
        print("Aktiviere switch")
        for _ in range(durchläufe):
            print(f"Anzahl der Durchlaüfe {durchläufe}")

            for char in code_wort:
                if char == self.DOT:
                    self.signal(self.FAKTOR_DOT)

                elif char == self.DASH:
                    self.signal( self.FAKTOR_DASH)

                else:
                    sleep_ms(self.UNIT*self.FAKTOR_LETTERS)