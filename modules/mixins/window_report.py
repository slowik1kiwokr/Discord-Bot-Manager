import os
import json
import datetime
from collections import Counter
from tkinter import filedialog, messagebox

import customtkinter as ctk

import modules.config as config


class WindowReportMixin:
    """Havi riport ablak és automatikus riport figyelő."""

    # ------------------------------------------------------------------
    #  Automatikus riport figyelő
    # ------------------------------------------------------------------
    def init_monthly_report(self):
        """Ellenőrzi, hogy eljött-e az új hónap és felugrik-e a riport."""
        self.after(8000, self._check_monthly_report)

    def _check_monthly_report(self):
        """Ha új hónap kezdődött, felajánlja a havi riportot."""
        current_month = datetime.datetime.now().strftime("%Y-%m")
        last_report = getattr(self, "last_report_month", "") or ""

        if last_report != current_month:
            # Új hónap van, kérdezzük meg
            result = messagebox.askyesno(
                "📊 Havi riport",
                f"Új hónap kezdődött!\n\n"
                f"Szeretnéd látni a(z) {self._previous_month_name()} "
                f"havi összefoglalót?\n\n"
                f"(A 'Nem' gombra kattintva is megnyithatod "
                f"később a 📊 Havi riport menüből.)",
                parent=self
            )
            self.last_report_month = current_month
            self.save_config()

            if result:
                self.after(300, lambda: self.open_monthly_report_window(previous=True))

        # Következő ellenőrzés 6 óra múlva
        self.after(6 * 3600 * 1000, self._check_monthly_report)

    def _previous_month_name(self):
        """Az előző hónap neve magyarul."""
        today = datetime.date.today()
        first_of_month = today.replace(day=1)
        last_month = first_of_month - datetime.timedelta(days=1)
        months_hu = [
            "január", "február", "március", "április", "május", "június",
            "július", "augusztus", "szeptember", "október", "november", "december"
        ]
        return f"{last_month.year}. {months_hu[last_month.month - 1]}"

    # ------------------------------------------------------------------
    #  Riport ablak
    # ------------------------------------------------------------------
    def open_monthly_report_window(self, previous=False):
        """Megnyitja a havi riport ablakot."""
        win = ctk.CTkToplevel(self)
        win.title("📊 Havi riport")
        win.geometry("820x680")
        win.minsize(700, 520)
        win.grab_set()

        win.update_idletasks()
        x = (win.winfo_screenwidth() - 820) // 2
        y = (win.winfo_screenheight() - 680) // 2
        win.geometry(f"820x680+{x}+{y}")

        # --- Fejléc ---
        header = ctk.CTkFrame(win, fg_color="#8e44ad", corner_radius=0, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text="📊 Havi riport",
            font=("Arial", 22, "bold"), text_color="white"
        ).pack(pady=(14, 0))

        # Hónap választó
        month_frame = ctk.CTkFrame(win, fg_color="transparent")
        month_frame.pack(fill="x", padx=20, pady=(12, 4))

        ctk.CTkLabel(
            month_frame, text="Hónap:",
            font=("Arial", 13, "bold")
        ).pack(side="left", padx=(0, 8))

        # Elmúlt 12 hónap
        today = datetime.date.today()
        months_list = []
        for i in range(12):
            d = today.replace(day=1) - datetime.timedelta(days=i * 30)
            months_list.append(d.strftime("%Y-%m"))

        current_selection = month_frame.winfo_children()  # placeholder
        month_var = ctk.StringVar(value=months_list[1] if previous and len(months_list) > 1 else months_list[0])
        ctk.CTkComboBox(
            month_frame, values=months_list, variable=month_var,
            width=140, command=lambda v: refresh_report(v)
        ).pack(side="left")

        # --- Görgethető tartalom ---
        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=10)

        status = ctk.CTkLabel(
            win, text="", font=("Arial", 11), text_color="#aaaaaa"
        )
        status.pack(pady=2)

        def _clear_scroll():
            for child in scroll.winfo_children():
                child.destroy()

        def refresh_report(month_str):
            _clear_scroll()
            stats = self._compute_monthly_stats(month_str)
            _render_report(scroll, stats, month_str)
            status.configure(text=f"Adatok: {month_str}")

        # --- Gombok alul ---
        btns = ctk.CTkFrame(win, fg_color="transparent")
        btns.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            btns, text="📤 Export JSON",
            fg_color="#2980b9", hover_color="#3498db",
            width=140,
            command=lambda: self._export_report(month_var.get())
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            btns, text="📄 Export szöveg",
            fg_color="#16a085", hover_color="#1abc9c",
            width=140,
            command=lambda: self._export_report_text(month_var.get())
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            btns, text="Bezárás",
            fg_color="#555555", hover_color="#666666",
            width=100,
            command=win.destroy
        ).pack(side="right", padx=4)

        # Kezdeti betöltés
        refresh_report(month_var.get())

    # ------------------------------------------------------------------
    #  Adatok összesítése
    # ------------------------------------------------------------------
    def _compute_monthly_stats(self, month_str):
        """Összegyűjti az adott hónap statisztikáit."""
        stats = {
            "month": month_str,
            "bots": {},
            "total_errors": 0,
            "total_commands": 0,
            "total_uptime_seconds": 0,
            "top_commands": Counter(),
            "daily_errors": Counter(),
            "daily_activity": Counter(),
        }

        for bot_key, bot in self.bots.items():
            bot_stats = {
                "error_count": 0,
                "total_commands": 0,
                "log_entries": 0,
                "uptime_seconds": 0,
                "first_log": None,
                "last_log": None,
            }

            for entry in bot.get("raw_logs", []):
                date_str = entry.get("date", "")
                if not date_str.startswith(month_str):
                    continue

                bot_stats["log_entries"] += 1
                log_type = entry.get("type", "INFO")

                if log_type == "ERROR":
                    bot_stats["error_count"] += 1
                    stats["total_errors"] += 1
                    stats["daily_errors"][date_str] += 1

                if log_type == "SUCCESS":
                    # Parancs statisztika
                    bot_stats["total_commands"] += 1
                    stats["total_commands"] += 1
                    msg = entry.get("msg", "")
                    # Egyszerű parancs detektálás
                    if "/" in msg:
                        parts = [p for p in msg.split() if p.startswith("/")]
                        if parts:
                            stats["top_commands"][parts[0]] += 1

                stats["daily_activity"][date_str] += 1

                # Időbélyegek
                ts = f"{date_str} {entry.get('time', '')}"
                if bot_stats["first_log"] is None or ts < bot_stats["first_log"]:
                    bot_stats["first_log"] = ts
                if bot_stats["last_log"] is None or ts > bot_stats["last_log"]:
                    bot_stats["last_log"] = ts

            # Weekly uptime arányosítása (kb.)
            bot_stats["uptime_seconds"] = bot.get("weekly_uptime_seconds", 0) * 4
            stats["total_uptime_seconds"] += bot_stats["uptime_seconds"]
            stats["bots"][bot_key] = bot_stats

        return stats

    def _export_report(self, month_str):
        """JSON export."""
        stats = self._compute_monthly_stats(month_str)
        # Counter → dict
        stats["top_commands"] = dict(stats["top_commands"].most_common(20))
        stats["daily_errors"] = dict(stats["daily_errors"])
        stats["daily_activity"] = dict(stats["daily_activity"])

        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            initialfile=f"report_{month_str}.json"
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(stats, f, ensure_ascii=False, indent=4, default=str)
            messagebox.showinfo("Export", f"Riport elmentve:\n{path}")
            self.notify("📤 Riport exportálva", "success")
        except Exception as e:
            messagebox.showerror("Hiba", str(e))

    def _export_report_text(self, month_str):
        """Szöveges export."""
        stats = self._compute_monthly_stats(month_str)
        lines = []
        lines.append(f"📊 HAVI RIPORT — {month_str}")
        lines.append("=" * 50)
        lines.append("")
        lines.append(f"Összes hiba:        {stats['total_errors']}")
        lines.append(f"Összes parancs:     {stats['total_commands']}")
        hours = stats['total_uptime_seconds'] // 3600
        lines.append(f"Összes uptime:      {hours} óra")
        lines.append("")

        lines.append("BOTONKÉNTI BONTÁS")
        lines.append("-" * 50)
        for bot_key, bot_stats in stats["bots"].items():
            lines.append(f"\n🤖 {bot_key}")
            lines.append(f"   Hibák:      {bot_stats['error_count']}")
            lines.append(f"   Parancsok:  {bot_stats['total_commands']}")
            lines.append(f"   Naplók:     {bot_stats['log_entries']}")
            if bot_stats['first_log']:
                lines.append(f"   Első:       {bot_stats['first_log']}")
                lines.append(f"   Utolsó:     {bot_stats['last_log']}")

        if stats["top_commands"]:
            lines.append("")
            lines.append("TOP PARANCSOK")
            lines.append("-" * 50)
            for cmd, count in stats["top_commands"].most_common(10):
                lines.append(f"  {cmd}: {count}x")

        text = "\n".join(lines)

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Szöveg", "*.txt")],
            initialfile=f"report_{month_str}.txt"
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Export", f"Riport elmentve:\n{path}")
            self.notify("📤 Szöveges riport exportálva", "success")
        except Exception as e:
            messagebox.showerror("Hiba", str(e))


# =====================================================================
#  Riport megjelenítő
# =====================================================================
def _render_report(parent, stats, month_str):
    """A riport vizuális megjelenítése."""
    # Összesítő kártyák
    summary_frame = ctk.CTkFrame(parent, fg_color="transparent")
    summary_frame.pack(fill="x", pady=(0, 12))

    def make_card(title, value, color):
        card = ctk.CTkFrame(summary_frame, fg_color="#232323", corner_radius=10)
        card.pack(side="left", fill="both", expand=True, padx=4)
        ctk.CTkLabel(
            card, text=title,
            font=("Arial", 11), text_color="#aaaaaa"
        ).pack(pady=(12, 2))
        ctk.CTkLabel(
            card, text=str(value),
            font=("Arial", 22, "bold"), text_color=color
        ).pack(pady=(0, 12))

    make_card("Hibák", stats["total_errors"], "#e74c3c")
    make_card("Parancsok", stats["total_commands"], "#2ecc71")
    make_card("Naplók", sum(b["log_entries"] for b in stats["bots"].values()), "#3498db")

    hours = stats["total_uptime_seconds"] // 3600
    make_card("Uptime", f"{hours}h", "#f39c12")

    # Botonkénti bontás
    ctk.CTkLabel(
        parent, text="🤖 Botonkénti bontás",
        font=("Arial", 14, "bold"), anchor="w"
    ).pack(fill="x", pady=(8, 4))

    if not stats["bots"]:
        ctk.CTkLabel(
            parent, text="Nincs adat erre a hónapra.",
            font=("Arial", 11), text_color="#777"
        ).pack(pady=20)
        return

    for bot_key, bot_stats in stats["bots"].items():
        card = ctk.CTkFrame(parent, fg_color="#232323", corner_radius=8)
        card.pack(fill="x", pady=4)

        ctk.CTkLabel(
            card, text=f"🤖 {bot_key}",
            font=("Arial", 13, "bold"), anchor="w"
        ).pack(fill="x", padx=12, pady=(10, 4))

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", padx=12, pady=(0, 10))

        ctk.CTkLabel(
            info_frame,
            text=f"Hibák: {bot_stats['error_count']}   •   "
                 f"Parancsok: {bot_stats['total_commands']}   •   "
                 f"Naplók: {bot_stats['log_entries']}",
            font=("Consolas", 11), text_color="#cccccc", anchor="w"
        ).pack(fill="x")

    # Top parancsok
    if stats["top_commands"]:
        ctk.CTkLabel(
            parent, text="⚡ Top parancsok",
            font=("Arial", 14, "bold"), anchor="w"
        ).pack(fill="x", pady=(16, 4))

        top_frame = ctk.CTkFrame(parent, fg_color="#232323", corner_radius=8)
        top_frame.pack(fill="x", pady=4)

        for cmd, count in stats["top_commands"].most_common(10):
            row = ctk.CTkFrame(top_frame, fg_color="transparent")
            row.pack(fill="x", padx=12, pady=2)
            ctk.CTkLabel(
                row, text=cmd, font=("Consolas", 12),
                anchor="w", text_color="#3498db"
            ).pack(side="left")
            ctk.CTkLabel(
                row, text=f"{count}x", font=("Consolas", 12, "bold"),
                anchor="e", text_color="#2ecc71"
            ).pack(side="right")

    # Napi aktivitás
    if stats["daily_activity"]:
        ctk.CTkLabel(
            parent, text="📅 Napi aktivitás",
            font=("Arial", 14, "bold"), anchor="w"
        ).pack(fill="x", pady=(16, 4))

        act_frame = ctk.CTkFrame(parent, fg_color="#232323", corner_radius=8)
        act_frame.pack(fill="x", pady=4)

        max_act = max(stats["daily_activity"].values()) if stats["daily_activity"] else 1
        for day, count in sorted(stats["daily_activity"].items()):
            row = ctk.CTkFrame(act_frame, fg_color="transparent")
            row.pack(fill="x", padx=12, pady=2)
            ctk.CTkLabel(
                row, text=day, font=("Consolas", 11),
                anchor="w", width=100, text_color="#cccccc"
            ).pack(side="left")

            # Kis progress bar
            bar_width = int((count / max_act) * 300)
            bar = ctk.CTkFrame(
                row, height=14, width=max(bar_width, 4),
                fg_color="#3498db", corner_radius=3
            )
            bar.pack(side="left", padx=8)
            bar.pack_propagate(False)

            ctk.CTkLabel(
                row, text=str(count), font=("Consolas", 11),
                anchor="w", text_color="#ffffff"
            ).pack(side="left", padx=4)