"""Hang effektek a panelhez.

A hangok fix kulcsokkal azonosíthatók (pl. "beep", "double_beep").
A UI a languages.py-ból fordítja le a megjelenítendő neveket.
Így új nyelv hozzáadásakor NEM kell módosítani ezt a fájlt.
"""
import time
import threading

try:
    import winsound
    WINSOUND_AVAILABLE = True
except ImportError:
    WINSOUND_AVAILABLE = False


# =====================================================================
#  HANG KULCSOK — ezek a fix azonosítók, NEM fordítjuk őket!
#  A megjelenítendő nevek a languages.py-ban vannak:
#    sound_beep, sound_double_beep, sound_buzz, ...
# =====================================================================
SOUND_KEYS = [
    "beep",
    "double_beep",
    "buzz",
    "triple_beep",
    "slow_buzz",
    "fast_double",
    "long_cry",
    "none",
]

# Alapértelmezett hang
DEFAULT_SOUND_KEY = "beep"

# Régi magyar nevek → új kulcs (visszafele kompatibilitás)
_LEGACY_NAME_MAP = {
    "Alap (Beep)": "beep",
    "Dupla Pittyogás": "double_beep",
    "Mély Hiba (Buzz)": "buzz",
    "Hármas Sípjel": "triple_beep",
    "Lassú Búgás": "slow_buzz",
    "Gyors Dupla": "fast_double",
    "Hosszú Sírás": "long_cry",
    "Nincs hang": "none",
}


# =====================================================================
#  Hang szekvenciák: (frekvencia Hz, hossz ms)
#  0 Hz = szünet
# =====================================================================
_SOUND_MAP = {
    "beep":         [(1000, 200)],
    "double_beep":  [(1200, 100), (0, 50), (1200, 100)],
    "buzz":         [(400, 350)],
    "triple_beep":  [(1500, 80), (0, 50), (1500, 80), (0, 50), (1500, 80)],
    "slow_buzz":    [(300, 600)],
    "fast_double":  [(2000, 60), (0, 30), (2000, 60)],
    "long_cry":     [(800, 200), (0, 100), (600, 200), (0, 100), (400, 400)],
    "none":         [],
}


# =====================================================================
#  Segédfüggvények
# =====================================================================
def _normalize_key(name_or_key):
    """Ha régi magyar nevet kap, átalakítja kulcsra.

    Ha már kulcs, visszaadja változatlanul.
    Ha ismeretlen, az alapértelmezettet adja vissza.
    """
    if name_or_key in _SOUND_MAP:
        return name_or_key
    if name_or_key in _LEGACY_NAME_MAP:
        return _LEGACY_NAME_MAP[name_or_key]
    return DEFAULT_SOUND_KEY


def _play_sequence_blocking(sequence):
    """Egy (freq, duration_ms) tuple-lista lejátszása (blokkoló)."""
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


# =====================================================================
#  Publikus API
# =====================================================================
def play_error_sound_by_key(key, async_play=True):
    """Lejátssza a megadott kulcsú hangot.

    key: fix kulcs (pl. "beep", "double_beep") VAGY régi magyar név
         (pl. "Alap (Beep)") — visszafele kompatibilitás miatt.
    async_play: True esetén háttérszálban szólal meg.
    """
    normalized = _normalize_key(key)
    if normalized == "none":
        return
    sequence = _SOUND_MAP.get(normalized)
    if not sequence:
        return

    if async_play:
        threading.Thread(
            target=_play_sequence_blocking, args=(sequence,), daemon=True
        ).start()
    else:
        _play_sequence_blocking(sequence)


# Régi név megtartása visszafele kompatibilitás miatt
def play_error_sound_by_name(name, async_play=True):
    """[DEPRECATED] Használd a play_error_sound_by_key()-t helyette."""
    return play_error_sound_by_key(name, async_play=async_play)


def get_all_sound_keys():
    """Visszaadja az összes elérhető hang kulcsát."""
    return list(SOUND_KEYS)

def play_error_sound_safe(panel, name=None):
    """
    Hiba hang lejátszása — de csak akkor, ha nincs csendes óra.
    
    panel: a fő panel példány (self)
    name:  a hang neve (opcionális; ha None, a panel beállításából veszi)
    """
    try:
        # Csendes órák ellenőrzése
        if hasattr(panel, "is_quiet_hours") and panel.is_quiet_hours():
            print("[SOUND] 🔇 Csendes órák — hang kihagyva")
            return

        # Ha nincs megadva név, a panel beállításából vesszük
        if name is None:
            name = getattr(panel, "selected_error_sound", None)

        if not name:
            return

        play_error_sound_by_name(name)
    except Exception as e:
        print(f"[SOUND] Hiba: {e}")