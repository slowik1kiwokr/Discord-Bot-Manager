import math
import os
import sys
import json
import random
import tkinter as tk

import customtkinter as ctk

try:
    from PIL import Image, ImageTk
    PIL_OK = True
except ImportError:
    PIL_OK = False


# ============================================================
#  Nyelvi szótár
# ============================================================
_SPLASH_STRINGS = {
    "hu": {
        "title": "Discord Bot Manager",
        "subtitle": "Professzionális Multi-Bot Panel",
        "loading_config": "Konfiguráció betöltése",
        "loading_modules": "Modulok betöltése",
        "loading_bots": "Botok előkészítése",
        "loading_ui": "Felület építése",
        "ready": "Kész!",
    },
    "en": {
        "title": "Discord Bot Manager",
        "subtitle": "Professional Multi-Bot Panel",
        "loading_config": "Loading configuration",
        "loading_modules": "Loading modules",
        "loading_bots": "Preparing bots",
        "loading_ui": "Building interface",
        "ready": "Ready!",
    },
}


def _detect_language():
    try:
        import modules.config as config
        if os.path.exists(config.SETTINGS_FILE):
            with open(config.SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            lang = data.get("language", "")
            if lang in ("English", "Magyar"):
                return "hu" if lang == "Magyar" else "en"
    except Exception:
        pass
    try:
        import locale
        code = locale.getlocale()[0] or ""
        if code.lower().startswith("hu"):
            return "hu"
    except Exception:
        pass
    return "en"


_SPLASH_LANG = _detect_language()


def _tr(key):
    return _SPLASH_STRINGS.get(_SPLASH_LANG, _SPLASH_STRINGS["en"]).get(key, key)


# ============================================================
#  Splash Screen — Toplevel (a panel Tk-jából)
# ============================================================
class SplashScreen(ctk.CTkToplevel):
    WIDTH = 820
    HEIGHT = 520

    def __init__(self, parent):
        super().__init__(parent)

        self.overrideredirect(True)
        try:
            self.attributes("-topmost", True)
            self.attributes("-alpha", 0.0)
        except Exception:
            pass

        self.configure(fg_color="#0a0e1a")

        # Középre
        try:
            self.update_idletasks()
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            x = (sw - self.WIDTH) // 2
            y = (sh - self.HEIGHT) // 2
            self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")
        except Exception:
            self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        # Állapot
        self._phase = "config"
        self._progress = 0.0
        self._angle = 0.0
        self._dots = 0
        self._particles = []
        self._active = True
        self._discord_logo_img = None
        self._discord_logo_tk = None

        self.canvas = tk.Canvas(
            self, width=self.WIDTH, height=self.HEIGHT,
            bg="#0a0e1a", highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self._build_static_elements()
        self._build_particles()

        self._fade_in(0.0)
        self.after(30, self._animate)
        self._start_progress_simulation()

    # ----------------------------------------------------------
    def _build_static_elements(self):
        W, H = self.WIDTH, self.HEIGHT
        cx = W // 2

        # Diagonalis rács
        for i in range(-5, 12):
            x1 = i * 100
            self.canvas.create_line(x1, 0, x1 + H, H, fill="#101828", width=1)

        # Ring középpont
        ring_cy = 190
        r_outer = 100

        # Alap halvány kör
        self.canvas.create_oval(
            cx - r_outer, ring_cy - r_outer,
            cx + r_outer, ring_cy + r_outer,
            outline="#1e2340", width=7, fill="",
        )

        # Forgó blurple ív
        self._arc_blurple = self.canvas.create_arc(
            cx - r_outer, ring_cy - r_outer,
            cx + r_outer, ring_cy + r_outer,
            start=90, extent=270,
            outline="#5865F2", width=7, style="arc",
        )

        # Forgó cyan ív
        self._arc_cyan = self.canvas.create_arc(
            cx - r_outer, ring_cy - r_outer,
            cx + r_outer, ring_cy + r_outer,
            start=270, extent=90,
            outline="#7dd3fc", width=7, style="arc",
        )

        # Discord logó
        logo_loaded = False
        if PIL_OK:
            for logo_name in ("logo.png", "logo_watermark.png", "title_logo.jpg"):
                try:
                    from modules.config import SCRIPT_DIR
                    logo_path = os.path.join(SCRIPT_DIR, logo_name)
                except Exception:
                    logo_path = logo_name

                if os.path.isfile(logo_path):
                    try:
                        img = Image.open(logo_path).convert("RGBA")
                        max_dim = 130
                        ratio = min(max_dim / img.width, max_dim / img.height)
                        new_w = int(img.width * ratio)
                        new_h = int(img.height * ratio)
                        img = img.resize((new_w, new_h), Image.LANCZOS)

                        self._discord_logo_img = img
                        self._discord_logo_tk = ImageTk.PhotoImage(img)

                        self.canvas.create_image(
                            cx, ring_cy,
                            image=self._discord_logo_tk,
                            anchor="center",
                        )
                        logo_loaded = True
                        break
                    except Exception as e:
                        print(f"[SPLASH] Logo hiba ({logo_name}): {e}")

        if not logo_loaded:
            self._draw_fallback_logo(cx, ring_cy)

        # Cím
        self._title_id = self.canvas.create_text(
            cx, 340,
            text=_tr("title"),
            fill="#7dd3fc",
            font=("Arial", 34, "bold"),
        )

        # Alcím
        self.canvas.create_text(
            cx, 378,
            text=_tr("subtitle"),
            fill="#5a6070",
            font=("Arial", 13),
        )

        # Progress bar
        bar_w = 500
        bar_h = 8
        bar_x1 = cx - bar_w // 2
        bar_y1 = 428
        bar_x2 = cx + bar_w // 2
        bar_y2 = bar_y1 + bar_h

        self._bar_coords = (bar_x1, bar_y1, bar_x2, bar_y2)

        self.canvas.create_rectangle(
            bar_x1, bar_y1, bar_x2, bar_y2,
            fill="#1e2340", outline="",
        )

        self._bar_fill = self.canvas.create_rectangle(
            bar_x1, bar_y1, bar_x1, bar_y2,
            fill="#7dd3fc", outline="",
        )

        # Státusz
        self._status_id = self.canvas.create_text(
            cx, 462,
            text=_tr("loading_config") + "...",
            fill="#8a8e98",
            font=("Arial", 11),
        )

        # 3 pont
        self._dot_ids = []
        dot_y = 486
        for i in range(3):
            dot_x = cx - 12 + i * 12
            dot_id = self.canvas.create_oval(
                dot_x - 3, dot_y - 3, dot_x + 3, dot_y + 3,
                fill="#2a3050", outline="",
            )
            self._dot_ids.append(dot_id)

    def _draw_fallback_logo(self, cx, cy):
        self.canvas.create_rectangle(
            cx - 42, cy - 28, cx + 42, cy + 32,
            fill="#3b82f6", outline="#7dd3fc", width=2,
        )
        self.canvas.create_oval(cx - 22, cy - 10, cx - 10, cy + 2,
                                 fill="#0a0e1a", outline="")
        self.canvas.create_oval(cx + 10, cy - 10, cx + 22, cy + 2,
                                 fill="#0a0e1a", outline="")
        self.canvas.create_line(cx, cy - 28, cx, cy - 42,
                                 fill="#7dd3fc", width=3)
        self.canvas.create_oval(cx - 5, cy - 47, cx + 5, cy - 37,
                                 fill="#7dd3fc", outline="")

    def _build_particles(self):
        cx = self.WIDTH // 2
        cy = 190
        for _ in range(18):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(115, 165)
            px = cx + dist * math.cos(angle)
            py = cy + dist * math.sin(angle)

            color = random.choice(
                ["#7dd3fc", "#9b59b6", "#5865F2", "#00bcd4", "#c084fc"]
            )
            size = random.randint(2, 5)

            pid = self.canvas.create_oval(
                px - size, py - size, px + size, py + size,
                fill=color, outline="",
            )
            self._particles.append({
                "id": pid,
                "angle": angle,
                "dist": dist,
                "speed": random.uniform(0.015, 0.04),
                "size": size,
                "phase": random.uniform(0, 6.28),
            })

    # ----------------------------------------------------------
    def _fade_in(self, alpha):
        if not self._active:
            return
        try:
            new_alpha = min(1.0, alpha + 0.08)
            self.attributes("-alpha", new_alpha)
            if new_alpha < 1.0:
                self.after(20, lambda: self._fade_in(new_alpha))
        except Exception:
            pass

    def _fade_out(self):
        def step(alpha=1.0):
            try:
                new_alpha = max(0.0, alpha - 0.12)
                self.attributes("-alpha", new_alpha)
                if new_alpha > 0:
                    self.after(15, lambda: step(new_alpha))
                else:
                    self._active = False
                    try:
                        self.destroy()
                    except Exception:
                        pass
            except Exception:
                try:
                    self.destroy()
                except Exception:
                    pass
        step(1.0)

    # ----------------------------------------------------------
    def _animate(self):
        if not self._active:
            return
        try:
            if not self.winfo_exists():
                return
        except Exception:
            return

        cx = self.WIDTH // 2
        cy = 190

        self._angle = (self._angle + 3) % 360
        try:
            self.canvas.itemconfig(self._arc_blurple,
                                    start=90 - self._angle,
                                    extent=270)
            self.canvas.itemconfig(self._arc_cyan,
                                    start=90 - self._angle + 180,
                                    extent=90)
        except Exception:
            pass

        for p in self._particles:
            p["angle"] += p["speed"]
            if p["angle"] > 2 * math.pi:
                p["angle"] -= 2 * math.pi

            pulse = math.sin(self._angle * 0.08 + p["phase"]) * 8
            d = p["dist"] + pulse
            px = cx + d * math.cos(p["angle"])
            py = cy + d * math.sin(p["angle"])

            s = p["size"] + math.sin(self._angle * 0.1 + p["phase"]) * 1.5
            s = max(1, s)

            try:
                self.canvas.coords(p["id"], px - s, py - s, px + s, py + s)
            except Exception:
                pass

        try:
            bar_x1, bar_y1, bar_x2, bar_y2 = self._bar_coords
            fill_x = bar_x1 + (bar_x2 - bar_x1) * self._progress
            self.canvas.coords(self._bar_fill,
                                bar_x1, bar_y1, fill_x, bar_y2)
        except Exception:
            pass

        self._dots = (self._dots + 1) % 6
        active_idx = self._dots // 2
        for i, dot_id in enumerate(self._dot_ids):
            try:
                if i <= active_idx:
                    self.canvas.itemconfig(dot_id, fill="#7dd3fc")
                else:
                    self.canvas.itemconfig(dot_id, fill="#2a3050")
            except Exception:
                pass

        try:
            t = (math.sin(self._angle * 0.05) + 1) / 2
            r = int(0x58 + (0x7d - 0x58) * t)
            g = int(0x65 + (0xd3 - 0x65) * t)
            b = int(0xF2 + (0xfc - 0xF2) * t)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.itemconfig(self._title_id, fill=color)
        except Exception:
            pass

        try:
            self.after(30, self._animate)
        except Exception:
            pass

    # ----------------------------------------------------------
    def _start_progress_simulation(self):
        def tick():
            if not self._active:
                return
            try:
                if not self.winfo_exists():
                    return
            except Exception:
                return

            if self._progress < 0.9:
                self._progress += random.uniform(0.015, 0.035)
                self._progress = min(0.9, self._progress)

            if self._progress < 0.25:
                txt = _tr("loading_config")
            elif self._progress < 0.55:
                txt = _tr("loading_modules")
            elif self._progress < 0.8:
                txt = _tr("loading_bots")
            else:
                txt = _tr("loading_ui")

            try:
                self.canvas.itemconfig(self._status_id, text=txt + "...")
            except Exception:
                pass

            try:
                self.after(180, tick)
            except Exception:
                pass

        tick()

    # ----------------------------------------------------------
    def finish(self):
        """A panel elkészült — befejezzük."""
        try:
            self._progress = 1.0
            self.canvas.coords(
                self._bar_fill,
                self._bar_coords[0], self._bar_coords[1],
                self._bar_coords[2], self._bar_coords[3],
            )
            self.canvas.itemconfig(
                self._status_id, text=_tr("ready"), fill="#2ecc71"
            )
        except Exception:
            pass

        try:
            self.after(400, self._fade_out)
        except Exception:
            self._fade_out()