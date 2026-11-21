import machine
import time
from empfanger import Empfanger


def main() -> None:
    print("ESP32 Wake-Up Routine gestartet ---")
    empfänger = None

    def handle_signal(mac, msg):
        """Callback-Funktion: Wird automatisch aufgerufen, sobald ein Signal eingeht."""
        print(f"Signal empfangen von {mac}: {msg}")

        # Hier die Logik zur Ansteuerung platzieren
        # morse_code.play_morse_code()
        time.sleep(5)
        if empfänger:
            empfänger.puffer_leeren()
        print("Ansteuerung erfolgreich!")

    try:
        # Initialisierung registriert direkt den Hardware-Callback
        empfänger = Empfanger(on_receive_callback=handle_signal)

    except OSError as e:
        print(f"Fehler bei der Initialisierung des Empfängers: {e}")
        print("Gehe in 5 Minuten Sicherheits-Schlaf...")
        machine.deepsleep(300000)

    print(">>> ESP im Aktivmodus (Interrupt-basiert). Warte auf Signale...")
    # empfänger.aktiviere_empfänger()

    # Ereignisschleife: CPU schläft bis zum nächsten Interrupt
    while True:
        # machine.idle() schaltet die CPU ab, bis ein beliebiger Hardware-Interrupt
        # (z. B. ESP-NOW Empfang) auftritt. Verbraucht 0% CPU-Rechenleistung.
        machine.idle()


if __name__ == "__main__":
    main()