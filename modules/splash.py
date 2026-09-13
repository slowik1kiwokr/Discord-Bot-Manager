import os
import random
import customtkinter as ctk
from PIL import Image
from version import version


SPLASH_LOGO_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "logo.jpg"
)
SPLASH_LOGO_PNG = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "logo.png"
)


# Tipp szövegek, amik véletlenszerűen jelennek meg
LOADING_TIPS = [
    "💡 Tipp: Használd a Ctrl+B-t gyors backup-hoz",
    "💡 Tipp: A Commanderrel kód nélkül hozhatsz létre parancsokat",
    "💡 Tipp: Állíts be emojit minden botnak",
    "💡 Tipp: Az AI asszisztens segít a hibakeresésben",
    "💡 Tipp: Használd az Ollama-t ingyenes helyi AI-hoz",
    "💡 Tipp: Ctrl+1..9 váltás a botok között",
    "💡 Tipp: A Havi riport exportálható JSON-ba",
    "💡 Tipp: Kattints a 🎨 Megjelenés gombra bot színezéshez",
    "💡 Tipp: A Dashboard widgetek testreszabhatók",
    "💡 Tipp: 15 achievementet oldhatsz fel",
]


class SplashScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._closing = False
        self._after_ids = []
        self._logo_image = None
        self._fade_alpha = 0.0

        self.title("Betöltés...")
        self.geometry("620x520")
        self.overrideredirect(True)
        self.configure(fg_color="#0d0f14")

        # Átlátszó ablak effekt
        try:
            self.attributes("-alpha", 0.0)
        except Exception:
            pass

        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry(f"620x520+{int(w / 2 - 310)}+{int(h / 2 - 260)}")

        # ============================================================
        #  KERET (színes szegély)
        # ============================================================
        border = ctk.CTkFrame(
            self, fg_color="#0d0f14",
            corner_radius=18,
            border_width=2,
            border_color="#5865F2",
        )
        border.pack(fill="both", expand=True, padx=1, pady=1)

        # ============================================================
        #  LOGÓ TERÜLET
        # ============================================================
        self._build_logo(border)

        # ============================================================
        #  CÍM
        # ============================================================
        title_frame = ctk.CTkFrame(border, fg_color="transparent")
        title_frame.pack(pady=(0, 4))

        ctk.CTkLabel(
            title_frame,
            text="Discord Bot Manager",
            font=("Segoe UI", 26, "bold"),
            text_color="#ffffff",
        ).pack()

        ctk.CTkLabel(
            title_frame,
            text="Professional Multi-Bot Panel",
            font=("Segoe UI", 11),
            text_color="#6a6e78",
        ).pack(pady=(0, 6))

        # ============================================================
        #  VERZIÓ BADGE
        # ============================================================
        version_frame = ctk.CTkFrame(
            border, fg_color="#1a1d24",
            corner_radius=12, border_width=1, border_color="#2f3542",
        )
        version_frame.pack(pady=(0, 14))

        ctk.CTkLabel(
            version_frame,
            text=f"  v{version}  ",
            font=("Segoe UI", 10, "bold"),
            text_color="#5865F2",
        ).pack(padx=6, pady=3)

        # ============================================================
        #  PROGRESS BAR
        # ============================================================
        self.progress = ctk.CTkProgressBar(
            border, width=480, height=10,
            progress_color="#5865F2",
            fg_color="#1a1d24",
            corner_radius=5,
        )
        self.progress.pack(pady=(0, 8))
        self.progress.set(0)

        # ============================================================
        #  STÁTUSZ SZÖVEG
        # ============================================================
        self.status_label = ctk.CTkLabel(
            border, text="Indítás...",
            font=("Segoe UI", 11),
            text_color="#8a8e98",
        )
        self.status_label.pack(pady=(0, 6))

        # ============================================================
        #  TIPP SZÖVEG
        # ============================================================
        self.tip_label = ctk.CTkLabel(
            border,
            text=random.choice(LOADING_TIPS),
            font=("Segoe UI", 10),
            text_color="#5a5e68",
            wraplength=480,
        )
        self.tip_label.pack(pady=(6, 18))

        # Animációk indítása
        self._start_fade_in()
        self.animate_progress()

    # --------------------------------------------------------------
    #  Logó betöltése
    # --------------------------------------------------------------
    def _build_logo(self, parent):
        """Betölti a logót, vagy fallback szöveget jelenít meg."""
        logo_path = None
        if os.path.isfile(SPLASH_LOGO_PNG):
            logo_path = SPLASH_LOGO_PNG
        elif os.path.isfile(SPLASH_LOGO_PATH):
            logo_path = SPLASH_LOGO_PATH

        logo_container = ctk.CTkFrame(parent, fg_color="transparent", height=200)
        logo_container.pack(pady=(26, 8))
        logo_container.pack_propagate(False)

        if logo_path:
            try:
                pil_image = Image.open(logo_path).convert("RGBA")

                max_w, max_h = 200, 180
                ratio = min(max_w / pil_image.width, max_h / pil_image.height)
                new_w = int(pil_image.width * ratio)
                new_h = int(pil_image.height * ratio)

                self._logo_image = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=(new_w, new_h),
                )
                ctk.CTkLabel(
                    logo_container, image=self._logo_image, text=""
                ).pack(expand=True)
                return
            except Exception as e:
                print(f"[SPLASH] Logó hiba: {e}")

        # Fallback: szöveges shield
        ctk.CTkLabel(
            logo_container,
            text="🛡️",
            font=("Segoe UI Emoji", 90),
            text_color="#5865F2",
        ).pack(expand=True)

    # --------------------------------------------------------------
    #  Fade-in effekt
    # --------------------------------------------------------------
    def _start_fade_in(self):
        """Lassú fade-in animáció."""
        try:
            self.attributes("-alpha", self._fade_alpha)
        except Exception:
            return

        def step():
            if self._closing:
                return
            self._fade_alpha = min(1.0, self._fade_alpha + 0.05)
            try:
                self.attributes("-alpha", self._fade_alpha)
            except Exception:
                return
            if self._fade_alpha < 1.0:
                self._safe_after(16, step)

        self._safe_after(20, step)

    # --------------------------------------------------------------
    #  Animációk
    # --------------------------------------------------------------
    def _safe_after(self, ms, func):
        aid = self.after(ms, func)
        self._after_ids.append(aid)
        return aid

    def animate_progress(self):
        if self._closing:
            return
        try:
            value = self.progress.get()
        except Exception:
            return

        if value < 1:
            try:
                self.progress.set(value + 0.01)
            except Exception:
                return

            # Státusz szövegek
            try:
                if value < 0.15:
                    self.status_label.configure(text="🔧 Rendszer inicializálása...")
                elif value < 0.35:
                    self.status_label.configure(text="📂 Konfiguráció betöltése...")
                elif value < 0.55:
                    self.status_label.configure(text="🧩 Modulok betöltése...")
                elif value < 0.75:
                    self.status_label.configure(text="🤖 Botok előkészítése...")
                elif value < 0.9:
                    self.status_label.configure(text="🎨 Felhasználói felület...")
                else:
                    self.status_label.configure(text="✅ Minden kész!")
            except Exception:
                pass

            self._safe_after(25, self.animate_progress)
        else:
            self._closing = True
            # Fade-out
            self._start_fade_out()

    def _start_fade_out(self):
        """Lassú fade-out bezárás előtt."""
        def step():
            try:
                current = self.attributes("-alpha")
                new_alpha = max(0.0, current - 0.1)
                self.attributes("-alpha", new_alpha)
                if new_alpha > 0:
                    self._safe_after(20, step)
            except Exception:
                pass

        self._safe_after(300, step)

    # --------------------------------------------------------------
    #  Biztonságos megsemmisítés
    # --------------------------------------------------------------
    def safe_destroy(self):
        self._closing = True

        for aid in self._after_ids:
            try:
                self.after_cancel(aid)
            except Exception:
                pass
        self._after_ids.clear()

        try:
            for aid in self.tk.call("after", "info"):
                try:
                    self.after_cancel(aid)
                except Exception:
                    pass
        except Exception:
            pass

        try:
            self.update_idletasks()
        except Exception:
            pass

        try:
            self.quit()
        except Exception:
            pass
        try:
            self.destroy()
        except Exception:
            pass