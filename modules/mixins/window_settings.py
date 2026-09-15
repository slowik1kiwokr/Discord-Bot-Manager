import customtkinter as ctk
from tkinter import messagebox

import modules.config as config
from modules.sounds import SOUND_KEYS, play_error_sound_by_key
from modules.theme import get_theme_names
import os
from PIL import Image



# =====================================================================
#  AFK időzítő opciók — fix kulcs + másodperc
# =====================================================================
AFK_TIMEOUT_OPTIONS = [
    ("afk_timeout_15s", 15),
    ("afk_timeout_30s", 30),
    ("afk_timeout_1m", 60),
    ("afk_timeout_2m", 120),
    ("afk_timeout_5m", 300),
    ("afk_timeout_10m", 600),
    ("afk_timeout_30m", 1800),
]

# =====================================================================
#  GitHub update ellenőrzési opciók — fix kulcs + perc
# =====================================================================
UPDATE_INTERVAL_OPTIONS = [
    ("update_interval_never", 0),
    ("update_interval_1min", 1),
    ("update_interval_10min", 10),
    ("update_interval_1hour", 60),
    ("update_interval_1day", 1440),
]

# =====================================================================
#  Log szint opciók — fix kulcs
# =====================================================================
LOG_LEVEL_KEYS = ["all", "errors", "events", "success"]


class WindowSettingsMixin:
    """Settings ablak — modern, színes kártyákkal."""

    # ------------------------------------------------------------------
    #  Segédfüggvények
    # ------------------------------------------------------------------
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

    def _sound_display_name(self, sound_key):
        """A fix hang kulcs → megjelenítendő név (fordítva)."""
        return self.tr(f"sound_{sound_key}")

    def _sound_key_from_display(self, display_name):
        """A megjelenített név → fix kulcs."""
        for key in SOUND_KEYS:
            if self.tr(f"sound_{key}") == display_name:
                return key
        return "beep"

    def _log_display_name(self, log_key):
        """A fix log szint kulcs → megjelenítendő név."""
        return self.tr(f"settings_log_{log_key}")

    def _log_key_from_display(self, display_name):
        """A megjelenített név → fix kulcs."""
        for key in LOG_LEVEL_KEYS:
            if self.tr(f"settings_log_{key}") == display_name:
                return key
        return "all"

    # ==================================================================
    #  Settings ablak
    # ==================================================================
    def open_settings_window_v2(self):
        win = ctk.CTkToplevel(self)
        win.title(self.tr("settings_title"))
        self._center_on_screen(win, 720, 800)
        win.minsize(560, 500)
        win.grab_set()

        # --- Fejléc ---
        header = ctk.CTkFrame(win, fg_color="#0f1a3a", corner_radius=0, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Vékony cián csík a fejléc alján — „glow" effekt
        glow_line = ctk.CTkFrame(header, height=2, fg_color="#3b82f6",
                                  corner_radius=0)
        glow_line.pack(side="bottom", fill="x")

        # Bal oldal: ⚙️ + Settings
        left_header = ctk.CTkFrame(header, fg_color="transparent")
        left_header.pack(side="left", padx=(24, 0), pady=14)

        ctk.CTkLabel(
            left_header, text="⚙️",
            font=("Segoe UI Emoji", 22),
            text_color="#7dd3fc",
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            left_header, text="Settings",
            font=("Arial", 19, "bold"),
            text_color="#7dd3fc",
        ).pack(side="left")

        # Jobb oldal: Discord Bot Manager
        ctk.CTkLabel(
            header, text="Discord Bot Manager",
            font=("Arial", 24, "bold"),
            text_color="#5fc8ff",
        ).pack(side="right", padx=24, pady=14)

        # --- Alsó mentés sáv (fix) ---
        save_bar = ctk.CTkFrame(win, fg_color="#151820", height=64, corner_radius=0)
        save_bar.pack(side="bottom", fill="x")
        save_bar.pack_propagate(False)

        status_lbl = ctk.CTkLabel(
            save_bar, text="", font=("Arial", 11), text_color="#8a8e98"
        )
        status_lbl.pack(side="left", padx=20)

        save_btn = ctk.CTkButton(
            save_bar, text=self.tr("settings_save_close_btn"),
            fg_color="#27ae60", hover_color="#2ecc71",
            width=200, height=42, font=("Arial", 13, "bold"),
            corner_radius=8,
        )
        save_btn.pack(side="right", padx=16, pady=11)

        # --- Tabview ---
        tabs = ctk.CTkTabview(
            win, fg_color="#0d0f14",
            segmented_button_selected_color="#5865F2",
            segmented_button_selected_hover_color="#4752C4",
        )
        tabs.pack(fill="both", expand=True, padx=12, pady=(12, 0))
        panel_tab = tabs.add(self.tr("settings_tab_panel"))
        bot_tab = tabs.add(self.tr("settings_tab_bot"))

        # ==============================================================
        #  PANEL TAB
        # ==============================================================
        panel_scroll = ctk.CTkScrollableFrame(panel_tab, fg_color="transparent")
        panel_scroll.pack(fill="both", expand=True)

        # ---------- Biztonság ----------
        s = self._settings_section(
            panel_scroll, self.tr("settings_sec_security"), "🔐",
            accent="#e74c3c", bg_tint="#241014",
        )
        self._row_label(s, self.tr("settings_password_lbl"))
        password_entry = ctk.CTkEntry(s, show="*", width=300, placeholder_text="••••••••")
        if self.panel_password:
            password_entry.insert(0, self.panel_password)
        password_entry.pack(anchor="w")

        # ---------- Megjelenés ----------
        s = self._settings_section(
            panel_scroll, self.tr("settings_sec_appearance"), "🎨",
            accent="#9b59b6", bg_tint="#1f1726",
        )

        lang_frame = ctk.CTkFrame(s, fg_color="transparent")
        lang_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(
            lang_frame, text=self.tr("settings_language_lbl"),
            font=("Arial", 11), text_color="#b8bcc6",
            width=140, anchor="w",
        ).pack(side="left")
        language_var = ctk.StringVar(value=self.current_language)
        ctk.CTkComboBox(
            lang_frame, values=["English", "Magyar"],
            variable=language_var, width=200,
            command=self.apply_language,
        ).pack(side="left")

        theme_frame = ctk.CTkFrame(s, fg_color="transparent")
        theme_frame.pack(fill="x", pady=(8, 2))
        ctk.CTkLabel(
            theme_frame, text=self.tr("settings_theme_lbl"),
            font=("Arial", 11), text_color="#b8bcc6",
            width=140, anchor="w",
        ).pack(side="left")
        theme_var = ctk.StringVar(value=self.current_theme)
        ctk.CTkComboBox(
            theme_frame,
            values=get_theme_names(),
            variable=theme_var, width=220,
        ).pack(side="left")

        tray_switch = ctk.CTkSwitch(s, text=self.tr("settings_tray_switch"))
        tray_switch.pack(anchor="w", pady=(10, 2))
        if self.minimize_to_tray_enabled:
            tray_switch.select()

        rpc_switch = ctk.CTkSwitch(s, text=self.tr("settings_rpc_switch"))
        rpc_switch.pack(anchor="w", pady=2)
        if self.rpc_enabled:
            rpc_switch.select()

        # ---------- Értesítések ----------
        s = self._settings_section(
            panel_scroll, self.tr("settings_sec_notifications"), "🔔",
            accent="#f39c12", bg_tint="#231f0f",
        )

        ctk.CTkLabel(
            s, text=self.tr("settings_error_sound_lbl"),
            font=("Arial", 11), text_color="#b8bcc6",
            anchor="w",
        ).pack(fill="x", pady=(2, 2))

        # Hang: a combobox fix kulcsokat tartalmaz, de a megjelenítés fordítva
        sound_display_values = [self.tr(f"sound_{k}") for k in SOUND_KEYS]
        sound_display_var = ctk.StringVar(
            value=self._sound_display_name(self.selected_error_sound)
        )

        def on_sound_change(choice_display):
            key = self._sound_key_from_display(choice_display)
            play_error_sound_by_key(key)

        sound_frame = ctk.CTkFrame(s, fg_color="transparent")
        sound_frame.pack(fill="x")
        ctk.CTkComboBox(
            sound_frame, values=sound_display_values,
            variable=sound_display_var,
            width=240, command=on_sound_change,
        ).pack(side="left")
        ctk.CTkButton(
            sound_frame, text=self.tr("settings_sound_test_btn"),
            width=100, height=28,
            fg_color="#3498db", hover_color="#5dade2",
            command=lambda: play_error_sound_by_key(
                self._sound_key_from_display(sound_display_var.get())
            ),
        ).pack(side="left", padx=8)

        # ---------- Naplók ----------
        s = self._settings_section(
            panel_scroll, self.tr("settings_sec_logs"), "📝",
            accent="#3498db", bg_tint="#152029",
        )
        ctk.CTkLabel(
            s, text=self.tr("settings_log_level_lbl"),
            font=("Arial", 11), text_color="#b8bcc6",
            anchor="w",
        ).pack(fill="x", pady=(2, 2))

        # Log szint: combobox fix kulcsok → megjelenítés fordítva
        log_display_values = [
            self.tr(f"settings_log_{k}") for k in LOG_LEVEL_KEYS
        ]
        log_display_var = ctk.StringVar(
            value=self._log_display_name(self.log_save_level)
        )
        ctk.CTkComboBox(
            s, values=log_display_values,
            variable=log_display_var, width=280,
        ).pack(anchor="w")

        # ---------- AFK Screen ----------
        s = self._settings_section(
            panel_scroll, self.tr("settings_sec_afk"), "💤",
            accent="#00bcd4", bg_tint="#0f1a24",
        )

        ctk.CTkLabel(
            s,
            text=self.tr("settings_afk_hint"),
            font=("Arial", 10), text_color="#8a8e98",
            justify="left", anchor="w",
        ).pack(fill="x", pady=(2, 8))

        afk_switch = ctk.CTkSwitch(s, text=self.tr("settings_afk_switch"))
        afk_switch.pack(anchor="w", pady=(0, 8))
        if getattr(self, "afk_enabled", True):
            afk_switch.select()

        ctk.CTkLabel(
            s, text=self.tr("settings_afk_timeout_lbl"),
            font=("Arial", 11), text_color="#b8bcc6",
            anchor="w",
        ).pack(fill="x", pady=(4, 2))

        afk_timeout_labels = [self.tr(k) for k, _ in AFK_TIMEOUT_OPTIONS]
        current_seconds = getattr(self, "afk_idle_seconds", 60)
        current_label = next(
            (self.tr(k) for k, val in AFK_TIMEOUT_OPTIONS if val == current_seconds),
            self.tr("afk_timeout_1m"),
        )
        afk_timeout_var = ctk.StringVar(value=current_label)
        ctk.CTkComboBox(
            s, values=afk_timeout_labels,
            variable=afk_timeout_var, width=200,
        ).pack(anchor="w")

        ctk.CTkButton(
            s, text=self.tr("settings_afk_preview_btn"), height=30,
            fg_color="#16a085", hover_color="#1abc9c",
            width=200,
            command=self._afk_preview,
        ).pack(anchor="w", pady=(8, 0))

        # ---------- Backup ----------
        s = self._settings_section(
            panel_scroll, self.tr("settings_sec_backup"), "💾",
            accent="#2980b9", bg_tint="#101a26",
        )

        backup_switch = ctk.CTkSwitch(s, text=self.tr("settings_backup_switch"))
        backup_switch.pack(anchor="w", pady=2)
        if self.backup_enabled:
            backup_switch.select()

        backup_start_switch = ctk.CTkSwitch(
            s, text=self.tr("settings_backup_start_switch")
        )
        backup_start_switch.pack(anchor="w", pady=2)
        if self.backup_on_start:
            backup_start_switch.select()

        ctk.CTkLabel(
            s, text=self.tr("settings_backup_interval_lbl"),
            font=("Arial", 11), text_color="#b8bcc6",
            anchor="w",
        ).pack(fill="x", pady=(8, 2))
        backup_interval_entry = ctk.CTkEntry(s, width=100)
        backup_interval_entry.insert(0, str(self.backup_interval_hours))
        backup_interval_entry.pack(anchor="w")

        ctk.CTkButton(
            s, text=self.tr("settings_backup_manager_btn"), height=32,
            fg_color="#3498db", hover_color="#5dade2",
            width=240,
            command=self.open_backup_manager,
        ).pack(anchor="w", pady=(10, 0))

        # ---------- GitHub frissítés ----------
        s = self._settings_section(
            panel_scroll, self.tr("settings_sec_github"), "🚀",
            accent="#3498db", bg_tint="#101a26",
        )

        ctk.CTkLabel(
            s,
            text=self.tr("settings_github_hint"),
            font=("Arial", 10), text_color="#8a8e98",
            justify="left", anchor="w",
            wraplength=460,
        ).pack(fill="x", pady=(2, 8))

        ctk.CTkLabel(
            s, text=self.tr("settings_update_interval_lbl"),
            font=("Arial", 11), text_color="#b8bcc6",
            anchor="w",
        ).pack(fill="x", pady=(2, 2))

        current_minutes = getattr(self, "update_check_interval_minutes", 60)
        current_interval_label = next(
            (self.tr(k) for k, m in UPDATE_INTERVAL_OPTIONS if m == current_minutes),
            self.tr("update_interval_1hour"),
        )

        update_interval_var = ctk.StringVar(value=current_interval_label)
        ctk.CTkComboBox(
            s, values=[self.tr(k) for k, _ in UPDATE_INTERVAL_OPTIONS],
            variable=update_interval_var, width=260,
        ).pack(anchor="w")

        ctk.CTkButton(
            s, text=self.tr("settings_update_check_now_btn"), height=30,
            fg_color="#2980b9", hover_color="#3498db",
            width=200,
            command=lambda: self.check_for_updates(silent=False),
        ).pack(anchor="w", pady=(10, 0))

        ctk.CTkButton(
            s, text=self.tr("settings_update_history_btn"), height=30,
            fg_color="#8e44ad", hover_color="#9b59b6",
            width=200,
            command=lambda: self.open_update_history_window(),
        ).pack(anchor="w", pady=(4, 0))

        # ---------- AI ----------
        s = self._settings_section(
            panel_scroll, self.tr("settings_sec_ai"), "🤖",
            accent="#8e44ad", bg_tint="#1a1230",
        )

        ctk.CTkLabel(
            s, text=self.tr("ai_settings_provider_lbl"),
            font=("Arial", 11), text_color="#b8bcc6",
            anchor="w",
        ).pack(fill="x", pady=(2, 2))
        provider_var = ctk.StringVar(
            value=getattr(self, "ai_provider", "OpenAI (GPT)")
        )
        ctk.CTkComboBox(
            s,
            values=[
                "OpenAI (GPT)", "Anthropic (Claude)",
                "Ollama (local)", "LM Studio (local)",
            ],
            variable=provider_var, width=280,
        ).pack(anchor="w")

        ctk.CTkLabel(
            s, text=self.tr("ai_settings_key_lbl"),
            font=("Arial", 11), text_color="#b8bcc6",
            anchor="w",
        ).pack(fill="x", pady=(8, 2))
        ai_key_entry = ctk.CTkEntry(
            s, show="*", width=380, placeholder_text="sk-..."
        )
        if getattr(self, "ai_api_key", ""):
            ai_key_entry.insert(0, self.ai_api_key)
        ai_key_entry.pack(anchor="w")

        ctk.CTkLabel(
            s, text=self.tr("settings_ai_model_lbl"),
            font=("Arial", 11), text_color="#b8bcc6",
            anchor="w",
        ).pack(fill="x", pady=(8, 2))
        ai_model_entry = ctk.CTkEntry(
            s, width=280, placeholder_text=getattr(self, "ai_model", "")
        )
        ai_model_entry.pack(anchor="w")

        # ==============================================================
        #  BOT TAB
        # ==============================================================
        bot_scroll = ctk.CTkScrollableFrame(bot_tab, fg_color="transparent")
        bot_scroll.pack(fill="both", expand=True)

        bot = self.bots[self.active_bot_key]

        # ---------- Erőforrások ----------
        s = self._settings_section(
            bot_scroll, self.tr("settings_sec_resources"), "💻",
            accent="#2ecc71", bg_tint="#16231a",
        )
        ctk.CTkLabel(
            s, text=self.tr("settings_max_ram_lbl"),
            font=("Arial", 11), text_color="#b8bcc6",
            anchor="w",
        ).pack(fill="x", pady=(2, 2))
        ram_entry = ctk.CTkEntry(s, width=180)
        ram_entry.insert(0, str(self.max_ram_mb))
        ram_entry.pack(anchor="w")

        ctk.CTkLabel(
            s,
            text=self.tr("settings_max_ram_hint"),
            font=("Arial", 10), text_color="#7a8090",
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # ---------- Teszt mód ----------
        s = self._settings_section(
            bot_scroll, self.tr("settings_sec_test_mode"), "🧪",
            accent="#e67e22", bg_tint="#241c12",
        )
        test_switch = ctk.CTkSwitch(s, text=self.tr("settings_test_switch"))
        test_switch.pack(anchor="w", pady=2)
        if bot.get("test_mode", False):
            test_switch.select()

        ctk.CTkLabel(
            s, text=self.tr("settings_testers_lbl"),
            font=("Arial", 11), text_color="#b8bcc6",
            anchor="w",
        ).pack(fill="x", pady=(8, 2))
        testers_entry = ctk.CTkEntry(
            s, width=420,
            placeholder_text="123456789012345678, 987654321098765432",
        )
        testers_entry.insert(
            0, ", ".join(str(v) for v in bot.get("allowed_discord_ids", []))
        )
        testers_entry.pack(anchor="w")

        ctk.CTkLabel(
            s,
            text=self.tr("settings_testers_hint"),
            font=("Arial", 10), text_color="#7a8090",
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # ---------- Crash kezelés ----------
        s = self._settings_section(
            bot_scroll, self.tr("settings_sec_crash"), "🔄",
            accent="#e74c3c", bg_tint="#241014",
        )
        crash_switch = ctk.CTkSwitch(s, text=self.tr("settings_crash_switch"))
        crash_switch.pack(anchor="w", pady=2)
        if bot.get("auto_restart_on_crash", False):
            crash_switch.select()

        ctk.CTkLabel(
            s, text=self.tr("settings_crash_delay_lbl"),
            font=("Arial", 11), text_color="#b8bcc6",
            anchor="w",
        ).pack(fill="x", pady=(8, 2))
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

            # Fix kulcsok a megjelenített nevekből
            self.log_save_level = self._log_key_from_display(
                log_display_var.get()
            )
            self.selected_error_sound = self._sound_key_from_display(
                sound_display_var.get()
            )

            # AFK
            self.afk_enabled = bool(afk_switch.get())
            selected_timeout_label = afk_timeout_var.get()
            for key, seconds in AFK_TIMEOUT_OPTIONS:
                if self.tr(key) == selected_timeout_label:
                    self.afk_idle_seconds = seconds
                    break

            # Backup
            self.backup_enabled = bool(backup_switch.get())
            self.backup_on_start = bool(backup_start_switch.get())
            try:
                self.backup_interval_hours = max(
                    0, int(backup_interval_entry.get())
                )
            except ValueError:
                status_lbl.configure(
                    text=self.tr("settings_err_backup_interval"),
                    text_color="#e74c3c",
                )
                return

            # --- GitHub update intervallum ---
            selected_update_label = update_interval_var.get()
            for key, minutes in UPDATE_INTERVAL_OPTIONS:
                if self.tr(key) == selected_update_label:
                    self.update_check_interval_minutes = minutes
                    break

            # Ha "Soha" → ne ütemezzük
            try:
                if (hasattr(self, "_update_check_after_id")
                        and self._update_check_after_id):
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
                bot["crash_restart_delay"] = max(
                    1, int(crash_delay_entry.get())
                )
            except ValueError:
                status_lbl.configure(
                    text=self.tr("settings_err_crash_delay"),
                    text_color="#e74c3c",
                )
                return
            bot["allowed_discord_ids"] = [
                v.strip() for v in testers_entry.get().split(",")
                if v.strip().isdigit()
            ]
            try:
                self.max_ram_mb = max(50, int(ram_entry.get()))
            except ValueError:
                status_lbl.configure(
                    text=self.tr("settings_err_ram"),
                    text_color="#e74c3c",
                )
                return

            # --- Téma alkalmazása ---
            selected_theme = theme_var.get()
            if selected_theme != self.current_theme:
                self.apply_theme_setting(selected_theme)

            # --- Mentés ---
            self.save_config()
            self.switch_bot(self.active_bot_key)
            self.update_ui_texts()

            status_lbl.configure(
                text=self.tr("settings_saved_status"),
                text_color="#2ecc71",
            )
            self.notify(self.tr("settings_saved_toast"), "success", 2000)
            self.after(400, win.destroy)

        save_btn.configure(command=save_settings)

    # ==================================================================
    #  AFK előnézet
    # ==================================================================
    def _afk_preview(self):
        """Azonnal megnyitja az AFK képernyőt (előnézet)."""
        try:
            if hasattr(self, "_show_afk_screen"):
                if getattr(self, "_afk_running", False):
                    return
                self._show_afk_screen()
        except Exception as e:
            print(f"[AFK] Előnézet hiba: {e}")