import os
import customtkinter as ctk
from PIL import Image
from version import version


# A logo elérési útja (a panel gyökérkönyvtárában)
SPLASH_LOGO_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "logo.jpg"
)


class SplashScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._closing = False
        self._after_ids = []
        self._logo_image = None  # fontos: életben kell tartani, különben eltűnik

        self.title("Betöltés...")
        self.geometry("540x480")
        self.overrideredirect(True)
        self.configure(fg_color="#1a1d24")

        # Középre
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry(f"540x480+{int(w / 2 - 270)}+{int(h / 2 - 240)}")

        # --- Logó megjelenítése ---
        self._build_logo_area()

        # --- Verziószám ---
        self.version = ctk.CTkLabel(
            self, text=f"v{version}", font=("Arial", 12),
            text_color="#6a6e78"
        )
        self.version.pack(pady=(4, 18))

        # --- Progress bar ---
        self.progress = ctk.CTkProgressBar(
            self, width=400, height=14,
            progress_color="#5865F2", fg_color="#252932",
            corner_radius=7,
        )
        self.progress.pack(pady=(0, 8))
        self.progress.set(0)

        # --- Státusz szöveg ---
        self.status_label = ctk.CTkLabel(
            self, text="Betöltés...", font=("Arial", 11),
            text_color="#8a8e98"
        )
        self.status_label.pack(pady=(0, 16))

        self.animate_progress()

    # --------------------------------------------------------------
    #  Logó terület
    # --------------------------------------------------------------
    def _build_logo_area(self):
        """Betölti a logo.jpg-t, vagy fallback szöveget jelenít meg."""
        if os.path.isfile(SPLASH_LOGO_PATH):
            try:
                pil_image = Image.open(SPLASH_LOGO_PATH)

                # Méretarány megtartása, max 380x220
                max_w, max_h = 380, 220
                ratio = min(max_w / pil_image.width, max_h / pil_image.height)
                new_w = int(pil_image.width * ratio)
                new_h = int(pil_image.height * ratio)

                self._logo_image = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=(new_w, new_h)
                )
                logo_label = ctk.CTkLabel(self, image=self._logo_image, text="")
                logo_label.pack(pady=(28, 4))
                return
            except Exception as e:
                print(f"[SPLASH] Nem sikerült a logó betöltése: {e}")

        # Fallback: szöveges cím
        ctk.CTkLabel(
            self, text="Discord Bot Manager",
            font=("Arial", 28, "bold"), text_color="#5865F2"
        ).pack(pady=(40, 4))
        ctk.CTkLabel(
            self, text="Made by: _Valii_Balint_",
            font=("Arial", 14), text_color="#8a8e98"
        ).pack(pady=(0, 8))

    # --------------------------------------------------------------
    #  Animáció
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
            # Frissítjük a státusz szöveget is
            try:
                if value < 0.3:
                    self.status_label.configure(text="Rendszer betöltése...")
                elif value < 0.6:
                    self.status_label.configure(text="Konfiguráció olvasása...")
                elif value < 0.9:
                    self.status_label.configure(text="Modulok inicializálása...")
                else:
                    self.status_label.configure(text="Indítás...")
            except Exception:
                pass
            self._safe_after(30, self.animate_progress)
        else:
            self._closing = True

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
            self.quit()
        except Exception:
            pass
        try:
            self.destroy()
        except Exception:
            pass