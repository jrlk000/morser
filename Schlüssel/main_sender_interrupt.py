from machine import Pin, ADC
from sender import Sender
import machine
import time
import esp32

# MSG_KISTE = "Motor"
ZIEL_MAC_KISTE = b'\x08\xb6\x1fo.\xe4'
# b'\x08\xb6\x1fo.\xe4' # (wroover)
ZIEL_MAC_LEUCHTE = b'\xb0\xa6\x04\x07R8'
ZUSTAND = 1
# b'\xb0\xa6\x04\x07R8'# (xiao)

DEBUG =  b'\xb0\xa6\x04\x04G4'

WAKE_PIN = Pin(3, Pin.IN, Pin.PULL_DOWN, value=0)
VCC = Pin(5, Pin.OUT, Pin.PULL_UP, value=1)
GND = Pin(4, Pin.OUT, Pin.PULL_DOWN, value=0)

LIGHT_SLEEP = 30000  # ms
HIGH_TRIGGER = esp32.WAKEUP_ANY_HIGH
LOW_TRIGGER = esp32.WAKEUP_ALL_LOW

try:
    # ---- Sender Initialisierung ----
    print("Initialisiere Sender...")
    sender = Sender()

    # ----Sende Vorgang ----
    sender.kontaktiere_empfänger(ZIEL_MAC_KISTE, ZUSTAND)
    sender.kontaktiere_empfänger(ZIEL_MAC_LEUCHTE, ZUSTAND)


    sender.deinit_sender()
    print("Trigger-Pin Initialisiert")

    # ----Konfiguration vor dem Schlafgehen----
    esp32.wake_on_gpio([WAKE_PIN], LOW_TRIGGER)
    WAKE_PIN.init(hold=True)
    GND.init(hold=True)
    VCC.init(hold=True)
    esp32.gpio_deep_sleep_hold(True)

    time.sleep_ms(500)
    machine.deepsleep()

except KeyboardInterrupt:
    # Sauberes Aufräumen beim Beenden (fürs Debuggen)
    print("Programm beendet. Räume auf...")

except Exception as e:
    # Fange unerwartete Hardware-Fehler ab
    print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")