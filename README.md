# Mobile Mouse

Smartphone als WLAN-Trackpad für den Laptop (Fedora/Wayland).

Ich wollte eine App schreiben und brauchte zufällig eine WLAN-Maus für Linux — also lieber selber gebaut als gesucht. FastAPI + WebSocket + PWA + `evdev`/`uinput`, weil X11-Tools auf Wayland nicht funktionieren. Funktioniert für mich, ist aber nicht als Produkt gedacht.

## Einmalige Einrichtung (udev + Gruppe)

```bash
echo 'KERNEL=="uinput", GROUP="input", MODE="0660"' | sudo tee /etc/udev/rules.d/99-uinput.rules
sudo udevadm control --reload-rules && sudo usermod -aG input $USER
# Neuanmeldung erforderlich
```

## Installation

```bash
git clone https://github.com/VibeCodeSolutions/mobile-mouse.git
cd mobile-mouse
pip install -r requirements.txt
```

## Starten

```bash
python server.py
```

Der Server gibt die URL (und optional einen QR-Code) aus. Diese URL im Chrome des Smartphones öffnen. Chrome fragt nach „Zum Startbildschirm hinzufügen" für PWA-Installation.

## Gesten

| Geste | Aktion |
|---|---|
| Einzelfinger wischen | Mausbewegung |
| Einzelfinger tippen | Linksklick |
| Zwei-Finger tippen | Rechtsklick |
| Zwei-Finger wischen (hoch/runter) | Scrollen |
| Buttons unten | Links-/Rechtsklick (Fallback) |

## Akzeptanzkriterien

- AK1: Server startet mit einem Befehl und zeigt URL/QR-Code
- AK2: Mausbewegung reagiert auf Touch-Wischen
- AK3: Linksklick, Rechtsklick und Scrollen funktionieren
- AK4: Latenz subjektiv < 100ms

## Sicherheitshinweis

Der Server ist ohne Authentifizierung. Nur im vertrauenswürdigen WLAN betreiben. Port 8765 ist lokal gebunden und nicht von außen erreichbar, solange keine Portweiterleitung konfiguriert ist.

## Abhängigkeiten

- `evdev` >= 1.6.0 — Kernel-Maussteuerung via uinput (Wayland-kompatibel)
- `fastapi` + `uvicorn` — WebSocket-Server + PWA-Hosting
- `qrcode` — QR-Code-Anzeige beim Start (optional)

## Lizenz

MIT.
