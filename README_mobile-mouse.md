# Mobile Mouse

Smartphone als WLAN-Trackpad fuer den Laptop (Fedora/Wayland).

## Einmalige Einrichtung (udev + Gruppe)

```bash
echo 'KERNEL=="uinput", GROUP="input", MODE="0660"' | sudo tee /etc/udev/rules.d/99-uinput.rules
sudo udevadm control --reload-rules && sudo usermod -aG input $USER
# Neuanmeldung erforderlich
```

## Installation

```bash
cd "KI Team/Entwicklung/mobile-mouse"
pip install -r requirements.txt
```

## Starten

```bash
python server.py
```

Der Server gibt die URL (und optional einen QR-Code) aus. Diese URL im Chrome des
Smartphones oeffnen. Chrome fragt nach "Zum Startbildschirm hinzufuegen" fuer
PWA-Installation.

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

Der Server ist ohne Authentifizierung. Nur im vertrauenswuerdigen WLAN betreiben.
Port 8765 ist lokal gebunden und nicht von aussen erreichbar, solange keine
Portweiterleitung konfiguriert ist.

## Abhaengigkeiten

- `evdev` >= 1.6.0 — Kernel-Maussteuerung via uinput (Wayland-kompatibel)
- `fastapi` + `uvicorn` — WebSocket-Server + PWA-Hosting
- `qrcode` — QR-Code-Anzeige beim Start (optional)
