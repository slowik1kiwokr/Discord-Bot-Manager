import customtkinter as ctk
from tkinter import messagebox

import modules.config as config
from modules.sounds import SOUND_KEYS, play_error_sound_by_key
from modules.theme import get_theme_names
import os
from PIL import Image


# =====================================================================
#  Opciók — fix kulcs + érték
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

UPDATE_INTERVAL_OPTIONS = [
    ("update_interval_never", 0),
    ("update_interval_1min", 1),
    ("update_interval_10min", 10),
    ("update_interval_1hour", 60),
    ("update_interval_1day", 1440),
]

LOG_LEVEL_KEYS = ["all", "errors", "events", "success"]


# =====================================================================
#  Tab definíciók — (id, ikon, cím kulcs, accent szín, kártya háttér)
# =====================================================================
SETTINGS_TABS = [
    ("security",      "🔐", "settings_sec_security",      "#e74c3c", "#241014"),
    ("appearance",    "🎨", "settings_sec_appearance",    "#9b59b6", "#1f1726"),
    ("notifications", "🔔", "settings_sec_notifications", "#f39c12", "#231f0f"),
    ("logs",          "📝", "settings_sec_logs",          "#3498db", "#152029"),
    ("afk",           "💤", "settings_sec_afk",           "#00bcd4", "#0f1a24"),
    ("backup",        "💾", "settings_sec_backup",        "#2980b9", "#101a26"),
    ("github",        "🚀", "settings_sec_github",        "#3498db", "#101a26"),
    ("ai",            "🤖", "settings_sec_ai",            "#8e44ad", "#1a1230"),
    ("lan",           "🔗", "settings_sec_lan",           "#16a085", "#0f2318"),
]


class WindowSettingsMixin:
    """Settings ablak — tab-alapú, animációkkal."""

    # ------------------------------------------------------------------
    #  Animációs segédfüggvények
    # ------------------------------------------------------------------
    def _hex_lerp(self, c1, c2, t):
        """Két hex szín között interpolál (t = 0..1)."""
        c1 = c1.lstrip("#")
        c2 = c2.lstrip("#")
        r = int(int(c1[0:2], 16) + (int(c2[0:2], 16) - int(c1[0:2], 16)) * t)
        g = int(int(c1[2:4], 16) + (int(c2[2:4], 16) - int(c1[2:4], 16)) * t)
        b = int(int(c1[4:6], 16) + (int(c2[4:6], 16) - int(c1[4:6], 16)) * t)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _animate_color(self, widget, start, end, steps=8, delay=20,
                        attr="fg_color", key=None):
        """Szín-átmenet animáció."""
        if key:
            key["_anim_id"] = key.get("_anim_id", 0) + 1
            my_id = key["_anim_id"]
        else:
            my_id = None

        def step(i=0):
            if key is not None and key.get("_anim_id") != my_id:
                return
            if i > steps:
                try:
                    widget.configure(**{attr: end})
                except Exception:
                    pass
                return
            t = i / steps
            t = 1 - (1 - t) ** 3  # ease out cubic
            color = self._hex_lerp(start, end, t)
            try:
                widget.configure(**{attr: color})
            except Exception:
                return
            try:
                widget.after(delay, lambda: step(i + 1))
            except Exception:
                pass

        step(0)

    def _animate_int(self, getter, setter, start, end, steps=10, delay=15,
                      ease=True, on_done=None):
        """Egész érték animálása (pl. magasság, szélesség)."""

        def step(i=0):
            if i > steps:
                try:
                    setter(end)
                except Exception:
                    pass
                if on_done:
                    try:
                        on_done()
                    except Exception:
                        pass
                return
            t = i / steps
            if ease:
                t = 1 - (1 - t) ** 3
            value = int(start + (end - start) * t)
            try:
                setter(value)
            except Exception:
                return
            try:
                # A setter a widget.after-ját használjuk — a hívó ad egy widgetet
                pass
            except Exception:
                pass
            # A hívó ad egy widgetet, amin az after-t futtatjuk
            # Ezért külön metódus kell, lásd lejjebb

        step(0)

    def _center_on_screen(self, win, width, height):
        screen_w = win.winfo_screenwidth()
        screen_h = win.winfo_screenheight()
        width = min(width, screen_w - 60)
        height = min(height, screen_h - 80)
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        win.geometry(f"{width}x{height}+{x}+{y}")

    def _settings_card(self, parent, accent, bg_tint):
        """Színes kártya — accent border + tinted háttér."""
        card = ctk.CTkFrame(
            parent, fg_color=bg_tint, corner_radius=12,
            border_width=2, border_color=accent,
        )
        card.pack(fill="x", padx=18, pady=(0, 14))
        return card

    def _card_header(self, card, icon, title, accent):
        """Kártya fejléc."""
        h = ctk.CTkFrame(card, fg_color="transparent")
        h.pack(fill="x", padx=16, pady=(12, 6))
        ctk.CTkLabel(
            h, text=f"{icon}  {title}",
            font=("Arial", 13, "bold"),
            text_color=accent, anchor="w",
        ).pack(side="left")
        ctk.CTkFrame(card, height=1, fg_color=accent, corner_radius=0).pack(
            fill="x", padx=16, pady=(0, 10)
        )
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=16, pady=(0, 14))
        return content

    def _label(self, parent, text, color="#b8bcc6"):
        ctk.CTkLabel(
            parent, text=text, font=("Arial", 11),
            text_color=color, anchor="w",
        ).pack(fill="x", pady=(6, 2))

    # ------------------------------------------------------------------
    #  Fordítás segédek
    # ------------------------------------------------------------------
    def _sound_display_name(self, sound_key):
        return self.tr(f"sound_{sound_key}")

    def _sound_key_from_display(self, display_name):
        for key in SOUND_KEYS:
            if self.tr(f"sound_{key}") == display_name:
                return key
        return "beep"

    def _log_display_name(self, log_key):
        return self.tr(f"settings_log_{log_key}")

    def _log_key_from_display(self, display_name):
        for key in LOG_LEVEL_KEYS:
            if self.tr(f"settings_log_{key}") == display_name:
                return key
        return "all"

    # ==================================================================
    #  Settings ablak — ÚJ dizájn
    # ==================================================================
    def open_settings_window_v2(self):
        win = ctk.CTkToplevel(self)
        win.title(self.tr("settings_title"))
        self._center_on_screen(win, 860, 720)
        win.minsize(760, 560)
        win.grab_set()
        win.configure(fg_color="#0a0c10")

        # ============================================================
        #  FEJLÉC
        # ============================================================
        header = ctk.CTkFrame(win, fg_color="#0f1a3a", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkFrame(header, height=2, fg_color="#3b82f6",
                     corner_radius=0).pack(side="bottom", fill="x")

        left_h = ctk.CTkFrame(header, fg_color="transparent")
        left_h.pack(side="left", padx=20, pady=14)

        ctk.CTkLabel(
            left_h, text="⚙️", font=("Segoe UI Emoji", 20),
            text_color="#7dd3fc",
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            left_h, text="Settings", font=("Arial", 16, "bold"),
            text_color="#7dd3fc",
        ).pack(side="left")

        ctk.CTkLabel(
            header, text="Discord Bot Manager",
            font=("Arial", 17, "bold"), text_color="#5fc8ff",
        ).pack(side="right", padx=22)

        # ============================================================
        #  ALSÓ SÁV
        # ============================================================
        bottom = ctk.CTkFrame(win, fg_color="#0f1420",
                                corner_radius=0, height=58)
        bottom.pack(side="bottom", fill="x")
        bottom.pack_propagate(False)

        ctk.CTkFrame(bottom, height=1, fg_color="#1e2430",
                     corner_radius=0).pack(side="top", fill="x")

        status_lbl = ctk.CTkLabel(
            bottom, text="", font=("Arial", 11), text_color="#8a8e98"
        )
        status_lbl.pack(side="left", padx=22)

        save_btn = ctk.CTkButton(
            bottom, text=self.tr("settings_save_close_btn"),
            fg_color="#27ae60", hover_color="#2ecc71",
            width=180, height=38, font=("Arial", 12, "bold"),
            corner_radius=8,
        )
        save_btn.pack(side="right", padx=20, pady=10)

        # ============================================================
        #  TÖRZS — Sidebar + Content
        # ============================================================
        body = ctk.CTkFrame(win, fg_color="transparent")
        body.pack(fill="both", expand=True)

        # --- BAL: Sidebar ---
        sidebar = ctk.CTkFrame(body, fg_color="#0d0f14",
                                width=210, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkFrame(sidebar, width=1, fg_color="#1e2430",
                     corner_radius=0).pack(side="right", fill="y")

        tabs_container = ctk.CTkFrame(sidebar, fg_color="transparent")
        tabs_container.pack(fill="both", expand=True, padx=10, pady=14)

        # --- JOBB: Content ---
        content_wrap = ctk.CTkFrame(body, fg_color="#0a0c10", corner_radius=0)
        content_wrap.pack(side="right", fill="both", expand=True)

        # ---- Tab tárolók ----
        tab_buttons = {}       # key → {"btn", "indicator", "accent", "default_bg"}
        tab_frames = {}        # key → scrollable frame
        vars_store = {} 
        anim_state = {"current": None}

        # Content frame-ek létrehozása
        for key, icon, title_key, accent, bg in SETTINGS_TABS:
            sf = ctk.CTkScrollableFrame(content_wrap, fg_color="transparent")
            tab_frames[key] = sf

        # ---- Sidebar tab gombok ----
        def make_tab_button(key, icon, title_key, accent, bg):
            row = ctk.CTkFrame(
                tabs_container, fg_color="transparent",
                corner_radius=8, height=42,
            )
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)

            # Bal oldali indicator (accent sáv)
            indicator = ctk.CTkFrame(
                row, width=3, height=0, fg_color=accent,
                corner_radius=2,
            )
            indicator.pack(side="left", padx=(0, 0), pady=0)

            # Ikon
            icon_lbl = ctk.CTkLabel(
                row, text=icon, font=("Segoe UI Emoji", 15),
                text_color="#8a8e98", width=32,
            )
            icon_lbl.pack(side="left", padx=(10, 6))

            # Szöveg
            text_lbl = ctk.CTkLabel(
                row, text=self.tr(title_key),
                font=("Arial", 12),
                text_color="#b8bcc6", anchor="w",
            )
            text_lbl.pack(side="left", fill="x", expand=True)

            tab_buttons[key] = {
                "row": row,
                "indicator": indicator,
                "icon_lbl": icon_lbl,
                "text_lbl": text_lbl,
                "accent": accent,
                "default_bg": "#0d0f14",
                "hover_bg": "#1a2030",
                "active_bg": "#1e2430",
                "_anim_id": 0,
            }

            # Kattintás
            for w in (row, icon_lbl, text_lbl):
                w.bind("<Button-1>", lambda e, k=key: switch_tab(k))

            # Hover
            def on_enter(e, k=key):
                if anim_state["current"] == k:
                    return
                info = tab_buttons[k]
                self._animate_color(
                    info["row"], info["default_bg"], info["hover_bg"],
                    steps=5, delay=15, attr="fg_color", key=info,
                )

            def on_leave(e, k=key):
                if anim_state["current"] == k:
                    return
                info = tab_buttons[k]
                self._animate_color(
                    info["row"], info["hover_bg"], info["default_bg"],
                    steps=5, delay=15, attr="fg_color", key=info,
                )

            row.bind("<Enter>", on_enter)
            row.bind("<Leave>", on_leave)
            icon_lbl.bind("<Enter>", on_enter)
            icon_lbl.bind("<Leave>", on_leave)
            text_lbl.bind("<Enter>", on_enter)
            text_lbl.bind("<Leave>", on_leave)

        for key, icon, title_key, accent, bg in SETTINGS_TABS:
            make_tab_button(key, icon, title_key, accent, bg)

        # ---- Tab váltás animációval ----
        def _animate_indicator(key, target_h):
            info = tab_buttons[key]
            ind = info["indicator"]

            def setter(h):
                try:
                    ind.configure(height=max(0, h))
                except Exception:
                    pass

            steps = 8
            delay = 15

            def step(i=0):
                if i > steps:
                    setter(target_h)
                    return
                t = i / steps
                t = 1 - (1 - t) ** 3
                setter(int(target_h * t))
                ind.after(delay, lambda: step(i + 1))

            step(0)

        def switch_tab(new_key, animate=True):
            old_key = anim_state["current"]
            if old_key == new_key:
                return

            # Régi tab elrejtése
            if old_key and old_key in tab_buttons:
                old_info = tab_buttons[old_key]
                old_info["_anim_id"] += 1
                # Indicator összecsukás
                try:
                    old_info["indicator"].configure(height=0)
                except Exception:
                    pass
                # Szín vissza
                try:
                    old_info["row"].configure(fg_color=old_info["default_bg"])
                except Exception:
                    pass
                try:
                    old_info["icon_lbl"].configure(text_color="#8a8e98")
                except Exception:
                    pass
                try:
                    old_info["text_lbl"].configure(text_color="#b8bcc6")
                except Exception:
                    pass
                # Frame elrejtés
                try:
                    tab_frames[old_key].pack_forget()
                except Exception:
                    pass

            # Új tab megjelenítés
            anim_state["current"] = new_key
            new_info = tab_buttons[new_key]

            # Content fade-in
            sf = tab_frames[new_key]
            sf.pack(fill="both", expand=True, padx=0, pady=0)

            # Gombok színe
            new_info["_anim_id"] += 1
            my_id = new_info["_anim_id"]

            def bg_anim(i=0):
                if new_info["_anim_id"] != my_id:
                    return
                steps = 6
                delay = 15
                if i > steps:
                    try:
                        new_info["row"].configure(fg_color=new_info["active_bg"])
                    except Exception:
                        pass
                    return
                t = i / steps
                t = 1 - (1 - t) ** 3
                color = self._hex_lerp(
                    new_info["default_bg"], new_info["active_bg"], t
                )
                try:
                    new_info["row"].configure(fg_color=color)
                except Exception:
                    pass
                new_info["row"].after(delay, lambda: bg_anim(i + 1))

            bg_anim(0)

            # Ikon + szöveg accent színre
            try:
                new_info["icon_lbl"].configure(text_color=new_info["accent"])
                new_info["text_lbl"].configure(text_color=new_info["accent"])
            except Exception:
                pass

            # Indicator animáció (felfelé nő)
            row_h = new_info["row"].winfo_height()
            if row_h <= 1:
                row_h = 38
            _animate_indicator(new_key, row_h - 8)

            # Kártyák stagger animációja (ha még nem voltak "belépve")
            if not sf.winfo_children():
                build_tab_content(new_key, sf)
            # Belépő animáció minden alkalommal
            stagger_cards(sf)

        def stagger_cards(container):
            """A kártyák egymás után jelennek meg (fade + slide)."""
            kids = list(container.winfo_children())
            if not kids:
                return

            # Kezdetben mind rejtve
            for k in kids:
                try:
                    k.pack_forget()
                except Exception:
                    pass

            def show_one(i=0):
                if i >= len(kids):
                    return
                k = kids[i]
                try:
                    k.pack(fill="x", padx=18, pady=(0, 14), before=None)
                except Exception:
                    pass
                container.after(60, lambda: show_one(i + 1))

            show_one(0)

        # ============================================================
        #  TARTALOM ÉPÍTÉS — minden tabhoz
        # ============================================================
        def build_tab_content(key, parent):
            if key == "security":
                build_security(parent)
            elif key == "appearance":
                build_appearance(parent)
            elif key == "notifications":
                build_notifications(parent)
            elif key == "logs":
                build_logs(parent)
            elif key == "afk":
                build_afk(parent)
            elif key == "backup":
                build_backup(parent)
            elif key == "github":
                build_github(parent)
            elif key == "ai":
                build_ai(parent)
            elif key == "lan":
                build_lan(parent)


        # ---- 1. SECURITY ----
        def build_security(parent):
            accent, bg = "#e74c3c", "#241014"
            card = ctk.CTkFrame(
                parent, fg_color=bg, corner_radius=12,
                border_width=2, border_color=accent,
            )
            card.pack(fill="x", padx=18, pady=(14, 14))
            c = self._card_header(card, "🔐", self.tr("settings_sec_security"), accent)

            self._label(c, self.tr("settings_password_lbl"))
            password_entry = ctk.CTkEntry(
                c, show="*", width=320, placeholder_text="••••••••"
            )
            if self.panel_password:
                password_entry.insert(0, self.panel_password)
            password_entry.pack(anchor="w")
            vars_store["password_entry"] = password_entry

        # ---- 2. APPEARANCE ----
        def build_appearance(parent):
            accent, bg = "#9b59b6", "#1f1726"
            card = ctk.CTkFrame(
                parent, fg_color=bg, corner_radius=12,
                border_width=2, border_color=accent,
            )
            card.pack(fill="x", padx=18, pady=(14, 14))
            c = self._card_header(card, "🎨", self.tr("settings_sec_appearance"), accent)

            lang_row = ctk.CTkFrame(c, fg_color="transparent")
            lang_row.pack(fill="x", pady=4)
            ctk.CTkLabel(
                lang_row, text=self.tr("settings_language_lbl"),
                font=("Arial", 11), text_color="#b8bcc6",
                width=130, anchor="w",
            ).pack(side="left")
            language_var = ctk.StringVar(value=self.current_language)
            ctk.CTkComboBox(
                lang_row, values=["English", "Magyar"],
                variable=language_var, width=200,
                command=self.apply_language,
            ).pack(side="left")
            vars_store["language_var"] = language_var

            theme_row = ctk.CTkFrame(c, fg_color="transparent")
            theme_row.pack(fill="x", pady=(8, 4))
            ctk.CTkLabel(
                theme_row, text=self.tr("settings_theme_lbl"),
                font=("Arial", 11), text_color="#b8bcc6",
                width=130, anchor="w",
            ).pack(side="left")
            theme_var = ctk.StringVar(value=self.current_theme)
            ctk.CTkComboBox(
                theme_row, values=get_theme_names(),
                variable=theme_var, width=220,
            ).pack(side="left")
            vars_store["theme_var"] = theme_var

            tray_switch = ctk.CTkSwitch(c, text=self.tr("settings_tray_switch"))
            tray_switch.pack(anchor="w", pady=(12, 2))
            if self.minimize_to_tray_enabled:
                tray_switch.select()
            vars_store["tray_switch"] = tray_switch

            rpc_switch = ctk.CTkSwitch(c, text=self.tr("settings_rpc_switch"))
            rpc_switch.pack(anchor="w", pady=2)
            if self.rpc_enabled:
                rpc_switch.select()
            vars_store["rpc_switch"] = rpc_switch

        # ---- 3. NOTIFICATIONS ----
        def build_notifications(parent):
            accent, bg = "#f39c12", "#231f0f"
            card = ctk.CTkFrame(
                parent, fg_color=bg, corner_radius=12,
                border_width=2, border_color=accent,
            )
            card.pack(fill="x", padx=18, pady=(14, 14))
            c = self._card_header(card, "🔔", self.tr("settings_sec_notifications"), accent)

            ctk.CTkLabel(
                c, text=self.tr("settings_error_sound_lbl"),
                font=("Arial", 11), text_color="#b8bcc6", anchor="w",
            ).pack(fill="x", pady=(2, 4))

            sound_display_values = [self.tr(f"sound_{k}") for k in SOUND_KEYS]
            sound_display_var = ctk.StringVar(
                value=self._sound_display_name(self.selected_error_sound)
            )

            def on_sound_change(choice_display):
                k = self._sound_key_from_display(choice_display)
                play_error_sound_by_key(k)

            sound_row = ctk.CTkFrame(c, fg_color="transparent")
            sound_row.pack(fill="x")
            ctk.CTkComboBox(
                sound_row, values=sound_display_values,
                variable=sound_display_var,
                width=240, command=on_sound_change,
            ).pack(side="left")
            ctk.CTkButton(
                sound_row, text=self.tr("settings_sound_test_btn"),
                width=100, height=28,
                fg_color="#3498db", hover_color="#5dade2",
                command=lambda: play_error_sound_by_key(
                    self._sound_key_from_display(sound_display_var.get())
                ),
            ).pack(side="left", padx=8)
            vars_store["sound_display_var"] = sound_display_var

            # Elválasztó
            ctk.CTkFrame(c, height=1, fg_color="#3a2f1f").pack(
                fill="x", pady=(14, 10)
            )

            # Csendes órák
            quiet_switch = ctk.CTkSwitch(c, text=self.tr("settings_quiet_switch"))
            quiet_switch.pack(anchor="w", pady=(0, 6))
            if getattr(self, "quiet_hours_enabled", False):
                quiet_switch.select()

            ctk.CTkLabel(
                c, text=self.tr("settings_quiet_hint"),
                font=("Arial", 10), text_color="#8a8e98",
                justify="left", anchor="w", wraplength=440,
            ).pack(fill="x", pady=(0, 8))

            time_row = ctk.CTkFrame(c, fg_color="transparent")
            time_row.pack(fill="x", pady=2)

            ctk.CTkLabel(
                time_row, text=self.tr("settings_quiet_from_lbl"),
                font=("Arial", 11), text_color="#b8bcc6",
                width=100, anchor="w",
            ).pack(side="left")
            quiet_start_entry = ctk.CTkEntry(
                time_row, width=90, height=32, font=("Consolas", 12)
            )
            quiet_start_entry.insert(0, getattr(self, "quiet_hours_start", "22:00"))
            quiet_start_entry.pack(side="left", padx=(0, 12))

            ctk.CTkLabel(
                time_row, text=self.tr("settings_quiet_to_lbl"),
                font=("Arial", 11), text_color="#b8bcc6",
                width=30, anchor="w",
            ).pack(side="left")
            quiet_end_entry = ctk.CTkEntry(
                time_row, width=90, height=32, font=("Consolas", 12)
            )
            quiet_end_entry.insert(0, getattr(self, "quiet_hours_end", "06:00"))
            quiet_end_entry.pack(side="left", padx=(12, 0))

            quiet_status = ctk.CTkLabel(
                c, text="", font=("Arial", 10), anchor="w"
            )
            quiet_status.pack(fill="x", pady=(8, 0))

            def refresh_quiet_status():
                try:
                    self.quiet_hours_enabled = bool(quiet_switch.get())
                    self.quiet_hours_start = quiet_start_entry.get().strip()
                    self.quiet_hours_end = quiet_end_entry.get().strip()
                    if self.is_quiet_hours():
                        quiet_status.configure(
                            text=self.tr("settings_quiet_now_active"),
                            text_color="#e67e22",
                        )
                    else:
                        quiet_status.configure(
                            text=self.tr("settings_quiet_now_inactive"),
                            text_color="#2ecc71",
                        )
                except Exception:
                    pass

            quiet_switch.configure(command=refresh_quiet_status)
            quiet_start_entry.bind(
                "<KeyRelease>", lambda e: refresh_quiet_status()
            )
            quiet_end_entry.bind(
                "<KeyRelease>", lambda e: refresh_quiet_status()
            )
            refresh_quiet_status()

            vars_store["quiet_switch"] = quiet_switch
            vars_store["quiet_start_entry"] = quiet_start_entry
            vars_store["quiet_end_entry"] = quiet_end_entry

        # ---- 4. LOGS ----
        def build_logs(parent):
            accent, bg = "#3498db", "#152029"
            card = ctk.CTkFrame(
                parent, fg_color=bg, corner_radius=12,
                border_width=2, border_color=accent,
            )
            card.pack(fill="x", padx=18, pady=(14, 14))
            c = self._card_header(card, "📝", self.tr("settings_sec_logs"), accent)

            ctk.CTkLabel(
                c, text=self.tr("settings_log_level_lbl"),
                font=("Arial", 11), text_color="#b8bcc6", anchor="w",
            ).pack(fill="x", pady=(2, 4))

            log_display_values = [
                self.tr(f"settings_log_{k}") for k in LOG_LEVEL_KEYS
            ]
            log_display_var = ctk.StringVar(
                value=self._log_display_name(self.log_save_level)
            )
            ctk.CTkComboBox(
                c, values=log_display_values,
                variable=log_display_var, width=280,
            ).pack(anchor="w")
            vars_store["log_display_var"] = log_display_var

        # ---- 5. AFK ----
        def build_afk(parent):
            accent, bg = "#00bcd4", "#0f1a24"
            card = ctk.CTkFrame(
                parent, fg_color=bg, corner_radius=12,
                border_width=2, border_color=accent,
            )
            card.pack(fill="x", padx=18, pady=(14, 14))
            c = self._card_header(card, "💤", self.tr("settings_sec_afk"), accent)

            ctk.CTkLabel(
                c, text=self.tr("settings_afk_hint"),
                font=("Arial", 10), text_color="#8a8e98",
                justify="left", anchor="w",
            ).pack(fill="x", pady=(2, 8))

            afk_switch = ctk.CTkSwitch(c, text=self.tr("settings_afk_switch"))
            afk_switch.pack(anchor="w", pady=(0, 8))
            if getattr(self, "afk_enabled", True):
                afk_switch.select()
            vars_store["afk_switch"] = afk_switch

            ctk.CTkLabel(
                c, text=self.tr("settings_afk_timeout_lbl"),
                font=("Arial", 11), text_color="#b8bcc6", anchor="w",
            ).pack(fill="x", pady=(4, 2))

            afk_timeout_labels = [self.tr(k) for k, _ in AFK_TIMEOUT_OPTIONS]
            current_seconds = getattr(self, "afk_idle_seconds", 60)
            current_label = next(
                (self.tr(k) for k, val in AFK_TIMEOUT_OPTIONS
                 if val == current_seconds),
                self.tr("afk_timeout_1m"),
            )
            afk_timeout_var = ctk.StringVar(value=current_label)
            ctk.CTkComboBox(
                c, values=afk_timeout_labels,
                variable=afk_timeout_var, width=200,
            ).pack(anchor="w")
            vars_store["afk_timeout_var"] = afk_timeout_var

            ctk.CTkButton(
                c, text=self.tr("settings_afk_preview_btn"),
                height=32, fg_color="#16a085", hover_color="#1abc9c",
                width=200, command=self._afk_preview,
            ).pack(anchor="w", pady=(10, 0))

        # ---- 6. BACKUP ----
        def build_backup(parent):
            accent, bg = "#2980b9", "#101a26"
            card = ctk.CTkFrame(
                parent, fg_color=bg, corner_radius=12,
                border_width=2, border_color=accent,
            )
            card.pack(fill="x", padx=18, pady=(14, 14))
            c = self._card_header(card, "💾", self.tr("settings_sec_backup"), accent)

            backup_switch = ctk.CTkSwitch(
                c, text=self.tr("settings_backup_switch")
            )
            backup_switch.pack(anchor="w", pady=2)
            if self.backup_enabled:
                backup_switch.select()
            vars_store["backup_switch"] = backup_switch

            backup_start_switch = ctk.CTkSwitch(
                c, text=self.tr("settings_backup_start_switch")
            )
            backup_start_switch.pack(anchor="w", pady=2)
            if self.backup_on_start:
                backup_start_switch.select()
            vars_store["backup_start_switch"] = backup_start_switch

            ctk.CTkLabel(
                c, text=self.tr("settings_backup_interval_lbl"),
                font=("Arial", 11), text_color="#b8bcc6", anchor="w",
            ).pack(fill="x", pady=(10, 2))
            backup_interval_entry = ctk.CTkEntry(c, width=100)
            backup_interval_entry.insert(0, str(self.backup_interval_hours))
            backup_interval_entry.pack(anchor="w")
            vars_store["backup_interval_entry"] = backup_interval_entry

            ctk.CTkButton(
                c, text=self.tr("settings_backup_manager_btn"),
                height=32, fg_color="#3498db", hover_color="#5dade2",
                width=240, command=self.open_backup_manager,
            ).pack(anchor="w", pady=(12, 0))

        # ---- 7. GITHUB ----
        def build_github(parent):
            accent, bg = "#3498db", "#101a26"
            card = ctk.CTkFrame(
                parent, fg_color=bg, corner_radius=12,
                border_width=2, border_color=accent,
            )
            card.pack(fill="x", padx=18, pady=(14, 14))
            c = self._card_header(card, "🚀", self.tr("settings_sec_github"), accent)

            ctk.CTkLabel(
                c, text=self.tr("settings_github_hint"),
                font=("Arial", 10), text_color="#8a8e98",
                justify="left", anchor="w", wraplength=460,
            ).pack(fill="x", pady=(2, 8))

            ctk.CTkLabel(
                c, text=self.tr("settings_update_interval_lbl"),
                font=("Arial", 11), text_color="#b8bcc6", anchor="w",
            ).pack(fill="x", pady=(2, 4))

            current_minutes = getattr(
                self, "update_check_interval_minutes", 60
            )
            current_interval_label = next(
                (self.tr(k) for k, m in UPDATE_INTERVAL_OPTIONS
                 if m == current_minutes),
                self.tr("update_interval_1hour"),
            )
            update_interval_var = ctk.StringVar(value=current_interval_label)
            ctk.CTkComboBox(c, values=[self.tr(k) for k, _ in UPDATE_INTERVAL_OPTIONS], variable=update_interval_var, width=260).pack(anchor="w")
            vars_store["update_interval_var"] = update_interval_var   # ← EZT ADD HOZZÁ

            btn_row = ctk.CTkFrame(c, fg_color="transparent")
            btn_row.pack(fill="x", pady=(12, 0))

            ctk.CTkButton(
                btn_row, text=self.tr("settings_update_check_now_btn"),
                height=32, fg_color="#2980b9", hover_color="#3498db",
                width=180,
                command=lambda: self.check_for_updates(silent=False),
            ).pack(side="left", padx=(0, 6))

            ctk.CTkButton(
                btn_row, text=self.tr("settings_update_history_btn"),
                height=32, fg_color="#8e44ad", hover_color="#9b59b6",
                width=180,
                command=lambda: self.open_update_history_window(),
            ).pack(side="left")

        # ---- 8. AI ----
        def build_ai(parent):
            accent, bg = "#8e44ad", "#1a1230"
            card = ctk.CTkFrame(
                parent, fg_color=bg, corner_radius=12,
                border_width=2, border_color=accent,
            )
            card.pack(fill="x", padx=18, pady=(14, 14))
            c = self._card_header(card, "🤖", self.tr("settings_sec_ai"), accent)

            ctk.CTkLabel(
                c, text=self.tr("ai_settings_provider_lbl"),
                font=("Arial", 11), text_color="#b8bcc6", anchor="w",
            ).pack(fill="x", pady=(2, 4))
            provider_var = ctk.StringVar(
                value=getattr(self, "ai_provider", "OpenAI (GPT)")
            )
            ctk.CTkComboBox(
                c,
                values=[
                    "OpenAI (GPT)", "Anthropic (Claude)",
                    "Ollama (local)", "LM Studio (local)",
                ],
                variable=provider_var, width=280,
            ).pack(anchor="w")
            vars_store["provider_var"] = provider_var

            ctk.CTkLabel(
                c, text=self.tr("ai_settings_key_lbl"),
                font=("Arial", 11), text_color="#b8bcc6", anchor="w",
            ).pack(fill="x", pady=(10, 4))
            ai_key_entry = ctk.CTkEntry(
                c, show="*", width=380, placeholder_text="sk-..."
            )
            if getattr(self, "ai_api_key", ""):
                ai_key_entry.insert(0, self.ai_api_key)
            ai_key_entry.pack(anchor="w")
            vars_store["ai_key_entry"] = ai_key_entry

            ctk.CTkLabel(
                c, text=self.tr("settings_ai_model_lbl"),
                font=("Arial", 11), text_color="#b8bcc6", anchor="w",
            ).pack(fill="x", pady=(10, 4))
            ai_model_entry = ctk.CTkEntry(
                c, width=280, placeholder_text=getattr(self, "ai_model", "")
            )
            ai_model_entry.pack(anchor="w")
            vars_store["ai_model_entry"] = ai_model_entry

        # ---- 9. LAN ----
        def build_lan(parent):
            import secrets as _secrets

            accent, bg = "#16a085", "#0f2318"
            card = ctk.CTkFrame(
                parent, fg_color=bg, corner_radius=12,
                border_width=2, border_color=accent,
            )
            card.pack(fill="x", padx=18, pady=(14, 14))
            c = self._card_header(
                card, "🔗", self.tr("settings_sec_lan"), accent
            )

            # --- Host szekció ---
            ctk.CTkLabel(
                c, text="🖥️  " + self.tr("settings_lan_host_section"),
                font=("Arial", 12, "bold"), text_color="#16a085",
                anchor="w",
            ).pack(fill="x", pady=(2, 8))

            lan_switch = ctk.CTkSwitch(
                c, text=self.tr("settings_lan_enable")
            )
            lan_switch.pack(anchor="w", pady=(0, 6))
            if getattr(self, "lan_enabled", False):
                lan_switch.select()
            vars_store["lan_switch"] = lan_switch 

            # Port
            port_row = ctk.CTkFrame(c, fg_color="transparent")
            port_row.pack(fill="x", pady=(4, 2))
            ctk.CTkLabel(
                port_row, text=self.tr("settings_lan_port_lbl"),
                font=("Arial", 11), text_color="#b8bcc6",
                width=140, anchor="w",
            ).pack(side="left")
            lan_port_entry = ctk.CTkEntry(
                port_row, width=100, height=32, font=("Consolas", 12)
            )
            lan_port_entry.insert(0, str(getattr(self, "lan_port", 8765)))
            lan_port_entry.pack(side="left")
            vars_store["lan_port_entry"] = lan_port_entry

            # Token
            token_row = ctk.CTkFrame(c, fg_color="transparent")
            token_row.pack(fill="x", pady=(6, 2))
            ctk.CTkLabel(
                token_row, text=self.tr("settings_lan_token_lbl"),
                font=("Arial", 11), text_color="#b8bcc6",
                width=140, anchor="w",
            ).pack(side="left")

            token_value = getattr(self, "lan_token", "") or _secrets.token_hex(16)
            lan_token_entry = ctk.CTkEntry(
                token_row, width=260, height=32,
                font=("Consolas", 10),
            )
            lan_token_entry.insert(0, token_value)
            lan_token_entry.pack(side="left", padx=(0, 6))
            vars_store["lan_token_entry"] = lan_token_entry

            def copy_token():
                try:
                    self.clipboard_clear()
                    self.clipboard_append(lan_token_entry.get())
                    self.update()
                    self.notify(self.tr("copied_msg"), "success", 1500)
                except Exception:
                    pass

            def regen_token():
                new_token = _secrets.token_hex(16)
                lan_token_entry.delete(0, "end")
                lan_token_entry.insert(0, new_token)

            ctk.CTkButton(
                token_row, text="📋", width=36, height=32,
                fg_color="#3498db", hover_color="#5dade2",
                command=copy_token,
            ).pack(side="left", padx=2)
            ctk.CTkButton(
                token_row, text="🔄", width=36, height=32,
                fg_color="#9b59b6", hover_color="#8e44ad",
                command=regen_token,
            ).pack(side="left", padx=2)

            # Vezérlés engedélyezése
            allow_switch = ctk.CTkSwitch(
                c, text=self.tr("settings_lan_allow_control")
            )
            allow_switch.pack(anchor="w", pady=(10, 4))
            if getattr(self, "lan_allow_control", True):
                allow_switch.select()
            vars_store["lan_allow_switch"] = allow_switch

            # Státusz
            lan_status = ctk.CTkLabel(
                c, text="", font=("Arial", 10), anchor="w"
            )
            lan_status.pack(fill="x", pady=(4, 0))
            vars_store["lan_status_lbl"] = lan_status

            def refresh_lan_status():
                try:
                    if getattr(self, "lan_enabled", False) and self._lan_server is not None:
                        lan_status.configure(
                            text=self.tr("settings_lan_status_on",
                                          port=self.lan_port),
                            text_color="#2ecc71",
                        )
                    else:
                        lan_status.configure(
                            text=self.tr("settings_lan_status_off"),
                            text_color="#8a8e98",
                        )
                except Exception:
                    pass

            refresh_lan_status()

            # Elválasztó
            ctk.CTkFrame(c, height=1, fg_color="#1e3a2e").pack(
                fill="x", pady=(14, 10)
            )

            # --- Kliens szekció ---
            ctk.CTkLabel(
                c, text="🌐  " + self.tr("settings_lan_client_section"),
                font=("Arial", 12, "bold"), text_color="#3498db",
                anchor="w",
            ).pack(fill="x", pady=(0, 8))

            ctk.CTkLabel(
                c, text=self.tr("settings_lan_client_hint"),
                font=("Arial", 10), text_color="#8a8e98",
                justify="left", anchor="w", wraplength=520,
            ).pack(fill="x", pady=(0, 10))

            ctk.CTkButton(
                c, text=self.tr("settings_lan_open_client"),
                height=38, fg_color="#3498db", hover_color="#5dade2",
                width=280, font=("Arial", 12, "bold"),
                command=self.open_lan_client_window,
            ).pack(anchor="w")

        # --- MINDEN TAB ELŐRE FELÉPÍTÉSE ---
        for _key, _icon, _title, _accent, _bg in SETTINGS_TABS:
            _frame = tab_frames[_key]
            build_tab_content(_key, _frame)
            _frame.pack_forget()

        # ============================================================
        #  MENTÉS
        # ============================================================
        def save_settings():
            print(f"[DEBUG] save_settings elindult")
            print(f"[DEBUG] vars_store kulcsok: {list(vars_store.keys())}")
            # --- Panel beállítások (biztonságos get) ---
            _v = vars_store.get("language_var")
            if _v is not None:
                self.current_language = _v.get()

            _v = vars_store.get("password_entry")
            if _v is not None:
                self.panel_password = _v.get().strip() or self.panel_password

            _v = vars_store.get("tray_switch")
            if _v is not None:
                self.minimize_to_tray_enabled = bool(_v.get())

            _v = vars_store.get("rpc_switch")
            if _v is not None:
                self.rpc_enabled = bool(_v.get())

            # Csendes órák
            _v = vars_store.get("quiet_switch")
            if _v is not None:
                self.quiet_hours_enabled = bool(_v.get())
            _v = vars_store.get("quiet_start_entry")
            if _v is not None:
                self.quiet_hours_start = _v.get().strip() or "22:00"
            _v = vars_store.get("quiet_end_entry")
            if _v is not None:
                self.quiet_hours_end = _v.get().strip() or "06:00"

            # Hang + log
            _v = vars_store.get("log_display_var")
            if _v is not None:
                self.log_save_level = self._log_key_from_display(_v.get())
            _v = vars_store.get("sound_display_var")
            if _v is not None:
                self.selected_error_sound = self._sound_key_from_display(_v.get())

            # AFK
            _v = vars_store.get("afk_switch")
            if _v is not None:
                self.afk_enabled = bool(_v.get())
            _v = vars_store.get("afk_timeout_var")
            if _v is not None:
                selected_timeout_label = _v.get()
                for key, seconds in AFK_TIMEOUT_OPTIONS:
                    if self.tr(key) == selected_timeout_label:
                        self.afk_idle_seconds = seconds
                        break

            # Backup
            _v = vars_store.get("backup_switch")
            if _v is not None:
                self.backup_enabled = bool(_v.get())
            _v = vars_store.get("backup_start_switch")
            if _v is not None:
                self.backup_on_start = bool(_v.get())
            _v = vars_store.get("backup_interval_entry")
            if _v is not None:
                try:
                    self.backup_interval_hours = max(0, int(_v.get()))
                except ValueError:
                    status_lbl.configure(
                        text=self.tr("settings_err_backup_interval"),
                        text_color="#e74c3c",
                    )
                    return

            # GitHub update intervallum
            _v = vars_store.get("update_interval_var")
            if _v is not None:
                selected_update_label = _v.get()
                for key, minutes in UPDATE_INTERVAL_OPTIONS:
                    if self.tr(key) == selected_update_label:
                        self.update_check_interval_minutes = minutes
                        break

            try:
                if getattr(self, "_update_check_after_id", None):
                    self.after_cancel(self._update_check_after_id)
                    self._update_check_after_id = None
            except Exception:
                pass

            if self.update_check_interval_minutes > 0:
                self.after(200, lambda: self.schedule_update_check(
                    interval_minutes=self.update_check_interval_minutes
                ))

            # AI
            _v = vars_store.get("provider_var")
            if _v is not None:
                self.ai_provider = _v.get()
            _v = vars_store.get("ai_key_entry")
            if _v is not None:
                self.ai_api_key = _v.get().strip()
            _v = vars_store.get("ai_model_entry")
            if _v is not None:
                self.ai_model = _v.get().strip()

            # --- LAN ---
            print(f"[DEBUG] LAN előtt, vars_store lan kulcsok: lan_switch={'lan_switch' in vars_store}")
            lan_sw = vars_store.get("lan_switch")
            lan_port_entry = vars_store.get("lan_port_entry")
            lan_token_entry = vars_store.get("lan_token_entry")
            lan_allow_sw = vars_store.get("lan_allow_switch")

            if lan_sw is not None:
                old_enabled = getattr(self, "lan_enabled", False)
                old_port = getattr(self, "lan_port", 8765)
                old_token = getattr(self, "lan_token", "")

                print(f"[DEBUG] lan_enabled beállítva: {self.lan_enabled}")
                self.lan_enabled = bool(lan_sw.get())

                if lan_port_entry is not None:
                    try:
                        self.lan_port = int(lan_port_entry.get().strip())
                    except (ValueError, AttributeError):
                        self.lan_port = 8765

                if lan_token_entry is not None:
                    self.lan_token = lan_token_entry.get().strip()

                if lan_allow_sw is not None:
                    self.lan_allow_control = bool(lan_allow_sw.get())

                # Szerver újraindítás, ha változott
                if (old_enabled != self.lan_enabled
                        or old_port != self.lan_port
                        or old_token != self.lan_token):
                    if self.lan_enabled:
                        self.after(300, self.restart_lan_server)
                    else:
                        self.stop_lan_server()

            # --- Bot beállítások ---
            bot = self.bots.get(self.active_bot_key)
            if bot:
                _v = vars_store.get("test_switch")
                if _v is not None:
                    bot["test_mode"] = bool(_v.get())
                _v = vars_store.get("crash_switch")
                if _v is not None:
                    bot["auto_restart_on_crash"] = bool(_v.get())
                _v = vars_store.get("crash_delay_entry")
                if _v is not None:
                    try:
                        bot["crash_restart_delay"] = max(1, int(_v.get()))
                    except ValueError:
                        status_lbl.configure(
                            text=self.tr("settings_err_crash_delay"),
                            text_color="#e74c3c",
                        )
                        return
                _v = vars_store.get("testers_entry")
                if _v is not None:
                    bot["allowed_discord_ids"] = [
                        x.strip() for x in _v.get().split(",")
                        if x.strip().isdigit()
                    ]
                _v = vars_store.get("ram_entry")
                if _v is not None:
                    try:
                        self.max_ram_mb = max(50, int(_v.get()))
                    except ValueError:
                        status_lbl.configure(
                            text=self.tr("settings_err_ram"),
                            text_color="#e74c3c",
                        )
                        return

            # Téma
            _v = vars_store.get("theme_var")
            if _v is not None:
                selected_theme = _v.get()
                if selected_theme != self.current_theme:
                    self.apply_theme_setting(selected_theme)

            # --- MENTÉS ---
            self.save_config()
            print(f"[DEBUG] save_config lefutott, self.lan_enabled = {getattr(self, 'lan_enabled', 'NINCS')}")
            self.update_ui_texts()

            status_lbl.configure(
                text=self.tr("settings_saved_status"),
                text_color="#2ecc71",
            )
            self.notify(self.tr("settings_saved_toast"), "success", 2000)
            self.after(400, win.destroy)

        # Save gomb hozzákötése a mentés függvényhez
        save_btn.configure(command=save_settings)

        # ============================================================
        #  INDÍTÁS — első tab aktív
        # ============================================================
        switch_tab("security", animate=False)

    # ==================================================================
    #  AFK előnézet
    # ==================================================================
    def _afk_preview(self):
        try:
            if hasattr(self, "_show_afk_screen"):
                if getattr(self, "_afk_running", False):
                    return
                self._show_afk_screen()
        except Exception as e:
            print(f"[AFK] Előnézet hiba: {e}")