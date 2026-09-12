import customtkinter as ctk
from version import version


class SplashScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Betöltés...")
        self.geometry("500x300")
        self.overrideredirect(True)
        self.configure(fg_color="#1e1e1e")

        # Középre helyezés
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry(f"500x300+{int(w / 2 - 250)}+{int(h / 2 - 150)}")

        self.logo = ctk.CTkLabel(self, text="Discord Bot Manager",
                                 font=("Arial", 28, "bold"))
        self.logo.pack(pady=20)

        self.subtitle = ctk.CTkLabel(self, text="Made by: _Valii_Balint_",
                                     font=("Arial", 16))
        self.subtitle.pack()

        self.version = ctk.CTkLabel(self, text=f"{version}", font=("Arial", 12),
                                    text_color="#888")
        self.version.pack(pady=5)

        self.progress = ctk.CTkProgressBar(self, width=350)
        self.progress.pack(pady=30)
        self.progress.set(0)

        self.animate_progress()

    def animate_progress(self):
        value = self.progress.get()
        if value < 1:
            self.progress.set(value + 0.01)
            self.after(30, self.animate_progress)