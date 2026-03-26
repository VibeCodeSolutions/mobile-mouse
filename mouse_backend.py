"""
Maus-Backend via python-evdev/uinput.
Wayland-kompatibel, keine Root-Rechte im Betrieb (udev-Regel vorausgesetzt).
Siehe README_mobile-mouse.md fuer Einrichtung.
"""
from evdev import UInput, ecodes as e

_capabilities = {
    e.EV_KEY: [e.BTN_LEFT, e.BTN_RIGHT, e.BTN_MIDDLE],
    e.EV_REL: [e.REL_X, e.REL_Y, e.REL_WHEEL],
}

_ui: UInput | None = None

_SETUP_HINT = """
Fehler: Kein Zugriff auf /dev/uinput.
Einmalige Einrichtung (danach kein Root mehr noetig):

  echo 'KERNEL=="uinput", GROUP="input", MODE="0660"' | sudo tee /etc/udev/rules.d/99-uinput.rules
  sudo udevadm control --reload-rules && sudo usermod -aG input $USER

Danach neu anmelden und Server erneut starten.
"""


def _get_ui() -> UInput:
    global _ui
    if _ui is None:
        try:
            _ui = UInput(_capabilities, name="mobile-mouse-virtual")
        except PermissionError:
            raise SystemExit(_SETUP_HINT)
    return _ui


def move(dx: int, dy: int) -> None:
    """Relative Mausbewegung in Pixeln."""
    ui = _get_ui()
    ui.write(e.EV_REL, e.REL_X, dx)
    ui.write(e.EV_REL, e.REL_Y, dy)
    ui.syn()


def click(button: str = "left") -> None:
    """Mausklick: 'left', 'right' oder 'middle'."""
    ui = _get_ui()
    btn = {"left": e.BTN_LEFT, "right": e.BTN_RIGHT, "middle": e.BTN_MIDDLE}[button]
    ui.write(e.EV_KEY, btn, 1)
    ui.syn()
    ui.write(e.EV_KEY, btn, 0)
    ui.syn()


def scroll(delta: int) -> None:
    """Scrollen: positiv = hoch, negativ = runter."""
    ui = _get_ui()
    ui.write(e.EV_REL, e.REL_WHEEL, delta)
    ui.syn()


def close() -> None:
    global _ui
    if _ui is not None:
        _ui.close()
        _ui = None
