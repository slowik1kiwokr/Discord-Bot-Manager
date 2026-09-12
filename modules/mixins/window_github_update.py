import os
import sys
import shutil
import zipfile
import urllib.request
import threading
import subprocess
import datetime
from tkinter import messagebox

import customtkinter as ctk

import modules.config as config
from modules.languages import LANGUAGES

# --- GitHub konfiguráció (frissítve az új repóra) ---
GITHUB_USER = "slowik1kiwokr"
GITHUB_REPO = "Discord-Bot-Manager"
GITHUB_BRANCH = "main"

VERSION_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/version.txt"
CHANGELOG_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/changelog.txt"
ZIP_URL = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/archive/refs/heads/{GITHUB_BRANCH}.zip"

# Védett fájlok/mappák – ezeket az update NEM írja felül
PROTECTED_ITEMS = {
    "bots.json", "settings.json", "lang.json", "local_version.txt",
    "backups", "plugins", "logs", "panel_responses", "__pycache__",
    "discord_icon.ico", "temp_app_icon.ico",
    "panel_commands.json", "panel_broadcast_requests.json",
    ".git", ".github", ".gitignore", "README.md", "LICENSE",
    "requirements.txt", "update.zip", "update_extract",
}


class WindowGithubMixin:
    """Automatikus GitHub alapú frissítéskezelő."""

    # ------------------------------------------------------------------
    #  Verzióellenőrzés
    # ------------------------------------------------------------------
    def get_local_version(self):
        try:
            from version import version as local_v
            return str(local_v).strip()
        except Exception:
            return "0.0.0"

    def fetch_remote_version(self, timeout=6):
        try:
            req = urllib.request.Request(VERSION_URL, headers={"Cache-Control": "no-cache"})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read().decode("utf-8").strip()
        except Exception as error:
            print(f"[UPDATE] Nem sikerült a verzió leolvasása: {error}")
            return None

    def fetch_changelog(self, timeout=6):
        try:
            req = urllib.request.Request(CHANGELOG_URL, headers={"Cache-Control": "no-cache"})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read().decode("utf-8").strip()
        except Exception:
            return ""

    # ------------------------------------------------------------------
    #  Csendes, automatikus ellenőrzés
    # ------------------------------------------------------------------
    def check_for_updates(self, silent=True):
        if not silent:
            self.log_event("EVENT", "[UPDATE] Manuális frissítésellenőrzés indítva.")

        def worker():
            remote_version = self.fetch_remote_version()
            local_version = self.get_local_version()

            if remote_version is None:
                if not silent:
                    self.after(0, lambda: messagebox.showerror(
                        "Frissítés",
                        "Nem sikerült kapcsolódni a GitHubhoz.\n"
                        "Ellenőrizd az internetkapcsolatot!"
                    ))
                return

            if remote_version == local_version:
                if not silent:
                    self.after(0, lambda: messagebox.showinfo(
                        "Frissítés",
                        f"A panel naprakész!\n\nJelenlegi verzió: {local_version}"
                    ))
                return

            changelog = self.fetch_changelog()
            self.after(0, lambda: self.ask_update(remote_version, local_version, changelog))

        threading.Thread(target=worker, daemon=True).start()

    def schedule_update_check(self, interval_minutes=60):
        self.check_for_updates(silent=True)
        self.after(
            interval_minutes * 60 * 1000,
            lambda: self.schedule_update_check(interval_minutes)
        )

    # ------------------------------------------------------------------
    #  Felugró ablak új verzió esetén
    # ------------------------------------------------------------------
    def ask_update(self, remote_version, local_version, changelog=""):
        win = ctk.CTkToplevel(self)
        win.title("Frissítés elérhető")
        win.geometry("520x420")
        win.resizable(False, False)
        win.grab_set()

        win.update_idletasks()
        x = (win.winfo_screenwidth() - 520) // 2
        y = (win.winfo_screenheight() - 420) // 2
        win.geometry(f"520x420+{x}+{y}")

        ctk.CTkLabel(
            win, text="🚀 Új verzió érhető el!",
            font=("Arial", 20, "bold"), text_color="#5865F2"
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            win, text=f"Jelenlegi: {local_version}  →  Új: {remote_version}",
            font=("Arial", 13)
        ).pack(pady=5)

        if changelog:
            ctk.CTkLabel(
                win, text="📝 Újdonságok:", font=("Arial", 12, "bold"), anchor="w"
            ).pack(padx=25, anchor="w", pady=(10, 2))
            log_box = ctk.CTkTextbox(win, height=140, font=("Consolas", 11))
            log_box.pack(fill="x", padx=25, pady=5)
            log_box.insert("1.0", changelog)
            log_box.configure(state="disabled")

        status_label = ctk.CTkLabel(win, text="", font=("Arial", 11), text_color="#aaaaaa")
        status_label.pack(pady=6)

        progress = ctk.CTkProgressBar(win, width=420)
        progress.set(0)
        progress.pack(pady=(2, 10))

        def start_download():
            yes_btn.configure(state="disabled")
            no_btn.configure(state="disabled")
            threading.Thread(
                target=self._download_and_install,
                args=(remote_version, win, status_label, progress),
                daemon=True
            ).start()

        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=10)

        yes_btn = ctk.CTkButton(
            btn_frame, text="✅ Igen, frissítek",
            fg_color="#27ae60", hover_color="#2ecc71",
            width=180, command=start_download
        )
        yes_btn.pack(side="left", padx=6)

        no_btn = ctk.CTkButton(
            btn_frame, text="❌ Most nem",
            fg_color="#c0392b", hover_color="#e74c3c",
            width=180, command=win.destroy
        )
        no_btn.pack(side="left", padx=6)

    # ------------------------------------------------------------------
    #  Letöltés + telepítés
    # ------------------------------------------------------------------
    def _download_and_install(self, remote_version, win, status_label, progress):
        try:
            self.after(0, lambda: status_label.configure(text="📥 ZIP letöltése..."))
            self.after(0, lambda: progress.set(0.1))

            temp_zip = os.path.join(config.SCRIPT_DIR, "update.zip")
            extract_dir = os.path.join(config.SCRIPT_DIR, "update_extract")

            for path in (temp_zip, extract_dir):
                if os.path.exists(path):
                    if os.path.isdir(path):
                        shutil.rmtree(path, ignore_errors=True)
                    else:
                        os.remove(path)

            urllib.request.urlretrieve(ZIP_URL, temp_zip)
            self.after(0, lambda: progress.set(0.45))
            self.after(0, lambda: status_label.configure(text="📦 Kicsomagolás..."))

            with zipfile.ZipFile(temp_zip, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
            self.after(0, lambda: progress.set(0.6))

            root_folder = os.listdir(extract_dir)[0]
            full_root = os.path.join(extract_dir, root_folder)

            # A fájlok a gyökérben vannak (nincs 'panel' almappa)
            panel_folder = full_root

            self.after(0, lambda: status_label.configure(text="💾 Fájlok másolása..."))
            self.after(0, lambda: progress.set(0.75))

            for bot in self.bots.values():
                if bot.get("is_running") and bot.get("process"):
                    try:
                        bot["process"].terminate()
                    except Exception:
                        pass

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

            self.after(0, lambda: progress.set(0.95))

            try:
                with open(os.path.join(config.SCRIPT_DIR, "version.py"), "w", encoding="utf-8") as vf:
                    vf.write(f'version = "{remote_version}"\n')
            except Exception as e:
                print(f"[UPDATE] version.py írási hiba: {e}")

            try:
                os.remove(temp_zip)
                shutil.rmtree(extract_dir, ignore_errors=True)
            except Exception:
                pass

            self.after(0, lambda: progress.set(1.0))
            self.after(0, lambda: status_label.configure(text="✅ Telepítés kész! Újraindítás..."))

            self.after(1500, lambda: self._restart_panel(win, remote_version))

        except Exception as error:
            error_message = str(error)
            self.after(0, lambda: messagebox.showerror(
                "Frissítési hiba",
                f"Nem sikerült a frissítés:\n{error_message}",
                parent=win
            ))
            self.after(0, lambda: status_label.configure(text="❌ Hiba történt"))
            self.after(0, lambda: progress.set(0))

    def _restart_panel(self, win, new_version):
        self.log_event("EVENT", f"[UPDATE] Panel újraindítás a(z) {new_version} verzióval.")

        try:
            if win and win.winfo_exists():
                win.destroy()
        except Exception:
            pass

        try:
            self.save_config()
        except Exception:
            pass

        try:
            self.stop_tray()
        except Exception:
            pass

        for bot in self.bots.values():
            if bot.get("is_running") and bot.get("process"):
                try:
                    bot["process"].terminate()
                except Exception:
                    pass

        script_path = os.path.abspath(sys.argv[0])
        python_exe = sys.executable

        try:
            subprocess.Popen([python_exe, script_path], cwd=config.SCRIPT_DIR)
        except Exception as e:
            messagebox.showerror("Újraindítási hiba", str(e))
            return

        self.destroy()
        sys.exit(0)

    # ------------------------------------------------------------------
    #  Sidebar gombhoz
    # ------------------------------------------------------------------
    def update_from_github(self, mode="manual"):
        self.check_for_updates(silent=False)
