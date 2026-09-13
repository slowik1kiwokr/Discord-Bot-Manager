import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk


class HotkeysMixin:
    """Billentyűparancsok a főablakhoz."""

    def register_hotkeys(self):
        """A főablakhoz köti a gyorsgombokat."""
        # Fájl műveletek
        self.bind("<Control-s>", self._hk_save)
        self.bind("<Control-S>", self._hk_save)
        self.bind("<Control-b>", self._hk_backup)
        self.bind("<Control-B>", self._hk_backup)

        # Bot vezérlés
        self.bind("<Control-r>", self._hk_restart_all)
        self.bind("<Control-R>", self._hk_restart_all)

        # Keresés
        self.bind("<Control-f>", self._hk_focus_search)
        self.bind("<Control-F>", self._hk_focus_search)

        # Napló
        self.bind("<Control-l>", self._hk_clear_logs)
        self.bind("<Control-L>", self._hk_clear_logs)

        # Ablakok
        self.bind("<Control-t>", self._hk_tutorial)
        self.bind("<Control-T>", self._hk_tutorial)
        self.bind("<Control-comma>", self._hk_settings)
        self.bind("<F1>", self._hk_tutorial)
        self.bind("<F5>", self._hk_refresh)

        # Bezárás
        self.bind("<Control-w>", lambda e: self.on_window_close())
        self.bind("<Control-W>", lambda e: self.on_window_close())

        # Gyorsgombok súgó
        self.bind("<F2>", self._hk_show_help)

        self.log_event("EVENT", "[HOTKEYS] Gyorsgombok regisztrálva.")

    # ------------------------------------------------------------------
    #  Segédfüggvény: beviteli mezőben vagyunk-e?
    # ------------------------------------------------------------------
    def _in_text_input(self):
        """Igaz, ha a fókusz egy beviteli mezőn van."""
        try:
            focused = self.focus_get()
        except Exception:
            return False
        if focused is None:
            return False
        text_input_types = (
            tk.Entry, tk.Text,
            ctk.CTkEntry, ctk.CTkTextbox,
        )
        return isinstance(focused, text_input_types)

    # ------------------------------------------------------------------
    #  Hotkey kezelők
    # ------------------------------------------------------------------
    def _hk_save(self, event=None):
        if self._in_text_input():
            return
        try:
            self.save_config()
            self.notify("💾 Beállítások mentve", "success")
        except Exception as e:
            self.notify(f"Mentési hiba: {e}", "error")
        return "break"

    def _hk_backup(self, event=None):
        if self._in_text_input():
            return
        try:
            self.create_backup(show_message=False)
            self.notify("💾 Biztonsági mentés elkészült", "success")
        except Exception as e:
            self.notify(f"Mentési hiba: {e}", "error")
        return "break"

    def _hk_restart_all(self, event=None):
        if self._in_text_input():
            return
        if not messagebox.askyesno(
            "Megerősítés",
            "Biztosan újraindítod az ÖSSZES botot?"
        ):
            return
        try:
            self.restart_all_bots()
            self.notify("🔄 Összes bot újraindítva", "info")
        except Exception as e:
            self.notify(f"Hiba: {e}", "error")
        return "break"

    def _hk_focus_search(self, event=None):
        try:
            self.search_entry.focus_set()
        except Exception:
            pass
        return "break"

    def _hk_clear_logs(self, event=None):
        if self._in_text_input():
            return
        self.clear_logs()
        self.notify("🧹 Naplók törölve", "info")
        return "break"

    def _hk_tutorial(self, event=None):
        try:
            self.open_tutorial_window()
        except Exception:
            pass
        return "break"

    def _hk_settings(self, event=None):
        try:
            self.open_settings_window_v2()
        except Exception:
            pass
        return "break"

    def _hk_refresh(self, event=None):
        try:
            self.update_stats_loop()
        except Exception:
            pass
        return "break"

    def _hk_show_help(self, event=None):
        """F2 — gyorsgombok listája."""
        help_text = (
            "⌨️  Gyorsgombok\n\n"
            "Ctrl + S     Beállítások mentése\n"
            "Ctrl + B     Biztonsági mentés készítése\n"
            "Ctrl + R     Összes bot újraindítása\n"
            "Ctrl + F     Keresés a naplókban\n"
            "Ctrl + L     Naplók törlése\n"
            "Ctrl + T     Tutorial megnyitása\n"
            "Ctrl + ,     Beállítások megnyitása\n"
            "Ctrl + W     Panel bezárása\n"
            "F1           Tutorial\n"
            "F2           Ez a súgó\n"
            "F5           Statisztikák frissítése\n"
        )
        messagebox.showinfo("⌨️ Gyorsgombok", help_text)
        return "break"