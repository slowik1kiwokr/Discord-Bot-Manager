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
    BOT_VEZERLO_CODE,
    PANEL_EXTENSION_CODE,
    VERSION_FILE_TEMPLATE,
    INFO_FILE_TEMPLATE,
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
    #  Fő Integrációs ablak
    # ==================================================================
    def open_alapok_window(self):
        win = ctk.CTkToplevel(self)
        win.title(self.tr("integration_title"))
        win.geometry("880x720")
        win.minsize(760, 560)
        win.grab_set()

        win.update_idletasks()
        x = (win.winfo_screenwidth() - 880) // 2
        y = (win.winfo_screenheight() - 720) // 2
        win.geometry(f"880x720+{x}+{y}")

        ctk.CTkLabel(
            win, text=self.tr("integration_help"),
            font=("Arial", 16, "bold"), text_color="#8e44ad"
        ).pack(pady=(12, 5))

        ctk.CTkLabel(
            win, text=self.tr("integration_info"),
            justify="left", font=("Arial", 11), text_color="#aaa"
        ).pack(padx=15, anchor="w")

        tabview = ctk.CTkTabview(win, width=840, height=520)
        tabview.pack(padx=15, pady=10, fill="both", expand=True)

        tab_botpy = tabview.add(self.tr("integration_bot_template"))
        tab_vezerlo = tabview.add(self.tr("integration_panel_code"))
        tab_tutorial = tabview.add(self.tr("integration_tutorial"))
        tab_deps = tabview.add("🔧 Függőségek")

        # --- 1. fül: bot.py sablon ---
        box_bot = ctk.CTkTextbox(tab_botpy, font=("Consolas", 11), width=810, height=460)
        box_bot.pack(fill="both", expand=True, padx=5, pady=5)
        sablon_kod = (
            "# --- SABLON A SAJÁT BOT.PY FÁJLODHOZ ---\n"
            "import discord\n"
            "from discord.ext import commands\n\n"
            "from version import BOT_NAME, BOT_VERSION, BOT_TOKEN\n"
            "from info import BOT_INFO\n\n"
            "CURRENT_PREFIX = \"/\"\n\n"
            "async def get_prefix(bot, message):\n"
            "    return CURRENT_PREFIX\n\n"
            "intents = discord.Intents.default()\n"
            "intents.message_content = True\n\n"
            "bot = commands.Bot(command_prefix=get_prefix, intents=intents)\n\n"
            "@bot.event\n"
            "async def on_ready():\n"
            "    print(f'{BOT_NAME} v{BOT_VERSION} bejelentkezve: {bot.user}')\n"
            "    try:\n"
            "        await bot.load_extension('Panel')\n"
            "        await bot.tree.sync()\n"
            "        print('Panel integráció sikeresen betöltve.')\n"
            "    except Exception as e:\n"
            "        print(f'Hiba a vezérlő betöltésekor: {{e}}')\n\n"
            "@bot.command(name='teszt', aliases=['test'])\n"
            "async def teszt_parancs(ctx):\n"
            "    embed = discord.Embed(title=BOT_NAME, description=f'✅ A bot működik! Verzió: {BOT_VERSION}', color=discord.Color.green())\n"
            "    await ctx.send(embed=embed)\n"
            "\n"
            "@bot.command(name='parancsok', aliases=['menu'])\n"
            "async def parancsok_menu(ctx):\n"
            "    embed = discord.Embed(title='🤖 Parancsok', color=discord.Color.blue())\n"
            "    embed.add_field(name='/teszt', value='Bot tesztelése', inline=False)\n"
            "    embed.add_field(name='/parancsok', value='Ez a menü', inline=False)\n"
            "    embed.set_footer(text=f'Verzió: {BOT_VERSION}')\n"
            "    await ctx.send(embed=embed)\n"
            "\n"
            "bot.run(BOT_TOKEN)\n"
        )
        box_bot.insert("1.0", sablon_kod)
        box_bot.configure(state="disabled")

        # --- 2. fül: Panel.py kód ---
        box_vezerlo = ctk.CTkTextbox(tab_vezerlo, font=("Consolas", 11), width=810, height=460)
        box_vezerlo.pack(fill="both", expand=True, padx=5, pady=5)
        box_vezerlo.insert("1.0", BOT_VEZERLO_CODE)
        box_vezerlo.configure(state="disabled")

        # --- 3. fül: Tutorial ---
        ctk.CTkLabel(
            tab_tutorial, text=self.tr("tutorial_text"),
            justify="left", anchor="w", wraplength=800
        ).pack(fill="x", padx=12, pady=12)

        # --- 4. fül: Függőségek ---
        self._build_dependencies_tab(tab_deps, win)

        # --- Alsó gombok ---
        def save_bot_vezerlo_file():
            script_path = self.entry_path.get().strip()
            if not script_path or not os.path.exists(script_path):
                messagebox.showwarning(self.tr("error_counter"),
                                        self.tr("choose_bot_file"), parent=win)
                return
            bot_dir = os.path.dirname(script_path)
            try:
                with open(os.path.join(bot_dir, "bot_vezerlo.py"), "w", encoding="utf-8") as f:
                    f.write(BOT_VEZERLO_CODE)
                vpath = os.path.join(bot_dir, "version.py")
                if not os.path.exists(vpath) or os.path.getsize(vpath) == 0:
                    with open(vpath, "w", encoding="utf-8") as f:
                        f.write(VERSION_FILE_TEMPLATE)
                with open(os.path.join(bot_dir, "info.py"), "w", encoding="utf-8") as f:
                    f.write(INFO_FILE_TEMPLATE)
                messagebox.showinfo(self.tr("success"),
                                     f"{self.tr('saved_controller')}\n{bot_dir}",
                                     parent=win)
            except Exception as e:
                messagebox.showerror(self.tr("errors"),
                                      f"{self.tr('save_failed')}\n{e}", parent=win)

        def save_panel_extension():
            script_path = self.entry_path.get().strip()
            if not script_path or not os.path.exists(script_path):
                messagebox.showwarning(self.tr("error_counter"),
                                        self.tr("choose_bot_file"), parent=win)
                return
            bot_dir = os.path.dirname(script_path)
            try:
                with open(os.path.join(bot_dir, "Panel.py"), "w", encoding="utf-8") as f:
                    f.write(PANEL_EXTENSION_CODE)
                messagebox.showinfo(self.tr("success"),
                                     f"{self.tr('saved_panel')}\n{bot_dir}",
                                     parent=win)
            except OSError as e:
                messagebox.showerror(self.tr("errors"),
                                      f"{self.tr('save_failed')}\n{e}", parent=win)

        def save_generated_files():
            folder = filedialog.askdirectory(parent=win, title=self.tr("choose_bot_file"))
            if not folder:
                return
            try:
                with open(os.path.join(folder, "bot.py"), "w", encoding="utf-8") as f:
                    f.write(sablon_kod)
                with open(os.path.join(folder, "bot_vezerlo.py"), "w", encoding="utf-8") as f:
                    f.write(BOT_VEZERLO_CODE)
                with open(os.path.join(folder, "Panel.py"), "w", encoding="utf-8") as f:
                    f.write(PANEL_EXTENSION_CODE)
                with open(os.path.join(folder, "version.py"), "w", encoding="utf-8") as f:
                    f.write(VERSION_FILE_TEMPLATE)
                with open(os.path.join(folder, "info.py"), "w", encoding="utf-8") as f:
                    f.write(INFO_FILE_TEMPLATE)
                messagebox.showinfo(self.tr("success"),
                                     f"{self.tr('generated_files')}\n{folder}",
                                     parent=win)
            except OSError as e:
                messagebox.showerror(self.tr("errors"),
                                      f"{self.tr('generation_failed')}\n{e}", parent=win)

        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(btn_frame, text=self.tr("save_controller"),
                       fg_color="#27ae60", hover_color="#2ecc71",
                       command=save_bot_vezerlo_file).pack(side="left", padx=5)
        self.btn_integrate_panel = ctk.CTkButton(
            btn_frame, text=self.tr("integrate_panel"),
            fg_color="#16a085", hover_color="#1abc9c",
            command=save_panel_extension)
        self.btn_integrate_panel.pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=self.tr("generate_template"),
                       fg_color="#2980b9", hover_color="#3498db",
                       command=save_generated_files).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=self.tr("close"),
                       fg_color="#555555", command=win.destroy).pack(side="right", padx=5)

    # ==================================================================
    #  Függőségek fül
    # ==================================================================
    def _build_dependencies_tab(self, parent, parent_win):
        ctk.CTkLabel(
            parent, text="🔧  Panel függőségek kezelése",
            font=("Arial", 15, "bold"), text_color="#3498db"
        ).pack(pady=(12, 4))

        ctk.CTkLabel(
            parent,
            text="Ellenőrizd, hogy minden szükséges Python csomag telepítve van-e.\n"
                 "A hiányzó csomagokat egy kattintással telepítheted.",
            font=("Arial", 11), text_color="#aaa",
        ).pack(pady=(0, 10))

        # --- Görgethető lista a csomagokról ---
        list_frame = ctk.CTkScrollableFrame(parent, fg_color="#1e2129",
                                             corner_radius=10, height=260)
        list_frame.pack(fill="both", expand=True, padx=14, pady=6)

        # Tároló a package sorokhoz
        self._dep_rows = {}

        def check_package_status(pip_name, import_name):
            """Visszaadja: (telepítve?, verzió)"""
            try:
                spec = importlib.util.find_spec(import_name)
                if spec is None:
                    return False, "—"
                # Verzió lekérése (importlib.metadata)
                try:
                    import importlib.metadata as md
                    ver = md.version(pip_name)
                    return True, ver
                except Exception:
                    return True, "?"
            except Exception:
                return False, "—"

        def build_rows():
            for w in list_frame.winfo_children():
                w.destroy()
            self._dep_rows = {}

            all_pkgs = [(p, i, d, "required") for p, i, d in REQUIRED_PACKAGES]
            all_pkgs += [(p, i, d, "optional") for p, i, d in OPTIONAL_PACKAGES]

            for pip_name, import_name, desc, category in all_pkgs:
                row = ctk.CTkFrame(list_frame, fg_color="#252932", corner_radius=8)
                row.pack(fill="x", padx=4, pady=3)

                installed, version = check_package_status(pip_name, import_name)

                icon = "✅" if installed else ("⚠️" if category == "optional" else "❌")
                color = "#2ecc71" if installed else ("#f39c12" if category == "optional" else "#e74c3c")

                ctk.CTkLabel(row, text=icon, font=("Arial", 16), width=30).pack(side="left", padx=(10, 4), pady=8)

                info_frame = ctk.CTkFrame(row, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, pady=8)

                ctk.CTkLabel(
                    info_frame, text=pip_name,
                    font=("Consolas", 12, "bold"),
                    text_color=color, anchor="w"
                ).pack(fill="x")

                ctk.CTkLabel(
                    info_frame, text=desc,
                    font=("Arial", 10), text_color="#888", anchor="w"
                ).pack(fill="x")

                ver_text = f"v{version}" if installed else "hiányzik"
                ctk.CTkLabel(
                    row, text=ver_text,
                    font=("Consolas", 10, "bold"),
                    text_color=color, width=100
                ).pack(side="right", padx=10)

                self._dep_rows[pip_name] = {
                    "installed": installed,
                    "category": category,
                    "row": row,
                }

        # --- Gombok ---
        btn_row = ctk.CTkFrame(parent, fg_color="transparent")
        btn_row.pack(fill="x", padx=14, pady=(8, 4))

        status_label = ctk.CTkLabel(parent, text="", font=("Arial", 11),
                                     text_color="#aaa")
        status_label.pack(pady=(0, 4))

        progress = ctk.CTkProgressBar(parent, width=700)
        progress.set(0)
        progress.pack(pady=(0, 6))

        # Output box
        output_box = ctk.CTkTextbox(parent, height=100, font=("Consolas", 10))
        output_box.pack(fill="x", padx=14, pady=(0, 10))
        output_box.insert("1.0", "Kattints az „Ellenőrzés\" gombra a csomagok állapotának megtekintéséhez.\n")
        output_box.configure(state="disabled")

        def log_output(text):
            output_box.configure(state="normal")
            output_box.insert("end", text)
            output_box.see("end")
            output_box.configure(state="disabled")

        def refresh_status():
            build_rows()
            required_ok = sum(1 for p, _, _ in REQUIRED_PACKAGES
                              if self._dep_rows.get(p, {}).get("installed"))
            total_req = len(REQUIRED_PACKAGES)

            if required_ok == total_req:
                status_label.configure(
                    text=f"✅ Minden szükséges csomag telepítve van ({required_ok}/{total_req})",
                    text_color="#2ecc71"
                )
            else:
                missing = total_req - required_ok
                status_label.configure(
                    text=f"❌ {missing} szükséges csomag hiányzik ({required_ok}/{total_req})",
                    text_color="#e74c3c"
                )

        def install_packages(packages, reinstall=False):
            if not packages:
                messagebox.showinfo("Info", "Minden csomag telepítve van!", parent=parent_win)
                return

            log_output(f"\n{'='*60}\n")
            log_output(f"📦 Telepítés indul: {len(packages)} csomag\n")
            log_output(f"{'='*60}\n")

            progress.set(0)
            status_label.configure(text="⏳ Telepítés folyamatban...", text_color="#f39c12")

            def worker():
                total = len(packages)
                for i, pkg in enumerate(packages, 1):
                    cmd = [sys.executable, "-m", "pip", "install"]
                    if reinstall:
                        cmd.append("--upgrade")
                    cmd.append(pkg)

                    self.after(0, lambda p=pkg, idx=i, t=total: (
                        log_output(f"\n[{idx}/{t}] Telepítés: {p}\n"),
                        progress.set(idx / t),
                        status_label.configure(text=f"⏳ [{idx}/{t}] {p}...")
                    ))

                    try:
                        proc = subprocess.Popen(
                            cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True,
                            bufsize=1,
                            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                        )
                        for line in iter(proc.stdout.readline, ""):
                            self.after(0, lambda l=line: log_output(l))
                        proc.wait()
                        self.after(0, lambda p=pkg, c=proc.returncode: log_output(
                            f"{'✅' if c == 0 else '❌'} {p}: {'sikeres' if c == 0 else f'hiba (kód: {c})'}\n"
                        ))
                    except Exception as e:
                        self.after(0, lambda e=e, p=pkg: log_output(f"❌ {p}: {e}\n"))

                self.after(0, lambda: (
                    progress.set(1.0),
                    log_output(f"\n{'='*60}\n✅ Telepítés befejezve!\n{'='*60}\n"),
                    status_label.configure(text="✅ Telepítés kész!", text_color="#2ecc71"),
                    refresh_status(),
                ))

            threading.Thread(target=worker, daemon=True).start()

        def check_only():
            log_output("\n🔍 Csomagok ellenőrzése...\n")
            refresh_status()
            installed = sum(1 for r in self._dep_rows.values() if r["installed"])
            total = len(self._dep_rows)
            log_output(f"Telepítve: {installed}/{total}\n")

            missing_req = [p for p, _, _ in REQUIRED_PACKAGES
                           if not self._dep_rows.get(p, {}).get("installed")]
            if missing_req:
                log_output(f"Hiányzó (kötelező): {', '.join(missing_req)}\n")

        def install_missing():
            refresh_status()
            missing = [p for p, _, _ in REQUIRED_PACKAGES
                       if not self._dep_rows.get(p, {}).get("installed")]
            if not missing:
                messagebox.showinfo("Info", "Minden szükséges csomag telepítve van!",
                                     parent=parent_win)
                return
            if not messagebox.askyesno("Telepítés",
                                        f"Telepítse a hiányzó csomagokat?\n\n{chr(10).join(missing)}",
                                        parent=parent_win):
                return
            install_packages(missing)

        def reinstall_all():
            if not messagebox.askyesno(
                "Újratelepítés",
                "Újratelepíti az ÖSSZES csomagot (akár már telepítve van)?\n\n"
                "Ez eltarthat néhány percig.",
                parent=parent_win
            ):
                return
            all_pkgs = [p for p, _, _ in REQUIRED_PACKAGES]
            install_packages(all_pkgs, reinstall=True)

        ctk.CTkButton(
            btn_row, text="🔍  Ellenőrzés",
            fg_color="#3498db", hover_color="#5dade2",
            width=150, height=38, command=check_only
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            btn_row, text="📥  Hiányzók telepítése",
            fg_color="#27ae60", hover_color="#2ecc71",
            width=200, height=38, command=install_missing
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            btn_row, text="🔄  Mindent újratelepít",
            fg_color="#e67e22", hover_color="#d35400",
            width=200, height=38, command=reinstall_all
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            btn_row, text="📋  Requirements.txt mentés",
            fg_color="#8e44ad", hover_color="#9b59b6",
            width=220, height=38,
            command=lambda: self._save_requirements_txt()
        ).pack(side="right", padx=4)

        # Kezdeti ellenőrzés
        refresh_status()

    # ==================================================================
    #  Requirements.txt mentése
    # ==================================================================
    def _save_requirements_txt(self):
        path = os.path.join(config.SCRIPT_DIR, "requirements.txt")
        try:
            lines = []
            for pip_name, _, _ in REQUIRED_PACKAGES:
                lines.append(pip_name)
            for pip_name, _, _ in OPTIONAL_PACKAGES:
                lines.append(f"# {pip_name}  # opcionális")
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            self.notify("📋 requirements.txt mentve", "success")
            self.log_event("EVENT", f"[DEPS] requirements.txt mentve: {path}")
        except OSError as e:
            messagebox.showerror("Hiba", f"Nem sikerült menteni:\n{e}")