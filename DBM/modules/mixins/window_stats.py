import os
import re
import json
import time
import datetime
from collections import Counter
from tkinter import filedialog, messagebox

import customtkinter as ctk
import psutil

try:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    MATPLOTLIB_ERROR = "A matplotlib csomag nem tölthető be."

import modules.config as config
from modules.languages import LANGUAGES


class WindowStatsMixin:

    # --------------------------------------------------------------
    #  Globális statisztika ablak
    # --------------------------------------------------------------
    def open_global_stats_window(self):
        win = ctk.CTkToplevel(self)
        win.title(self.tr("global_stats_title"))
        win.geometry("950x650")
        win.grab_set()
        tabs = ctk.CTkTabview(win)
        tabs.pack(fill="both", expand=True, padx=12, pady=12)
        overview_tab = tabs.add(self.tr("global_stats"))
        commands_tab = tabs.add(self.tr("command_stats"))
        ctk.CTkLabel(overview_tab, text=self.tr("global_stats_title"),
                     font=("Arial", 18, "bold"), text_color="#3498db").pack(pady=15)
        scroll_frame = ctk.CTkScrollableFrame(overview_tab)
        scroll_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        for k, bot in self.bots.items():
            card = ctk.CTkFrame(scroll_frame, fg_color=self.theme_colors["card_bg"])
            card.pack(fill="x", padx=5, pady=4)
            status_text = self.tr("online") if bot["is_running"] else self.tr("offline")
            ctk.CTkLabel(
                card,
                text=f"🤖 {k} | {status_text} | {self.tr('total_commands')}: {bot['total_commands']} | {self.tr('errors')}: {bot['error_count']}",
                font=("Consolas", 12), text_color=self.theme_colors["text"]
            ).pack(anchor="w", padx=10, pady=10)

        daily, popular = self.get_command_usage_stats()
        ctk.CTkLabel(commands_tab, text=self.tr("daily_commands"),
                     font=("Arial", 14, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        daily_box = ctk.CTkTextbox(commands_tab, height=170)
        daily_box.pack(fill="x", padx=12, pady=5)
        daily_lines = ["%s: %s" % (day, count) for day, count in sorted(daily.items())]
        daily_box.insert("1.0", "\n".join(daily_lines) or self.tr("no_command_data"))
        daily_box.configure(state="disabled")

        ctk.CTkLabel(commands_tab, text=self.tr("popular_commands"),
                     font=("Arial", 14, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        popular_box = ctk.CTkTextbox(commands_tab, height=170)
        popular_box.pack(fill="both", expand=True, padx=12, pady=5)
        popular_lines = ["%s: %s" % (command, count) for command, count in popular.most_common()]
        popular_box.insert("1.0", "\n".join(popular_lines) or self.tr("no_command_data"))
        popular_box.configure(state="disabled")

    def get_command_usage_stats(self):
        daily = {}
        popular = {}
        for bot in self.bots.values():
            for entry in bot.get("raw_logs", []):
                message = entry.get("msg", "")
                lowered = message.lower()
                if "command" not in lowered and "parancs" not in lowered and not re.search(r"(?:^|\s)/[a-zA-Z0-9_-]+", message):
                    continue
                date_key = entry.get("date", datetime.datetime.now().strftime("%Y-%m-%d"))
                daily[date_key] = daily.get(date_key, 0) + 1
                match = re.search(r"(?:command|parancs)\s*[:=]?\s*([/a-zA-Z0-9_-]+)", message, re.IGNORECASE)
                command_name = match.group(1) if match else (
                    re.search(r"(/[a-zA-Z0-9_-]+)", message).group(1)
                    if re.search(r"(/[a-zA-Z0-9_-]+)", message) else "unknown"
                )
                popular[command_name] = popular.get(command_name, 0) + 1
        return daily, Counter(popular)

    # --------------------------------------------------------------
    #  Élő statisztika loop
    # --------------------------------------------------------------
    def update_stats_loop(self):
        bot = self.bots.get(self.active_bot_key)
        self.lbl_temperature.configure(text=self.get_temperature_text())
        if bot and bot["is_running"] and bot["process"] and bot["start_time"]:
            elapsed = int(time.time() - bot["start_time"])
            self.lbl_uptime.configure(text=str(datetime.timedelta(seconds=elapsed)))

            self.check_auto_restarts()

            bot["weekly_uptime_seconds"] += 1
            w_hours = bot["weekly_uptime_seconds"] // 3600
            w_mins = (bot["weekly_uptime_seconds"] % 3600) // 60
            self.lbl_weekly_uptime.configure(text=f"{w_hours}h {w_mins}m")

            try:
                proc = psutil.Process(bot["process"].pid)
                self.lbl_ram.configure(text=f"{proc.memory_info().rss / (1024 * 1024):.1f} MB")
                self.lbl_cpu.configure(text=f"{proc.cpu_percent(interval=None):.1f} %")
            except Exception:
                pass

            script_path = bot.get("path", "")
            if script_path and os.path.exists(script_path):
                stats_file = os.path.join(os.path.dirname(script_path), "bot_stats.json")
                if os.path.exists(stats_file):
                    try:
                        with open(stats_file, "r", encoding="utf-8") as f:
                            stats = json.load(f)
                            self.lbl_servers.configure(text=str(stats.get("guilds", 0)))
                            self.lbl_users.configure(text=str(stats.get("users", 0)))
                            api_p = stats.get("api_ping", stats.get("ping", 0))
                            msg_p = stats.get("msg_ping", stats.get("message_ping", 0))
                            self.lbl_api_ping.configure(text=f"API: {api_p}ms")
                            self.lbl_msg_ping.configure(text=f"Msg: {msg_p}ms")
                    except Exception:
                        pass
        self.after(1000, self.update_stats_loop)

    # --------------------------------------------------------------
    #  Teljesítmény grafikon
    # --------------------------------------------------------------
    def open_performance_charts_window(self):
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showerror(
                self.tr("missing_library_title"),
                f"{self.tr('missing_library_msg')}\n{MATPLOTLIB_ERROR}\n\n"
                f"{self.tr('install_instruction')}: py -m pip install matplotlib"
            )
            return

        win = ctk.CTkToplevel(self)
        win.title(self.tr("performance_title"))
        win.geometry("900x550")
        win.grab_set()

        range_var = ctk.StringVar(value=self.tr("last_1_hour"))
        control_frame = ctk.CTkFrame(win, fg_color="transparent")
        control_frame.pack(fill="x", padx=10, pady=(8, 0))
        ctk.CTkLabel(control_frame, text=self.tr("time_range") + ":").pack(side="left", padx=4)
        
        range_options = [self.tr("last_10_mins"), self.tr("last_1_hour"), self.tr("last_24_hours")]
        range_combo = ctk.CTkComboBox(
            control_frame, variable=range_var,
            values=range_options, width=150
        )
        range_combo.pack(side="left", padx=4)

        def history_for_range():
            current_val = range_var.get()
            if current_val == self.tr("last_10_mins"):
                limit = 120
            elif current_val == self.tr("last_24_hours"):
                limit = 17280
            else:
                limit = 720
                
            current_bot = self.bots.get(self.active_bot_key)
            if not current_bot:
                return [], [], []
            return (
                list(current_bot.get("history_ram", []))[-limit:],
                list(current_bot.get("history_cpu", []))[-limit:],
                list(current_bot.get("history_time", []))[-limit:],
            )

        history_ram, history_cpu, history_time = history_for_range()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 4.8), facecolor="#2b2b2b")
        fig.tight_layout(pad=3.0)

        def style_axis(ax, title, ylabel):
            ax.set_facecolor("#1e1e1e")
            ax.set_title(title, color="white", fontsize=11, fontweight="bold")
            ax.set_ylabel(ylabel, color="white", fontsize=10)
            ax.tick_params(colors="white", labelsize=9)
            for spine in ax.spines.values():
                spine.set_color("#555555")
            ax.grid(True, color="#444444", linestyle="--", alpha=0.5)

        style_axis(ax1, f"{self.tr('chart_ram')} ({range_var.get()}) - {self.active_bot_key}", "RAM (MB)")
        style_axis(ax2, f"{self.tr('chart_cpu')} ({range_var.get()}) - {self.active_bot_key}", "CPU (%)")

        line_ram, = ax1.plot(history_time, history_ram, color="#3498db", linewidth=2, marker="o", markersize=3)
        line_cpu, = ax2.plot(history_time, history_cpu, color="#2ecc71", linewidth=2, marker="o", markersize=3)

        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        def refresh_range(*_):
            h_ram, h_cpu, h_time = history_for_range()
            line_ram.set_data(h_time, h_ram)
            line_cpu.set_data(h_time, h_cpu)
            ax1.set_title(f"{self.tr('chart_ram')} ({range_var.get()}) - {self.active_bot_key}",
                          color="white", fontsize=11, fontweight="bold")
            ax2.set_title(f"{self.tr('chart_cpu')} ({range_var.get()}) - {self.active_bot_key}",
                          color="white", fontsize=11, fontweight="bold")
            for axis in (ax1, ax2):
                axis.relim()
                axis.autoscale_view()
            canvas.draw_idle()

        range_var.trace_add("write", refresh_range)

        def export_png():
            target = filedialog.asksaveasfilename(
                parent=win, defaultextension=".png",
                filetypes=[(self.tr("png_filter"), "*.png")],
                initialfile="%s_%s.png" % (
                    self.active_bot_key,
                    datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                )
            )
            if target:
                fig.savefig(target, dpi=160, facecolor=fig.get_facecolor(), bbox_inches="tight")
                messagebox.showinfo(self.tr("export_title"), self.tr("export_success_msg").format(target=target), parent=win)

        ctk.CTkButton(control_frame, text=self.tr("save_png"),
                      command=export_png).pack(side="right", padx=4)

        is_active = [True]

        def update_plot():
            if not is_active[0] or not win.winfo_exists():
                return
            b = self.bots.get(self.active_bot_key)
            if b:
                h_ram, h_cpu, h_time = history_for_range()
                line_ram.set_data(h_time, h_ram)
                line_cpu.set_data(h_time, h_cpu)
                for ax in (ax1, ax2):
                    ax.relim()
                    ax.autoscale_view()
                canvas.draw_idle()
            win.after(3000, update_plot)

        win.after(3000, update_plot)

        def on_close():
            is_active[0] = False
            win.destroy()

        win.protocol("WM_DELETE_WINDOW", on_close)