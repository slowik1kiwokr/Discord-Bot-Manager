import os
import json
import shutil
from tkinter import filedialog, messagebox, simpledialog, ttk

import customtkinter as ctk

import modules.config as config
from modules.languages import LANGUAGES


COMMANDER_FILE_NAME = "commander_commands.json"
EXTENSIONS_FILE_NAME = "bot_extensions.txt"


# =====================================================================
#  PARANCS SABLONOK
# =====================================================================
COMMAND_TEMPLATES = {
    "💬  Egyszerű szöveges üzenet": {
        "type": "message",
        "description": "Egyszerű szöveges válasz",
        "content": "👋 Szia! Ez egy egyedi parancs válasza.",
        "embed": {"title": "", "description": "", "color": "#5865F2",
                   "footer": "", "thumbnail": "", "fields": []},
        "ephemeral": False,
    },
    "🎉  Üdvözlő üzenet": {
        "type": "message",
        "description": "Új tagok üdvözlése",
        "content": "🎉 Üdv a szerveren! Jó szórakozást kívánunk!",
        "embed": {"title": "", "description": "", "color": "#5865F2",
                   "footer": "", "thumbnail": "", "fields": []},
        "ephemeral": False,
    },
    "📢  Bejelentés (szöveg)": {
        "type": "message",
        "description": "Fontos bejelentés mindenkinek",
        "content": "📢 **FIGYELEM!**\n\nHamarosan karbantartás lesz a szerveren.",
        "embed": {"title": "", "description": "", "color": "#5865F2",
                   "footer": "", "thumbnail": "", "fields": []},
        "ephemeral": False,
    },
    "📌  Egyszerű embed": {
        "type": "embed",
        "description": "Szép embed üzenet",
        "content": "",
        "embed": {
            "title": "📌 Cím",
            "description": "Ez egy egyszerű embed üzenet. Ide jön a részletes szöveg.",
            "color": "#5865F2",
            "footer": "Bot által generálva",
            "thumbnail": "",
            "fields": [],
        },
        "ephemeral": False,
    },
    "❌  Hiba embed (piros)": {
        "type": "embed",
        "description": "Hibaüzenet formázva",
        "content": "",
        "embed": {
            "title": "❌ Hiba történt",
            "description": "Valami hiba történt. Kérlek próbáld újra később.",
            "color": "#e74c3c",
            "footer": "Hiba kód: 500",
            "thumbnail": "",
            "fields": [],
        },
        "ephemeral": True,
    },
    "✅  Siker embed (zöld)": {
        "type": "embed",
        "description": "Sikeres művelet visszajelzés",
        "content": "",
        "embed": {
            "title": "✅ Siker!",
            "description": "A művelet sikeresen végrehajtva!",
            "color": "#2ecc71",
            "footer": "",
            "thumbnail": "",
            "fields": [],
        },
        "ephemeral": True,
    },
    "⚠️  Figyelmeztetés (sárga)": {
        "type": "embed",
        "description": "Figyelmeztető üzenet",
        "content": "",
        "embed": {
            "title": "⚠️ Figyelem!",
            "description": "Ez egy figyelmeztetés. Kérlek olvasd el figyelmesen!",
            "color": "#f39c12",
            "footer": "",
            "thumbnail": "",
            "fields": [],
        },
        "ephemeral": False,
    },
    "❓  Segítség menü (több mezővel)": {
        "type": "embed",
        "description": "Több mezős segítség panel",
        "content": "",
        "embed": {
            "title": "❓ Segítség",
            "description": "Az elérhető parancsok listája:",
            "color": "#3498db",
            "footer": "További info: /help",
            "thumbnail": "",
            "fields": [
                {"name": "🎮 Játék", "value": "/játék - Játék indítása", "inline": False},
                {"name": "🎵 Zene", "value": "/play - Zene lejátszása", "inline": False},
                {"name": "⚙️ Beállítások", "value": "/config - Bot beállítások", "inline": False},
            ],
        },
        "ephemeral": False,
    },
    "📜  Szerver szabályok": {
        "type": "embed",
        "description": "Szerver szabályok listája",
        "content": "",
        "embed": {
            "title": "📜 Szerver Szabályok",
            "description": "Kérlek olvasd el figyelmesen a szabályokat!",
            "color": "#9b59b6",
            "footer": "Az utolsó frissítés: 2025",
            "thumbnail": "",
            "fields": [
                {"name": "1️⃣ Tiszteld a többieket", "value": "Légy kedves mindenkivel!", "inline": False},
                {"name": "2️⃣ Ne spam-elj", "value": "Tilos a spam és a reklám.", "inline": False},
                {"name": "3️⃣ NSFW tartalom tilos", "value": "Csak családbarát tartalom.", "inline": False},
                {"name": "4️⃣ Hallgass a moderátorokra", "value": "A döntéseik véglegesek.", "inline": False},
            ],
        },
        "ephemeral": False,
    },
    "📊  Információs embed": {
        "type": "embed",
        "description": "Szerver információk",
        "content": "",
        "embed": {
            "title": "📊 Szerver Információk",
            "description": "Minden, amit a szerverről tudni érdemes.",
            "color": "#3498db",
            "footer": "Kösz hogy itt vagy!",
            "thumbnail": "",
            "fields": [
                {"name": "👑 Tulajdonos", "value": "@tulajdonos", "inline": True},
                {"name": "👥 Tagok", "value": "100+", "inline": True},
                {"name": "📅 Létrehozva", "value": "2024", "inline": True},
            ],
        },
        "ephemeral": False,
    },
    "🎁  Giveaway bejelentés": {
        "type": "embed",
        "description": "Nyereményjáték bejelentés",
        "content": "",
        "embed": {
            "title": "🎁 NYEREMÉNYJÁTÉK!",
            "description": "Reagálj 🎉-tal a részvételhez!",
            "color": "#e91e63",
            "footer": "Sok szerencsét!",
            "thumbnail": "",
            "fields": [
                {"name": "🎁 Nyeremény", "value": "Nitro Classic", "inline": True},
                {"name": "⏰ Lejárat", "value": "24 óra múlva", "inline": True},
                {"name": "📋 Feltétel", "value": "Nincs", "inline": True},
            ],
        },
        "ephemeral": False,
    },
    "🎫  Ticket nyitás": {
        "type": "embed",
        "description": "Ticket rendszer nyitás",
        "content": "",
        "embed": {
            "title": "🎫 Ticket Rendszer",
            "description": "Kattints az alábbi reakcióra, hogy ticketet nyiss.",
            "color": "#16a085",
            "footer": "Csak vészhelyzetben használd!",
            "thumbnail": "",
            "fields": [
                {"name": "📩 Segítség", "value": "Reagálj 📩-tal", "inline": False},
                {"name": "🐛 Bug jelentés", "value": "Reagálj 🐛-tal", "inline": False},
                {"name": "❓ Egyéb", "value": "Reagálj ❓-tal", "inline": False},
            ],
        },
        "ephemeral": False,
    },
    "📅  Esemény bejelentés": {
        "type": "embed",
        "description": "Esemény részletei",
        "content": "",
        "embed": {
            "title": "📅 Esemény hamarosan!",
            "description": "Ne maradj le a közelgő eseményről!",
            "color": "#f39c12",
            "footer": "Jelentkezz időben!",
            "thumbnail": "",
            "fields": [
                {"name": "🎮 Esemény", "value": "Minecraft verseny", "inline": True},
                {"name": "🕐 Időpont", "value": "Szombat 18:00", "inline": True},
                {"name": "🏆 Nyeremény", "value": "Discord Nitro", "inline": True},
            ],
        },
        "ephemeral": False,
    },
    "🤖  Bot info embed": {
        "type": "embed",
        "description": "Bot információk",
        "content": "",
        "embed": {
            "title": "🤖 Bot Információk",
            "description": "A botról minden fontos adat.",
            "color": "#5865F2",
            "footer": "Kösz hogy használod!",
            "thumbnail": "",
            "fields": [
                {"name": "📛 Név", "value": "Main Bot", "inline": True},
                {"name": "🔢 Verzió", "value": "1.0.0", "inline": True},
                {"name": "📡 Szerverek", "value": "5", "inline": True},
            ],
        },
        "ephemeral": False,
    },
    "🎵  Zene parancs lista": {
        "type": "embed",
        "description": "Zene bot parancsok",
        "content": "",
        "embed": {
            "title": "🎵 Zene Parancsok",
            "description": "Az összes elérhető zenei parancs.",
            "color": "#e91e63",
            "footer": "",
            "thumbnail": "",
            "fields": [
                {"name": "▶️ /play", "value": "Zene indítása", "inline": False},
                {"name": "⏸️ /pause", "value": "Zene szüneteltetése", "inline": False},
                {"name": "⏭️ /skip", "value": "Következő dal", "inline": False},
                {"name": "🔊 /volume", "value": "Hangerő állítás", "inline": False},
            ],
        },
        "ephemeral": False,
    },
    "🔒  Moderáció embed": {
        "type": "embed",
        "description": "Moderációs intézkedés",
        "content": "",
        "embed": {
            "title": "🔒 Felhasználó némítva",
            "description": "A felhasználó némítva lett.",
            "color": "#c0392b",
            "footer": "Moderátor: @mod",
            "thumbnail": "",
            "fields": [
                {"name": "👤 Felhasználó", "value": "@user", "inline": True},
                {"name": "⏰ Időtartam", "value": "10 perc", "inline": True},
                {"name": "📝 Indok", "value": "Spam", "inline": False},
            ],
        },
        "ephemeral": False,
    },
    "🎨  Színes értesítő": {
        "type": "embed",
        "description": "Színes értesítés mindenkinek",
        "content": "",
        "embed": {
            "title": "🔔 Értesítés",
            "description": "Ez egy fontos értesítés, amit mindenkinek látnia kell.",
            "color": "#f39c12",
            "footer": "Automatikus értesítés",
            "thumbnail": "",
            "fields": [],
        },
        "ephemeral": False,
    },
    "💜  Egyedi szín": {
        "type": "embed",
        "description": "Saját színű embed",
        "content": "",
        "embed": {
            "title": "💜 Egyedi cím",
            "description": "Ide jön a szöveg.",
            "color": "#9b59b6",
            "footer": "",
            "thumbnail": "",
            "fields": [],
        },
        "ephemeral": False,
    },
    "🖼️  Képes embed": {
        "type": "embed",
        "description": "Embed thumbnail képpel",
        "content": "",
        "embed": {
            "title": "🖼️ Képes embed",
            "description": "Ez egy embed, amihez kép tartozik a jobb felső sarokban.",
            "color": "#3498db",
            "footer": "",
            "thumbnail": "https://via.placeholder.com/150",
            "fields": [],
        },
        "ephemeral": False,
    },
    "🔗  Link gyűjtemény": {
        "type": "embed",
        "description": "Hasznos linkek listája",
        "content": "",
        "embed": {
            "title": "🔗 Hasznos Linkek",
            "description": "Az összes fontos link egy helyen.",
            "color": "#3498db",
            "footer": "",
            "thumbnail": "",
            "fields": [
                {"name": "🌐 Weboldal", "value": "[Katt ide](https://example.com)", "inline": False},
                {"name": "📱 Discord", "value": "[Csatlakozz](https://discord.gg/example)", "inline": False},
                {"name": "📺 YouTube", "value": "[Feliratkozás](https://youtube.com/example)", "inline": False},
            ],
        },
        "ephemeral": False,
    },
}


class WindowCommanderMixin:
    """Commander & Fájlkezelő ablak."""

    # ==================================================================
    #  Segéd metódusok
    # ==================================================================
    def _bot_dir(self):
        bot = self.bots.get(self.active_bot_key, {})
        script_path = bot.get("path", "")
        if not script_path:
            return None
        return os.path.dirname(script_path)

    def _commander_config_path(self):
        d = self._bot_dir()
        return os.path.join(d, COMMANDER_FILE_NAME) if d else None

    def _extensions_file_path(self):
        d = self._bot_dir()
        return os.path.join(d, EXTENSIONS_FILE_NAME) if d else None

    # ==================================================================
    #  FŐ ABLAK
    # ==================================================================
    def open_commander_window(self):
        bot_dir = self._bot_dir()
        if not bot_dir:
            messagebox.showwarning(
                "Figyelem",
                "Előbb tallózd be a bot fő .py fájlját a fő panelen!"
            )
            return

        self._current_edited_file = None
        self._extensions = self._load_extensions()

        win = ctk.CTkToplevel(self)
        win.title("⚡ Commander & Fájlkezelő")
        win.geometry("1100x740")
        win.minsize(900, 560)
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 1100) // 2
        y = (win.winfo_screenheight() - 740) // 2
        win.geometry(f"1100x740+{x}+{y}")

        # Fejléc
        header = ctk.CTkFrame(win, fg_color="#f39c12", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text="⚡  Commander & Fájlkezelő",
            font=("Arial", 18, "bold"), text_color="white"
        ).pack(side="left", padx=24, pady=16)
        ctk.CTkLabel(
            header, text=f"📁 {bot_dir}",
            font=("Consolas", 10), text_color="#ffe0b0"
        ).pack(side="right", padx=20)

        # Fő terület
        main = ctk.CTkFrame(win, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # ============================================================
        #  BAL: fájlfa
        # ============================================================
        left = ctk.CTkFrame(main, width=300)
        left.pack(side="left", fill="y", padx=(0, 8))
        left.pack_propagate(False)

        ctk.CTkLabel(left, text="📁 Bot mappa",
                      font=("Arial", 13, "bold")).pack(pady=(8, 4))

        tree_frame = ctk.CTkFrame(left, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=4, pady=4)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Treeview",
                         background="#1e2129", foreground="white",
                         fieldbackground="#1e2129",
                         borderwidth=0, rowheight=26)
        style.map("Treeview", background=[("selected", "#5865F2")])

        self._tree = ttk.Treeview(tree_frame, show="tree", selectmode="browse")
        self._tree.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self._tree.yview)
        sb.pack(side="right", fill="y")
        self._tree.configure(yscrollcommand=sb.set)
        self._tree.bind("<<TreeviewSelect>>", lambda e: self._on_tree_select(win))

        # Fájl műveletek
        btns1 = ctk.CTkFrame(left, fg_color="transparent")
        btns1.pack(fill="x", padx=4, pady=(0, 4))
        ctk.CTkButton(btns1, text="➕ Fájl", height=28,
                       fg_color="#27ae60", hover_color="#2ecc71",
                       command=lambda: self._new_file(win)
                       ).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(btns1, text="📁 Mappa", height=28,
                       fg_color="#3498db", hover_color="#5dade2",
                       command=lambda: self._new_folder(win)
                       ).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(btns1, text="🔄", width=36, height=28,
                       fg_color="#7f8c8d", hover_color="#95a5a6",
                       command=lambda: self._refresh_tree(win)
                       ).pack(side="left", padx=2)

        btns2 = ctk.CTkFrame(left, fg_color="transparent")
        btns2.pack(fill="x", padx=4, pady=(0, 6))
        ctk.CTkButton(btns2, text="✏️ Átnevez", height=28,
                       fg_color="#9b59b6", hover_color="#8e44ad",
                       command=lambda: self._rename_item(win)
                       ).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(btns2, text="🗑️ Törlés", height=28,
                       fg_color="#c0392b", hover_color="#e74c3c",
                       command=lambda: self._delete_item(win)
                       ).pack(side="left", padx=2, expand=True, fill="x")

        # ============================================================
        #  JOBB: tabview
        # ============================================================
        right = ctk.CTkFrame(main, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True)

        tabs = ctk.CTkTabview(right)
        tabs.pack(fill="both", expand=True)

        tab_editor = tabs.add("📄 Szerkesztő")
        tab_cmd = tabs.add("⚡ Commander")
        tab_ext = tabs.add("🔌 Extension")

        # --- Editor tab ---
        self._editor_label = ctk.CTkLabel(
            tab_editor, text="Válassz fájlt a bal oldalról",
            font=("Arial", 12, "bold"), anchor="w",
        )
        self._editor_label.pack(fill="x", padx=8, pady=(8, 4))

        self._editor_box = ctk.CTkTextbox(
            tab_editor, font=("Consolas", 12), wrap="none"
        )
        self._editor_box.pack(fill="both", expand=True, padx=8, pady=4)

        editor_btns = ctk.CTkFrame(tab_editor, fg_color="transparent")
        editor_btns.pack(fill="x", padx=8, pady=(4, 8))

        self._editor_status = ctk.CTkLabel(
            editor_btns, text="", font=("Arial", 10), text_color="#8a8e98"
        )
        self._editor_status.pack(side="left", padx=4)

        ctk.CTkButton(editor_btns, text="💾  Mentés",
                       fg_color="#27ae60", hover_color="#2ecc71",
                       width=120, height=34,
                       command=lambda: self._save_editor(win)
                       ).pack(side="right", padx=4)

        # --- Commander tab ---
        ctk.CTkLabel(tab_cmd, text="Egyedi parancsok (commander_commands.json)",
                      font=("Arial", 12, "bold")).pack(anchor="w", padx=8, pady=(8, 4))

        self._cmd_list = ctk.CTkScrollableFrame(tab_cmd, fg_color="#1e2129")
        self._cmd_list.pack(fill="both", expand=True, padx=8, pady=4)

        cmd_btns = ctk.CTkFrame(tab_cmd, fg_color="transparent")
        cmd_btns.pack(fill="x", padx=8, pady=(4, 8))

        ctk.CTkButton(cmd_btns, text="➕ Új parancs",
                       fg_color="#27ae60", hover_color="#2ecc71", width=150,
                       command=self._new_command
                       ).pack(side="left", padx=4)
        ctk.CTkButton(cmd_btns, text="🔄 Frissítés",
                       fg_color="#3498db", hover_color="#5dade2", width=120,
                       command=self._refresh_command_list
                       ).pack(side="left", padx=4)

        # --- Extension tab ---
        ctk.CTkLabel(tab_ext, text="Automatikusan betöltött extension-ök",
                      font=("Arial", 12, "bold")).pack(anchor="w", padx=8, pady=(8, 4))

        ctk.CTkLabel(
            tab_ext,
            text="A bot indulásakor a panel_integrity.py betölti az itt listázott\n"
                 "extension-öket a bot_extensions.txt fájlból.",
            font=("Arial", 11), text_color="#8a8e98", justify="left",
        ).pack(anchor="w", padx=8, pady=(0, 8))

        self._ext_list = ctk.CTkScrollableFrame(tab_ext, fg_color="#1e2129")
        self._ext_list.pack(fill="both", expand=True, padx=8, pady=4)

        ext_btns = ctk.CTkFrame(tab_ext, fg_color="transparent")
        ext_btns.pack(fill="x", padx=8, pady=(4, 8))

        ctk.CTkButton(ext_btns, text="➕ Hozzáadás",
                       fg_color="#27ae60", hover_color="#2ecc71", width=140,
                       command=lambda: self._add_extension(win)
                       ).pack(side="left", padx=4)
        ctk.CTkButton(ext_btns, text="💾 Mentés",
                       fg_color="#3498db", hover_color="#5dade2", width=120,
                       command=lambda: self._save_extensions(win)
                       ).pack(side="left", padx=4)

        # Inicializálás
        self._refresh_tree(win)
        self._refresh_command_list()
        self._refresh_extension_list()

    # ==================================================================
    #  FÁJLFA
    # ==================================================================
    def _refresh_tree(self, win):
        try:
            for item in self._tree.get_children():
                self._tree.delete(item)
        except Exception:
            pass

        bot_dir = self._bot_dir()
        if not bot_dir:
            return

        ignore_dirs = {
            "__pycache__", ".git", "data", "logs", "backups",
            ".venv", "venv", "env", "node_modules", ".idea", ".vscode",
        }
        ignore_exts = {".pyc", ".pyo", ".pyd", ".log", ".tmp"}

        def add_items(parent, path, depth=0):
            if depth > 6:
                return
            try:
                items = sorted(os.listdir(path))
            except OSError:
                return
            for name in items:
                if name.startswith("."):
                    continue
                full = os.path.join(path, name)
                is_dir = os.path.isdir(full)
                if is_dir and name in ignore_dirs:
                    continue
                if not is_dir and any(name.endswith(e) for e in ignore_exts):
                    continue
                icon = "📁" if is_dir else "📄"
                node = self._tree.insert(
                    parent, "end", text=f"{icon} {name}",
                    values=[full], open=(depth == 0)
                )
                if is_dir:
                    add_items(node, full, depth + 1)

        add_items("", bot_dir)

    def _on_tree_select(self, win):
        sel = self._tree.selection()
        if not sel:
            return
        values = self._tree.item(sel[0], "values")
        if not values:
            return
        path = values[0]
        if not os.path.isfile(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            messagebox.showwarning("Figyelem",
                                    "Ez egy bináris fájl, nem lehet megnyitni.",
                                    parent=win)
            return
        except OSError as e:
            messagebox.showerror("Hiba", str(e), parent=win)
            return
        self._current_edited_file = path
        self._editor_label.configure(text=f"📄 {os.path.basename(path)}")
        self._editor_box.delete("1.0", "end")
        self._editor_box.insert("1.0", content)
        self._editor_status.configure(text="")

    def _save_editor(self, win):
        path = getattr(self, "_current_edited_file", None)
        if not path:
            messagebox.showwarning("Figyelem", "Nincs megnyitott fájl!", parent=win)
            return
        content = self._editor_box.get("1.0", "end-1c")
        if path.endswith(".py"):
            try:
                compile(content, os.path.basename(path), "exec")
            except SyntaxError as e:
                if not messagebox.askyesno(
                    "Szintaktikai hiba",
                    f"A fájl hibás:\n\nSor {e.lineno}: {e.msg}\n\nMentse mindenképp?",
                    parent=win
                ):
                    return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self._editor_status.configure(
                text=f"✅ Mentve: {os.path.basename(path)}",
                text_color="#2ecc71"
            )
            self.notify(f"💾 Mentve: {os.path.basename(path)}", "success", 1500)
        except OSError as e:
            messagebox.showerror("Hiba", str(e), parent=win)

    def _new_file(self, win):
        name = simpledialog.askstring("Új fájl",
                                        "Fájlnév (pl. uj_parancs.py):",
                                        parent=win)
        if not name:
            return
        if "." not in name:
            name += ".py"

        base = self._bot_dir()
        sel = self._tree.selection()
        if sel:
            values = self._tree.item(sel[0], "values")
            if values and os.path.isdir(values[0]):
                base = values[0]

        path = os.path.join(base, name)
        if os.path.exists(path):
            messagebox.showerror("Hiba", "Már létezik ilyen fájl!", parent=win)
            return

        if name.endswith(".py"):
            cls_name = os.path.splitext(name)[0].title().replace("_", "").replace(" ", "")
            template = (
                f"# {name}\n\n"
                f"from discord.ext import commands\n\n\n"
                f"class {cls_name}(commands.Cog):\n"
                f"    def __init__(self, bot):\n"
                f"        self.bot = bot\n\n\n"
                f"async def setup(bot):\n"
                f"    await bot.add_cog({cls_name}(bot))\n"
            )
        else:
            template = ""

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(template)
            self._refresh_tree(win)

            if name.endswith(".py"):
                ext_name = self._path_to_ext_name(path)
                if ext_name and messagebox.askyesno(
                    "Extension hozzáadása",
                    f"Szeretnéd a(z) '{ext_name}' extension-t hozzáadni\n"
                    "az automatikusan betöltendő listához?",
                    parent=win
                ):
                    self._add_extension_by_name(ext_name, win)
        except OSError as e:
            messagebox.showerror("Hiba", str(e), parent=win)

    def _path_to_ext_name(self, path):
        bot_dir = self._bot_dir()
        if not bot_dir:
            return None
        try:
            rel = os.path.relpath(path, bot_dir)
            rel = rel.replace(os.sep, ".").rsplit(".", 1)[0]
            return rel
        except Exception:
            return None

    def _new_folder(self, win):
        name = simpledialog.askstring("Új mappa", "Mappa neve:", parent=win)
        if not name or "/" in name or "\\" in name:
            return
        base = self._bot_dir()
        sel = self._tree.selection()
        if sel:
            values = self._tree.item(sel[0], "values")
            if values and os.path.isdir(values[0]):
                base = values[0]

        path = os.path.join(base, name)
        try:
            os.makedirs(path, exist_ok=False)
            with open(os.path.join(path, "__init__.py"), "w", encoding="utf-8") as f:
                f.write("")
            self._refresh_tree(win)
        except OSError as e:
            messagebox.showerror("Hiba", str(e), parent=win)

    def _rename_item(self, win):
        sel = self._tree.selection()
        if not sel:
            return
        values = self._tree.item(sel[0], "values")
        if not values:
            return
        old = values[0]
        new_name = simpledialog.askstring(
            "Átnevezés", "Új név:",
            initialvalue=os.path.basename(old), parent=win
        )
        if not new_name or new_name == os.path.basename(old):
            return
        new = os.path.join(os.path.dirname(old), new_name)
        try:
            os.rename(old, new)
            self._refresh_tree(win)
        except OSError as e:
            messagebox.showerror("Hiba", str(e), parent=win)

    def _delete_item(self, win):
        sel = self._tree.selection()
        if not sel:
            return
        values = self._tree.item(sel[0], "values")
        if not values:
            return
        path = values[0]
        name = os.path.basename(path)
        if not messagebox.askyesno("Megerősítés",
                                     f"Biztosan törlöd: {name}?",
                                     parent=win):
            return
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            self._refresh_tree(win)
        except OSError as e:
            messagebox.showerror("Hiba", str(e), parent=win)

    # ==================================================================
    #  COMMANDER PARANCSOK
    # ==================================================================
    def _load_commander_commands(self):
        path = self._commander_config_path()
        if not path or not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return []

    def _save_commander_commands(self, commands):
        path = self._commander_config_path()
        if not path:
            return False
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(commands, f, ensure_ascii=False, indent=4)
            return True
        except OSError as e:
            messagebox.showerror("Hiba", str(e))
            return False

    def _refresh_command_list(self):
        if not hasattr(self, "_cmd_list"):
            return
        for w in self._cmd_list.winfo_children():
            w.destroy()

        commands = self._load_commander_commands()
        if not commands:
            ctk.CTkLabel(self._cmd_list, text="Még nincs egyedi parancs.",
                          text_color="#777").pack(pady=20)
            return

        for i, cmd in enumerate(commands):
            card = ctk.CTkFrame(self._cmd_list, fg_color="#252932", corner_radius=8)
            card.pack(fill="x", padx=4, pady=3)

            type_str = "Embed" if cmd.get("type") == "embed" else "Üzenet"
            enabled = "✅" if cmd.get("enabled", True) else "⛔"

            ctk.CTkLabel(
                card,
                text=f"{enabled}  /{cmd.get('name', '?')}   •   {type_str}   •   {cmd.get('description', '')}",
                font=("Consolas", 11), anchor="w",
            ).pack(side="left", padx=10, pady=8, fill="x", expand=True)

            ctk.CTkButton(card, text="✏️", width=32, height=28,
                           fg_color="#2980b9", hover_color="#3498db",
                           command=lambda idx=i: self._edit_command(idx)
                           ).pack(side="right", padx=4, pady=6)
            ctk.CTkButton(card, text="🗑️", width=32, height=28,
                           fg_color="#c0392b", hover_color="#e74c3c",
                           command=lambda idx=i: self._delete_command(idx)
                           ).pack(side="right", padx=4, pady=6)

    def _new_command(self):
        self._open_command_editor(None, existing=None)

    def _edit_command(self, idx):
        commands = self._load_commander_commands()
        if not (0 <= idx < len(commands)):
            return
        self._open_command_editor(idx, existing=commands[idx])

    def _open_command_editor(self, idx, existing=None):
        """Közös parancs szerkesztő (új + meglévő) — sablonokkal."""
        is_new = existing is None

        data = existing or {
            "name": "",
            "description": "Egyedi parancs",
            "type": "message",
            "content": "",
            "embed": {"title": "", "description": "", "color": "#5865F2",
                       "footer": "", "thumbnail": "", "fields": []},
            "ephemeral": False,
            "enabled": True,
        }

        dlg = ctk.CTkToplevel(self)
        dlg.title("✏️  Parancs szerkesztése" if not is_new else "➕  Új parancs")
        dlg.geometry("720x820")
        dlg.minsize(640, 560)
        dlg.grab_set()
        dlg.update_idletasks()
        x = (dlg.winfo_screenwidth() - 720) // 2
        y = (dlg.winfo_screenheight() - 820) // 2
        dlg.geometry(f"720x820+{x}+{y}")

        # Fejléc
        header = ctk.CTkFrame(dlg, fg_color="#f39c12" if is_new else "#3498db",
                                corner_radius=0, height=56)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header,
            text="➕  Új parancs" if is_new else "✏️  Parancs szerkesztése",
            font=("Arial", 16, "bold"), text_color="white",
        ).pack(side="left", padx=20, pady=14)

        # Alsó mentés sáv
        bottom = ctk.CTkFrame(dlg, fg_color="transparent")
        bottom.pack(side="bottom", fill="x", padx=16, pady=12)

        scroll = ctk.CTkScrollableFrame(dlg, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=14, pady=12)

        # ============================================================
        #  SABLON VÁLASZTÓ (csak új parancs esetén)
        # ============================================================
        if is_new:
            ctk.CTkLabel(
                scroll, text="🎨  Sablon választása",
                font=("Arial", 13, "bold"), anchor="w",
            ).pack(fill="x", pady=(4, 4))

            ctk.CTkLabel(
                scroll,
                text="Válassz egy kész sablont — a mezők automatikusan kitöltődnek,\n"
                     "és utána szabadon módosíthatod őket.",
                font=("Arial", 10), text_color="#8a8e98",
                justify="left", anchor="w",
            ).pack(fill="x", pady=(0, 8))

            template_grid = ctk.CTkFrame(scroll, fg_color="transparent")
            template_grid.pack(fill="x", pady=(0, 12))

            # Előre létrehozott mezők referenciái
            field_refs = {}

            def apply_template(tpl_key):
                tpl = COMMAND_TEMPLATES[tpl_key]
                field_refs["type_var"].set("Embed" if tpl["type"] == "embed" else "Üzenet")
                desc_entry.delete(0, "end")
                desc_entry.insert(0, tpl.get("description", ""))
                content_box.delete("1.0", "end")
                content_box.insert("1.0", tpl.get("content", ""))
                emb = tpl.get("embed", {})
                emb_title.delete(0, "end")
                emb_title.insert(0, emb.get("title", ""))
                emb_desc.delete("1.0", "end")
                emb_desc.insert("1.0", emb.get("description", ""))
                emb_color.delete(0, "end")
                emb_color.insert(0, emb.get("color", "#5865F2"))
                emb_footer.delete(0, "end")
                emb_footer.insert(0, emb.get("footer", ""))
                emb_thumb.delete(0, "end")
                emb_thumb.insert(0, emb.get("thumbnail", ""))
                field_refs["eph_var"].set(tpl.get("ephemeral", False))
                field_refs["toggle_sections"]()

            keys = list(COMMAND_TEMPLATES.keys())
            for i, tpl_key in enumerate(keys):
                btn = ctk.CTkButton(
                    template_grid,
                    text=tpl_key,
                    height=38,
                    anchor="w",
                    fg_color="#252932",
                    hover_color="#3a4155",
                    font=("Arial", 11),
                    corner_radius=6,
                    command=lambda k=tpl_key: apply_template(k),
                )
                btn.grid(row=i // 2, column=i % 2, sticky="ew", padx=3, pady=3)
            template_grid.grid_columnconfigure(0, weight=1)
            template_grid.grid_columnconfigure(1, weight=1)

            ctk.CTkFrame(scroll, height=1, fg_color="#3a4258").pack(fill="x", pady=(4, 12))

        # ============================================================
        #  PARANCS ADATOK
        # ============================================================
        ctk.CTkLabel(scroll, text="📝  Parancs adatai",
                      font=("Arial", 13, "bold"), anchor="w").pack(fill="x", pady=(4, 8))

        ctk.CTkLabel(scroll, text="Parancs neve (per jel nélkül):",
                      font=("Arial", 11), anchor="w").pack(fill="x", pady=(4, 2))
        name_entry = ctk.CTkEntry(scroll, width=460, height=36,
                                    font=("Arial", 12))
        name_entry.insert(0, data.get("name", ""))
        name_entry.pack(anchor="w")

        ctk.CTkLabel(scroll, text="Leírás (megjelenik a Discord / menüben):",
                      font=("Arial", 11), anchor="w").pack(fill="x", pady=(10, 2))
        desc_entry = ctk.CTkEntry(scroll, width=460, height=36,
                                    font=("Arial", 12))
        desc_entry.insert(0, data.get("description", ""))
        desc_entry.pack(anchor="w")

        ctk.CTkLabel(scroll, text="Típus:",
                      font=("Arial", 11), anchor="w").pack(fill="x", pady=(10, 2))
        type_var = ctk.StringVar(value="Embed" if data.get("type") == "embed" else "Üzenet")
        ctk.CTkComboBox(scroll, values=["Üzenet", "Embed"],
                        variable=type_var, width=220, height=36).pack(anchor="w")

        # ============================================================
        #  ÜZENET SZEKCIÓ
        # ============================================================
        msg_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        ctk.CTkLabel(msg_frame, text="Üzenet tartalma:",
                      font=("Arial", 11), anchor="w").pack(fill="x", pady=(0, 2))
        content_box = ctk.CTkTextbox(msg_frame, height=100, font=("Consolas", 11))
        content_box.pack(fill="x")
        content_box.insert("1.0", data.get("content", ""))

        # ============================================================
        #  EMBED SZEKCIÓ
        # ============================================================
        embed_frame = ctk.CTkFrame(scroll, fg_color="transparent")

        ctk.CTkLabel(embed_frame, text="Embed cím:",
                      font=("Arial", 11), anchor="w").pack(fill="x", pady=(0, 2))
        emb_title = ctk.CTkEntry(embed_frame, width=460, height=36)
        emb_title.insert(0, data.get("embed", {}).get("title", ""))
        emb_title.pack(anchor="w")

        ctk.CTkLabel(embed_frame, text="Embed leírás:",
                      font=("Arial", 11), anchor="w").pack(fill="x", pady=(8, 2))
        emb_desc = ctk.CTkTextbox(embed_frame, height=100, font=("Arial", 11))
        emb_desc.pack(fill="x")
        emb_desc.insert("1.0", data.get("embed", {}).get("description", ""))

        color_row = ctk.CTkFrame(embed_frame, fg_color="transparent")
        color_row.pack(fill="x", pady=(8, 0))

        ctk.CTkLabel(color_row, text="Szín (hex):",
                      font=("Arial", 11)).pack(side="left")
        emb_color = ctk.CTkEntry(color_row, width=120, height=32)
        emb_color.insert(0, data.get("embed", {}).get("color", "#5865F2"))
        emb_color.pack(side="left", padx=6)

        color_preview = ctk.CTkFrame(
            color_row, width=32, height=32, corner_radius=6,
            fg_color=data.get("embed", {}).get("color", "#5865F2"),
        )
        color_preview.pack(side="left", padx=4)
        color_preview.pack_propagate(False)

        def update_color(*_):
            try:
                color_preview.configure(fg_color=emb_color.get().strip() or "#5865F2")
            except Exception:
                pass

        emb_color.bind("<KeyRelease>", update_color)

        quick_colors = [
            ("Blurple", "#5865F2"), ("Zöld", "#2ecc71"), ("Piros", "#e74c3c"),
            ("Narancs", "#f39c12"), ("Kék", "#3498db"), ("Lila", "#9b59b6"),
            ("Rózsa", "#e91e63"), ("Cián", "#16a085"),
        ]
        color_quick = ctk.CTkFrame(embed_frame, fg_color="transparent")
        color_quick.pack(fill="x", pady=(6, 0))
        ctk.CTkLabel(color_quick, text="Gyors:",
                      font=("Arial", 10)).pack(side="left", padx=(0, 4))
        for name, hexcode in quick_colors:
            ctk.CTkButton(
                color_quick, text=name, width=62, height=26,
                fg_color=hexcode, hover_color=hexcode,
                text_color="white", font=("Arial", 10),
                command=lambda h=hexcode: (
                    emb_color.delete(0, "end"),
                    emb_color.insert(0, h),
                    update_color(),
                ),
            ).pack(side="left", padx=2)

        ctk.CTkLabel(embed_frame, text="Footer (alcím):",
                      font=("Arial", 11), anchor="w").pack(fill="x", pady=(10, 2))
        emb_footer = ctk.CTkEntry(embed_frame, width=460, height=36)
        emb_footer.insert(0, data.get("embed", {}).get("footer", ""))
        emb_footer.pack(anchor="w")

        ctk.CTkLabel(embed_frame, text="Thumbnail URL (kép):",
                      font=("Arial", 11), anchor="w").pack(fill="x", pady=(8, 2))
        emb_thumb = ctk.CTkEntry(embed_frame, width=460, height=36,
                                   placeholder_text="https://...")
        emb_thumb.insert(0, data.get("embed", {}).get("thumbnail", ""))
        emb_thumb.pack(anchor="w")

        # ============================================================
        #  OPCIÓK
        # ============================================================
        ctk.CTkLabel(scroll, text="⚙️  Opciók",
                      font=("Arial", 13, "bold"), anchor="w").pack(fill="x", pady=(16, 8))

        eph_var = ctk.BooleanVar(value=data.get("ephemeral", False))
        ctk.CTkCheckBox(scroll, text="  Csak a hívónak látszódjon (ephemeral)",
                          variable=eph_var, font=("Arial", 11)).pack(anchor="w", pady=3)

        en_var = ctk.BooleanVar(value=data.get("enabled", True))
        ctk.CTkCheckBox(scroll, text="  Parancs engedélyezve",
                          variable=en_var, font=("Arial", 11)).pack(anchor="w", pady=3)

        # ============================================================
        #  SZEKCIÓK KI/BE
        # ============================================================
        def toggle_sections(*_):
            if type_var.get() == "Embed":
                msg_frame.pack_forget()
                embed_frame.pack(fill="x", pady=(10, 0))
            else:
                embed_frame.pack_forget()
                msg_frame.pack(fill="x", pady=(10, 0))

        type_var.trace_add("write", toggle_sections)
        toggle_sections()

        # Sablon hozzáférjen a mezőkhöz
        if is_new:
            field_refs["type_var"] = type_var
            field_refs["eph_var"] = eph_var
            field_refs["toggle_sections"] = toggle_sections

        # ============================================================
        #  MENTÉS
        # ============================================================
        def save():
            name = name_entry.get().strip().lstrip("/").replace(" ", "_").lower()
            if not name:
                messagebox.showerror("Hiba", "A parancs neve nem lehet üres!", parent=dlg)
                return
            if not name.replace("_", "").isalnum():
                messagebox.showerror("Hiba",
                                       "A név csak betű, szám és alulvonás lehet!",
                                       parent=dlg)
                return

            all_cmds = self._load_commander_commands()
            for i, c in enumerate(all_cmds):
                if c.get("name") == name and (is_new or i != idx):
                    messagebox.showerror("Hiba",
                                           f"Már létezik /{name} parancs!", parent=dlg)
                    return

            cmd_data = {
                "name": name,
                "description": desc_entry.get().strip() or "Egyedi parancs",
                "type": "embed" if type_var.get() == "Embed" else "message",
                "content": content_box.get("1.0", "end-1c").strip(),
                "embed": {
                    "title": emb_title.get().strip(),
                    "description": emb_desc.get("1.0", "end-1c").strip(),
                    "color": emb_color.get().strip() or "#5865F2",
                    "footer": emb_footer.get().strip(),
                    "thumbnail": emb_thumb.get().strip(),
                    "fields": data.get("embed", {}).get("fields", []),
                },
                "ephemeral": bool(eph_var.get()),
                "enabled": bool(en_var.get()),
            }

            if is_new:
                all_cmds.append(cmd_data)
            else:
                all_cmds[idx] = cmd_data

            if self._save_commander_commands(all_cmds):
                self.notify(
                    f"{'✅ Létrehozva' if is_new else '💾 Mentve'}: /{name}",
                    "success", 2000
                )
                self._refresh_command_list()
                dlg.destroy()

        ctk.CTkButton(bottom, text="❌  Mégse",
                       fg_color="#555555", hover_color="#666666",
                       width=140, height=44,
                       command=dlg.destroy).pack(side="right", padx=4)

        ctk.CTkButton(bottom, text="💾  Mentés",
                       fg_color="#27ae60", hover_color="#2ecc71",
                       width=180, height=44, font=("Arial", 13, "bold"),
                       command=save).pack(side="right", padx=4)

    def _delete_command(self, idx):
        commands = self._load_commander_commands()
        if not (0 <= idx < len(commands)):
            return
        name = commands[idx].get("name", "?")
        if not messagebox.askyesno("Törlés", f"Törlöd a /{name} parancsot?"):
            return
        commands.pop(idx)
        self._save_commander_commands(commands)
        self._refresh_command_list()

    # ==================================================================
    #  EXTENSION LISTA
    # ==================================================================
    def _load_extensions(self):
        path = self._extensions_file_path()
        if not path or not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                return [line.strip() for line in f
                        if line.strip() and not line.startswith("#")]
        except OSError:
            return []

    def _save_extensions(self, win=None):
        path = self._extensions_file_path()
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("# Automatikusan betöltendő extension-ök\n")
                f.write("# Egy sor = egy extension neve (pl. cogs.parancsok)\n")
                f.write("# A panel_integrity.py tölti be induláskor.\n\n")
                for ext in self._extensions:
                    f.write(ext + "\n")
            if win:
                self._refresh_extension_list()
                self.notify("💾 Extension lista mentve", "success", 1500)
        except OSError as e:
            if win:
                messagebox.showerror("Hiba", str(e), parent=win)

    def _refresh_extension_list(self):
        if not hasattr(self, "_ext_list"):
            return
        for w in self._ext_list.winfo_children():
            w.destroy()

        if not hasattr(self, "_extensions"):
            self._extensions = self._load_extensions()

        if not self._extensions:
            ctk.CTkLabel(self._ext_list,
                          text="Még nincs hozzáadott extension.",
                          text_color="#777").pack(pady=20)
            return

        for i, ext in enumerate(self._extensions):
            card = ctk.CTkFrame(self._ext_list, fg_color="#252932", corner_radius=8)
            card.pack(fill="x", padx=4, pady=3)
            ctk.CTkLabel(card, text=f"🔌  {ext}",
                          font=("Consolas", 11), anchor="w").pack(
                side="left", padx=10, pady=8, fill="x", expand=True)
            ctk.CTkButton(card, text="🗑️", width=32, height=28,
                           fg_color="#c0392b", hover_color="#e74c3c",
                           command=lambda idx=i: self._remove_extension(idx)
                           ).pack(side="right", padx=4, pady=6)

    def _add_extension(self, win):
        name = simpledialog.askstring(
            "Új extension",
            "Extension neve (pl. cogs.parancsok vagy egyszerű: uj_parancs):",
            parent=win
        )
        if not name:
            return
        self._add_extension_by_name(name.strip(), win)

    def _add_extension_by_name(self, name, win):
        if not hasattr(self, "_extensions"):
            self._extensions = self._load_extensions()
        if name in self._extensions:
            return
        self._extensions.append(name)
        self._save_extensions()
        self._refresh_extension_list()

    def _remove_extension(self, idx):
        if not hasattr(self, "_extensions"):
            return
        if 0 <= idx < len(self._extensions):
            self._extensions.pop(idx)
            self._save_extensions()
            self._refresh_extension_list()