import customtkinter as ctk
from tkinter import messagebox

import modules.config as config
from modules.languages import LANGUAGES
from modules.sounds import ERROR_SOUNDS, play_error_sound_by_name
from modules.theme import get_theme_names

# AFK időzítő opciók (címke, másodperc)
AFK_TIMEOUT_OPTIONS = [
    ("15 másodperc", 15),
    ("30 másodperc", 30),
    ("1 perc", 60),
    ("2 perc", 120),
    ("5 perc", 300),
    ("10 perc", 600),
    ("30 perc", 1800),
]


class WindowSettingsMixin:
    """Settings ablak — modern, színes kártyákkal."""

    def _center_on_screen(self, win, width, height):
        screen_w = win.winfo_screenwidth()
        screen_h = win.winfo_screenheight()
        width = min(width, screen_w - 60)
        height = min(height, screen_h - 80)
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        win.geometry(f"{width}x{height}+{x}+{y}")

    def _settings_section(self, parent, title, icon, accent, bg_tint):
        """Színes szekció kártya a beállításokhoz."""
        card = ctk.CTkFrame(
            parent, fg_color=bg_tint, corner_radius=10,
            border_width=1, border_color=accent,
        )
        card.pack(fill="x", pady=6)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=14, pady=(10, 6))

        ctk.CTkLabel(
            header,
            text=f"{icon}   {title}",
            font=("Arial", 12, "bold"),
            text_color=accent,
            anchor="w",
        ).pack(side="left")

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=14, pady=(0, 12))
        return content

    def _row_label(self, parent, text):
        ctk.CTkLabel(
            parent, text=text,
            font=("Arial", 11),
            text_color="#b8bcc6",
            anchor="w",
        ).pack(fill="x", pady=(6, 2))

    # ==================================================================
    #  Settings ablak
    # ==================================================================
    def open_settings_window_v2(self):
        win = ctk.CTkToplevel(self)
        win.title("⚙️ Beállítások")
        self._center_on_screen(win, 720, 800)
        win.minsize(560, 500)
        win.grab_set()

        # --- Fejléc ---
        header = ctk.CTkFrame(win, fg_color="#5865F2", corner_radius=0, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text="⚙️   Beállítások",
            font=("Arial", 20, "bold"), text_color="white",
        ).pack(side="left", padx=24, pady=16)
        ctk.CTkLabel(
            header, text="Discord Bot Manager",
            font=("Arial", 11), text_color="#c0c8ff",
        ).pack(side="right", padx=24)

        # --- Alsó mentés sáv (fix) ---
        save_bar = ctk.CTkFrame(win, fg_color="#151820", height=64, corner_radius=0)
        save_bar.pack(side="bottom", fill="x")
        save_bar.pack_propagate(False)

        status_lbl = ctk.CTkLabel(
            save_bar, text="", font=("Arial", 11), text_color="#8a8e98"
        )
        status_lbl.pack(side="left", padx=20)

        save_btn = ctk.CTkButton(
            save_bar, text="💾   Mentés és bezárás",
            fg_color="#27ae60", hover_color="#2ecc71",
            width=200, height=42, font=("Arial", 13, "bold"),
            corner_radius=8,
        )
        save_btn.pack(side="right", padx=16, pady=11)

        # --- Tabview ---
        tabs = ctk.CTkTabview(win, fg_color="#0d0f14",
                               segmented_button_selected_color="#5865F2",
                               segmented_button_selected_hover_color="#4752C4")
        tabs.pack(fill="both", expand=True, padx=12, pady=(12, 0))
        panel_tab = tabs.add("🖥️   Panel")
        bot_tab = tabs.add("🤖   Bot")

        # ==============================================================
        #  PANEL TAB
        # ==============================================================
        panel_scroll = ctk.CTkScrollableFrame(panel_tab, fg_color="transparent")
        panel_scroll.pack(fill="both", expand=True)

        # ---------- Biztonság ----------
        s = self._settings_section(
            panel_scroll, "Biztonság", "🔐",
            accent="#e74c3c", bg_tint="#241014",
        )
        self._row_label(s, "Panel jelszó (üresen hagyva nincs védelem):")
        password_entry = ctk.CTkEntry(s, show="*", width=300, placeholder_text="••••••••")
        if self.panel_password:
            password_entry.insert(0, self.panel_password)
        password_entry.pack(anchor="w")

        # ---------- Megjelenés ----------
        s = self._settings_section(
            panel_scroll, "Megjelenés és nyelv", "🎨",
            accent="#9b59b6", bg_tint="#1f1726",
        )

        lang_frame = ctk.CTkFrame(s, fg_color="transparent")
        lang_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(lang_frame, text="Nyelv:", font=("Arial", 11),
                      text_color="#b8bcc6", width=140, anchor="w").pack(side="left")
        language_var = ctk.StringVar(value=self.current_language)
        ctk.CTkComboBox(
            lang_frame, values=["English", "Magyar"],
            variable=language_var, width=200,
            command=self.apply_language,
        ).pack(side="left")

        theme_frame = ctk.CTkFrame(s, fg_color="transparent")
        theme_frame.pack(fill="x", pady=(8, 2))
        ctk.CTkLabel(theme_frame, text="Téma:", font=("Arial", 11),
                      text_color="#b8bcc6", width=140, anchor="w").pack(side="left")
        theme_var = ctk.StringVar(value=self.current_theme)
        ctk.CTkComboBox(
            theme_frame,
            values=get_theme_names(),
            variable=theme_var, width=220,
        ).pack(side="left")

        tray_switch = ctk.CTkSwitch(s, text="  Kicsinyítés tálcára bezáráskor")
        tray_switch.pack(anchor="w", pady=(10, 2))
        if self.minimize_to_tray_enabled:
            tray_switch.select()

        rpc_switch = ctk.CTkSwitch(s, text="  Discord Rich Presence")
        rpc_switch.pack(anchor="w", pady=2)
        if self.rpc_enabled:
            rpc_switch.select()

        # ---------- Értesítések ----------
        s = self._settings_section(
            panel_scroll, "Értesítések", "🔔",
            accent="#f39c12", bg_tint="#231f0f",
        )

        ctk.CTkLabel(s, text="Hiba hang:", font=("Arial", 11),
                      text_color="#b8bcc6", anchor="w").pack(fill="x", pady=(2, 2))
        sound_var = ctk.StringVar(value=self.selected_error_sound)

        def on_sound_change(choice):
            play_error_sound_by_name(choice)

        sound_frame = ctk.CTkFrame(s, fg_color="transparent")
        sound_frame.pack(fill="x")
        ctk.CTkComboBox(
            sound_frame, values=ERROR_SOUNDS, variable=sound_var,
            width=240, command=on_sound_change,
        ).pack(side="left")
        ctk.CTkButton(
            sound_frame, text="🔊  Teszt", width=100, height=28,
            fg_color="#3498db", hover_color="#5dade2",
            command=lambda: play_error_sound_by_name(sound_var.get()),
        ).pack(side="left", padx=8)

        # ---------- Naplók ----------
        s = self._settings_section(
            panel_scroll, "Naplók", "📝",
            accent="#3498db", bg_tint="#152029",
        )
        ctk.CTkLabel(s, text="Napló mentési szint:", font=("Arial", 11),
                      text_color="#b8bcc6", anchor="w").pack(fill="x", pady=(2, 2))
        log_var = ctk.StringVar(value=self.log_save_level)
        ctk.CTkComboBox(
            s,
            values=["Mindent mentse", "Csak hibák", "Csak események", "Sikeres interakciók"],
            variable=log_var, width=280,
        ).pack(anchor="w")

        # ---------- AFK Screen ----------
        s = self._settings_section(
            panel_scroll, "AFK képernyő", "💤",
            accent="#00bcd4", bg_tint="#0f1a24",
        )

        ctk.CTkLabel(
            s,
            text="Ha nem használod a panelt, egy animált képernyő jelenik meg,\n"
                 "ami a botok élő állapotát mutatja.",
            font=("Arial", 10), text_color="#8a8e98",
            justify="left", anchor="w",
        ).pack(fill="x", pady=(2, 8))

        afk_switch = ctk.CTkSwitch(s, text="  AFK képernyő engedélyezése")
        afk_switch.pack(anchor="w", pady=(0, 8))
        if getattr(self, "afk_enabled", True):
            afk_switch.select()

        ctk.CTkLabel(s, text="Időzítő (ennyi tétlenség után jelenjen meg):",
                      font=("Arial", 11), text_color="#b8bcc6",
                      anchor="w").pack(fill="x", pady=(4, 2))

        # Időzítő címkék
        afk_timeout_labels = [l for l, _ in AFK_TIMEOUT_OPTIONS]
        current_seconds = getattr(self, "afk_idle_seconds", 60)
        current_label = next(
            (l for l, s_val in AFK_TIMEOUT_OPTIONS if s_val == current_seconds),
            "1 perc",
        )
        afk_timeout_var = ctk.StringVar(value=current_label)
        ctk.CTkComboBox(
            s, values=afk_timeout_labels,
            variable=afk_timeout_var, width=200,
        ).pack(anchor="w")

        ctk.CTkButton(
            s, text="👁  Előnézet megnyitása", height=30,
            fg_color="#16a085", hover_color="#1abc9c",
            width=200,
            command=self._afk_preview,
        ).pack(anchor="w", pady=(8, 0))

        # ---------- Backup ----------
        s = self._settings_section(
            panel_scroll, "Biztonsági mentés", "💾",
            accent="#2980b9", bg_tint="#101a26",
        )

        backup_switch = ctk.CTkSwitch(s, text="  Automatikus biztonsági mentés")
        backup_switch.pack(anchor="w", pady=2)
        if self.backup_enabled:
            backup_switch.select()

        backup_start_switch = ctk.CTkSwitch(s, text="  Mentés panelindításkor")
        backup_start_switch.pack(anchor="w", pady=2)
        if self.backup_on_start:
            backup_start_switch.select()

        ctk.CTkLabel(s, text="Időzített mentés gyakorisága (óra, 0 = kikapcsolva):",
                      font=("Arial", 11), text_color="#b8bcc6",
                      anchor="w").pack(fill="x", pady=(8, 2))
        backup_interval_entry = ctk.CTkEntry(s, width=100)
        backup_interval_entry.insert(0, str(self.backup_interval_hours))
        backup_interval_entry.pack(anchor="w")

        ctk.CTkButton(
            s, text="📁  Backup kezelő megnyitása", height=32,
            fg_color="#3498db", hover_color="#5dade2",
            width=240,
            command=self.open_backup_manager,
        ).pack(anchor="w", pady=(10, 0))

        # ---------- GitHub frissítés ----------
        s = self._settings_section(
            panel_scroll, "GitHub frissítés", "🚀",
            accent="#3498db", bg_tint="#101a26",
        )

        ctk.CTkLabel(
            s,
            text="A panel automatikusan ellenőrzi, van-e új verzió a GitHubon.",
            font=("Arial", 10), text_color="#8a8e98",
            justify="left", anchor="w",
            wraplength=460,
        ).pack(fill="x", pady=(2, 8))

        ctk.CTkLabel(s, text="Ellenőrzés gyakorisága:",
                      font=("Arial", 11), text_color="#b8bcc6",
                      anchor="w").pack(fill="x", pady=(2, 2))

        # Opciók (címke, perc)
        UPDATE_INTERVAL_OPTIONS = [
            ("❌  Soha", 0),
            ("⚡  Percenként", 1),
            ("🔵  10 percenként", 10),
            ("🟢  Óránként", 60),
            ("🌙  Naponta", 1440),
        ]

        # Aktuális érték meghatározása
        current_minutes = getattr(self, "update_check_interval_minutes", 60)
        current_label = next(
            (l for l, m in UPDATE_INTERVAL_OPTIONS if m == current_minutes),
            "🟢  Óránként",
        )

        update_interval_var = ctk.StringVar(value=current_label)
        ctk.CTkComboBox(
            s, values=[l for l, _ in UPDATE_INTERVAL_OPTIONS],
            variable=update_interval_var, width=260,
        ).pack(anchor="w")

        ctk.CTkButton(
            s, text="🔄   Azonnali ellenőrzés", height=30,
            fg_color="#2980b9", hover_color="#3498db",
            width=200,
            command=lambda: self.check_for_updates(silent=False),
        ).pack(anchor="w", pady=(10, 0))

        ctk.CTkButton(
            s, text="📜   Előző frissítések", height=30,
            fg_color="#8e44ad", hover_color="#9b59b6",
            width=200,
            command=lambda: self.open_update_history_window(),
        ).pack(anchor="w", pady=(4, 0))

        # ---------- AI ----------
        s = self._settings_section(
            panel_scroll, "AI beállítások", "🤖",
            accent="#8e44ad", bg_tint="#1a1230",
        )

        ctk.CTkLabel(s, text="Provider:", font=("Arial", 11),
                      text_color="#b8bcc6", anchor="w").pack(fill="x", pady=(2, 2))
        provider_var = ctk.StringVar(value=getattr(self, "ai_provider", "OpenAI (GPT)"))
        ctk.CTkComboBox(
            s,
            values=["OpenAI (GPT)", "Anthropic (Claude)", "Ollama (helyi)", "LM Studio (helyi)"],
            variable=provider_var, width=280,
        ).pack(anchor="w")

        ctk.CTkLabel(s, text="API kulcs (OpenAI/Claude esetén):",
                      font=("Arial", 11), text_color="#b8bcc6",
                      anchor="w").pack(fill="x", pady=(8, 2))
        ai_key_entry = ctk.CTkEntry(s, show="*", width=380, placeholder_text="sk-...")
        if getattr(self, "ai_api_key", ""):
            ai_key_entry.insert(0, self.ai_api_key)
        ai_key_entry.pack(anchor="w")

        ctk.CTkLabel(s, text="Modell (pl. llama3.2, gpt-4o-mini):",
                      font=("Arial", 11), text_color="#b8bcc6",
                      anchor="w").pack(fill="x", pady=(8, 2))
        ai_model_entry = ctk.CTkEntry(s, width=280,
                                       placeholder_text=getattr(self, "ai_model", ""))
        ai_model_entry.pack(anchor="w")

        # ==============================================================
        #  BOT TAB
        # ==============================================================
        bot_scroll = ctk.CTkScrollableFrame(bot_tab, fg_color="transparent")
        bot_scroll.pack(fill="both", expand=True)

        bot = self.bots[self.active_bot_key]

        # ---------- Erőforrások ----------
        s = self._settings_section(
            bot_scroll, "Erőforrások", "💻",
            accent="#2ecc71", bg_tint="#16231a",
        )
        ctk.CTkLabel(s, text="Maximum RAM használat (MB):",
                      font=("Arial", 11), text_color="#b8bcc6",
                      anchor="w").pack(fill="x", pady=(2, 2))
        ram_entry = ctk.CTkEntry(s, width=180)
        ram_entry.insert(0, str(self.max_ram_mb))
        ram_entry.pack(anchor="w")

        ctk.CTkLabel(
            s,
            text="Ha a bot túllépi a limitet, a panel figyelmeztet (vagy leállítja).",
            font=("Arial", 10), text_color="#7a8090",
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # ---------- Teszt mód ----------
        s = self._settings_section(
            bot_scroll, "Teszt mód", "🧪",
            accent="#e67e22", bg_tint="#241c12",
        )
        test_switch = ctk.CTkSwitch(s, text="  Teszt mód engedélyezése")
        test_switch.pack(anchor="w", pady=2)
        if bot.get("test_mode", False):
            test_switch.select()

        ctk.CTkLabel(s, text="Tesztelők Discord ID-i (vesszővel elválasztva):",
                      font=("Arial", 11), text_color="#b8bcc6",
                      anchor="w").pack(fill="x", pady=(8, 2))
        testers_entry = ctk.CTkEntry(
            s, width=420,
            placeholder_text="123456789012345678, 987654321098765432",
        )
        testers_entry.insert(0, ", ".join(str(v) for v in bot.get("allowed_discord_ids", [])))
        testers_entry.pack(anchor="w")

        ctk.CTkLabel(
            s,
            text="Teszt módban csak ezek az azonosítók használhatják a botot.",
            font=("Arial", 10), text_color="#7a8090",
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # ---------- Crash kezelés ----------
        s = self._settings_section(
            bot_scroll, "Összeomlás kezelés", "🔄",
            accent="#e74c3c", bg_tint="#241014",
        )
        crash_switch = ctk.CTkSwitch(s, text="  Automatikus újraindítás összeomlás után")
        crash_switch.pack(anchor="w", pady=2)
        if bot.get("auto_restart_on_crash", False):
            crash_switch.select()

        ctk.CTkLabel(s, text="Várakozási idő újraindítás előtt (másodperc):",
                      font=("Arial", 11), text_color="#b8bcc6",
                      anchor="w").pack(fill="x", pady=(8, 2))
        crash_delay_entry = ctk.CTkEntry(s, width=100)
        crash_delay_entry.insert(0, str(bot.get("crash_restart_delay", 10)))
        crash_delay_entry.pack(anchor="w")

        # ==============================================================
        #  Mentés
        # ==============================================================
        def save_settings():
            # --- Panel beállítások ---
            self.current_language = language_var.get()
            self.panel_password = password_entry.get().strip()
            self.minimize_to_tray_enabled = bool(tray_switch.get())
            self.rpc_enabled = bool(rpc_switch.get())
            self.log_save_level = log_var.get()
            self.selected_error_sound = sound_var.get()

            # AFK
            self.afk_enabled = bool(afk_switch.get())
            selected_timeout_label = afk_timeout_var.get()
            for label, seconds in AFK_TIMEOUT_OPTIONS:
                if label == selected_timeout_label:
                    self.afk_idle_seconds = seconds
                    break

            # Backup
            self.backup_enabled = bool(backup_switch.get())
            self.backup_on_start = bool(backup_start_switch.get())
            try:
                self.backup_interval_hours = max(0, int(backup_interval_entry.get()))
            except ValueError:
                status_lbl.configure(text="❌ Backup gyakoriság egész szám legyen!",
                                      text_color="#e74c3c")
                return

            # --- GitHub update intervallum ---
            selected_update_label = update_interval_var.get()
            for label, minutes in UPDATE_INTERVAL_OPTIONS:
                if label == selected_update_label:
                    self.update_check_interval_minutes = minutes
                    break

            # Ha "Soha" → ne ütemezzük
            try:
                if hasattr(self, "_update_check_after_id") and self._update_check_after_id:
                    self.after_cancel(self._update_check_after_id)
                    self._update_check_after_id = None
            except Exception:
                pass

            if self.update_check_interval_minutes > 0:
                self.after(200, lambda: self.schedule_update_check(
                    interval_minutes=self.update_check_interval_minutes
                ))

            # AI
            self.ai_provider = provider_var.get()
            self.ai_api_key = ai_key_entry.get().strip()
            self.ai_model = ai_model_entry.get().strip()

            # --- Bot beállítások ---
            bot["test_mode"] = bool(test_switch.get())
            bot["auto_restart_on_crash"] = bool(crash_switch.get())
            try:
                bot["crash_restart_delay"] = max(1, int(crash_delay_entry.get()))
            except ValueError:
                status_lbl.configure(text="❌ Crash várakozási idő egész szám legyen!",
                                      text_color="#e74c3c")
                return
            bot["allowed_discord_ids"] = [
                v.strip() for v in testers_entry.get().split(",") if v.strip().isdigit()
            ]
            try:
                self.max_ram_mb = max(50, int(ram_entry.get()))
            except ValueError:
                status_lbl.configure(text="❌ RAM érték egész szám legyen!",
                                      text_color="#e74c3c")
                return

            # --- Téma alkalmazása ---
            selected_theme = theme_var.get()
            if selected_theme != self.current_theme:
                self.apply_theme_setting(selected_theme)

            # --- Mentés ---
            self.save_config()
            self.switch_bot(self.active_bot_key)
            self.update_ui_texts()

            status_lbl.configure(text="✅ Beállítások mentve!", text_color="#2ecc71")
            self.notify("⚙️ Beállítások mentve", "success", 2000)
            self.after(400, win.destroy)

        save_btn.configure(command=save_settings)

    # ==================================================================
    #  AFK előnézet
    # ==================================================================
    def _afk_preview(self):
        """Azonnal megnyitja az AFK képernyőt (előnézet)."""
        try:
            if hasattr(self, "_show_afk_screen"):
                # Ha már nyitva van, ne nyissa újra
                if getattr(self, "_afk_running", False):
                    return
                self._show_afk_screen()
        except Exception as e:
            print(f"[AFK] Előnézet hiba: {e}")