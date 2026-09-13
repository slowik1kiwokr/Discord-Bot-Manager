import os
import sys
import shutil
import zipfile
import urllib.request
import threading
import subprocess
from tkinter import messagebox

import customtkinter as ctk

import modules.config as config
from version import version as LOCAL_VERSION


# --- GitHub konfiguráció ---
GITHUB_USER = "slowik1kiwokr"
GITHUB_REPO = "Discord-Bot-Manager"
GITHUB_BRANCH = "main"

VERSION_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/version.txt"
CHANGELOG_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/changelog.txt"
ZIP_URL = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/archive/refs/heads/{GITHUB_BRANCH}.zip"

# Ezeket a fájlokat/mappákat NEM írjuk felül update közben
PROTECTED_ITEMS = {
    "bots.json", "settings.json", "lang.json", "local_version.txt",
    "backups", "plugins", "logs", "panel_responses", "__pycache__",
    "icon.ico", "icon.jpg", "logo.jpg", "logo.png", "dc_logo.ico",
    "temp_app_icon.ico", "_icon_temp.ico",
    "panel_commands.json", "panel_broadcast_requests.json",
    ".git", ".github", ".gitignore", "README.md", "LICENSE",
    "requirements.txt", "update.zip", "update_extract",
}


class WindowGithubMixin:
    """Automatikus GitHub alapú frissítéskezelő."""

    # ==================================================================
    #  Verzió lekérdezés
    # ==================================================================
    def get_local_version(self):
        try:
            return str(LOCAL_VERSION).strip()
        except Exception:
            return "0.0.0"

    def fetch_remote_version(self, timeout=6):
        try:
            req = urllib.request.Request(VERSION_URL,
                                         headers={"Cache-Control": "no-cache"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8").strip()
        except Exception as e:
            print(f"[UPDATE] Verzió lekérdezési hiba: {e}")
            return None

    def fetch_changelog(self, timeout=6):
        try:
            req = urllib.request.Request(CHANGELOG_URL,
                                         headers={"Cache-Control": "no-cache"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8").strip()
        except Exception:
            return ""

    # ==================================================================
    #  Frissítés keresés
    # ==================================================================
    def check_for_updates(self, silent=True):
        if not silent:
            self.log_event("EVENT", "[UPDATE] Manuális frissítésellenőrzés indítva.")

        def worker():
            remote = self.fetch_remote_version()
            local = self.get_local_version()

            if remote is None:
                if not silent:
                    self.after(0, lambda: messagebox.showerror(
                        "Frissítés",
                        "Nem sikerült kapcsolódni a GitHubhoz.\n"
                        "Ellenőrizd az internetkapcsolatot!"
                    ))
                return

            # Ha ezt a verziót kihagytuk, ne jelezzük újra
            skipped = getattr(self, "skipped_version", None)
            if skipped and skipped == remote:
                return

            if remote == local:
                if not silent:
                    self.after(0, lambda: messagebox.showinfo(
                        "Frissítés",
                        f"A panel naprakész!\n\nJelenlegi verzió: {local}"
                    ))
                return

            changelog = self.fetch_changelog()
            self.after(0, lambda: self.show_update_dialog(remote, local, changelog))

        threading.Thread(target=worker, daemon=True).start()

    def schedule_update_check(self, interval_minutes=60):
        self.check_for_updates(silent=True)
        self.after(interval_minutes * 60 * 1000,
                   lambda: self.schedule_update_check(interval_minutes))

    # ==================================================================
    #  Frissítés ablak (changelog + letöltés + újraindítás)
    # ==================================================================
    def show_update_dialog(self, remote_version, local_version, changelog):
        win = ctk.CTkToplevel(self)
        win.title("🚀 Frissítés elérhető")
        win.geometry("620x640")
        win.minsize(520, 480)
        win.grab_set()
        win.resizable(False, False)

        win.update_idletasks()
        x = (win.winfo_screenwidth() - 620) // 2
        y = (win.winfo_screenheight() - 640) // 2
        win.geometry(f"620x640+{x}+{y}")

        # --- Fejléc ---
        header = ctk.CTkFrame(win, fg_color="#5865F2", corner_radius=0, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text="🚀 Új verzió érhető el!",
            font=("Arial", 22, "bold"), text_color="white"
        ).pack(pady=(18, 0))
        ctk.CTkLabel(
            header, text=f"{local_version}  →  {remote_version}",
            font=("Arial", 13), text_color="#dcdcdc"
        ).pack(pady=(0, 10))

        # --- Changelog ---
        ctk.CTkLabel(
            win, text="📝 Újdonságok és változások:",
            font=("Arial", 14, "bold"), anchor="w"
        ).pack(fill="x", padx=20, pady=(16, 4))

        changelog_box = ctk.CTkTextbox(win, height=280,
                                        font=("Consolas", 12), wrap="word")
        changelog_box.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        if changelog:
            changelog_box.insert("1.0", changelog)
        else:
            changelog_box.insert(
                "1.0",
                "ℹ️ A fejlesztő nem adott meg changelog-ot ehhez a verzióhoz.\n\n"
                "A frissítés a legújabb kódot tölti le a GitHub-ról."
            )
        changelog_box.configure(state="disabled")

        # --- Infó ---
        ctk.CTkLabel(
            win,
            text="ℹ️ A mentések, pluginok, beállítások és botok megmaradnak.",
            font=("Arial", 11), text_color="#aaaaaa"
        ).pack(pady=(0, 4))

        # --- Státusz ---
        status_label = ctk.CTkLabel(win, text="",
                                     font=("Arial", 11), text_color="#aaaaaa")
        status_label.pack(pady=(0, 2))

        progress = ctk.CTkProgressBar(win, width=520)
        progress.set(0)
        progress.pack(pady=(0, 12))

        # --- Gombok ---
        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=(0, 16))

        def start_download():
            yes_btn.configure(state="disabled")
            later_btn.configure(state="disabled")
            skip_btn.configure(state="disabled")
            threading.Thread(
                target=self._download_and_install,
                args=(remote_version, win, status_label, progress),
                daemon=True
            ).start()

        yes_btn = ctk.CTkButton(
            btn_frame, text="✅ Frissítés letöltése",
            fg_color="#27ae60", hover_color="#2ecc71",
            width=180, height=42, font=("Arial", 13, "bold"),
            command=start_download
        )
        yes_btn.pack(side="left", padx=6)

        later_btn = ctk.CTkButton(
            btn_frame, text="⏰ Később",
            fg_color="#f39c12", hover_color="#e67e22",
            width=130, height=42, font=("Arial", 13),
            command=win.destroy
        )
        later_btn.pack(side="left", padx=6)

        skip_btn = ctk.CTkButton(
            btn_frame, text="❌ Kihagyás",
            fg_color="#7f8c8d", hover_color="#95a5a6",
            width=130, height=42, font=("Arial", 13),
            command=lambda: self._skip_this_version(remote_version, win)
        )
        skip_btn.pack(side="left", padx=6)

    # ==================================================================
    #  Verzió kihagyása
    # ==================================================================
    def _skip_this_version(self, version, win):
        if not messagebox.askyesno(
            "Verzió kihagyása",
            f"Biztosan kihagyod a(z) {version} verziót?\n\n"
            f"Amíg újra nem indítod a panelt, nem fogod látni ezt a jelzést.",
            parent=win
        ):
            return
        self.skipped_version = version
        self.log_event("EVENT", f"[UPDATE] Kihagyott verzió: {version}")
        win.destroy()

    # ==================================================================
    #  Letöltés + telepítés
    # ==================================================================
    def _download_and_install(self, remote_version, win, status_label, progress):
        try:
            def set_status(text, value=None):
                self.after(0, lambda: status_label.configure(text=text))
                if value is not None:
                    self.after(0, lambda: progress.set(value))

            set_status("📥 ZIP letöltése a GitHub-ról...", 0.1)

            temp_zip = os.path.join(config.SCRIPT_DIR, "update.zip")
            extract_dir = os.path.join(config.SCRIPT_DIR, "update_extract")

            for path in (temp_zip, extract_dir):
                if os.path.exists(path):
                    if os.path.isdir(path):
                        shutil.rmtree(path, ignore_errors=True)
                    else:
                        os.remove(path)

            urllib.request.urlretrieve(ZIP_URL, temp_zip)
            set_status("📦 Kicsomagolás...", 0.4)

            with zipfile.ZipFile(temp_zip, "r") as zf:
                zf.extractall(extract_dir)
            set_status("🔍 Fájlok előkészítése...", 0.55)

            root_folder = os.listdir(extract_dir)[0]
            full_root = os.path.join(extract_dir, root_folder)
            panel_folder = full_root

            # Ha van 'panel' almappa a repóban, azt használjuk
            candidate = os.path.join(full_root, "panel")
            if os.path.isdir(candidate):
                panel_folder = candidate

            # Botok leállítása
            set_status("🛑 Futó botok leállítása...", 0.65)
            for bot in self.bots.values():
                if bot.get("is_running") and bot.get("process"):
                    try:
                        bot["process"].terminate()
                    except Exception:
                        pass

            # Fájlok másolása (védett elemek kihagyásával)
            set_status("💾 Fájlok frissítése...", 0.75)
            for item in os.listdir(panel_folder):
                if item in PROTECTED_ITEMS:
                    continue
                src = os.path.join(panel_folder, item)
                dst = os.path.join(config.SCRIPT_DIR, item)

                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst, ignore_errors=True)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

            set_status("🏷️ Verziószám frissítése...", 0.9)

            # version.py frissítése
            try:
                with open(os.path.join(config.SCRIPT_DIR, "version.py"),
                          "w", encoding="utf-8") as vf:
                    vf.write(f'version = "{remote_version}"\n')
            except Exception as e:
                print(f"[UPDATE] version.py írási hiba: {e}")

            # Takarítás
            try:
                os.remove(temp_zip)
                shutil.rmtree(extract_dir, ignore_errors=True)
            except Exception:
                pass

            set_status("✅ Telepítés kész!", 1.0)
            self.log_event("EVENT",
                           f"[UPDATE] Telepítve: {remote_version}. Újraindítás...")

            self.after(800, lambda: self._ask_restart(win, remote_version))

        except Exception as error:
            error_msg = str(error)
            self.after(0, lambda: messagebox.showerror(
                "Frissítési hiba",
                f"Nem sikerült a frissítés:\n\n{error_msg}\n\n"
                f"Ellenőrizd az internetkapcsolatot, vagy próbáld újra később.",
                parent=win
            ))
            set_status("❌ Hiba történt", 0)

    # ==================================================================
    #  Újraindítás kérdés
    # ==================================================================
    def _ask_restart(self, win, new_version):
        try:
            if win and win.winfo_exists():
                win.destroy()
        except Exception:
            pass

        restart_dialog = ctk.CTkToplevel(self)
        restart_dialog.title("Újraindítás szükséges")
        restart_dialog.geometry("460x320")
        restart_dialog.resizable(False, False)
        restart_dialog.grab_set()
        restart_dialog.update_idletasks()
        x = (restart_dialog.winfo_screenwidth() - 460) // 2
        y = (restart_dialog.winfo_screenheight() - 320) // 2
        restart_dialog.geometry(f"460x320+{x}+{y}")

        ctk.CTkLabel(
            restart_dialog, text="✅ Frissítés sikeres!",
            font=("Arial", 18, "bold"), text_color="#2ecc71"
        ).pack(pady=(20, 4))

        ctk.CTkLabel(
            restart_dialog,
            text=f"A panel a(z) {new_version} verzióra frissült.",
            font=("Arial", 12)
        ).pack(pady=4)

        ctk.CTkLabel(
            restart_dialog,
            text="Újra kell indítani a panelt, hogy életbe lépjenek a változások.",
            font=("Arial", 11), text_color="#aaaaaa",
            wraplength=420,
        ).pack(pady=(4, 10))

        info = ctk.CTkFrame(restart_dialog, fg_color="#2b2b2b", corner_radius=8)
        info.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(
            info,
            text="💡 A mentések, pluginok és botok megmaradnak.",
            font=("Arial", 11), text_color="#cccccc"
        ).pack(pady=8)

        btn_frame = ctk.CTkFrame(restart_dialog, fg_color="transparent")
        btn_frame.pack(pady=14)

        def do_restart():
            restart_dialog.destroy()
            self._perform_restart()

        ctk.CTkButton(
            btn_frame, text="🔄 Újraindítás most",
            fg_color="#27ae60", hover_color="#2ecc71",
            width=170, height=40, font=("Arial", 13, "bold"),
            command=do_restart
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            btn_frame, text="🚪 Kilépés",
            fg_color="#c0392b", hover_color="#e74c3c",
            width=120, height=40, font=("Arial", 13),
            command=lambda: (restart_dialog.destroy(), self.perform_exit())
        ).pack(side="left", padx=6)

    # ==================================================================
    #  Újraindítás végrehajtása
    # ==================================================================
    def _perform_restart(self):
        self.log_event("EVENT", "[UPDATE] Panel újraindítás...")

        try:
            self.save_config()
        except Exception:
            pass

        try:
            self.stop_tray()
        except Exception:
            pass

        # Botok leállítása
        for bot in self.bots.values():
            if bot.get("is_running") and bot.get("process"):
                try:
                    bot["process"].terminate()
                except Exception:
                    pass

        # Újraindítás subprocess-szel (pyw-kompatibilis)
        script_path = os.path.abspath(sys.argv[0])
        python_exe = sys.executable

        try:
            subprocess.Popen([python_exe, script_path], cwd=config.SCRIPT_DIR)
        except Exception as e:
            messagebox.showerror("Újraindítási hiba", str(e))
            return

        try:
            self.destroy()
        except Exception:
            pass
        os._exit(0)

    # ==================================================================
    #  Kompatibilitás a sidebar gombhoz
    # ==================================================================
    def update_from_github(self, mode="manual"):
        """Sidebar 'GitHub Frissítés' gombja ezt hívja."""
        self.check_for_updates(silent=False)