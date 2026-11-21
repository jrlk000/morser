from morser import MorseCode
from led_controller import LedController
from empfanger import Empfanger
from machine import Pin
import machine

# ---- Kommunikations Konfiguration Empfänger----
EMPFANGS_ZEITRAUM = 150  # [ms]
EMPFANGS_PAUSE = 1800  # [ms]
CDW = "DAF"
DURCHLÄUFE = 1
PIN_NUM = 3

def main() -> None:
    print("\nESP32 Wake-Up Routine gestartet ---")

    empfänger = None
    m_c = None
    l_c = None

    def handle_signal(mac, msg):
        """Callback-Funktion: Wird automatisch aufgerufen, sobald ein Signal eingeht."""
        print(f"Signal empfangen von {mac}: {msg}")

        # ---- Interaktion ----

        # Übersetze CDW in das Morser Alphabet
        morse_cdw = m_c.übersetze()

        #Übersetze das Morser Alphabet in ein Spannungssignal am Xiao c3
        l_c.switch(morse_cdw)

        if empfänger:
            empfänger.puffer_leeren()
        print("Ansteuerung erfolgreich!")

    try:
        # Initialisierung registriert direkt den Hardware-Callback
        empfänger = Empfanger(on_receive_callback=handle_signal)
        empfänger.mac_anzeigen()

        #Erstelle MOrseCode und Led Objecte
        m_c = MorseCode(CDW)
        l_c = LedController(PIN_NUM)

    except OSError as e:
        print(f"Fehler bei der Initialisierung des Empfängers: {e}")
        print("Gehe in 5 Minuten Sicherheits-Schlaf...")
        machine.deepsleep(300000)

        # Ereignisschleife: CPU schläft bis zum nächsten Interrupt
    while True:
        machine.idle()

if __name__ == "__main__":
    main()