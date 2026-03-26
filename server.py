"""
Mobile Mouse Server
Startet WebSocket-Server + statisches PWA-Frontend in einem Prozess.
Aufruf: python server.py
"""
import json
import socket
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

import mouse_backend

app = FastAPI()

STATIC_DIR = Path(__file__).parent / "static"


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            raw = await websocket.receive_text()
            msg = json.loads(raw)
            t = msg.get("type")
            if t == "move":
                mouse_backend.move(int(msg["dx"]), int(msg["dy"]))
            elif t == "click":
                mouse_backend.click(msg.get("button", "left"))
            elif t == "scroll":
                mouse_backend.scroll(int(msg["delta"]))
    except WebSocketDisconnect:
        pass
    except Exception as exc:
        print(f"WS-Fehler: {exc}", file=sys.stderr)


# Statische Dateien werden nach dem WebSocket-Router gemountet,
# damit /ws nicht vom StaticFiles-Handler abgefangen wird.
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")


def _get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()


if __name__ == "__main__":
    ip = _get_local_ip()
    port = 8765
    url = f"http://{ip}:{port}"

    print(f"\n{'='*52}")
    print(f"  Mobile Mouse gestartet")
    print(f"  URL: {url}")
    print(f"{'='*52}")

    try:
        import qrcode
        qr = qrcode.QRCode(border=1)
        qr.add_data(url)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
    except ImportError:
        print("  Tipp: pip install qrcode  (fuer QR-Code-Anzeige)")

    print()
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")
