import os
import sys
import shutil
import zipfile
import urllib.request
import threading
import subprocess
import datetime
import json
import re
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

# Védett fájlok
PROTECTED_ITEMS = {
    "bots.json", "settings.json", "lang.json", "local_version.txt",
    "backups", "plugins", "logs", "panel_responses", "__pycache__",
    "icon.ico", "icon.jpg", "logo.jpg", "logo.png", "dc_logo.ico",
    "temp_app_icon.ico", "_icon_temp.ico",
    "panel_commands.json", "panel_broadcast_requests.json",
    ".git", ".github", ".gitignore", "README.md", "LICENSE",
    "requirements.txt", "update.zip", "update_extract",
    "achievements.json", "streak.json", "panel_stats.json",
    "update_history.json",
}


class WindowGithubMixin:
    """Automatikus GitHub frissítéskezelő."""

    # ==================================================================
    #  Segéd metódusok
    # ==================================================================
    def _update_history_path(self):
        return os.path.join(config.SCRIPT_DIR, "update_history.json")

    def _load_update_history(self):
        path = self._update_history_path()
        if not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return []

    def _save_update_history(self, history):
        path = self._update_history_path()
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=4)
        except OSError:
            pass

    def _add_to_history(self, version, title, description):
        history = self._load_update_history()
        # Ha már benne van, frissítjük
        history = [h for h in history if h.get("version") != version]
        history.insert(0, {
            "version": version,
            "title": title,
            "description": description,
            "date": datetime.datetime.now().isoformat(timespec="seconds"),
        })
        # Max 50 bejegyzés
        self._save_update_history(history[:50])

    def _parse_changelog(self, text):
        """A changelog.txt-t szekciókra bontja.

        Visszaad: [
            {"version": "1.0.6", "title": "...", "content": "..."},
            ...
        ]
        """
        if not text:
            return []

        lines = text.split("\n")
        sections = []
        current = None

        version_pattern = re.compile(r"^[vV]?\s*(\d+\.\d+(?:\.\d+)?)", re.IGNORECASE)

        for line in lines:
            stripped = line.strip()
            match = version_pattern.match(stripped)
            if match and len(stripped) < 60:
                # Új verzió kezdete
                if current:
                    sections.append(current)
                # Verzió cím
                version_str = match.group(1)
                # A cím a többi rész (ha van)
                title = stripped
                current = {
                    "version": version_str,
                    "title": title,
                    "content": "",
                }
            else:
                if current is not None:
                    current["content"] += line + "\n"
                elif stripped:
                    # Ha még nincs verzió, az elejét egy "Általános" szekcióba tesszük
                    if not sections and current is None:
                        current = {
                            "version": "",
                            "title": "Általános",
                            "content": line + "\n",
                        }

        if current:
            sections.append(current)

        # Tisztítás: levágjuk a felesleges üres sorokat, elválasztó vonalakat
        for s in sections:
            content = s["content"]
            # Levágjuk az elválasztó vonalakat (━━━, ===, ---)
            content = re.sub(r"^[━═=\-─]{5,}\s*$", "", content, flags=re.MULTILINE)
            # Több egymást követő üres sor → 1
            content = re.sub(r"\n{3,}", "\n\n", content)
            s["content"] = content.strip()

        return sections

    # ==================================================================
    #  Verzió lekérdezés
    # ==================================================================
    def get_local_version(self):
        try:
            return str(LOCAL_VERSION).strip()
        except Exception:
            return "0.0.0"

    def fetch_remote_version(self, timeout=8):
        try:
            req = urllib.request.Request(
                VERSION_URL,
                headers={"Cache-Control": "no-cache", "User-Agent": "DBM-Panel"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8").strip()
        except Exception as e:
            print(f"[UPDATE] Verzió lekérdezési hiba: {e}")
            return None

    def fetch_changelog(self, timeout=8):
        try:
            req = urllib.request.Request(
                CHANGELOG_URL,
                headers={"Cache-Control": "no-cache", "User-Agent": "DBM-Panel"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8").strip()
        except Exception:
            return ""

    # ==================================================================
    #  Frissítés keresés (auto + manuális)
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

            # ÚJ VERZIÓ VAN!
            changelog = self.fetch_changelog()
            sections = self._parse_changelog(changelog)

            # Megkeressük az aktuális frissítés szekcióját
            current_section = None
            for s in sections:
                if s["version"] == remote or s["version"].lstrip("v") == remote.lstrip("v"):
                    current_section = s
                    break

            if not current_section and sections:
                current_section = sections[0]

            self.after(0, lambda: self.show_update_dialog(
                remote, local, current_section, sections
            ))

        threading.Thread(target=worker, daemon=True).start()

    def schedule_update_check(self, interval_minutes=None, run_now=True):
        """Automatikus frissítés-ellenőrzés ütemezése.

        interval_minutes:
            0     → soha
            1     → percenként
            10    → 10 percenként
            60    → óránként
            1440  → naponta
        """
        # Régi ütemezés törlése
        try:
            if getattr(self, "_update_check_after_id", None):
                self.after_cancel(self._update_check_after_id)
                self._update_check_after_id = None
        except Exception:
            pass

        if interval_minutes is None:
            interval_minutes = getattr(self, "update_check_interval_minutes", 60)

        if interval_minutes <= 0:
            self.log_event("EVENT", "[UPDATE] Auto-ellenőrzés kikapcsolva.")
            return

        # Induláskor rögtön ellenőrzünk (ha kell)
        if run_now:
            self._update_check_after_id = self.after(
                3000, lambda: self.check_for_updates(silent=True)
            )
        else:
            self._update_check_after_id = self.after(
                interval_minutes * 60 * 1000,
                lambda: self.check_for_updates(silent=True)
            )
            # Újraütemezés a következő ciklusra
            self.after(
                interval_minutes * 60 * 1000 + 5000,
                lambda: self.schedule_update_check(
                    interval_minutes=interval_minutes, run_now=False
                )
            )

    # ==================================================================
    #  Frissítés ablak
    # ==================================================================
    def show_update_dialog(self, remote_version, local_version, section, all_sections):
        # AFK screen bezárása, hogy ne takarja ki az update ablakot
        try:
            if hasattr(self, "_close_afk_screen"):
                self._close_afk_screen()
            if hasattr(self, "_afk_last_activity"):
                import time as _t
                self._afk_last_activity = _t.time()
        except Exception:
            pass

        # Flag: ne jelenjen meg az AFK screen, amíg ez az ablak nyitva van
        self._update_dialog_open = True

        win = ctk.CTkToplevel(self)
        win.title("🚀 Frissítés elérhető")
        try:
            win.attributes("-topmost", True)
            win.lift()
            win.focus_force()
        except Exception:
            pass
        win.geometry("720x780")
        win.minsize(640, 600)
        win.grab_set()
        win.resizable(False, False)

        win.update_idletasks()
        x = (win.winfo_screenwidth() - 720) // 2
        y = (win.winfo_screenheight() - 780) // 2
        win.geometry(f"720x780+{x}+{y}")

        # --- Fejléc ---
        header = ctk.CTkFrame(win, fg_color="#5865F2", corner_radius=0, height=100)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="🚀  Új verzió érhető el!",
            font=("Arial", 22, "bold"), text_color="white"
        ).pack(pady=(18, 2))

        ctk.CTkLabel(
            header, text=f"{local_version}    →    {remote_version}",
            font=("Consolas", 14, "bold"), text_color="#dcdcff"
        ).pack(pady=(0, 12))

        # --- Changelog cím ---
        title_text = "📝  Újdonságok"
        if section and section.get("title"):
            title_text = f"📝  {section['title']}"

        ctk.CTkLabel(
            win, text=title_text,
            font=("Arial", 15, "bold"), anchor="w", text_color="#ffffff"
        ).pack(fill="x", padx=24, pady=(16, 4))

        # --- Changelog tartalom ---
        changelog_frame = ctk.CTkFrame(win, fg_color="#0a0c10", corner_radius=10,
                                         border_width=1, border_color="#2f3542")
        changelog_frame.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        changelog_box = ctk.CTkTextbox(
            changelog_frame, font=("Consolas", 12), wrap="word",
            fg_color="transparent",
        )
        changelog_box.pack(fill="both", expand=True, padx=4, pady=4)

        if section and section.get("content"):
            content = section["content"]
            # Szép formázás
            content = content.replace("  • ", "  ▸  ").replace("  - ", "  ▸  ")
            changelog_box.insert("1.0", content)
        else:
            changelog_box.insert(
                "1.0",
                "ℹ️  Ehhez a verzióhoz nincs changelog bejegyzés.\n\n"
                "A frissítés a legújabb kódot tölti le a GitHub-ról."
            )
        changelog_box.configure(state="disabled")

        # --- Info ---
        info = ctk.CTkFrame(win, fg_color="#1a1d24", corner_radius=8,
                             border_width=1, border_color="#2f3542")
        info.pack(fill="x", padx=24, pady=(0, 10))

        ctk.CTkLabel(
            info,
            text="ℹ️   A mentések, pluginok, beállítások és botok megmaradnak.",
            font=("Arial", 11), text_color="#b8bcc6"
        ).pack(padx=14, pady=10)

        # --- Státusz ---
        status_label = ctk.CTkLabel(
            win, text="", font=("Arial", 11), text_color="#8a8e98"
        )
        status_label.pack(pady=(0, 4))

        progress = ctk.CTkProgressBar(win, width=660, height=8,
                                        progress_color="#5865F2")
        progress.set(0)
        progress.pack(pady=(0, 12))

        # --- Gombok ---
        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=(0, 8), fill="x", padx=24)

        def start_download():
            yes_btn.configure(state="disabled")
            later_btn.configure(state="disabled")
            skip_btn.configure(state="disabled")
            history_btn.configure(state="disabled")
            threading.Thread(
                target=self._download_and_install,
                args=(remote_version, win, status_label, progress),
                daemon=True
            ).start()

        yes_btn = ctk.CTkButton(
            btn_frame, text="✅   Frissítés letöltése",
            fg_color="#27ae60", hover_color="#2ecc71",
            width=200, height=46, font=("Arial", 13, "bold"),
            corner_radius=8, command=start_download
        )
        yes_btn.pack(side="left", padx=4)

        later_btn = ctk.CTkButton(
            btn_frame, text="⏰   Később",
            fg_color="#f39c12", hover_color="#e67e22",
            width=130, height=46, font=("Arial", 13),
            corner_radius=8,
            command=lambda: (setattr(self, "_update_dialog_open", False), win.destroy())
        )

        skip_btn = ctk.CTkButton(
            btn_frame, text="❌   Kihagyás",
            fg_color="#7f8c8d", hover_color="#95a5a6",
            width=130, height=46, font=("Arial", 13),
            corner_radius=8,
            command=lambda: self._skip_this_version(remote_version, win)
        )
        skip_btn.pack(side="left", padx=4)

        # --- Előző frissítések gomb ---
        history_btn = ctk.CTkButton(
            win, text="📜   Előző frissítések megtekintése",
            fg_color="transparent", hover_color="#2f3542",
            text_color="#8a8e98", border_width=1, border_color="#2f3542",
            width=300, height=34, font=("Arial", 11),
            corner_radius=8,
            command=lambda: self.open_update_history_window(all_sections)
        )
        history_btn.pack(pady=(0, 14))

    # ==================================================================
    #  Verzió kihagyás
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
        self._update_dialog_open = False
        self.log_event("EVENT", f"[UPDATE] Kihagyott verzió: {version}")
        win.destroy()

    # ==================================================================
    #  Előző frissítések ablaka
    # ==================================================================
    def open_update_history_window(self, all_sections=None):
        win = ctk.CTkToplevel(self)
        win.title("📜 Frissítések története")
        win.geometry("760x720")
        win.minsize(640, 500)
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 760) // 2
        y = (win.winfo_screenheight() - 720) // 2
        win.geometry(f"760x720+{x}+{y}")

        # Fejléc
        header = ctk.CTkFrame(win, fg_color="#8e44ad", corner_radius=0, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text="📜   Frissítések története",
            font=("Arial", 18, "bold"), text_color="white"
        ).pack(side="left", padx=24, pady=18)

        ctk.CTkLabel(
            header, text=f"Jelenlegi: v{self.get_local_version()}",
            font=("Arial", 11), text_color="#e0c0f0"
        ).pack(side="right", padx=24)

        # --- Tartalom ---
        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=12, pady=12)

        # Szekciók: vagy a GitHub-ról jöttek, vagy helyi history
        sections = all_sections or []
        local_history = self._load_update_history()
        current_version = self.get_local_version()

        # Összegyűjtjük a helyi history-t verzió szerint
        history_map = {h.get("version"): h for h in local_history}

        if not sections and not local_history:
            ctk.CTkLabel(
                scroll, text="Nincs elérhető frissítési előzmény.",
                font=("Arial", 13), text_color="#6a6e78"
            ).pack(pady=60)
        else:
            # Ha van GitHub changelog, azt használjuk
            for section in sections:
                v = section.get("version", "")
                if not v:
                    continue

                is_current = (v == current_version or v.lstrip("v") == current_version.lstrip("v"))
                is_newer = self._is_newer_version(v, current_version)

                # Kártya
                card = ctk.CTkFrame(
                    scroll,
                    fg_color="#0f1a24" if is_newer else "#0a0c10",
                    corner_radius=10,
                    border_width=2 if is_current else 1,
                    border_color="#2ecc71" if is_current else (
                        "#5865F2" if is_newer else "#2f3542"
                    ),
                )
                card.pack(fill="x", pady=6, padx=4)

                # Cím sor
                title_row = ctk.CTkFrame(card, fg_color="transparent")
                title_row.pack(fill="x", padx=14, pady=(12, 6))

                icon = "🟢" if is_current else ("🔵" if is_newer else "⚪")
                title_text = section.get("title") or f"v{v}"

                ctk.CTkLabel(
                    title_row, text=f"{icon}  {title_text}",
                    font=("Arial", 13, "bold"),
                    text_color="#2ecc71" if is_current else (
                        "#5865F2" if is_newer else "#b8bcc6"
                    ),
                    anchor="w",
                ).pack(side="left")

                if is_current:
                    ctk.CTkLabel(
                        title_row, text="JELENLEGI",
                        font=("Arial", 9, "bold"),
                        text_color="#2ecc71",
                    ).pack(side="right", padx=4)

                # Tartalom
                content_box = ctk.CTkTextbox(
                    card, height=160, font=("Consolas", 11),
                    wrap="word", fg_color="#050608"
                )
                content_box.pack(fill="x", padx=14, pady=(0, 12))

                content = section.get("content", "").strip() or "(nincs leírás)"
                content = content.replace("  • ", "  ▸  ").replace("  - ", "  ▸  ")
                content_box.insert("1.0", content)
                content_box.configure(state="disabled")

            # Ha nincs GitHub changelog, de van helyi history
            if not sections and local_history:
                for h in local_history:
                    card = ctk.CTkFrame(scroll, fg_color="#0a0c10", corner_radius=10,
                                         border_width=1, border_color="#2f3542")
                    card.pack(fill="x", pady=6, padx=4)
                    ctk.CTkLabel(
                        card, text=f"⚪  {h.get('title', 'v' + h.get('version', '?'))}",
                        font=("Arial", 13, "bold"), text_color="#b8bcc6", anchor="w"
                    ).pack(fill="x", padx=14, pady=(12, 6))
                    ctk.CTkLabel(
                        card, text=h.get("date", ""),
                        font=("Arial", 10), text_color="#6a6e78", anchor="w"
                    ).pack(fill="x", padx=14, pady=(0, 12))

        # --- Alsó gombok ---
        btns = ctk.CTkFrame(win, fg_color="transparent")
        btns.pack(fill="x", padx=12, pady=(0, 12))

        ctk.CTkButton(
            btns, text="🔄   Frissítés a GitHubról",
            fg_color="#3498db", hover_color="#5dade2",
            width=220, height=40, font=("Arial", 12, "bold"),
            command=lambda: (win.destroy(), self.check_for_updates(silent=False))
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            btns, text="Bezárás",
            fg_color="#555555", hover_color="#666666",
            width=120, height=40, font=("Arial", 12),
            command=win.destroy
        ).pack(side="right", padx=4)

    def _is_newer_version(self, v1, v2):
        """Igaz, ha v1 > v2."""
        try:
            def parse(v):
                v = v.lstrip("v")
                parts = v.split(".")
                return tuple(int(p) for p in parts if p.isdigit())
            return parse(v1) > parse(v2)
        except Exception:
            return False

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

            candidate = os.path.join(full_root, "panel")
            if os.path.isdir(candidate):
                panel_folder = candidate

            set_status("🛑 Futó botok leállítása...", 0.65)
            for bot in self.bots.values():
                if bot.get("is_running") and bot.get("process"):
                    try:
                        bot["process"].terminate()
                    except Exception:
                        pass

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

            try:
                with open(os.path.join(config.SCRIPT_DIR, "version.py"),
                          "w", encoding="utf-8") as vf:
                    vf.write(f'version = "{remote_version}"\n')
            except Exception as e:
                print(f"[UPDATE] version.py írási hiba: {e}")

            # Changelog mentése a history-be
            try:
                changelog_text = self.fetch_changelog()
                sections = self._parse_changelog(changelog_text)
                for s in sections:
                    if s["version"] == remote_version:
                        self._add_to_history(
                            remote_version,
                            s.get("title", f"v{remote_version}"),
                            s.get("content", ""),
                        )
                        break
            except Exception:
                pass

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
        restart_dialog.geometry("480x340")
        restart_dialog.resizable(False, False)
        restart_dialog.grab_set()
        restart_dialog.update_idletasks()
        x = (restart_dialog.winfo_screenwidth() - 480) // 2
        y = (restart_dialog.winfo_screenheight() - 340) // 2
        restart_dialog.geometry(f"480x340+{x}+{y}")

        ctk.CTkLabel(
            restart_dialog, text="✅  Frissítés sikeres!",
            font=("Arial", 20, "bold"), text_color="#2ecc71"
        ).pack(pady=(24, 4))

        ctk.CTkLabel(
            restart_dialog,
            text=f"A panel a(z) v{new_version} verzióra frissült.",
            font=("Arial", 12)
        ).pack(pady=4)

        ctk.CTkLabel(
            restart_dialog,
            text="Újra kell indítani a panelt, hogy életbe lépjenek a változások.",
            font=("Arial", 11), text_color="#8a8e98",
            wraplength=420,
        ).pack(pady=(4, 10))

        info = ctk.CTkFrame(restart_dialog, fg_color="#1a1d24", corner_radius=8)
        info.pack(fill="x", padx=24, pady=6)
        ctk.CTkLabel(
            info,
            text="💡   A mentések, pluginok és botok megmaradnak.",
            font=("Arial", 11), text_color="#b8bcc6"
        ).pack(pady=8)

        btn_frame = ctk.CTkFrame(restart_dialog, fg_color="transparent")
        btn_frame.pack(pady=18)

        def do_restart():
            restart_dialog.destroy()
            self._perform_restart()

        ctk.CTkButton(
            btn_frame, text="🔄   Újraindítás most",
            fg_color="#27ae60", hover_color="#2ecc71",
            width=180, height=44, font=("Arial", 13, "bold"),
            command=do_restart
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            btn_frame, text="🚪   Kilépés",
            fg_color="#c0392b", hover_color="#e74c3c",
            width=130, height=44, font=("Arial", 13),
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

        try:
            self.destroy()
        except Exception:
            pass
        os._exit(0)

    # ==================================================================
    #  Sidebar gomb
    # ==================================================================
    def update_from_github(self, mode="manual"):
        self.check_for_updates(silent=False)