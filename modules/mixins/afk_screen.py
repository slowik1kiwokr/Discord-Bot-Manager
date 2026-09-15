import os
import time
import datetime

import customtkinter as ctk


class AfkScreenMixin:
    """AFK képernyő — tétlenség után megjelenő bot-állapot nézet."""

    # Nyelvi kulcsok a napokhoz / hónapokhoz
    _DAY_KEYS = [
        "day_monday", "day_tuesday", "day_wednesday", "day_thursday",
        "day_friday", "day_saturday", "day_sunday",
    ]
    _MONTH_KEYS = [
        "month_january", "month_february", "month_march", "month_april",
        "month_may", "month_june", "month_july", "month_august",
        "month_september", "month_october", "month_november", "month_december",
    ]

    # ------------------------------------------------------------------
    #  Inicializálás
    # ------------------------------------------------------------------
    def init_afk_screen(self, idle_seconds=60):
        self._afk_idle_seconds = getattr(self, "afk_idle_seconds", idle_seconds)
        self._afk_last_activity = time.time()
        self._afk_window = None
        self._afk_running = False
        self._afk_armed = False
        self._afk_after_id = None
        self._afk_animation_ids = []
        self._afk_widgets = {}

        try:
            self.bind_all("<Button>", self._afk_reset, add="+")
            self.bind_all("<Key>", self._afk_reset, add="+")
            self.bind_all("<Motion>", self._afk_reset, add="+")
            self.bind_all("<MouseWheel>", self._afk_reset, add="+")
        except Exception as e:
            print(f"[AFK] Bind hiba: {e}")

        self._afk_check()

    # ------------------------------------------------------------------
    #  Idle detektálás
    # ------------------------------------------------------------------
    def _afk_reset(self, event=None):
        self._afk_last_activity = time.time()
        if self._afk_running and self._afk_armed:
            self._close_afk_screen()

    def _afk_check(self):
        try:
            if not self.winfo_exists():
                return
        except Exception:
            return

        if not getattr(self, "is_monitoring", True):
            return

        if not getattr(self, "afk_enabled", True):
            try:
                self._afk_after_id = self.after(1000, self._afk_check)
            except Exception:
                pass
            return

        idle = time.time() - self._afk_last_activity
        if idle >= getattr(self, "afk_idle_seconds", self._afk_idle_seconds) and not self._afk_running:
            self._show_afk_screen()

        try:
            self._afk_after_id = self.after(1000, self._afk_check)
        except Exception:
            pass

    # ------------------------------------------------------------------
    #  AFK screen megjelenítése
    # ------------------------------------------------------------------
    def _show_afk_screen(self):
        self._afk_running = True
        self._afk_armed = False
        self._afk_animation_ids = []
        self._afk_widgets = {}

        win = ctk.CTkToplevel(self)
        self._afk_window = win
        win.overrideredirect(True)
        try:
            win.attributes("-topmost", True)
            win.attributes("-alpha", 0.0)
        except Exception:
            pass
        win.configure(fg_color="#0d0f14")

        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        w, h = 760, 680
        x = (sw - w) // 2
        y = (sh - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")

        border = ctk.CTkFrame(
            win, fg_color="#0d0f14", corner_radius=20,
            border_width=2, border_color="#5865F2",
        )
        border.pack(fill="both", expand=True, padx=1, pady=1)

        # --- Logó (csak logo.jpg) ---
        logo_frame = ctk.CTkFrame(border, fg_color="transparent")
        logo_frame.pack(fill="x", pady=(30, 12))
        self._build_afk_logo(logo_frame)

        # --- Óra ---
        clock_frame = ctk.CTkFrame(border, fg_color="transparent")
        clock_frame.pack(pady=(0, 4))

        self._afk_widgets["clock"] = ctk.CTkLabel(
            clock_frame, text="00:00:00",
            font=("Consolas", 44, "bold"), text_color="#ffffff",
        )
        self._afk_widgets["clock"].pack()

        self._afk_widgets["date"] = ctk.CTkLabel(
            clock_frame, text="",
            font=("Segoe UI", 12), text_color="#8a8e98",
        )
        self._afk_widgets["date"].pack(pady=(2, 0))

        ctk.CTkFrame(border, height=1, fg_color="#2f3542").pack(fill="x", padx=60, pady=(18, 12))

        # --- Összesítő kártyák ---
        summary_frame = ctk.CTkFrame(border, fg_color="transparent")
        summary_frame.pack(pady=(0, 8))

        self._afk_widgets["running_count"] = self._make_afk_stat(
            summary_frame, "🟢", self.tr("afk_stat_running"), "#2ecc71", "0"
        )
        self._afk_widgets["stopped_count"] = self._make_afk_stat(
            summary_frame, "🔴", self.tr("afk_stat_stopped"), "#e74c3c", "0"
        )
        self._afk_widgets["error_count"] = self._make_afk_stat(
            summary_frame, "⚠️", self.tr("afk_stat_error"), "#f39c12", "0"
        )

        ctk.CTkFrame(border, height=1, fg_color="#2f3542").pack(fill="x", padx=60, pady=(10, 10))

        # --- Bot lista ---
        bots_frame = ctk.CTkScrollableFrame(
            border, fg_color="#0a0c10",
            corner_radius=12, height=200,
        )
        bots_frame.pack(fill="both", expand=True, padx=50, pady=(0, 12))

        self._afk_widgets["bots_frame"] = bots_frame
        self._afk_widgets["bot_rows"] = {}
        self._build_afk_bots_list(bots_frame)

        ctk.CTkLabel(
            border,
            text=self.tr("afk_hint"),
            font=("Segoe UI", 10), text_color="#6a6e78",
        ).pack(pady=(0, 20))

        self._afk_fade_in(win, 0.0)
        self._afk_animate()

        self.after(1500, self._afk_arm)

        try:
            win.focus_force()
        except Exception:
            pass

    def _afk_arm(self):
        self._afk_armed = True

    def _afk_preview(self):
        try:
            if getattr(self, "_afk_running", False):
                return
            self._show_afk_screen()
        except Exception as e:
            print(f"[AFK] Előnézet hiba: {e}")

    # ------------------------------------------------------------------
    #  Logó
    # ------------------------------------------------------------------
    def _build_afk_logo(self, parent):
        """Betölti a logo.jpg-t a panel gyökeréből."""
        from PIL import Image
        import modules.config as config

        # Helyes útvonal — a panel gyökere
        script_dir = config.SCRIPT_DIR

        # Elsődleges: logo.jpg
        logo_path = os.path.join(script_dir, "logo.jpg")
        if not os.path.isfile(logo_path):
            logo_path = os.path.join(script_dir, "logo.png")
        if not os.path.isfile(logo_path):
            logo_path = os.path.join(script_dir, "logo_clean.png")

        print(f"[AFK] Logó keresés: {logo_path}")

        if os.path.isfile(logo_path):
            try:
                pil = Image.open(logo_path).convert("RGBA")
                max_w, max_h = 260, 260
                ratio = min(max_w / pil.width, max_h / pil.height)
                new_w = int(pil.width * ratio)
                new_h = int(pil.height * ratio)
                img = ctk.CTkImage(light_image=pil, dark_image=pil, size=(new_w, new_h))
                self._afk_widgets["logo_image"] = img
                ctk.CTkLabel(parent, image=img, text="").pack(expand=True)
                return
            except Exception as e:
                print(f"[AFK] Logó betöltési hiba: {e}")
        else:
            print(f"[AFK] A logó fájl nem található: {logo_path}")

        # Fallback: emoji
        ctk.CTkLabel(
            parent, text="🛡️",
            font=("Segoe UI Emoji", 120), text_color="#5865F2",
        ).pack(expand=True)

    # ------------------------------------------------------------------
    #  Összesítő kártya
    # ------------------------------------------------------------------
    def _make_afk_stat(self, parent, icon, label, color, value):
        frame = ctk.CTkFrame(
            parent, fg_color="#1a1d24", corner_radius=10,
            border_width=1, border_color="#2f3542",
        )
        frame.pack(side="left", padx=8, ipadx=14, ipady=8)

        top = ctk.CTkFrame(frame, fg_color="transparent")
        top.pack()

        ctk.CTkLabel(top, text=icon, font=("Segoe UI Emoji", 12)).pack(side="left", padx=(0, 4))
        ctk.CTkLabel(top, text=label, font=("Segoe UI", 9, "bold"),
                      text_color="#8a8e98").pack(side="left")

        val_label = ctk.CTkLabel(
            frame, text=value,
            font=("Segoe UI", 22, "bold"), text_color=color,
        )
        val_label.pack()
        return val_label

    # ------------------------------------------------------------------
    #  Bot lista
    # ------------------------------------------------------------------
    def _build_afk_bots_list(self, parent):
        for child in parent.winfo_children():
            child.destroy()
        self._afk_widgets["bot_rows"] = {}

        bots = list(self.bots.items())
        if not bots:
            ctk.CTkLabel(
                parent, text=self.tr("afk_no_bots"),
                font=("Segoe UI", 12), text_color="#6a6e78",
            ).pack(pady=30)
            return

        for bot_key, bot in bots:
            row = ctk.CTkFrame(parent, fg_color="#151820", corner_radius=8)
            row.pack(fill="x", padx=6, pady=3)

            emoji = bot.get("emoji", "🤖")
            color = bot.get("color", "#5865F2")

            dot_label = ctk.CTkLabel(
                row, text="●", font=("Segoe UI", 14),
                text_color=color, width=20,
            )
            dot_label.pack(side="left", padx=(12, 4), pady=10)

            name_frame = ctk.CTkFrame(row, fg_color="transparent")
            name_frame.pack(side="left", fill="x", expand=True, pady=10)
            ctk.CTkLabel(
                name_frame, text=f"{emoji}  {bot_key}",
                font=("Segoe UI", 12, "bold"),
                text_color="#ffffff", anchor="w",
            ).pack(fill="x")

            status_label = ctk.CTkLabel(
                row, text="", font=("Consolas", 11, "bold"),
                text_color="#8a8e98", width=190, anchor="e",
            )
            status_label.pack(side="right", padx=14, pady=10)

            self._afk_widgets["bot_rows"][bot_key] = {
                "dot": dot_label,
                "status": status_label,
                "color": color,
                "base_color": color,
            }

    # ------------------------------------------------------------------
    #  Fade-in animáció
    # ------------------------------------------------------------------
    def _afk_fade_in(self, win, alpha):
        if not self._afk_running:
            return
        try:
            new_alpha = min(1.0, alpha + 0.08)
            win.attributes("-alpha", new_alpha)
            if new_alpha < 1.0:
                aid = self.after(20, lambda: self._afk_fade_in(win, new_alpha))
                self._afk_animation_ids.append(aid)
        except Exception:
            pass

    # ------------------------------------------------------------------
    #  Élő animációk
    # ------------------------------------------------------------------
    def _afk_animate(self):
        if not self._afk_running:
            return
        try:
            if not (self._afk_window and self._afk_window.winfo_exists()):
                return
        except Exception:
            return

        now = datetime.datetime.now()

        try:
            self._afk_widgets["clock"].configure(text=now.strftime("%H:%M:%S"))
            day_name = self.tr(self._DAY_KEYS[now.weekday()])
            month_name = self.tr(self._MONTH_KEYS[now.month - 1])
            date_text = self.tr(
                "afk_date_format",
                year=now.year,
                month=month_name,
                day=now.day,
                day_name=day_name,
            )
            self._afk_widgets["date"].configure(text=date_text)
        except Exception:
            pass

        running = sum(1 for b in self.bots.values() if b.get("is_running"))
        stopped = len(self.bots) - running
        total_errors = sum(b.get("error_count", 0) for b in self.bots.values())

        try:
            self._afk_widgets["running_count"].configure(text=str(running))
            self._afk_widgets["stopped_count"].configure(text=str(stopped))
            self._afk_widgets["error_count"].configure(text=str(total_errors))
        except Exception:
            pass

        pulse = (int(time.time() * 2) % 2) == 0

        for bot_key, widgets in self._afk_widgets.get("bot_rows", {}).items():
            bot = self.bots.get(bot_key)
            if not bot:
                continue

            is_running = bot.get("is_running", False)

            if is_running and bot.get("start_time"):
                sec = int(time.time() - bot["start_time"])
                h, rem = divmod(sec, 3600)
                m, s = divmod(rem, 60)
                status_text = f"🟢  ⏱  {h:02d}:{m:02d}:{s:02d}"
                status_color = "#2ecc71"
            else:
                status_text = f"🔴  {self.tr('afk_status_stopped')}"
                status_color = "#e74c3c"

            try:
                widgets["status"].configure(text=status_text, text_color=status_color)
            except Exception:
                pass

            try:
                if is_running:
                    if pulse:
                        widgets["dot"].configure(text_color=widgets["base_color"])
                    else:
                        widgets["dot"].configure(text_color="#1e2a1e")
                else:
                    widgets["dot"].configure(text_color="#2a1e1e")
            except Exception:
                pass

        try:
            aid = self.after(1000, self._afk_animate)
            self._afk_animation_ids.append(aid)
        except Exception:
            pass

    # ------------------------------------------------------------------
    #  Bezárás
    # ------------------------------------------------------------------
    def _close_afk_screen(self):
        self._afk_running = False
        self._afk_armed = False

        for aid in self._afk_animation_ids:
            try:
                self.after_cancel(aid)
            except Exception:
                pass
        self._afk_animation_ids = []

        try:
            if self._afk_window and self._afk_window.winfo_exists():
                self._afk_window.destroy()
        except Exception:
            pass
        self._afk_window = None

        self._afk_last_activity = time.time()

    def stop_afk_screen(self):
        self._afk_idle_seconds = 999999
        self._close_afk_screen()