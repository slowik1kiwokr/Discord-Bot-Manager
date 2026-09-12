import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog

import modules.config as config
from modules.languages import LANGUAGES


class WindowGithubMixin:
    def update_from_github(self, new_version):
        import urllib.request
        import zipfile
        import os
        import shutil
        import sys
        import logging

        print("Frissítés indítása...")

        # 1) Botok leállítása
        try:
            for bot in self.bots.values():
                if bot["is_running"] and bot["process"]:
                    bot["process"].terminate()
            print("Botok leállítva.")
        except Exception as e:
            print("Bot leállítás hiba:", e)

        # 2) Log rendszer lezárása
        try:
            logging.shutdown()
            print("Log rendszer lezárva.")
        except Exception as e:
            print("Log lezárási hiba:", e)

        # 3) ZIP letöltése
        url = "https://github.com/slowik1kiwokr/Panel-Update/archive/refs/heads/main.zip"
        temp_zip = "update.zip"
        extract_dir = "update_extract"

        try:
            print("ZIP letöltése GitHubról...")
            urllib.request.urlretrieve(url, temp_zip)
            print("ZIP letöltve:", temp_zip)
        except Exception as e:
            print("ZIP letöltési hiba:", e)
            return

        # 4) Kicsomagolás
        try:
            print("ZIP kicsomagolása...")
            with zipfile.ZipFile(temp_zip, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
            print("Kicsomagolva:", extract_dir)
        except Exception as e:
            print("Kicsomagolási hiba:", e)
            return

        # 5) ZIP fő mappa
        try:
            root_folder = os.listdir(extract_dir)[0]
            full_root_path = os.path.join(extract_dir, root_folder)
            print("Fő mappa:", full_root_path)
        except Exception as e:
            print("Fő mappa keresési hiba:", e)
            return

        # 6) Panel mappa dinamikus keresése
        panel_folder = None
        for root, dirs, files in os.walk(full_root_path):
            if "panel.pyw" in files:
                panel_folder = root
                break

        if not panel_folder:
            print("Nem található panel.pyw a ZIP-ben!")
            return

        print("Panel mappa megtalálva:", panel_folder)

        # 7) Fájlok átmásolása
        try:
            print("Fájlok másolása...")
            for item in os.listdir(panel_folder):
                src = os.path.join(panel_folder, item)
                dst = os.path.join(os.getcwd(), item)

                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

            print("Fájlok sikeresen átmásolva.")
        except Exception as e:
            print("Fájlmásolási hiba:", e)
            return

        # 8) Takarítás
        try:
            os.remove(temp_zip)
            shutil.rmtree(extract_dir)
            print("Ideiglenes fájlok törölve.")
        except Exception as e:
            print("Takarítási hiba:", e)

        # 9) Verziószám frissítése
        try:
            with open("local_version.txt", "w") as f:
                f.write(new_version)
            print("Verzió frissítve:", new_version)
        except Exception as e:
            print("Verzió frissítési hiba:", e)

        # 10) Panel újraindítása
        print("Frissítés sikeres! A panel újraindul.")
        os.execv(sys.executable, ['python'] + sys.argv)

    def check_for_updates(self):
        import urllib.request
        import os

        github_version_url = "https://raw.githubusercontent.com/slowik1kiwokr/Panel-Update/main/panel%20v1.0.5/panel/version.txt"
        local_version_file = "local_version.txt"

        try:
            github_version = urllib.request.urlopen(github_version_url).read().decode().strip()

            if not os.path.exists(local_version_file):
                with open(local_version_file, "w") as f:
                    f.write("0.0.0")

            with open(local_version_file, "r") as f:
                local_version = f.read().strip()

            if github_version != local_version:
                self.ask_update(github_version)

        except Exception as e:
            print("Nem sikerült ellenőrizni a frissítést:", e)

    def ask_update(self, new_version):
        win = ctk.CTkToplevel(self)
        win.title("Frissítés elérhető")
        win.geometry("350x180")
        win.grab_set()

        ctk.CTkLabel(win, text=f"Új verzió elérhető: {new_version}", font=("Arial", 15, "bold")).pack(pady=10)
        ctk.CTkLabel(win, text="Szeretnéd telepíteni a frissítést?", font=("Arial", 12)).pack(pady=5)

        def yes():
            win.destroy()
            self.update_from_github(new_version)

        def no():
            win.destroy()

        ctk.CTkButton(win, text="Igen, frissítek", fg_color="#27ae60", command=yes).pack(pady=5)
        ctk.CTkButton(win, text="Nem", fg_color="#c0392b", command=no).pack(pady=5)