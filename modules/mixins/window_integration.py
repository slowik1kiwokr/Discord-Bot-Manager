import os
import sys
import subprocess
import threading
import importlib.util

import customtkinter as ctk
from tkinter import filedialog, messagebox

import modules.config as config
from modules.languages import LANGUAGES
from modules.templates import (
    VERSION_FILE_TEMPLATE,
    BOT_PY_TEMPLATE,
    PANEL_INTEGRITY_CODE,
)


# --- Szükséges csomagok ---
REQUIRED_PACKAGES = [
    ("customtkinter", "customtkinter", "Modern UI keretrendszer"),
    ("psutil", "psutil", "Rendszer erőforrás figyelés"),
    ("matplotlib", "matplotlib", "Grafikonok"),
    ("pystray", "pystray", "Rendszertálca ikon"),
    ("Pillow", "PIL", "Képkezelés"),
    ("pypresence", "pypresence", "Discord Rich Presence"),
    ("discord.py", "discord", "Discord API"),
]

OPTIONAL_PACKAGES = [
    ("wmi", "wmi", "Windows hőmérséklet olvasás"),
    ("requests", "requests", "HTTP kérések"),
]


class WindowIntegrationMixin:

    # ==================================================================
    #  Fő ablak
    # ==================================================================
    def open_alapok_window(self):
        win = ctk.CTkToplevel(self)
        win.title("📌 Alapok / Integráció")
        win.geometry("900x760")
        win.minsize(780, 560)
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 900) // 2
        y = (win.winfo_screenheight() - 760) // 2
        win.geometry(f"900x760+{x}+{y}")

        # --- Fejléc ---
        header = ctk.CTkFrame(win, fg_color="#8e44ad", corner_radius=0, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text="📌   Panel Integráció",
            font=("Arial", 20, "bold"), text_color="white"
        ).pack(side="left", padx=24, pady=18)

        # Függőségek gomb
        ctk.CTkButton(
            header, text="🔧  Függőségek",
            fg_color="#2c3e50", hover_color="#34495e",
            width=140, height=36,
            command=lambda: self._open_dependencies_window(win)
        ).pack(side="right", padx=20, pady=17)

        # --- Görgethető tartalom ---
        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=14, pady=14)

        # --- Választó ---
        ctk.CTkLabel(
            scroll, text="Üdvözlünk a panel integrációban! 🎉",
            font=("Arial", 18, "bold"), anchor="w"
        ).pack(fill="x", pady=(10, 4))

        ctk.CTkLabel(
            scroll,
            text="A panel 3 fájlt használ a bot oldalán:\n"
                 "   • bot.py — a bot fő fájlja\n"
                 "   • panel_integrity.py — a panel összes funkciója\n"
                 "   • version.py — bot név, verzió, token",
            font=("Arial", 11), text_color="#8a8e98",
            justify="left", anchor="w",
        ).pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            scroll, text="Van már működő botod?",
            font=("Arial", 14, "bold"), anchor="w"
        ).pack(fill="x", pady=(0, 8))

        choice_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        choice_frame.pack(fill="x", pady=(0, 16))

        ctk.CTkButton(
            choice_frame,
            text="✅  Van már botom\n(csak integrációt adok hozzá)",
            fg_color="#27ae60", hover_color="#2ecc71",
            height=70, width=380,
            font=("Arial", 13, "bold"),
            command=lambda: self._show_existing_flow(win),
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            choice_frame,
            text="🆕  Új botot készítek\n(teljes sablon)",
            fg_color="#3498db", hover_color="#5dade2",
            height=70, width=380,
            font=("Arial", 13, "bold"),
            command=lambda: self._show_new_flow(win),
        ).pack(side="left", padx=8)

    # ==================================================================
    #  "Van már botom" ág
    # ==================================================================
    def _show_existing_flow(self, parent):
        win = ctk.CTkToplevel(parent)
        win.title("✅  Integráció hozzáadása")
        win.geometry("820x700")
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 820) // 2
        y = (win.winfo_screenheight() - 700) // 2
        win.geometry(f"820x700+{x}+{y}")

        header = ctk.CTkFrame(win, fg_color="#27ae60", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text="✅   Integráció hozzáadása meglévő bothoz",
            font=("Arial", 16, "bold"), text_color="white"
        ).pack(side="left", padx=24, pady=16)

        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=16, pady=16)

        # Lépések
        ctk.CTkLabel(
            scroll, text="📋  Lépések", font=("Arial", 15, "bold"), anchor="w"
        ).pack(fill="x", pady=(0, 8))

        steps = [
            ("1.", "Tallózd be a botod fő .py fájlját a panelen (📁 Tallózás)."),
            ("2.", "Kattints az alábbi „📥 Panel integráció hozzáadása” gombra — létrejön a panel_integrity.py a bot mappájában."),
            ("3.", "Nyisd meg a bot.py fájlt, és az on_ready() függvényben add hozzá:"),
        ]
        for num, text in steps:
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=num, font=("Arial", 12, "bold"),
                          text_color="#2ecc71", width=30, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=text, font=("Arial", 12),
                          anchor="w", justify="left", wraplength=700).pack(side="left", fill="x", expand=True)

        code_box = ctk.CTkTextbox(scroll, height=80, font=("Consolas", 12),
                                    fg_color="#0a0c10", text_color="#8b95ff")
        code_box.pack(fill="x", padx=30, pady=(4, 12))
        code_box.insert("1.0",
            "@bot.event\n"
            "async def on_ready():\n"
            "    await bot.load_extension(\"panel_integrity\")\n"
            "    await bot.tree.sync()\n"
        )
        code_box.configure(state="disabled")

        for text in [
            "4.  Indítsd újra a botot.",
            "5.  Discordban írd be: /connect panel_id:<a panel azonosítója>",
        ]:
            ctk.CTkLabel(scroll, text=text, font=("Arial", 12),
                          anchor="w", justify="left").pack(fill="x", pady=2)

        # panel_integrity.py kód
        ctk.CTkLabel(
            scroll, text="📄  panel_integrity.py tartalma",
            font=("Arial", 14, "bold"), anchor="w"
        ).pack(fill="x", pady=(18, 6))

        code_view = ctk.CTkTextbox(scroll, height=260, font=("Consolas", 10))
        code_view.pack(fill="both", expand=True, pady=(0, 12))
        code_view.insert("1.0", PANEL_INTEGRITY_CODE)
        code_view.configure(state="disabled")

        # Gombok
        btns = ctk.CTkFrame(win, fg_color="transparent")
        btns.pack(fill="x", padx=16, pady=(0, 14))

        ctk.CTkButton(
            btns, text="📥  Panel integráció hozzáadása",
            fg_color="#27ae60", hover_color="#2ecc71",
            height=44, width=280, font=("Arial", 13, "bold"),
            command=lambda: self._save_panel_integrity(win),
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            btns, text="Bezárás",
            fg_color="#555555", hover_color="#666666",
            height=44, width=120,
            command=win.destroy,
        ).pack(side="right", padx=4)

    # ==================================================================
    #  "Új bot" ág
    # ==================================================================
    def _show_new_flow(self, parent):
        win = ctk.CTkToplevel(parent)
        win.title("🆕  Új bot készítése")
        win.geometry("820x760")
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 820) // 2
        y = (win.winfo_screenheight() - 760) // 2
        win.geometry(f"820x760+{x}+{y}")

        header = ctk.CTkFrame(win, fg_color="#3498db", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text="🆕   Új bot készítése — teljes sablon",
            font=("Arial", 16, "bold"), text_color="white"
        ).pack(side="left", padx=24, pady=16)

        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(
            scroll,
            text="A panel 3 fájlt generál a számodra. Válaszd ki a célmappát,\n"
                 "és a gombokkal külön-külön is mentheted őket.",
            font=("Arial", 11), text_color="#8a8e98",
            justify="left", anchor="w",
        ).pack(fill="x", pady=(0, 12))

        # 1) bot.py
        ctk.CTkLabel(scroll, text="📄  1. bot.py — a bot fő fájlja",
                      font=("Arial", 13, "bold"), anchor="w").pack(fill="x", pady=(8, 4))
        box_bot = ctk.CTkTextbox(scroll, height=200, font=("Consolas", 10))
        box_bot.pack(fill="x", pady=(0, 8))
        box_bot.insert("1.0", BOT_PY_TEMPLATE)
        box_bot.configure(state="disabled")

        # 2) panel_integrity.py
        ctk.CTkLabel(scroll, text="📄  2. panel_integrity.py — a panel összes funkciója",
                      font=("Arial", 13, "bold"), anchor="w").pack(fill="x", pady=(8, 4))
        box_panel = ctk.CTkTextbox(scroll, height=200, font=("Consolas", 10))
        box_panel.pack(fill="x", pady=(0, 8))
        box_panel.insert("1.0", PANEL_INTEGRITY_CODE)
        box_panel.configure(state="disabled")

        # 3) version.py
        ctk.CTkLabel(scroll, text="📄  3. version.py — bot név, verzió, token",
                      font=("Arial", 13, "bold"), anchor="w").pack(fill="x", pady=(8, 4))
        box_version = ctk.CTkTextbox(scroll, height=80, font=("Consolas", 10))
        box_version.pack(fill="x", pady=(0, 8))
        box_version.insert("1.0", VERSION_FILE_TEMPLATE)
        box_version.configure(state="disabled")

        # --- Token beállítás kártya ---
        token_card = ctk.CTkFrame(
            scroll,
            fg_color="#2a1f0f",
            corner_radius=10,
            border_width=1,
            border_color="#e67e22",
        )
        token_card.pack(fill="x", pady=(8, 12))

        ctk.CTkLabel(
            token_card,
            text="🔑  Bot Token beállítása",
            font=("Arial", 13, "bold"),
            text_color="#e67e22",
            anchor="w",
        ).pack(fill="x", padx=14, pady=(10, 4))

        ctk.CTkLabel(
            token_card,
            text="A bot tokent a „Bot adatai” ablakban tudod beállítani.\n"
                 "Ott a nevet, verziót és a tokent is szerkesztheted — a panel\n"
                 "automatikusan elmenti a version.py fájlba.",
            font=("Arial", 11),
            text_color="#b8bcc6",
            justify="left",
            anchor="w",
        ).pack(fill="x", padx=14, pady=(0, 8))

        ctk.CTkButton(
            token_card,
            text="🔑  Bot adatai szerkesztése",
            fg_color="#e67e22", hover_color="#d35400",
            height=38, width=240,
            font=("Arial", 12, "bold"),
            command=self._open_token_editor,
        ).pack(anchor="w", padx=14, pady=(0, 12))

        # Gombok
        btns = ctk.CTkFrame(win, fg_color="transparent")
        btns.pack(fill="x", padx=16, pady=(0, 14))

        ctk.CTkButton(
            btns, text="📁  Összes fájl generálása egy mappába",
            fg_color="#2980b9", hover_color="#3498db",
            height=44, width=320, font=("Arial", 13, "bold"),
            command=lambda: self._generate_full_template(win),
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            btns, text="Bezárás",
            fg_color="#555555", hover_color="#666666",
            height=44, width=120,
            command=win.destroy,
        ).pack(side="right", padx=4)

    # ==================================================================
    #  Fájlok mentése
    # ==================================================================
    def _get_bot_dir(self, parent):
        """A bot mappa útvonala (a panelen tallózott fájlból)."""
        script_path = self.entry_path.get().strip()
        if not script_path or not os.path.exists(script_path):
            messagebox.showwarning(
                "Figyelem",
                "Előbb tallózd be a bot fő .py fájlját a panelen (📁 Tallózás)!",
                parent=parent,
            )
            return None
        return os.path.dirname(script_path)

    def _save_panel_integrity(self, parent):
        bot_dir = self._get_bot_dir(parent)
        if not bot_dir:
            return
        target = os.path.join(bot_dir, "panel_integrity.py")
        try:
            with open(target, "w", encoding="utf-8") as f:
                f.write(PANEL_INTEGRITY_CODE)
            messagebox.showinfo(
                "✅ Siker",
                f"panel_integrity.py elkészült:\n{bot_dir}\n\n"
                "Ne felejtsd el a bot.py on_ready() függvényébe:\n"
                '    await bot.load_extension("panel_integrity")',
                parent=parent,
            )
            self.log_event("EVENT", f"[INTEGRATION] panel_integrity.py mentve: {target}")
            self.notify("✅ Panel integráció hozzáadva", "success")
        except OSError as e:
            messagebox.showerror("Hiba", str(e), parent=parent)

    def _generate_full_template(self, parent):
        folder = filedialog.askdirectory(parent=parent, title="Válaszd ki a célmappát")
        if not folder:
            return
        try:
            with open(os.path.join(folder, "bot.py"), "w", encoding="utf-8") as f:
                f.write(BOT_PY_TEMPLATE)
            with open(os.path.join(folder, "panel_integrity.py"), "w", encoding="utf-8") as f:
                f.write(PANEL_INTEGRITY_CODE)
            with open(os.path.join(folder, "version.py"), "w", encoding="utf-8") as f:
                f.write(VERSION_FILE_TEMPLATE)
            messagebox.showinfo(
                "✅ Siker",
                f"3 fájl elkészült:\n{folder}\n\n"
                "  • bot.py\n"
                "  • panel_integrity.py\n"
                "  • version.py\n\n"
                "⚠️ Ne felejtsd el a BOT_TOKEN-t kitölteni!",
                parent=parent,
            )
            self.log_event("EVENT", f"[INTEGRATION] Teljes sablon generálva: {folder}")
            self.notify("✅ Sablon generálva", "success")
        except OSError as e:
            messagebox.showerror("Hiba", str(e), parent=parent)

    def _open_token_editor(self):
        """Megnyitja a Bot adatai szerkesztőt, és figyelmeztet, ha nincs tallózva bot."""
        script_path = self.entry_path.get().strip()
        if not script_path or not os.path.exists(script_path):
            messagebox.showwarning(
                "Figyelem",
                "Előbb tallózd be a bot fő .py fájlját a panelen (📁 Tallózás)!\n\n"
                "A Bot adatai szerkesztő a bot mappájából olvassa a version.py-t,\n"
                "ezért tudnia kell, hol van a bot.",
            )
            return
        # Megnyitja a Bot adatai szerkesztőt
        self.open_bot_info_editor()

    # ==================================================================
    #  Függőségek ablak
    # ==================================================================
    def _open_dependencies_window(self, parent):
        win = ctk.CTkToplevel(parent)
        win.title("🔧  Függőségek")
        win.geometry("700x700")
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 700) // 2
        y = (win.winfo_screenheight() - 700) // 2
        win.geometry(f"700x700+{x}+{y}")

        header = ctk.CTkFrame(win, fg_color="#e67e22", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text="🔧   Panel függőségek",
            font=("Arial", 16, "bold"), text_color="white"
        ).pack(side="left", padx=24, pady=16)

        ctk.CTkLabel(
            win,
            text="Ellenőrizd, hogy minden szükséges Python csomag telepítve van-e.\n"
                 "A hiányzó csomagokat egy kattintással telepítheted.",
            font=("Arial", 11), text_color="#8a8e98", justify="center",
        ).pack(pady=(12, 6))

        list_frame = ctk.CTkScrollableFrame(win, fg_color="#1e2129",
                                              corner_radius=10, height=280)
        list_frame.pack(fill="both", expand=True, padx=14, pady=6)

        dep_rows = {}

        def check_package(pip_name, import_name):
            try:
                spec = importlib.util.find_spec(import_name)
                if spec is None:
                    return False, "—"
                try:
                    import importlib.metadata as md
                    return True, md.version(pip_name)
                except Exception:
                    return True, "?"
            except Exception:
                return False, "—"

        def build_rows():
            for w in list_frame.winfo_children():
                w.destroy()
            dep_rows.clear()

            all_pkgs = [(p, i, d, "required") for p, i, d in REQUIRED_PACKAGES]
            all_pkgs += [(p, i, d, "optional") for p, i, d in OPTIONAL_PACKAGES]

            for pip_name, import_name, desc, category in all_pkgs:
                row = ctk.CTkFrame(list_frame, fg_color="#252932", corner_radius=8)
                row.pack(fill="x", padx=4, pady=3)

                installed, version = check_package(pip_name, import_name)
                icon = "✅" if installed else ("⚠️" if category == "optional" else "❌")
                color = "#2ecc71" if installed else ("#f39c12" if category == "optional" else "#e74c3c")

                ctk.CTkLabel(row, text=icon, font=("Arial", 16), width=30).pack(
                    side="left", padx=(10, 4), pady=8)

                info = ctk.CTkFrame(row, fg_color="transparent")
                info.pack(side="left", fill="x", expand=True, pady=8)
                ctk.CTkLabel(info, text=pip_name, font=("Consolas", 12, "bold"),
                              text_color=color, anchor="w").pack(fill="x")
                ctk.CTkLabel(info, text=desc, font=("Arial", 10),
                              text_color="#888", anchor="w").pack(fill="x")

                ctk.CTkLabel(row, text=f"v{version}" if installed else "hiányzik",
                              font=("Consolas", 10, "bold"),
                              text_color=color, width=100).pack(side="right", padx=10)

                dep_rows[pip_name] = {"installed": installed, "category": category}

        status_lbl = ctk.CTkLabel(win, text="", font=("Arial", 11), text_color="#aaa")
        status_lbl.pack(pady=(4, 2))

        progress = ctk.CTkProgressBar(win, width=640)
        progress.set(0)
        progress.pack(pady=(0, 6))

        output = ctk.CTkTextbox(win, height=110, font=("Consolas", 10))
        output.pack(fill="x", padx=14, pady=(0, 10))
        output.insert("1.0", "Kattints az „Ellenőrzés” gombra.\n")
        output.configure(state="disabled")

        def log(text):
            output.configure(state="normal")
            output.insert("end", text)
            output.see("end")
            output.configure(state="disabled")

        def refresh():
            build_rows()
            req_ok = sum(1 for p, _, _ in REQUIRED_PACKAGES
                          if dep_rows.get(p, {}).get("installed"))
            total = len(REQUIRED_PACKAGES)
            if req_ok == total:
                status_lbl.configure(
                    text=f"✅ Minden szükséges csomag telepítve ({req_ok}/{total})",
                    text_color="#2ecc71")
            else:
                status_lbl.configure(
                    text=f"❌ {total - req_ok} szükséges csomag hiányzik ({req_ok}/{total})",
                    text_color="#e74c3c")

        def install(packages, reinstall=False):
            if not packages:
                messagebox.showinfo("Info", "Minden csomag telepítve van!", parent=win)
                return
            log(f"\n{'='*60}\n📦 Telepítés indul: {len(packages)} csomag\n{'='*60}\n")
            progress.set(0)
            status_lbl.configure(text="⏳ Telepítés folyamatban...", text_color="#f39c12")

            def worker():
                total = len(packages)
                for i, pkg in enumerate(packages, 1):
                    cmd = [sys.executable, "-m", "pip", "install"]
                    if reinstall:
                        cmd.append("--upgrade")
                    cmd.append(pkg)

                    self.after(0, lambda p=pkg, idx=i, t=total: (
                        log(f"\n[{idx}/{t}] {p}\n"),
                        progress.set(idx / t),
                        status_lbl.configure(text=f"⏳ [{idx}/{t}] {p}...")
                    ))

                    try:
                        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                                 stderr=subprocess.STDOUT, text=True,
                                                 bufsize=1,
                                                 creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                        for line in iter(proc.stdout.readline, ""):
                            self.after(0, lambda l=line: log(l))
                        proc.wait()
                    except Exception as e:
                        self.after(0, lambda e=e, p=pkg: log(f"❌ {p}: {e}\n"))

                self.after(0, lambda: (
                    progress.set(1.0),
                    log(f"\n✅ Telepítés befejezve.\n"),
                    status_lbl.configure(text="✅ Kész", text_color="#2ecc71"),
                    refresh()
                ))

            threading.Thread(target=worker, daemon=True).start()

        def install_missing():
            refresh()
            missing = [p for p, _, _ in REQUIRED_PACKAGES
                        if not dep_rows.get(p, {}).get("installed")]
            if not missing:
                messagebox.showinfo("Info", "Minden szükséges csomag telepítve van!", parent=win)
                return
            install(missing)

        def reinstall_all():
            if not messagebox.askyesno("Újratelepítés",
                                         "Újratelepíti az összes csomagot?",
                                         parent=win):
                return
            install([p for p, _, _ in REQUIRED_PACKAGES], reinstall=True)

        btns = ctk.CTkFrame(win, fg_color="transparent")
        btns.pack(fill="x", padx=14, pady=(0, 12))

        ctk.CTkButton(btns, text="🔍  Ellenőrzés", fg_color="#3498db",
                       width=130, height=38, command=refresh).pack(side="left", padx=4)
        ctk.CTkButton(btns, text="📥  Hiányzók telepítése", fg_color="#27ae60",
                       width=180, height=38, command=install_missing).pack(side="left", padx=4)
        ctk.CTkButton(btns, text="🔄  Újratelepít", fg_color="#e67e22",
                       width=140, height=38, command=reinstall_all).pack(side="left", padx=4)

        refresh()