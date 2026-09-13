import customtkinter as ctk


class UIExtrasMixin:
    """Modern UI/UX elemek: toast értesítések, összecsukható sidebar."""

    # ------------------------------------------------------------------
    #  Toast értesítések (Toplevel ablakokkal, nem foglalnak helyet)
    # ------------------------------------------------------------------
    def init_toast_system(self):
        """Inicializálja a toast rendszert (nem hoz létre látható konténert)."""
        self._active_toasts = []
        self._toast_counter = 0

    def notify(self, message, toast_type="info", duration=3500):
        """Felugró értesítés a képernyő jobb felső sarkában.

        toast_type: 'info' | 'success' | 'warning' | 'error'
        duration: hány ms után tűnjön el (0 = soha)
        """
        colors = {
            "info":    {"bg": "#1e3a8a", "accent": "#3498db", "icon": "ℹ️"},
            "success": {"bg": "#14532d", "accent": "#2ecc71", "icon": "✅"},
            "warning": {"bg": "#78350f", "accent": "#f39c12", "icon": "⚠️"},
            "error":   {"bg": "#7f1d1d", "accent": "#e74c3c", "icon": "❌"},
        }
        style = colors.get(toast_type, colors["info"])

        try:
            toast = ctk.CTkToplevel(self)
        except Exception:
            return

        toast.overrideredirect(True)
        try:
            toast.attributes("-topmost", True)
        except Exception:
            pass
        toast.configure(fg_color=style["bg"])

        # Fix méret: 340 x 80
        width, height = 340, 80

        # Jobb felső sarok — a főablak pozíciójához képest
        try:
            self.update_idletasks()
            main_x = self.winfo_rootx()
            main_y = self.winfo_rooty()
            main_w = self.winfo_width()
        except Exception:
            main_x, main_y, main_w = 100, 100, 1200

        # Több toast egymás alatt
        offset_y = main_y + 60 + (len(self._active_toasts) * (height + 8))
        pos_x = main_x + main_w - width - 30
        pos_y = offset_y

        toast.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

        # --- Belső tartalom ---
        inner = ctk.CTkFrame(toast, fg_color="transparent")
        inner.pack(fill="both", expand=True)

        # Bal oldali színcsík
        stripe = ctk.CTkFrame(inner, width=5, fg_color=style["accent"], corner_radius=0)
        stripe.pack(side="left", fill="y", padx=(0, 0))
        stripe.pack_propagate(False)

        text_frame = ctk.CTkFrame(inner, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=8)

        ctk.CTkLabel(
            text_frame,
            text=f"{style['icon']}  {message}",
            font=("Arial", 12),
            text_color="white",
            wraplength=250,
            justify="left",
            anchor="w",
        ).pack(fill="both", expand=True, anchor="w")

        # Bezárás gomb
        close_btn = ctk.CTkButton(
            inner, text="✕", width=22, height=22,
            fg_color="transparent", hover_color=style["accent"],
            text_color="#cccccc", font=("Arial", 11, "bold"),
            command=lambda: self._dismiss_toast(toast),
        )
        close_btn.pack(side="right", padx=(0, 6), pady=6, anchor="n")

        self._active_toasts.append(toast)

        # Automatikus eltűnés
        if duration > 0:
            self.after(duration, lambda: self._dismiss_toast(toast))

    def _dismiss_toast(self, toast):
        """Eltünteti a toast ablakot."""
        try:
            if toast in self._active_toasts:
                self._active_toasts.remove(toast)
        except Exception:
            pass
        try:
            if toast.winfo_exists():
                toast.destroy()
        except Exception:
            pass

    # ------------------------------------------------------------------
    #  Összecsukható sidebar
    # ------------------------------------------------------------------
    def init_collapsible_sidebar(self):
        """Hozzáad egy hamburger gombot a sidebar összecsukásához."""
        self._sidebar_collapsed = False

        self.btn_toggle_sidebar = ctk.CTkButton(
            self.top_tab_frame,
            text="☰",
            width=30, height=30,
            fg_color="#2b2b2b",
            hover_color="#3a3a3a",
            font=("Arial", 14, "bold"),
            command=self.toggle_sidebar,
        )
        self.btn_toggle_sidebar.pack(side="left", padx=(4, 2), pady=5)

    def toggle_sidebar(self):
        """Összecsukja / kinyitja a bal oldali menüt."""
        try:
            if self._sidebar_collapsed:
                # Kinyitás
                self.sidebar.configure(width=236)
                self.sidebar.pack_propagate(False)
                for child in self.sidebar.winfo_children():
                    try:
                        child.pack_info()  # csak hogy ne dobjon hibát
                    except Exception:
                        pass
                self._sidebar_collapsed = False
                self.notify("📂 Menü kinyitva", "info", 1500)
            else:
                # Összecsukás
                self.sidebar.configure(width=60)
                self.sidebar.pack_propagate(False)
                self._sidebar_collapsed = True
                self.notify("📁 Menü összecsukva", "info", 1500)
        except Exception as e:
            print(f"[UI] Sidebar toggle hiba: {e}")

    # ------------------------------------------------------------------
    #  Animált státusz pont
    # ------------------------------------------------------------------
    def init_animated_status(self):
        """A státuszjelző pontja lüktet, ha a bot fut."""
        self._status_pulse_state = False
        self._status_pulse_running = True
        self._start_status_pulse()

    def _start_status_pulse(self):
        if not getattr(self, "_status_pulse_running", False):
            return
        try:
            bot = self.bots.get(self.active_bot_key)
            if bot and bot.get("is_running"):
                if hasattr(self, "lbl_status"):
                    current = self.lbl_status.cget("text")
                    base = current.replace("●", "").strip()
                    self.lbl_status.configure(
                        text=f"● {base}",
                        text_color="#2ecc71" if self._status_pulse_state else "#27ae60"
                    )
                    self._status_pulse_state = not self._status_pulse_state
        except Exception:
            pass
        self.after(900, self._start_status_pulse)

    def stop_status_pulse(self):
        self._status_pulse_running = False