import threading

import customtkinter as ctk
from tkinter import messagebox


# Emoji és szín választó listák a botokhoz
BOT_EMOJIS = ["🤖", "🎵", "🎮", "⚙️", "🎨", "📚", "🛠️", "🎯", "🚀",
              "🌟", "💎", "🔥", "🎬", "🎤", "📡", "🧠", "🎲", "🏆",
              "🐍", "🦊", "🐺", "⚡", "🌙", "☀️"]

# (name_key, hex) — a nevek a languages.py-ból jönnek
BOT_COLORS = [
    ("color_blurple", "#5865F2"),
    ("color_blue",    "#3498db"),
    ("color_green",   "#2ecc71"),
    ("color_red",     "#e74c3c"),
    ("color_orange",  "#f39c12"),
    ("color_purple",  "#9b59b6"),
    ("color_teal",    "#1abc9c"),
    ("color_rose",    "#e91e63"),
    ("color_cyan",    "#00bcd4"),
    ("color_gold",    "#f1c40f"),
    ("color_mauve",   "#8e44ad"),
    ("color_graphite","#7f8c8d"),
]

# Spinner karakterek a futó bot jelzéséhez
SPINNER_CHARS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


class UIEnhancementsMixin:
    """Fejlettebb UI/UX: emoji + szín, kereső, spinner, gyors botváltás."""

    # ==================================================================
    #  Inicializálás
    # ==================================================================
    def init_ui_enhancements(self):
        self._bot_search_var = ctk.StringVar()
        self._bot_search_visible = False
        self._bot_search_frame = None
        self._spinner_index = 0
        self._spinner_active = False

        self.after(300, self._setup_ui_enhancements)

    def _setup_ui_enhancements(self):
        """Késleltetett beállítás, hogy minden widget létezzen."""
        try:
            self._setup_bot_search()
            self._start_spinner_loop()
            self._register_bot_hotkeys()
        except Exception as e:
            print(f"[UI-ENHANCE] Hiba: {e}")

    # ==================================================================
    #  Kereső mező a fülek fölé
    # ==================================================================
    def _setup_bot_search(self):
        """Kis kereső mező a tab_buttons_frame alá."""
        if len(self.bots) < 5:
            return  # csak sok bot esetén jelenik meg

        try:
            self._bot_search_frame = ctk.CTkFrame(
                self.top_tab_frame, fg_color="transparent"
            )
            self._bot_search_frame.pack(side="left", padx=8, pady=5)

            self._bot_search_entry = ctk.CTkEntry(
                self._bot_search_frame,
                placeholder_text=self.tr("ui_search_placeholder"),
                width=180, height=30,
                font=("Arial", 11),
            )
            self._bot_search_entry.pack(side="left")
            self._bot_search_entry.bind(
                "<KeyRelease>",
                lambda e: self._filter_bots(self._bot_search_entry.get())
            )
        except Exception as e:
            print(f"[UI-ENHANCE] Kereső hiba: {e}")

    def _filter_bots(self, query):
        """Szűri a füleket a keresés alapján."""
        query = query.strip().lower()
        for child in self.tab_buttons_frame.winfo_children():
            try:
                # Csak a CTkButton típusú elemeket vizsgáljuk
                text = child.cget("text") if hasattr(child, "cget") else ""
                if query and query not in str(text).lower():
                    child.pack_forget()
                else:
                    child.pack(side="left", padx=5, pady=5)
            except Exception:
                pass

    # ==================================================================
    #  Spinner a futó bot jelzéséhez
    # ==================================================================
    def _start_spinner_loop(self):
        """Animációs loop, ami a státuszjelzőt pörgeti."""
        self._spinner_active = True
        self._update_spinner()

    def _update_spinner(self):
        if not self._spinner_active:
            return
        try:
            self._spinner_index = (self._spinner_index + 1) % len(SPINNER_CHARS)
            char = SPINNER_CHARS[self._spinner_index]

            # Ha a bot fut, a státuszjelző pörög
            bot = self.bots.get(self.active_bot_key)
            if bot and bot.get("is_running") and hasattr(self, "lbl_status"):
                self.lbl_status.configure(
                    text=self.tr("ui_status_online_spinner", char=char),
                    text_color="#2ecc71"
                )
        except Exception:
            pass
        self.after(100, self._update_spinner)

    # ==================================================================
    #  Ctrl+1..9 botváltás
    # ==================================================================
    def _register_bot_hotkeys(self):
        """Ctrl+1..9 → botváltás index alapján."""
        for i in range(1, 10):
            self.bind(
                f"<Control-Key-{i}>",
                lambda e, idx=i - 1: self._switch_bot_by_index(idx)
            )

    def _switch_bot_by_index(self, idx):
        """A megadott indexű botra vált (0..8)."""
        keys = list(self.bots.keys())
        if 0 <= idx < len(keys):
            try:
                self.switch_bot(keys[idx])
                try:
                    self.notify(self.tr("ui_switch_toast", name=keys[idx]), "info", 1200)
                except Exception:
                    pass
            except Exception as e:
                print(f"[UI-ENHANCE] Váltási hiba: {e}")

    # ==================================================================
    #  Bot emoji + szín beállítása
    # ==================================================================
    def open_bot_appearance_editor(self):
        """Felugró ablak a bot emoji + szín beállításához."""
        bot_key = self.active_bot_key
        bot = self.bots.get(bot_key)
        if not bot:
            return

        current_emoji = bot.get("emoji", "🤖")
        current_color = bot.get("color", "#5865F2")

        win = ctk.CTkToplevel(self)
        win.title(self.tr("ui_appearance_title", name=bot_key))
        win.geometry("520x580")
        win.resizable(False, False)
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 520) // 2
        y = (win.winfo_screenheight() - 580) // 2
        win.geometry(f"520x580+{x}+{y}")

        # --- Fejléc ---
        header = ctk.CTkFrame(win, fg_color="#5865F2", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text=self.tr("ui_appearance_header", name=bot_key),
            font=("Arial", 17, "bold"), text_color="white"
        ).pack(pady=14)

        # --- Előnézet ---
        preview_frame = ctk.CTkFrame(win, fg_color="#232323", corner_radius=10)
        preview_frame.pack(fill="x", padx=20, pady=(16, 8))

        preview_label = ctk.CTkLabel(
            preview_frame,
            text=f"  {current_emoji}  {bot_key}  ",
            font=("Arial", 18, "bold"),
            fg_color=current_color,
            corner_radius=8,
            height=44,
        )
        preview_label.pack(pady=14)

        # --- Emoji választó ---
        ctk.CTkLabel(
            win, text=self.tr("ui_emoji_lbl"),
            font=("Arial", 13, "bold"), anchor="w"
        ).pack(fill="x", padx=20, pady=(12, 4))

        emoji_grid = ctk.CTkFrame(win, fg_color="transparent")
        emoji_grid.pack(fill="x", padx=20)

        selected_emoji = [current_emoji]

        def pick_emoji(em):
            selected_emoji[0] = em
            preview_label.configure(text=f"  {em}  {bot_key}  ")

        for i, em in enumerate(BOT_EMOJIS):
            btn = ctk.CTkButton(
                emoji_grid, text=em, width=42, height=36,
                fg_color="#2b2b2b", hover_color="#3a3a3a",
                font=("Arial", 18),
                command=lambda e=em: pick_emoji(e)
            )
            btn.grid(row=i // 8, column=i % 8, padx=2, pady=2)

        # --- Szín választó ---
        ctk.CTkLabel(
            win, text=self.tr("ui_color_lbl"),
            font=("Arial", 13, "bold"), anchor="w"
        ).pack(fill="x", padx=20, pady=(16, 4))

        color_grid = ctk.CTkFrame(win, fg_color="transparent")
        color_grid.pack(fill="x", padx=20)

        selected_color = [current_color]

        def pick_color(hexcode):
            selected_color[0] = hexcode
            preview_label.configure(fg_color=hexcode)

        for i, (name_key, hexcode) in enumerate(BOT_COLORS):
            btn = ctk.CTkButton(
                color_grid, text="", width=42, height=32,
                fg_color=hexcode, hover_color=hexcode,
                border_width=1, border_color="#444",
                command=lambda h=hexcode: pick_color(h)
            )
            btn.grid(row=i // 6, column=i % 6, padx=3, pady=3)

        # --- Egyéni hex bevitel ---
        custom_frame = ctk.CTkFrame(win, fg_color="transparent")
        custom_frame.pack(fill="x", padx=20, pady=(10, 4))

        ctk.CTkLabel(
            custom_frame, text=self.tr("ui_custom_hex_lbl"),
            font=("Arial", 11), text_color="#aaaaaa"
        ).pack(side="left")

        custom_entry = ctk.CTkEntry(custom_frame, width=120, placeholder_text="#RRGGBB")
        custom_entry.pack(side="left", padx=8)

        def apply_custom_color():
            value = custom_entry.get().strip()
            if value and not value.startswith("#"):
                value = "#" + value
            if len(value) == 7:
                pick_color(value)

        ctk.CTkButton(
            custom_frame, text=self.tr("ui_apply_btn"), width=90,
            fg_color="#2980b9", command=apply_custom_color
        ).pack(side="left")

        # --- Mentés ---
        def save():
            bot["emoji"] = selected_emoji[0]
            bot["color"] = selected_color[0]
            try:
                self.save_config()
                self.render_tabs()  # újraépíti a füleket
                try:
                    self.notify(self.tr("ui_appearance_saved", name=bot_key), "success")
                except Exception:
                    pass
            except Exception as e:
                messagebox.showerror(self.tr("common_error_title"), str(e), parent=win)
                return
            win.destroy()

        btns = ctk.CTkFrame(win, fg_color="transparent")
        btns.pack(fill="x", padx=20, pady=18)
        ctk.CTkButton(
            btns, text=self.tr("ui_save_btn"), fg_color="#27ae60",
            hover_color="#2ecc71", width=160, height=40,
            font=("Arial", 13, "bold"), command=save
        ).pack(side="left")
        ctk.CTkButton(
            btns, text=self.tr("ui_cancel_btn"), fg_color="#555555",
            hover_color="#666666", width=100, height=40,
            command=win.destroy
        ).pack(side="right")