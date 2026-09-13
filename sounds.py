"""Hang effektek a panelhez."""
import time
import threading

try:
    import winsound
    WINSOUND_AVAILABLE = True
except ImportError:
    WINSOUND_AVAILABLE = False


# A választható hangok listája (a sorrend számít, ez jelenik meg a legördülőben)
ERROR_SOUNDS = [
    "Alap (Beep)",
    "Dupla Pittyogás",
    "Mély Hiba (Buzz)",
    "Hármas Sípjel",
    "Lassú Búgás",
    "Gyors Dupla",
    "Hosszú Sírás",
    "Nincs hang",
]


def _play_sequence(sequence):
    """Egy (freq, duration_ms) tuple-lista lejátszása."""
    if not WINSOUND_AVAILABLE:
        return
    for freq, duration in sequence:
        try:
            winsound.Beep(freq, duration)
        except Exception:
            pass


# Minden hang leírása tuple-listaként: (frekvencia Hz, hossz ms)
_SOUND_MAP = {
    "Alap (Beep)":        [(1000, 200)],
    "Dupla Pittyogás":    [(1200, 100), (0, 50), (1200, 100)],   # 0 = szünet
    "Mély Hiba (Buzz)":   [(400, 350)],
    "Hármas Sípjel":      [(1500, 80), (0, 50), (1500, 80), (0, 50), (1500, 80)],
    "Lassú Búgás":        [(300, 600)],
    "Gyors Dupla":        [(2000, 60), (0, 30), (2000, 60)],
    "Hosszú Sírás":       [(800, 200), (0, 100), (600, 200), (0, 100), (400, 400)],
    "Nincs hang":         [],
}


def _play_sequence_blocking(sequence):
    if not WINSOUND_AVAILABLE:
        return
    for freq, duration in sequence:
        if freq == 0:
            time.sleep(duration / 1000.0)
        else:
            try:
                winsound.Beep(freq, duration)
            except Exception:
                pass


def play_error_sound_by_name(name, async_play=True):
    """Lejátssza a megadott nevű hangot.

    async_play=True esetén háttérszálban szólal meg, hogy a UI ne fagyjon le.
    """
    if name not in _SOUND_MAP or name == "Nincs hang":
        return
    sequence = _SOUND_MAP[name]
    if not sequence:
        return

    if async_play:
        threading.Thread(
            target=_play_sequence_blocking, args=(sequence,), daemon=True
        ).start()
    else:
        _play_sequence_blocking(sequence)