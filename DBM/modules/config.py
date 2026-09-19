import os
import secrets

# --- Verzió betöltése a version.py-ból ---
def _load_version():
    """Beolvassa a verziót a version.py-ból, fallback a version.txt-re."""
    try:
        import version as _version_mod
        v = (getattr(_version_mod, "version", None)
             or getattr(_version_mod, "__version__", None)
             or getattr(_version_mod, "VERSION", None))
        if v:
            return str(v).strip()
    except Exception:
        pass

    try:
        import os
        txt_path = os.path.join(SCRIPT_DIR, "version.txt")
        if os.path.exists(txt_path):
            with open(txt_path, "r", encoding="utf-8") as f:
                return f.read().strip().splitlines()[0].strip()
    except Exception:
        pass

    return "unknown"


VERSION = _load_version()

# A projekt gyökérkönyvtára (a modules/ szülője)
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BOTS_FILE = os.path.join(SCRIPT_DIR, "bots.json")
SETTINGS_FILE = os.path.join(SCRIPT_DIR, "settings.json")
LANG_FILE = os.path.join(SCRIPT_DIR, "lang.json")

# Ez a változó a load_config() során felülíródik, ezért MINDIG config.PANEL_ID-ként érd el!
PANEL_ID = "#" + secrets.token_hex(8).upper()

REMOTE_COMMANDS_FILE = os.path.join(SCRIPT_DIR, "panel_commands.json")
REMOTE_RESPONSES_DIR = os.path.join(SCRIPT_DIR, "panel_responses")
BROADCAST_REQUESTS_FILE = os.path.join(SCRIPT_DIR, "panel_broadcast_requests.json")
BACKUP_DIR = os.path.join(SCRIPT_DIR, "backups")
DISCORD_ICON_PATH = os.path.join(SCRIPT_DIR, "icon.ico")
PLUGINS_DIR = os.path.join(SCRIPT_DIR, "plugins")
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")
LOG_FILE_PATH = os.path.join(LOG_DIR, "bot_log.txt")

# Könyvtárak létrehozása induláskor
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(REMOTE_RESPONSES_DIR, exist_ok=True)