import espnow
import network
import ubinascii

class Empfanger:

    def __init__(self, on_receive_callback):
        # 1. AP-Modus sicherheitshalber ausschalten
        _ap = network.WLAN(network.AP_IF)
        _ap.active(False)

        # WLAN-Schnittstelle im Station-Modus aktivieren
        self.sta = network.WLAN(network.STA_IF)
        self.sta.active(True)
        self.sta.disconnect()

        # ESP-NOW Instanz erstellen
        self.esp = espnow.ESPNow()
        self.esp.active(True)

        self.user_callback = on_receive_callback

        # Hardware-Interrupt registrieren
        self.esp.irq(self._irq_handler)

    def _irq_handler(self, e):
        """Interner Handler: Wird direkt aus dem ESP-NOW Interrupt aufgerufen."""
        while e.any():
            host, msg = e.irecv()  # Liest Nachricht und MAC-Adresse aus
            if msg and self.user_callback:
                self.user_callback(host, msg)

    def aktiviere_empfänger(self):
        # Falls zusätzliche Aktivierungs-Logik nötig ist
        pass

    def deinit_empfänger(self) -> None:
        self.esp.active(False)
        self.sta.active(False)

    def mac_anzeigen(self) -> None:
        mac_bytes = self.sta.config('mac')
        mac_string = ubinascii.hexlify(mac_bytes, ':').decode()
        print("Die MAC-Adresse DIESES Boards lautet:", mac_string, mac_bytes)

    def puffer_leeren(self) -> None:
        """Zieht alle ungelesenen Nachrichten aus dem Puffer und verwirft sie."""
        print(">>> Leere alte Nachrichten aus dem Puffer...")
        while True:
            try:
                # timeout_ms=0 bedeutet: Sofort prüfen. Wenn nichts da ist, brich ab.
                mac, msg = self.esp.recv(timeout_ms=0)
                if not msg:
                    break  # Puffer ist leer
            except OSError:
                break