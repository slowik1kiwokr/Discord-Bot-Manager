import math
import random
import tkinter as tk

import customtkinter as ctk


class BotStartupAnimationMixin:
    """Animált bot-indítási képernyő."""

    def show_bot_startup_animation(self, bot_key="Main Bot", emoji="🤖"):
        """Megjelenít egy animált startup képernyőt a bot indításakor."""

        if getattr(self, "_startup_anim_running", False):
            return

        self._startup_anim_running = True

        win = ctk.CTkToplevel(self)
        win.overrideredirect(True)
        try:
            win.attributes("-topmost", True)
            win.attributes("-alpha", 0.0)
        except Exception:
            pass
        win.configure(fg_color="#0d0f14")

        w, h = 460, 560
        try:
            self.update_idletasks()
            x = self.winfo_rootx() + (self.winfo_width() - w) // 2
            y = self.winfo_rooty() + (self.winfo_height() - h) // 2
        except Exception:
            x, y = 300, 200
        win.geometry(f"{w}x{h}+{x}+{y}")

        border = ctk.CTkFrame(
            win, fg_color="#0d0f14", corner_radius=18,
            border_width=2, border_color="#5865F2",
        )
        border.pack(fill="both", expand=True, padx=2, pady=2)

        # --- Canvas a körhöz és részecskékhez ---
        canvas = tk.Canvas(
            border, width=200, height=200,
            bg="#0d0f14", highlightthickness=0,
        )
        canvas.pack(pady=(36, 16))

        center = 100
        radius = 68

        # Háttér kör
        canvas.create_oval(
            center - radius, center - radius,
            center + radius, center + radius,
            outline="#1e2430", width=7,
        )

        # Animált ív
        arc_id = canvas.create_arc(
            center - radius, center - radius,
            center + radius, center + radius,
            start=90, extent=0,
            outline="#5865F2", width=7, style="arc",
        )

        # Belső glow
        canvas.create_oval(
            center - radius + 12, center - radius + 12,
            center + radius - 12, center + radius - 12,
            outline="#2a3050", width=1,
        )

        # Bot emoji
        canvas.create_text(
            center, center, text=emoji,
            font=("Segoe UI Emoji", 42),
        )

        # Részecskék
        particles = []
        for _ in range(14):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(radius + 12, radius + 50)
            px = center + dist * math.cos(angle)
            py = center + dist * math.sin(angle)
            color = random.choice(["#7dd3fc", "#9b59b6", "#5865F2", "#00bcd4", "#f39c12"])
            size = random.randint(2, 5)
            pid = canvas.create_oval(
                px - size, py - size, px + size, py + size,
                fill=color, outline="",
            )
            particles.append({
                "id": pid,
                "angle": angle,
                "dist": dist,
                "speed": random.uniform(0.015, 0.04),
                "size": size,
                "phase": random.uniform(0, 6.28),
            })

        # --- Cím ---
        ctk.CTkLabel(
            border, text=f"Starting {bot_key}...",
            font=("Arial", 19, "bold"), text_color="#7dd3fc",
        ).pack(pady=(0, 18))

        # --- Státusz sorok ---
        stages_data = [
            "animation_stage_loading",
            "animation_stage_connecting",
            "animation_stage_syncing",
        ]

        stage_widgets = []
        for key in stages_data:
            row = ctk.CTkFrame(border, fg_color="transparent", height=30)
            row.pack(fill="x", padx=48, pady=3)
            row.pack_propagate(False)

            check_lbl = ctk.CTkLabel(
                row, text="○",
                font=("Arial", 15, "bold"),
                text_color="#3a4050", width=26,
            )
            check_lbl.pack(side="left")

            text_lbl = ctk.CTkLabel(
                row, text=self.tr(key),
                font=("Arial", 12),
                text_color="#5a6070",
                anchor="w",
            )
            text_lbl.pack(side="left", fill="x", expand=True, padx=(8, 0))

            stage_widgets.append((check_lbl, text_lbl))

        # --- Progress bar ---
        progress = ctk.CTkProgressBar(
            border, width=340, height=6,
            progress_color="#5865F2",
            fg_color="#1e2430",
            corner_radius=3,
        )
        progress.set(0)
        progress.pack(pady=(22, 26))

        # --- Animációs állapot ---
        state = {
            "angle": 0.0,
            "progress": 0.0,
            "current_stage": -1,
            "active": True,
        }

        # Fade-in
        def fade_in(alpha=0.0):
            try:
                if not win.winfo_exists():
                    return
                new_alpha = min(1.0, alpha + 0.1)
                win.attributes("-alpha", new_alpha)
                if new_alpha < 1.0:
                    win.after(20, lambda: fade_in(new_alpha))
            except Exception:
                pass

        win.after(10, fade_in)

        # Fade-out
        def fade_out(alpha=1.0):
            try:
                if not win.winfo_exists():
                    return
                new_alpha = max(0.0, alpha - 0.08)
                win.attributes("-alpha", new_alpha)
                if new_alpha > 0:
                    win.after(20, lambda: fade_out(new_alpha))
                else:
                    win.destroy()
                    self._startup_anim_running = False
            except Exception:
                self._startup_anim_running = False
                try:
                    win.destroy()
                except Exception:
                    pass

        # Fő animációs loop
        def animate():
            if not state["active"]:
                return
            try:
                if not win.winfo_exists():
                    return
            except Exception:
                return

            # Kör forgatás
            state["angle"] = (state["angle"] + 5) % 360
            extent = min(270, 60 + state["angle"])
            canvas.itemconfig(arc_id, start=90 - state["angle"], extent=extent)

            # Progress növelés
            state["progress"] = min(1.0, state["progress"] + 0.014)
            progress.set(state["progress"])

            # Részecskék mozgatása
            for p in particles:
                p["angle"] += p["speed"]
                if p["angle"] > 2 * math.pi:
                    p["angle"] -= 2 * math.pi

                # Pulzálás
                pulse = math.sin(state["angle"] * 0.08 + p["phase"]) * 6
                d = p["dist"] + pulse
                px = center + d * math.cos(p["angle"])
                py = center + d * math.sin(p["angle"])
                s = p["size"]

                # Méret pulzálás
                s_now = s + math.sin(state["angle"] * 0.1 + p["phase"]) * 1.5
                s_now = max(1, s_now)

                canvas.coords(p["id"], px - s_now, py - s_now, px + s_now, py + s_now)

            # Státusz frissítés
            stage_idx = -1
            if state["progress"] >= 0.33:
                stage_idx = 0
            if state["progress"] >= 0.66:
                stage_idx = 1
            if state["progress"] >= 0.95:
                stage_idx = 2

            if stage_idx > state["current_stage"]:
                state["current_stage"] = stage_idx
                for i, (cl, tl) in enumerate(stage_widgets):
                    if i < stage_idx:
                        cl.configure(text="✓", text_color="#2ecc71")
                        tl.configure(text_color="#2ecc71")
                    elif i == stage_idx:
                        cl.configure(text="●", text_color="#7dd3fc")
                        tl.configure(text_color="#7dd3fc")

            # Befejezés
            if state["progress"] >= 1.0:
                state["active"] = False
                for cl, tl in stage_widgets:
                    cl.configure(text="✓", text_color="#2ecc71")
                    tl.configure(text_color="#2ecc71")
                progress.set(1.0)
                win.after(500, lambda: fade_out(1.0))
                return

            win.after(30, animate)

        animate()