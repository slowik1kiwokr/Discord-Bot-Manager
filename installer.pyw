# installer.pyw — Discord Bot Manager telepítő
import os
import sys
import re
import shutil
import locale
import subprocess
import threading
import ctypes.wintypes

import customtkinter as ctk
from tkinter import filedialog, messagebox

try:
    from PIL import Image
    PIL_OK = True
except ImportError:
    PIL_OK = False


# ============================================================
#  Szükséges csomagok (pip_név, import_név, rövid leírás)
# ============================================================
REQUIRED_PACKAGES = [
    ("customtkinter", "customtkinter", "Modern UI framework"),
    ("psutil", "psutil", "System monitoring"),
    ("Pillow", "PIL", "Image handling"),
    ("matplotlib", "matplotlib", "Charts"),
    ("pystray", "pystray", "System tray icon"),
    ("pypresence", "pypresence", "Discord Rich Presence"),
]


# ============================================================
#  Nyelvi szótár
# ============================================================
L = {
    "hu": {
        "title": "Discord Bot Manager — Telepítő",
        "subtitle": "Telepítő",
        "welcome": "Üdvözlünk!",
        "welcome_text": "Ez a telepítő segít elhelyezni a panel fájljait egy fix helyre, "
                        "és létrehozza a szükséges parancsikonokat.",
        "info_title": "📋  Panel adatai",
        "info_version": "Verzió",
        "info_author": "Készítette",
        "info_github": "GitHub",
        "info_support": "Támogatás",
        "path_title": "📁  Telepítési hely",
        "path_label": "Hova telepítsük a panelt?",
        "path_browse": "Tallózás...",
        "path_hint": "Alapértelmezett: Documents\\Discord Bot Manager",
        "options_title": "⚙️  Opciók",
        "opt_desktop": "  Parancsikon létrehozása az asztalra",
        "opt_startmenu": "  Parancsikon a Start menübe",
        "opt_launch": "  Panel indítása telepítés után",
        "opt_delete_source": "  Forrásmappa törlése telepítés után",
        "install_btn": "📥   Telepítés",
        "installing": "Telepítés folyamatban...",
        "done": "✅  Telepítés kész!",
        "done_msg": "A panel sikeresen telepítve:\n{path}",
        "done_hint": "A parancsikonról indíthatod a panelt.",
        "error_title": "Hiba",
        "error_path": "Kérlek adj meg egy érvényes útvonalat!",
        "error_exists": "Ez a mappa már létezik és nem üres.\n\nFelülírjuk a fájlokat?",
        "error_install": "Telepítési hiba:\n{error}",
        "error_winrar": "❌ A telepítőt a ZIP-en BELÜLről futtattad!\n\n"
                        "A WinRAR csak egy ideiglenes fájlt másolt ki, a DBM mappa nincs mellette.\n\n"
                        "✅ Megoldás:\n"
                        "   1. Csomagold ki a ZIP-et (jobb klikk → Kibontás)\n"
                        "   2. A kicsomagolt mappából indítsd újra az installer.pyw-t.",
        "lang_btn": "🌐  English",
        "open_folder": "📂  Mappa megnyitása",
        "close_btn": "Bezárás",
        "launching": "Panel indítása...",
        "deleting": "Forrásmappa törlése...",

        # Függőségek
        "deps_title": "📦  Függőségek",
        "deps_hint": "Az alábbi Python csomagok szükségesek a panel futtatásához.\n"
                     "A hiányzókat a gombbal egy kattintással telepítheted.",
        "deps_recheck": "🔍  Újraellenőrzés",
        "deps_install_missing": "📥  Hiányzók telepítése",
        "deps_all_ok": "✅  Minden szükséges csomag telepítve!",
        "deps_missing_n": "❌  {count} csomag hiányzik — telepítsd őket!",
        "deps_checking": "⏳  Csomagok ellenőrzése...",
        "deps_installing": "⏳  Telepítés folyamatban...",
        "deps_install_done": "✅  Telepítés befejezve.",
        "deps_install_err": "❌  Hiba a telepítés során.",
        "install_disabled_deps": "⚠️  Előbb telepítsd a hiányzó csomagokat!",
    },
    "en": {
        "title": "Discord Bot Manager — Installer",
        "subtitle": "Installer",
        "welcome": "Welcome!",
        "welcome_text": "This installer helps you place the panel files in a fixed location "
                        "and creates the necessary shortcuts.",
        "info_title": "📋  Panel info",
        "info_version": "Version",
        "info_author": "Created by",
        "info_github": "GitHub",
        "info_support": "Support",
        "path_title": "📁  Install location",
        "path_label": "Where should we install the panel?",
        "path_browse": "Browse...",
        "path_hint": "Default: Documents\\Discord Bot Manager",
        "options_title": "⚙️  Options",
        "opt_desktop": "  Create desktop shortcut",
        "opt_startmenu": "  Create Start Menu shortcut",
        "opt_launch": "  Launch panel after install",
        "opt_delete_source": "  Delete source folder after install",
        "install_btn": "📥   Install",
        "installing": "Installing...",
        "done": "✅  Installation complete!",
        "done_msg": "Panel successfully installed:\n{path}",
        "done_hint": "You can start the panel from the shortcut.",
        "error_title": "Error",
        "error_path": "Please provide a valid path!",
        "error_exists": "This folder already exists and is not empty.\n\nOverwrite files?",
        "error_install": "Installation error:\n{error}",
        "error_winrar": "❌ You ran the installer from INSIDE the ZIP!\n\n"
                        "WinRAR only extracted one temporary file, the DBM folder is not next to it.\n\n"
                        "✅ Solution:\n"
                        "   1. Extract the ZIP first (right-click → Extract All)\n"
                        "   2. Run installer.pyw from the extracted folder.",
        "lang_btn": "🌐  Magyar",
        "open_folder": "📂  Open folder",
        "close_btn": "Close",
        "launching": "Launching panel...",
        "deleting": "Deleting source folder...",

        # Dependencies
        "deps_title": "📦  Dependencies",
        "deps_hint": "The following Python packages are required to run the panel.\n"
                     "You can install the missing ones with one click.",
        "deps_recheck": "🔍  Re-check",
        "deps_install_missing": "📥  Install missing",
        "deps_all_ok": "✅  All required packages installed!",
        "deps_missing_n": "❌  {count} package(s) missing — install them!",
        "deps_checking": "⏳  Checking packages...",
        "deps_installing": "⏳  Installation in progress...",
        "deps_install_done": "✅  Installation complete.",
        "deps_install_err": "❌  Error during installation.",
        "install_disabled_deps": "⚠️  Please install missing packages first!",
    },
}

GITHUB_USER = "slowik1kiwokr"
GITHUB_REPO = "Discord-Bot-Manager"
GITHUB_URL = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}"
SUPPORT_URL = f"{GITHUB_URL}/issues"
AUTHOR_NAME = "slowik1kiwokr"


# ============================================================
#  Segédfüggvények
# ============================================================
def log_debug(msg):
    """Egyszerű debug log a Temp mappába."""
    try:
        import tempfile, datetime
        p = os.path.join(tempfile.gettempdir(), "dbm_installer.log")
        with open(p, "a", encoding="utf-8") as f:
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            f.write(f"[{ts}] {msg}\n")
    except Exception:
        pass


def is_winrar_temp(path):
    """Igaz, ha a path egy WinRAR ideiglenes kibontási mappa."""
    p = path.lower()
    markers = ("rar$dia", "rar$", ".rartemp", "\\temp\\rar")
    return any(m in p for m in markers)


def source_dir():
    """A panel forrásmappája — .pyw-ből is működik, több helyen keres."""
    from pathlib import Path

    candidates = []

    # 1) sys.argv[0] — .pyw-nél is megbízható
    try:
        if sys.argv and sys.argv[0] and not sys.argv[0].startswith("-"):
            candidates.append(Path(sys.argv[0]).resolve().parent)
    except Exception as e:
        log_debug(f"argv[0] hiba: {e}")

    # 2) __file__
    try:
        candidates.append(Path(__file__).resolve().parent)
    except Exception as e:
        log_debug(f"__file__ hiba: {e}")

    # 3) cwd
    try:
        candidates.append(Path.cwd())
    except Exception:
        pass

    # 4) frozen exe
    if getattr(sys, "frozen", False):
        try:
            candidates.append(Path(sys.executable).resolve().parent)
        except Exception:
            pass

    # Egyediség
    seen = set()
    unique = []
    for c in candidates:
        s = str(c)
        if s not in seen:
            seen.add(s)
            unique.append(c)

    log_debug("=" * 60)
    log_debug("source_dir() keresés:")
    for u in unique:
        log_debug(f"  jelölt: {u}  (mappa: {u.is_dir()})")

    # Végigmegyünk a jelölteken
    for base in unique:
        if not base.is_dir():
            continue

        try:
            entries = list(base.iterdir())
        except Exception as e:
            log_debug(f"  olvasási hiba: {e}")
            continue

        log_debug(f"  tartalom: {[e.name for e in entries]}")

        # A) DBM közvetlenül
        for entry in entries:
            if entry.is_dir() and entry.name.lower() == "dbm":
                log_debug(f"  ✅ DBM: {entry}")
                return str(entry)

        # B) panel.pyw közvetlenül
        if (base / "panel.pyw").is_file():
            log_debug(f"  ✅ panel.pyw itt: {base}")
            return str(base)

        # C) 1 szint mélyebben: DBM vagy panel.pyw
        for entry in entries:
            if not entry.is_dir():
                continue
            if (entry / "panel.pyw").is_file():
                log_debug(f"  ✅ panel.pyw almappában: {entry}")
                return str(entry)
            try:
                for sub in entry.iterdir():
                    if sub.is_dir() and sub.name.lower() == "dbm":
                        log_debug(f"  ✅ DBM almappában: {sub}")
                        return str(sub)
            except Exception:
                pass

    # Fallback
    if unique:
        log_debug(f"  ⚠ Fallback: {unique[0]}")
        return str(unique[0])

    log_debug("  ❌ Semmi nem található")
    return "."


def shell_folder(csidl):
    """Windows speciális mappa (pl. Documents, Desktop)."""
    try:
        buf = ctypes.create_unicode_buffer(260)
        ctypes.windll.shell32.SHGetFolderPathW(None, csidl, None, 0, buf)
        return buf.value
    except Exception:
        return ""


def documents_dir():
    d = shell_folder(5)  # CSIDL_PERSONAL
    if d:
        return d
    return os.path.join(os.path.expanduser("~"), "Documents")


def desktop_dir():
    d = shell_folder(16)  # CSIDL_DESKTOPDIRECTORY
    if d:
        return d
    return os.path.join(os.path.expanduser("~"), "Desktop")


def startmenu_dir():
    d = shell_folder(23)  # CSIDL_COMMON_PROGRAMS
    if d:
        return d
    d = shell_folder(11)  # CSIDL_PROGRAMS (user)
    if d:
        return d
    return os.path.join(
        os.path.expanduser("~"),
        "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs"
    )


def default_install_path():
    return os.path.join(documents_dir(), "Discord Bot Manager")


def read_version(src):
    vt = os.path.join(src, "version.txt")
    if os.path.isfile(vt):
        try:
            with open(vt, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            pass
    vp = os.path.join(src, "version.py")
    if os.path.isfile(vp):
        try:
            with open(vp, "r", encoding="utf-8") as f:
                content = f.read()
            m = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
            if m:
                return m.group(1)
        except Exception:
            pass
    return "?"


def detect_default_lang():
    try:
        code = locale.getlocale()[0] or ""
    except Exception:
        code = ""
    if not code:
        try:
            code = locale.getdefaultlocale()[0] or ""
        except Exception:
            code = ""
    return "hu" if code.lower().startswith("hu") else "en"


def find_icon(target_dir):
    """Megkeresi a legjobb elérhető ikont a parancsikonhoz."""
    for name in ("icon.ico", "panel_icon.ico", "logo.ico"):
        p = os.path.join(target_dir, name)
        if os.path.isfile(p):
            return p
    return None


def create_shortcut(shortcut_path, target_dir, pythonw_exe):
    """Windows .lnk létrehozása PowerShell-lel (nem kell pywin32)."""
    panel_pyw = os.path.join(target_dir, "panel.pyw")
    if not os.path.isfile(panel_pyw):
        panel_pyw = os.path.join(target_dir, "panel.py")

    icon = find_icon(target_dir)

    ps_lines = [
        '$WshShell = New-Object -ComObject WScript.Shell',
        f'$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")',
        f'$Shortcut.TargetPath = "{pythonw_exe}"',
        f"$Shortcut.Arguments = '\"{panel_pyw}\"'",
        f'$Shortcut.WorkingDirectory = "{target_dir}"',
        '$Shortcut.Description = "Discord Bot Manager"',
    ]
    if icon:
        ps_lines.append(f'$Shortcut.IconLocation = "{icon}"')
    ps_lines.append('$Shortcut.Save()')

    ps_script = "; ".join(ps_lines)

    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            capture_output=True, timeout=20,
        )
        return True
    except Exception as e:
        print(f"[INSTALLER] Shortcut hiba: {e}")
        return False


def get_pythonw():
    """pythonw.exe útvonala (ha nincs, akkor python.exe)."""
    exe = sys.executable
    if exe.lower().endswith("python.exe"):
        candidate = exe[:-len("python.exe")] + "pythonw.exe"
        if os.path.isfile(candidate):
            return candidate
    return exe


def copy_panel_files(src, dst, log_cb=None):
    """A panel összes fájljának másolása."""
    log_debug(f"copy_panel_files: {src} → {dst}")

    if not os.path.isdir(src):
        log_debug(f"  HIBA: forrás nem létezik: {src}")
        raise FileNotFoundError(f"Forrásmappa nem található: {src}")

    skip = {"installer.pyw", "__pycache__", "update.zip", "update_extract",
            ".git", ".github", ".gitignore", ".idea", ".vscode",
            "venv", ".venv", "README.md", "README.txt"}

    try:
        items = [i for i in os.listdir(src) if i not in skip]
    except Exception as e:
        log_debug(f"  HIBA listázáskor: {e}")
        raise

    log_debug(f"  Másolandó elemek ({len(items)}): {items}")
    total = len(items)
    if total == 0:
        log_debug(f"  HIBA: nincs mit másolni!")
        raise RuntimeError("A forrásmappa üres!")

    for idx, item in enumerate(items, 1):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)

        try:
            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d, ignore_errors=True)
                shutil.copytree(s, d)
                log_debug(f"  [{idx}/{total}] Mappa: {item}")
            else:
                shutil.copy2(s, d)
                log_debug(f"  [{idx}/{total}] Fájl: {item}")
        except Exception as e:
            log_debug(f"  HIBA {item}: {e}")
            raise

        if log_cb:
            log_cb(item, idx / total)

    log_debug(f"  ✅ Másolás kész: {total} elem")
    return True


# ============================================================
#  Telepítő ablak
# ============================================================
class InstallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.src = source_dir()
        self.lang = detect_default_lang()
        self.version = read_version(self.src)
        self._install_running = False
        self._install_done = False
        self._target_path = ""
        self._deps_ok = False

        self.title("Discord Bot Manager — Installer")
        self.geometry("760x900")
        self.minsize(680, 700)
        self.resizable(False, True)
        self.configure(fg_color="#0d0f14")

        # Középre igazítás
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = 760, 900
        x = (sw - w) // 2
        y = max(20, (sh - h) // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

        self._build_ui()

    # ----------------------------------------------------------------
    #  UI felépítése
    # ----------------------------------------------------------------
    def _build_ui(self):
        # Header
        self.header = ctk.CTkFrame(self, fg_color="#0f1a3a", height=90, corner_radius=0)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        # Glow csík
        glow = ctk.CTkFrame(self.header, height=2, fg_color="#3b82f6", corner_radius=0)
        glow.pack(side="bottom", fill="x")

        # Bal: ikon + cím
        left = ctk.CTkFrame(self.header, fg_color="transparent")
        left.pack(side="left", padx=(24, 0), pady=14)

        # Ikon betöltése (icon.ico a forrás mappából)
        logo_loaded = False
        if PIL_OK:
            icon_path = os.path.join(self.src, "icon.ico")
            if os.path.isfile(icon_path):
                try:
                    ico = Image.open(icon_path)
                    best_size = max(ico.info.get("sizes", [(32, 32)]),
                                     key=lambda s: s[0] * s[1])
                    ico = Image.open(icon_path)
                    ico.size = best_size
                    ico.load()
                    pil_logo = ico.convert("RGBA")

                    target_h = 52
                    ratio = target_h / pil_logo.height
                    target_w = int(pil_logo.width * ratio)
                    self._header_logo = ctk.CTkImage(
                        light_image=pil_logo,
                        dark_image=pil_logo,
                        size=(target_w, target_h),
                    )
                    ctk.CTkLabel(left, image=self._header_logo, text="").pack(
                        side="left", padx=(0, 14)
                    )
                    logo_loaded = True
                except Exception as e:
                    print(f"[INSTALLER] Ikon betöltési hiba: {e}")

        if not logo_loaded:
            ctk.CTkLabel(left, text="🎯", font=("Segoe UI Emoji", 26),
                          text_color="#7dd3fc").pack(side="left", padx=(0, 12))

        title_col = ctk.CTkFrame(left, fg_color="transparent")
        title_col.pack(side="left")
        ctk.CTkLabel(title_col, text="Discord Bot Manager",
                      font=("Arial", 20, "bold"),
                      text_color="#7dd3fc", anchor="w").pack(anchor="w")
        ctk.CTkLabel(title_col, text=L[self.lang]["subtitle"],
                      font=("Arial", 11),
                      text_color="#5fc8ff", anchor="w").pack(anchor="w")

        # Jobb: nyelvváltó
        self.lang_btn = ctk.CTkButton(
            self.header, text=L[self.lang]["lang_btn"],
            fg_color="transparent", hover_color="#1e3a8a",
            border_width=1, border_color="#3b82f6",
            text_color="#7dd3fc",
            width=120, height=34, font=("Arial", 12, "bold"),
            command=self._toggle_lang,
        )
        self.lang_btn.pack(side="right", padx=24, pady=28)

        # ---- Görgethető tartalom ----
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=18, pady=14)

        # Üdvözlő
        self.welcome_lbl = ctk.CTkLabel(
            self.scroll, text=L[self.lang]["welcome"],
            font=("Arial", 22, "bold"), text_color="#ffffff", anchor="w"
        )
        self.welcome_lbl.pack(fill="x", pady=(4, 4))

        self.welcome_text_lbl = ctk.CTkLabel(
            self.scroll, text=L[self.lang]["welcome_text"],
            font=("Arial", 12), text_color="#8a8e98",
            anchor="w", justify="left", wraplength=660
        )
        self.welcome_text_lbl.pack(fill="x", pady=(0, 16))

        # Info szekció
        self._build_info_section()

        # Path szekció
        self._build_path_section()

        # Options szekció
        self._build_options_section()

        # Függőségek szekció
        self._build_dependencies_section()

        # Progress + log
        self.progress = ctk.CTkProgressBar(self.scroll, height=8,
                                             progress_color="#5865F2")
        self.progress.set(0)
        self.progress.pack(fill="x", pady=(18, 6))

        self.status_lbl = ctk.CTkLabel(
            self.scroll, text="", font=("Arial", 11),
            text_color="#8a8e98", anchor="w"
        )
        self.status_lbl.pack(fill="x", pady=(0, 6))

        self.log_box = ctk.CTkTextbox(
            self.scroll, height=100, font=("Consolas", 10),
            fg_color="#0a0c10", text_color="#8a8e98", wrap="none"
        )
        self.log_box.pack(fill="x", pady=(0, 12))
        self.log_box.insert("1.0", "• Készen áll a telepítésre.\n")
        self.log_box.configure(state="disabled")

        # Alsó gomb
        self.action_btn = ctk.CTkButton(
            self, text=L[self.lang]["install_btn"],
            fg_color="#27ae60", hover_color="#2ecc71",
            height=50, font=("Arial", 14, "bold"), corner_radius=10,
            command=self._on_action,
            state="disabled",
        )
        self.action_btn.pack(fill="x", padx=18, pady=(0, 16))

        # Induláskor automatikus ellenőrzés
        self.after(400, self._check_dependencies)

    def _build_info_section(self):
        card = ctk.CTkFrame(self.scroll, fg_color="#15202b",
                             corner_radius=10, border_width=1, border_color="#3498db")
        card.pack(fill="x", pady=6)

        ctk.CTkLabel(card, text=L[self.lang]["info_title"],
                      font=("Arial", 13, "bold"),
                      text_color="#3498db", anchor="w").pack(
            fill="x", padx=14, pady=(10, 6))

        rows = [
            (L[self.lang]["info_version"], self.version),
            (L[self.lang]["info_author"], AUTHOR_NAME),
            (L[self.lang]["info_github"], GITHUB_URL),
            (L[self.lang]["info_support"], SUPPORT_URL),
        ]
        for label, value in rows:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=2)
            ctk.CTkLabel(row, text=f"{label}:",
                          font=("Arial", 11, "bold"), text_color="#b8bcc6",
                          width=110, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=value,
                          font=("Consolas", 11), text_color="#7dd3fc",
                          anchor="w").pack(side="left")

        ctk.CTkFrame(card, height=8, fg_color="transparent").pack()

    def _build_path_section(self):
        card = ctk.CTkFrame(self.scroll, fg_color="#1e1a2b",
                             corner_radius=10, border_width=1, border_color="#9b59b6")
        card.pack(fill="x", pady=6)

        ctk.CTkLabel(card, text=L[self.lang]["path_title"],
                      font=("Arial", 13, "bold"),
                      text_color="#9b59b6", anchor="w").pack(
            fill="x", padx=14, pady=(10, 6))

        ctk.CTkLabel(card, text=L[self.lang]["path_label"],
                      font=("Arial", 11), text_color="#b8bcc6",
                      anchor="w").pack(fill="x", padx=14, pady=(0, 4))

        path_row = ctk.CTkFrame(card, fg_color="transparent")
        path_row.pack(fill="x", padx=14, pady=(0, 6))

        self.path_entry = ctk.CTkEntry(path_row, height=38, font=("Consolas", 11))
        self.path_entry.insert(0, default_install_path())
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))

        ctk.CTkButton(
            path_row, text=L[self.lang]["path_browse"],
            fg_color="#9b59b6", hover_color="#8e44ad",
            width=110, height=38, font=("Arial", 11),
            command=self._browse,
        ).pack(side="right")

        ctk.CTkLabel(card, text=L[self.lang]["path_hint"],
                      font=("Arial", 10), text_color="#7a8090",
                      anchor="w").pack(fill="x", padx=14, pady=(0, 12))

    def _build_options_section(self):
        card = ctk.CTkFrame(self.scroll, fg_color="#0f2318",
                             corner_radius=10, border_width=1, border_color="#27ae60")
        card.pack(fill="x", pady=6)

        ctk.CTkLabel(card, text=L[self.lang]["options_title"],
                      font=("Arial", 13, "bold"),
                      text_color="#27ae60", anchor="w").pack(
            fill="x", padx=14, pady=(10, 6))

        self.opt_desktop = ctk.BooleanVar(value=True)
        self.opt_startmenu = ctk.BooleanVar(value=False)
        self.opt_launch = ctk.BooleanVar(value=True)
        self.opt_delete_source = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(card, text=L[self.lang]["opt_desktop"],
                         variable=self.opt_desktop, font=("Arial", 12)).pack(
            anchor="w", padx=14, pady=4)
        ctk.CTkCheckBox(card, text=L[self.lang]["opt_startmenu"],
                         variable=self.opt_startmenu, font=("Arial", 12)).pack(
            anchor="w", padx=14, pady=4)
        ctk.CTkCheckBox(card, text=L[self.lang]["opt_launch"],
                         variable=self.opt_launch, font=("Arial", 12)).pack(
            anchor="w", padx=14, pady=4)
        ctk.CTkCheckBox(card, text=L[self.lang]["opt_delete_source"],
                         variable=self.opt_delete_source, font=("Arial", 12)).pack(
            anchor="w", padx=14, pady=(4, 12))

    # ----------------------------------------------------------------
    #  Függőség szekció
    # ----------------------------------------------------------------
    def _build_dependencies_section(self):
        card = ctk.CTkFrame(self.scroll, fg_color="#1a1520",
                             corner_radius=10, border_width=1, border_color="#e67e22")
        card.pack(fill="x", pady=6)

        ctk.CTkLabel(card, text=L[self.lang]["deps_title"],
                      font=("Arial", 13, "bold"),
                      text_color="#e67e22", anchor="w").pack(
            fill="x", padx=14, pady=(10, 4))

        ctk.CTkLabel(card, text=L[self.lang]["deps_hint"],
                      font=("Arial", 10), text_color="#8a8e98",
                      justify="left", anchor="w",
                      wraplength=640).pack(fill="x", padx=14, pady=(0, 8))

        # Lista konténer
        self._deps_list_frame = ctk.CTkFrame(card, fg_color="transparent")
        self._deps_list_frame.pack(fill="x", padx=14, pady=(0, 6))

        # Státusz
        self._deps_status = ctk.CTkLabel(
            card, text=L[self.lang]["deps_checking"],
            font=("Arial", 11, "bold"), text_color="#8a8e98", anchor="w"
        )
        self._deps_status.pack(fill="x", padx=14, pady=(0, 6))

        # Gombok
        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=14, pady=(0, 12))

        self._deps_recheck_btn = ctk.CTkButton(
            btn_row, text=L[self.lang]["deps_recheck"],
            fg_color="#3498db", hover_color="#5dade2",
            width=160, height=36, font=("Arial", 11, "bold"),
            command=self._check_dependencies,
        )
        self._deps_recheck_btn.pack(side="left", padx=(0, 6))

        self._deps_install_btn = ctk.CTkButton(
            btn_row, text=L[self.lang]["deps_install_missing"],
            fg_color="#e67e22", hover_color="#d35400",
            width=200, height=36, font=("Arial", 11, "bold"),
            command=self._install_dependencies,
        )
        self._deps_install_btn.pack(side="left", padx=6)

        # Kezdeti állapot
        self._render_deps_list([])

    # ----------------------------------------------------------------
    #  Ellenőrzés
    # ----------------------------------------------------------------
    def _check_dependencies(self):
        import importlib.util

        def _do():
            self._deps_status.configure(
                text=L[self.lang]["deps_checking"], text_color="#8a8e98")
            self.update_idletasks()

            results = []
            missing = 0
            for pip_name, import_name, desc in REQUIRED_PACKAGES:
                try:
                    spec = importlib.util.find_spec(import_name)
                    installed = spec is not None
                except Exception:
                    installed = False

                if not installed:
                    missing += 1
                results.append((pip_name, import_name, desc, installed))

            self._render_deps_list(results)

            if missing == 0:
                self._deps_ok = True
                self._deps_status.configure(
                    text=L[self.lang]["deps_all_ok"], text_color="#2ecc71")
                self.action_btn.configure(state="normal")
                self._deps_install_btn.configure(state="disabled")
            else:
                self._deps_ok = False
                self._deps_status.configure(
                    text=L[self.lang]["deps_missing_n"].format(count=missing),
                    text_color="#e74c3c")
                self.action_btn.configure(state="disabled")
                self._deps_install_btn.configure(state="normal")

        self.after(0, _do)

    def _render_deps_list(self, results):
        for w in self._deps_list_frame.winfo_children():
            w.destroy()

        if not results:
            ctk.CTkLabel(self._deps_list_frame,
                          text="...", font=("Arial", 11),
                          text_color="#666").pack(anchor="w", pady=2)
            return

        for pip_name, import_name, desc, installed in results:
            row = ctk.CTkFrame(self._deps_list_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)

            icon = "✅" if installed else "❌"
            color = "#2ecc71" if installed else "#e74c3c"

            ctk.CTkLabel(row, text=icon, font=("Arial", 14),
                          width=26).pack(side="left")
            ctk.CTkLabel(row, text=pip_name,
                          font=("Consolas", 11, "bold"),
                          text_color=color, width=130,
                          anchor="w").pack(side="left")
            ctk.CTkLabel(row, text="—  " + desc,
                          font=("Arial", 10), text_color="#8a8e98",
                          anchor="w").pack(side="left")

    # ----------------------------------------------------------------
    #  Függőség telepítés
    # ----------------------------------------------------------------
    def _install_dependencies(self):
        import importlib.util

        missing = []
        for pip_name, import_name, _ in REQUIRED_PACKAGES:
            try:
                if importlib.util.find_spec(import_name) is None:
                    missing.append(pip_name)
            except Exception:
                missing.append(pip_name)

        if not missing:
            self._check_dependencies()
            return

        # Gombok letiltása
        self._deps_install_btn.configure(
            state="disabled", text=L[self.lang]["deps_installing"])
        self._deps_recheck_btn.configure(state="disabled")
        self.action_btn.configure(state="disabled")

        self._deps_status.configure(
            text=L[self.lang]["deps_installing"], text_color="#f39c12")

        self._log(f"\n▶ Függőségek telepítése: {len(missing)} csomag")
        for m in missing:
            self._log(f"  • {m}")

        threading.Thread(target=self._deps_install_worker,
                          args=(missing,), daemon=True).start()

    def _deps_install_worker(self, packages):
        total = len(packages)
        failed = []
        try:
            for idx, pkg in enumerate(packages, 1):
                self._log(f"\n[{idx}/{total}] pip install {pkg}")
                self._deps_status.configure(
                    text=f"⏳  [{idx}/{total}]  {pkg}...")

                cmd = [sys.executable, "-m", "pip", "install", "--upgrade", pkg]
                try:
                    proc = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        bufsize=1,
                        encoding="utf-8",
                        errors="replace",
                        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                    )
                    for line in iter(proc.stdout.readline, ""):
                        line = line.rstrip()
                        if line:
                            self._log("    " + line)
                    proc.wait()

                    if proc.returncode != 0:
                        failed.append(pkg)
                        self._log(f"  ❌ {pkg} — hibakód: {proc.returncode}")
                except Exception as e:
                    failed.append(pkg)
                    self._log(f"  ❌ {pkg}: {e}")

            # Újraellenőrzés
            self.after(200, self._after_deps_install, failed)

        except Exception as e:
            self._log(f"\n❌ Függőség telepítési hiba: {e}")
            self.after(0, lambda: self._deps_status.configure(
                text=L[self.lang]["deps_install_err"], text_color="#e74c3c"))
            self.after(0, lambda: (
                self._deps_install_btn.configure(
                    state="normal", text=L[self.lang]["deps_install_missing"]),
                self._deps_recheck_btn.configure(state="normal"),
            ))

    def _after_deps_install(self, failed):
        self._deps_install_btn.configure(
            text=L[self.lang]["deps_install_missing"])
        self._deps_recheck_btn.configure(state="normal")

        if failed:
            self._log(f"\n⚠️  Sikertelen: {', '.join(failed)}")
        else:
            self._log(f"\n✅  {L[self.lang]['deps_install_done']}")

        # Automatikus újraellenőrzés
        self._check_dependencies()

    # ----------------------------------------------------------------
    #  Események
    # ----------------------------------------------------------------
    def _toggle_lang(self):
        self.lang = "en" if self.lang == "hu" else "hu"
        # Újraépítjük az ablakot
        for child in self.winfo_children():
            child.destroy()
        self._deps_ok = False
        self._build_ui()

    def _browse(self):
        folder = filedialog.askdirectory(
            title="Válassz célmappát" if self.lang == "hu"
                  else "Choose target folder"
        )
        if folder:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder)

    def _log(self, text):
        def _do():
            try:
                self.log_box.configure(state="normal")
                self.log_box.insert("end", text + "\n")
                self.log_box.see("end")
                self.log_box.configure(state="disabled")
            except Exception:
                pass
        self.after(0, _do)

    def _set_status(self, text, progress=None):
        def _do():
            try:
                self.status_lbl.configure(text=text)
                if progress is not None:
                    self.progress.set(progress)
            except Exception:
                pass
        self.after(0, _do)

    def _on_action(self):
        if self._install_done:
            self._close_or_launch()
            return
        if self._install_running:
            return
        self._start_install()

    def _start_install(self):
        # Függőségek ellenőrzése
        if not getattr(self, "_deps_ok", False):
            messagebox.showwarning(
                L[self.lang]["error_title"],
                L[self.lang]["install_disabled_deps"],
            )
            return

        # WinRAR temp figyelmeztetés
        if is_winrar_temp(self.src):
            messagebox.showerror(
                L[self.lang]["error_title"],
                L[self.lang]["error_winrar"],
            )
            return

        target = self.path_entry.get().strip()
        if not target:
            messagebox.showerror(L[self.lang]["error_title"],
                                   L[self.lang]["error_path"])
            return

        # Ha létezik és nem üres → kérdés
        if os.path.isdir(target) and os.listdir(target):
            if not messagebox.askyesno(L[self.lang]["error_title"],
                                         L[self.lang]["error_exists"]):
                return

        self._target_path = target
        self._install_running = True
        self.action_btn.configure(state="disabled", text=L[self.lang]["installing"])
        self.status_lbl.configure(text=L[self.lang]["installing"])
        self.progress.set(0)

        threading.Thread(target=self._install_worker,
                          args=(target,), daemon=True).start()

    def _install_worker(self, target):
        try:
            log_debug("=" * 60)
            log_debug(f"TELEPÍTÉS INDUL")
            log_debug(f"  src: {self.src}")
            log_debug(f"  dst: {target}")
            log_debug(f"  src létezik: {os.path.isdir(self.src)}")
            if os.path.isdir(self.src):
                log_debug(f"  src tartalom: {os.listdir(self.src)}")

            self._log(f"\n▶ Forrás: {self.src}")
            self._log(f"▶ Cél: {target}")
            self._set_status(L[self.lang]["installing"], 0.05)

            os.makedirs(target, exist_ok=True)
            self._log("  • Célmappa létrehozva")

            # 1. Fájlok másolása
            def log_cb(item, pct):
                self._log(f"  • {item}")
                self._set_status(L[self.lang]["installing"], 0.05 + pct * 0.7)

            copy_panel_files(self.src, target, log_cb)
            self._set_status(L[self.lang]["installing"], 0.8)

            # 2. Parancsikonok
            pythonw = get_pythonw()
            self._log(f"\n▶ Python: {pythonw}")

            if self.opt_desktop.get():
                shortcut = os.path.join(desktop_dir(), "Discord Bot Manager.lnk")
                ok = create_shortcut(shortcut, target, pythonw)
                self._log(f"  • Asztali parancsikon: {'OK' if ok else 'HIBA'}")
                self._set_status(L[self.lang]["installing"], 0.85)

            if self.opt_startmenu.get():
                sm = os.path.join(startmenu_dir(), "Discord Bot Manager.lnk")
                os.makedirs(startmenu_dir(), exist_ok=True)
                ok = create_shortcut(sm, target, pythonw)
                self._log(f"  • Start menü: {'OK' if ok else 'HIBA'}")
                self._set_status(L[self.lang]["installing"], 0.9)

            self._set_status(L[self.lang]["installing"], 1.0)
            self._log(f"\n✅ {L[self.lang]['done']}")
            self._log(f"  {target}")

            # Forrásmappa törlése
            if self.opt_delete_source.get():
                src_abs = os.path.abspath(self.src)
                tgt_abs = os.path.abspath(self._target_path)

                if src_abs != tgt_abs:
                    self._log(f"\n▶ Forrásmappa törlése: {src_abs}")
                    self._set_status(L[self.lang]["deleting"], 0.97)
                    self._schedule_source_delete(src_abs)
                else:
                    self._log("  • A forrás és a cél ugyanaz — kihagyva")

            self._install_done = True
            self.after(0, self._on_install_done)

        except Exception as e:
            self._log(f"\n❌ {e}")
            self.after(0, lambda: messagebox.showerror(
                L[self.lang]["error_title"],
                L[self.lang]["error_install"].format(error=e)
            ))
            self._install_running = False
            self.after(0, lambda: self.action_btn.configure(
                state="normal", text=L[self.lang]["install_btn"]))

    def _on_install_done(self):
        self._install_running = False

        messagebox.showinfo(
            L[self.lang]["done"],
            L[self.lang]["done_msg"].format(path=self._target_path)
            + "\n\n" + L[self.lang]["done_hint"],
        )

        self.action_btn.configure(
            text=L[self.lang]["open_folder"],
            fg_color="#3498db", hover_color="#5dade2",
            command=self._open_target_folder,
        )

        if self.opt_launch.get():
            self.after(400, self._close_or_launch)
        else:
            self.after(400, self._offer_close)

    def _offer_close(self):
        self.action_btn.configure(
            text=L[self.lang]["close_btn"],
            fg_color="#555555", hover_color="#666666",
            command=self.destroy,
        )

    def _open_target_folder(self):
        try:
            os.startfile(self._target_path)
        except Exception:
            pass

    def _close_or_launch(self):
        """Bezárja a telepítőt és elindítja a panelt."""
        try:
            panel_pyw = os.path.join(self._target_path, "panel.pyw")
            if not os.path.isfile(panel_pyw):
                panel_pyw = os.path.join(self._target_path, "panel.py")

            pythonw = get_pythonw()
            subprocess.Popen(
                [pythonw, panel_pyw],
                cwd=self._target_path,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        except Exception as e:
            messagebox.showerror(L[self.lang]["error_title"], str(e))

        self.destroy()

    def _schedule_source_delete(self, source_path):
        """Batch scriptet indít, ami a telepítő bezárása után törli a forrást."""
        try:
            import tempfile

            bat_path = os.path.join(
                tempfile.gettempdir(),
                "dbm_cleanup.bat"
            )

            bat_content = (
                "@echo off\n"
                "timeout /t 2 /nobreak >nul\n"
                f'rmdir /s /q "{source_path}"\n'
                'del "%~f0"\n'
            )

            with open(bat_path, "w", encoding="ascii") as f:
                f.write(bat_content)

            subprocess.Popen(
                ["cmd", "/c", bat_path],
                creationflags=subprocess.CREATE_NO_WINDOW
                              if hasattr(subprocess, "CREATE_NO_WINDOW") else 0,
                shell=False,
            )
            self._log(f"  • Törlés ütemezve: {source_path}")

        except Exception as e:
            self._log(f"  • Törlés ütemezési hiba: {e}")


# ============================================================
#  Indítás
# ============================================================
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = InstallerApp()
    app.mainloop()