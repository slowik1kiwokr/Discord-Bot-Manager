import os
import json
import datetime

import customtkinter as ctk

import modules.config as config


class StreakMixin:
    """Napi streak követés."""

    def init_streak(self):
        self.streak_file = os.path.join(config.SCRIPT_DIR, "streak.json")
        self.streak_data = self._load_streak()
        self._update_streak()

    def _load_streak(self):
        if os.path.exists(self.streak_file):
            try:
                with open(self.streak_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (OSError, json.JSONDecodeError):
                pass
        return {"current": 0, "best": 0, "last_open": "", "total_days": 0}

    def _save_streak(self):
        try:
            with open(self.streak_file, "w", encoding="utf-8") as f:
                json.dump(self.streak_data, f, ensure_ascii=False, indent=4)
        except OSError:
            pass

    def _update_streak(self):
        today = datetime.date.today().isoformat()
        last = self.streak_data.get("last_open", "")

        if last == today:
            return  # már ma megnyitottad

        if last:
            try:
                last_date = datetime.date.fromisoformat(last)
                delta = (datetime.date.today() - last_date).days
                if delta == 1:
                    self.streak_data["current"] = self.streak_data.get("current", 0) + 1
                elif delta > 1:
                    self.streak_data["current"] = 1
            except ValueError:
                self.streak_data["current"] = 1
        else:
            self.streak_data["current"] = 1

        self.streak_data["last_open"] = today
        self.streak_data["total_days"] = self.streak_data.get("total_days", 0) + 1

        if self.streak_data["current"] > self.streak_data.get("best", 0):
            self.streak_data["best"] = self.streak_data["current"]

        self._save_streak()

        # Toast üzenet
        current = self.streak_data["current"]
        try:
            if current == 1:
                self.notify("🔥 Új streak elkezdve!", "info", 3000)
            elif current in (3, 7, 14, 30, 60, 100, 365):
                self.notify(f"🔥 {current} napos streak!", "success", 5000)
            else:
                self.notify(f"🔥 {current} napos streak", "info", 2500)
        except Exception:
            pass

        self.log_event("EVENT", f"[STREAK] {current} nap (best: {self.streak_data['best']})")

    def get_streak_text(self):
        return f"🔥 {self.streak_data.get('current', 0)} nap"

    # ------------------------------------------------------------------
    #  Kis kártya a sidebar-hoz
    # ------------------------------------------------------------------
    def build_streak_widget(self, parent):
        card = ctk.CTkFrame(parent, fg_color="#2a1a10",
                             corner_radius=10, border_width=2,
                             border_color="#f39c12")
        card.pack(fill="x", padx=6, pady=(8, 4))

        ctk.CTkLabel(card, text="🔥  STREAK",
                     font=("Arial", 9, "bold"),
                     text_color="#f39c12").pack(pady=(10, 2))

        current = self.streak_data.get("current", 0)
        best = self.streak_data.get("best", 0)

        ctk.CTkLabel(card, text=f"{current} nap",
                     font=("Arial", 18, "bold"),
                     text_color="#f39c12").pack()

        ctk.CTkLabel(card, text=f"Legjobb: {best} nap",
                     font=("Arial", 9), text_color="#aaa").pack(pady=(0, 10))

        return card