import customtkinter as ctk
import psutil

try:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg, NavigationToolbar2Tk
    )
    MPL_OK = True
except ImportError:
    MPL_OK = False


class AnimatedChartsMixin:
    """Élő, animált grafikonok zoom/pan és hover támogatással."""

    def open_animated_charts_window(self):
        if not MPL_OK:
            from tkinter import messagebox
            messagebox.showerror(self.tr("common_error_title"),
                                 self.tr("charts_mpl_missing"))
            return

        win = ctk.CTkToplevel(self)
        win.title(self.tr("charts_title"))
        win.geometry("1000x700")
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 1000) // 2
        y = (win.winfo_screenheight() - 700) // 2
        win.geometry(f"1000x700+{x}+{y}")

        header = ctk.CTkFrame(win, fg_color="#e67e22", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text=self.tr("charts_header"),
                     font=("Arial", 17, "bold"), text_color="white").pack(side="left", padx=20, pady=14)
        ctk.CTkLabel(header, text=self.tr("charts_hint"),
                     font=("Arial", 10), text_color="#ffeecc").pack(side="right", padx=20)

        cpu_data, ram_data = [], []
        MAX_POINTS = 120

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 5.5), facecolor="#1a1d24")
        fig.tight_layout(pad=2.5)

        chart_titles = [
            (ax1, self.tr("charts_cpu_title")),
            (ax2, self.tr("charts_ram_title")),
        ]
        for ax, title in chart_titles:
            ax.set_facecolor("#12151c")
            ax.set_title(title, color="white", fontsize=11, fontweight="bold")
            ax.tick_params(colors="#aaa", labelsize=9)
            for spine in ax.spines.values():
                spine.set_color("#333")
            ax.grid(True, color="#2a2f3a", linestyle="--", alpha=0.5)
            ax.set_ylim(0, 100)

        line_cpu, = ax1.plot([], [], color="#2ecc71", linewidth=2)
        line_ram, = ax2.plot([], [], color="#3498db", linewidth=2)

        annot_cpu = ax1.annotate("", xy=(0, 0), xytext=(10, 20),
                                  textcoords="offset points",
                                  bbox=dict(boxstyle="round,pad=0.4",
                                            fc="#1e2129", ec="#2ecc71", lw=1),
                                  color="white", fontsize=9,
                                  arrowprops=dict(arrowstyle="->", color="#2ecc71"))
        annot_cpu.set_visible(False)

        annot_ram = ax2.annotate("", xy=(0, 0), xytext=(10, 20),
                                  textcoords="offset points",
                                  bbox=dict(boxstyle="round,pad=0.4",
                                            fc="#1e2129", ec="#3498db", lw=1),
                                  color="white", fontsize=9,
                                  arrowprops=dict(arrowstyle="->", color="#3498db"))
        annot_ram.set_visible(False)

        def on_hover(event):
            changed = False
            if event.inaxes == ax1 and cpu_data:
                idx = int(round(event.xdata)) if event.xdata is not None else -1
                idx = max(0, min(idx, len(cpu_data) - 1))
                if 0 <= idx < len(cpu_data):
                    annot_cpu.xy = (idx, cpu_data[idx])
                    annot_cpu.set_text(self.tr("charts_hover_cpu", value=f"{cpu_data[idx]:.1f}"))
                    annot_cpu.set_visible(True)
                    changed = True
            elif event.inaxes == ax2 and ram_data:
                idx = int(round(event.xdata)) if event.xdata is not None else -1
                idx = max(0, min(idx, len(ram_data) - 1))
                if 0 <= idx < len(ram_data):
                    annot_ram.xy = (idx, ram_data[idx])
                    annot_ram.set_text(self.tr("charts_hover_ram", value=f"{ram_data[idx]:.1f}"))
                    annot_ram.set_visible(True)
                    changed = True
            else:
                annot_cpu.set_visible(False)
                annot_ram.set_visible(False)
                changed = True

            if changed:
                try:
                    fig.canvas.draw_idle()
                except Exception:
                    pass

        fig.canvas.mpl_connect("motion_notify_event", on_hover)

        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(6, 0))

        toolbar_frame = ctk.CTkFrame(win, height=40)
        toolbar_frame.pack(fill="x", padx=10, pady=(0, 10))
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()

        status = ctk.CTkLabel(win, text=self.tr("charts_status_collecting"),
                              font=("Arial", 10), text_color="#888")
        status.pack(pady=(0, 6))

        stop_flag = {"stop": False}

        def update(frame):
            if stop_flag["stop"]:
                return line_cpu, line_ram
            try:
                cpu = psutil.cpu_percent(interval=None)
                ram = psutil.virtual_memory().percent
                cpu_data.append(cpu)
                ram_data.append(ram)
                if len(cpu_data) > MAX_POINTS:
                    cpu_data.pop(0)
                    ram_data.pop(0)

                line_cpu.set_data(range(len(cpu_data)), cpu_data)
                line_ram.set_data(range(len(ram_data)), ram_data)
                for ax in (ax1, ax2):
                    ax.set_xlim(0, max(10, len(cpu_data) - 1))

                status.configure(text=self.tr(
                    "charts_status_last",
                    cpu=f"{cpu:.1f}",
                    ram=f"{ram:.1f}",
                    points=len(cpu_data),
                ))
            except Exception:
                pass
            return line_cpu, line_ram

        anim = FuncAnimation(fig, update, interval=1000, blit=False, cache_frame_data=False)

        def on_close():
            stop_flag["stop"] = True
            try:
                anim.event_source.stop()
            except Exception:
                pass
            try:
                plt.close(fig)
            except Exception:
                pass
            win.destroy()

        win.protocol("WM_DELETE_WINDOW", on_close)