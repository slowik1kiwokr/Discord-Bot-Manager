import os
import json
from tkinter import messagebox

import customtkinter as ctk

import modules.config as config
from modules.languages import LANGUAGES


COMMANDER_FILE_NAME = "commander_commands.json"


# --- Commander sablonok ---
COMMANDER_TEMPLATES = {
    "Üres (kézzel kitöltöm)": {
        "type": "message",
        "description": "Egyedi parancs",
        "content": "",
        "embed": {
            "title": "", "description": "", "color": "#5865F2",
            "footer": "", "thumbnail": "", "fields": [],
        },
        "ephemeral": False,
    },
    "Egyszerű szöveges üzenet": {
        "type": "message",
        "description": "Egyszerű szöveges válasz",
        "content": "👋 Szia! Ez egy egyedi parancs válasza.",
        "embed": {
            "title": "", "description": "", "color": "#5865F2",
            "footer": "", "thumbnail": "", "fields": [],
        },
        "ephemeral": False,
    },
    "Üdvözlő szöveges üzenet": {
        "type": "message",
        "description": "Üdvözlés a szerveren",
        "content": "🎉 Üdv a szerveren! Jó szórakozást kívánunk!",
        "embed": {
            "title": "", "description": "", "color": "#5865F2",
            "footer": "", "thumbnail": "", "fields": [],
        },
        "ephemeral": False,
    },
    "Egyszerű embed": {
        "type": "embed",
        "description": "Szép embed válasz",
        "content": "",
        "embed": {
            "title": "📌 Cím",
            "description": "Ez egy egyszerű embed üzenet. Ide jön a részletes szöveg.",
            "color": "#5865F2",
            "footer": "Bot által generálva",
            "thumbnail": "",
            "fields": [],
        },
        "ephemeral": False,
    },
    "Színes értesítő embed": {
        "type": "embed",
        "description": "Értesítés színes embedben",
        "content": "",
        "embed": {
            "title": "🔔 Értesítés",
            "description": "Ez egy fontos értesítés, amit mindenkinek látnia kell.",
            "color": "#f39c12",
            "footer": "Automatikus értesítés",
            "thumbnail": "",
            "fields": [],
        },
        "ephemeral": False,
    },
    "Hiba embed (piros)": {
        "type": "embed",
        "description": "Hibaüzenet embedben",
        "content": "",
        "embed": {
            "title": "❌ Hiba",
            "description": "Valami hiba történt. Kérlek próbáld újra később.",
            "color": "#e74c3c",
            "footer": "",
            "thumbnail": "",
            "fields": [],
        },
        "ephemeral": True,
    },
    "Siker embed (zöld)": {
        "type": "embed",
        "description": "Sikeres művelet visszajelzése",
        "content": "",
        "embed": {
            "title": "✅ Siker",
            "description": "A művelet sikeresen végrehajtva!",
            "color": "#2ecc71",
            "footer": "",
            "thumbnail": "",
            "fields": [],
        },
        "ephemeral": True,
    },
    "Segítség embed (fields)": {
        "type": "embed",
        "description": "Több mezős segítség panel",
        "content": "",
        "embed": {
            "title": "❓ Segítség",
            "description": "Az elérhető parancsok listája:",
            "color": "#3498db",
            "footer": "További info: /help",
            "thumbnail": "",
            "fields": [
                {"name": "🎮 Játék", "value": "/játék - Játék indítása", "inline": False},
                {"name": "🎵 Zene", "value": "/play - Zene lejátszása", "inline": False},
                {"name": "⚙️ Beállítások", "value": "/config - Bot beállítások", "inline": False},
            ],
        },
        "ephemeral": False,
    },
}


class WindowCommanderMixin:
    """Dinamikus parancs- és embed-szerkesztő (Commander plugin)."""

    def _commander_config_path(self):
        bot = self.bots.get(self.active_bot_key, {})
        script_path = bot.get("path", "")
        if not script_path:
            return None
        bot_dir = os.path.dirname(script_path)
        return os.path.join(bot_dir, COMMANDER_FILE_NAME)

    def _load_commander_commands(self):
        path = self._commander_config_path()
        if not path or not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return []

    def _save_commander_commands(self, commands):
        path = self._commander_config_path()
        if not path:
            return False
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(commands, f, ensure_ascii=False, indent=4)
            return True
        except OSError as e:
            messagebox.showerror("Hiba", f"Nem sikerült menteni:\n{e}")
            return False

    # --------------------------------------------------------------
    #  Commander.py mentése a bot mappájába
    # --------------------------------------------------------------
    def save_commander_to_bot(self):
        bot = self.bots.get(self.active_bot_key, {})
        script_path = bot.get("path", "")
        if not script_path:
            messagebox.showwarning("Figyelem",
                                   "Előbb tallózd be a bot fő .py fájlját!")
            return
        bot_dir = os.path.dirname(script_path)
        target = os.path.join(bot_dir, "Commander.py")
        try:
            from modules.templates import COMMANDER_PLUGIN_CODE
            with open(target, "w", encoding="utf-8") as f:
                f.write(COMMANDER_PLUGIN_CODE)
            messagebox.showinfo(
                "Siker",
                f"A Commander.py elkészült:\n{bot_dir}\n\n"
                f"Ne felejtsd el betölteni a bot.py-ban:\n"
                f"await bot.load_extension('Commander')"
            )
            self.log_event("EVENT", f"[COMMANDER] Commander.py mentve: {bot_dir}")
        except Exception as e:
            messagebox.showerror("Hiba", str(e))

    # --------------------------------------------------------------
    #  Fő Commander ablak
    # --------------------------------------------------------------
    def open_commander_window(self):
        bot = self.bots.get(self.active_bot_key, {})
        if not bot.get("path"):
            messagebox.showwarning(
                "Figyelem",
                "Előbb tallózd be a bot fő .py fájlját a fő panelen!"
            )
            return

        win = ctk.CTkToplevel(self)
        win.title("⚡ Commander - Dinamikus parancsok")
        win.geometry("880x600")
        win.minsize(700, 460)
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 880) // 2
        y = (win.winfo_screenheight() - 600) // 2
        win.geometry(f"880x600+{x}+{y}")

        ctk.CTkLabel(win, text="⚡ Commander - Dinamikus parancsok",
                     font=("Arial", 18, "bold"), text_color="#f39c12").pack(pady=(12, 4))
        ctk.CTkLabel(
            win,
            text="Hozz létre egyedi Discord parancsokat. A bot a Commander.py "
                 "extension betöltésekor automatikusan regisztrálja őket.",
            font=("Arial", 11), text_color="#aaaaaa",
        ).pack(pady=(0, 8))

        # --- Lista ---
        list_frame = ctk.CTkScrollableFrame(win, height=320)
        list_frame.pack(fill="both", expand=True, padx=12, pady=4)

        def refresh_list():
            for child in list_frame.winfo_children():
                child.destroy()
            commands = self._load_commander_commands()
            if not commands:
                ctk.CTkLabel(list_frame, text="Még nincs egyedi parancs.",
                             text_color="#777").pack(pady=20)
                return
            for i, cmd in enumerate(commands):
                card = ctk.CTkFrame(list_frame, fg_color=self.theme_colors["card_bg"])
                card.pack(fill="x", padx=4, pady=4)
                type_str = "Embed" if cmd.get("type") == "embed" else "Üzenet"
                enabled_str = "✅" if cmd.get("enabled", True) else "⛔"
                ctk.CTkLabel(
                    card,
                    text=f"{enabled_str} /{cmd.get('name','?')}  •  {type_str}  •  {cmd.get('description','')}",
                    font=("Consolas", 11), anchor="w"
                ).pack(side="left", padx=10, pady=8, fill="x", expand=True)

                ctk.CTkButton(card, text="✏️", width=32, fg_color="#2980b9",
                              command=lambda idx=i: edit_command(idx)).pack(side="right", padx=4, pady=6)
                ctk.CTkButton(card, text="🗑️", width=32, fg_color="#c0392b",
                              command=lambda idx=i: delete_command(idx)).pack(side="right", padx=4, pady=6)

        def delete_command(idx):
            commands = self._load_commander_commands()
            if 0 <= idx < len(commands):
                name = commands[idx].get("name", "?")
                if not messagebox.askyesno("Törlés", f"Törlöd a /{name} parancsot?",
                                           parent=win):
                    return
                commands.pop(idx)
                if self._save_commander_commands(commands):
                    self.log_event("EVENT", f"[COMMANDER] Törölve: /{name}")
                    refresh_list()

        # --- Parancs szerkesztő dialógus ---
        def edit_command(idx=None):
            commands = self._load_commander_commands()
            is_new = idx is None
            data = {
                "name": "", "description": "Egyedi parancs",
                "type": "message", "content": "",
                "embed": {
                    "title": "", "description": "",
                    "color": "#5865F2", "footer": "", "thumbnail": "",
                    "fields": [],
                },
                "ephemeral": False, "enabled": True,
            }
            if not is_new and 0 <= idx < len(commands):
                data = commands[idx]

            dlg = ctk.CTkToplevel(win)
            dlg.title("Parancs szerkesztése" if not is_new else "Új parancs")
            dlg.geometry("640x780")
            dlg.minsize(560, 520)
            dlg.grab_set()
            dlg.update_idletasks()
            x = (dlg.winfo_screenwidth() - 640) // 2
            y = (dlg.winfo_screenheight() - 780) // 2
            dlg.geometry(f"640x780+{x}+{y}")

            top_save = ctk.CTkFrame(dlg, fg_color="transparent")
            top_save.pack(side="bottom", fill="x", padx=12, pady=10)

            scroll = ctk.CTkScrollableFrame(dlg, fg_color="transparent")
            scroll.pack(fill="both", expand=True, padx=12, pady=(12, 0))

            # --- Sablon választó (csak új parancsnál) ---
            template_var = ctk.StringVar(value="Egyszerű szöveges üzenet")
            if is_new:
                ctk.CTkLabel(scroll, text="🎨 Sablon választása:",
                             font=("Arial", 12, "bold"), anchor="w"
                             ).pack(fill="x", padx=10, pady=(4, 2))

            # --- Parancs adatok ---
            ctk.CTkLabel(scroll, text="Parancs neve (per jel nélkül):",
                         anchor="w").pack(fill="x", padx=10, pady=(10, 2))
            name_entry = ctk.CTkEntry(scroll, width=420)
            name_entry.insert(0, data.get("name", ""))
            name_entry.pack(anchor="w", padx=10)

            ctk.CTkLabel(scroll, text="Leírás:", anchor="w").pack(fill="x", padx=10, pady=(10, 2))
            desc_entry = ctk.CTkEntry(scroll, width=420)
            desc_entry.insert(0, data.get("description", ""))
            desc_entry.pack(anchor="w", padx=10)

            ctk.CTkLabel(scroll, text="Típus:", anchor="w").pack(fill="x", padx=10, pady=(10, 2))
            type_var = ctk.StringVar(value="Üzenet" if data.get("type") != "embed" else "Embed")
            ctk.CTkComboBox(scroll, values=["Üzenet", "Embed"],
                            variable=type_var, width=200).pack(anchor="w", padx=10)

            # --- Message szekció ---
            msg_frame = ctk.CTkFrame(scroll, fg_color="transparent")
            ctk.CTkLabel(msg_frame, text="Üzenet tartalma:", anchor="w").pack(fill="x")
            content_box = ctk.CTkTextbox(msg_frame, height=90)
            content_box.pack(fill="x", pady=4)
            content_box.insert("1.0", data.get("content", ""))

            # --- Embed szekció ---
            embed_frame = ctk.CTkFrame(scroll, fg_color="transparent")

            ctk.CTkLabel(embed_frame, text="Embed cím:").pack(anchor="w", pady=(6, 0))
            emb_title = ctk.CTkEntry(embed_frame, width=420)
            emb_title.insert(0, data.get("embed", {}).get("title", ""))
            emb_title.pack(anchor="w")

            ctk.CTkLabel(embed_frame, text="Embed leírás:").pack(anchor="w", pady=(6, 0))
            emb_desc = ctk.CTkTextbox(embed_frame, height=80)
            emb_desc.pack(anchor="w", fill="x")
            emb_desc.insert("1.0", data.get("embed", {}).get("description", ""))

            color_row = ctk.CTkFrame(embed_frame, fg_color="transparent")
            color_row.pack(fill="x", pady=(6, 0))
            ctk.CTkLabel(color_row, text="Szín (hex):").pack(side="left")
            emb_color = ctk.CTkEntry(color_row, width=120)
            emb_color.insert(0, data.get("embed", {}).get("color", "#5865F2"))
            emb_color.pack(side="left", padx=6)

            color_preview = ctk.CTkFrame(color_row, width=28, height=28,
                                         fg_color=data.get("embed", {}).get("color", "#5865F2"),
                                         corner_radius=6)
            color_preview.pack(side="left", padx=4)
            color_preview.pack_propagate(False)

            def update_color_preview(*_):
                try:
                    color_preview.configure(fg_color=emb_color.get().strip() or "#5865F2")
                except Exception:
                    pass

            emb_color.bind("<KeyRelease>", update_color_preview)

            color_quick = ctk.CTkFrame(embed_frame, fg_color="transparent")
            color_quick.pack(fill="x", pady=(4, 0))
            ctk.CTkLabel(color_quick, text="Gyors:").pack(side="left", padx=(0, 4))
            for label, hexcode in [
                ("Blurple", "#5865F2"),
                ("Zöld", "#2ecc71"),
                ("Piros", "#e74c3c"),
                ("Narancs", "#f39c12"),
                ("Kék", "#3498db"),
                ("Lila", "#9b59b6"),
                ("Sárga", "#f1c40f"),
            ]:
                ctk.CTkButton(
                    color_quick, text=label, width=60, height=24,
                    fg_color=hexcode, hover_color=hexcode,
                    text_color="white",
                    command=lambda h=hexcode: (emb_color.delete(0, "end"),
                                               emb_color.insert(0, h),
                                               update_color_preview())
                ).pack(side="left", padx=2)

            ctk.CTkLabel(embed_frame, text="Footer (alcím):").pack(anchor="w", pady=(6, 0))
            emb_footer = ctk.CTkEntry(embed_frame, width=420)
            emb_footer.insert(0, data.get("embed", {}).get("footer", ""))
            emb_footer.pack(anchor="w")

            ctk.CTkLabel(embed_frame, text="Thumbnail URL (kép, opcionális):").pack(anchor="w", pady=(6, 0))
            emb_thumb = ctk.CTkEntry(embed_frame, width=420)
            emb_thumb.insert(0, data.get("embed", {}).get("thumbnail", ""))
            emb_thumb.pack(anchor="w")

            # --- Opciók ---
            ctk.CTkLabel(scroll, text="", height=6).pack()
            eph_var = ctk.BooleanVar(value=data.get("ephemeral", False))
            ctk.CTkCheckBox(scroll, text="Csak a hívónak látszódjon (ephemeral)",
                            variable=eph_var).pack(anchor="w", padx=10, pady=4)

            en_var = ctk.BooleanVar(value=data.get("enabled", True))
            ctk.CTkCheckBox(scroll, text="Parancs engedélyezve",
                            variable=en_var).pack(anchor="w", padx=10, pady=4)

            def toggle_sections(*_):
                if type_var.get() == "Embed":
                    msg_frame.pack_forget()
                    embed_frame.pack(fill="x", padx=10, pady=(10, 0))
                else:
                    embed_frame.pack_forget()
                    msg_frame.pack(fill="x", padx=10, pady=(10, 0))

            type_var.trace_add("write", toggle_sections)
            toggle_sections()

            def apply_template(choice):
                tpl = COMMANDER_TEMPLATES.get(choice)
                if not tpl:
                    return
                type_var.set("Embed" if tpl["type"] == "embed" else "Üzenet")
                desc_entry.delete(0, "end")
                desc_entry.insert(0, tpl.get("description", ""))

                content_box.delete("1.0", "end")
                content_box.insert("1.0", tpl.get("content", ""))

                emb = tpl.get("embed", {})
                emb_title.delete(0, "end")
                emb_title.insert(0, emb.get("title", ""))

                emb_desc.delete("1.0", "end")
                emb_desc.insert("1.0", emb.get("description", ""))

                emb_color.delete(0, "end")
                emb_color.insert(0, emb.get("color", "#5865F2"))
                update_color_preview()

                emb_footer.delete(0, "end")
                emb_footer.insert(0, emb.get("footer", ""))

                emb_thumb.delete(0, "end")
                emb_thumb.insert(0, emb.get("thumbnail", ""))

                eph_var.set(tpl.get("ephemeral", False))
                toggle_sections()

            if is_new:
                ctk.CTkComboBox(
                    scroll,
                    values=list(COMMANDER_TEMPLATES.keys()),
                    variable=template_var,
                    width=420,
                    command=apply_template,
                ).pack(anchor="w", padx=10, pady=(0, 6))

                apply_template("Egyszerű szöveges üzenet")

            def save():
                name = name_entry.get().strip().lstrip("/").replace(" ", "_").lower()
                if not name:
                    messagebox.showerror("Hiba", "A parancs neve nem lehet üres!", parent=dlg)
                    return
                if not name.replace("_", "").isalnum():
                    messagebox.showerror("Hiba",
                                         "A parancs neve csak betű, szám és alulvonás lehet!",
                                         parent=dlg)
                    return
                all_commands = self._load_commander_commands()
                for i, c in enumerate(all_commands):
                    if c.get("name") == name and (is_new or i != idx):
                        messagebox.showerror("Hiba",
                                             f"Már létezik /{name} parancs!", parent=dlg)
                        return

                cmd_data = {
                    "name": name,
                    "description": desc_entry.get().strip() or "Egyedi parancs",
                    "type": "embed" if type_var.get() == "Embed" else "message",
                    "content": content_box.get("1.0", "end").strip(),
                    "embed": {
                        "title": emb_title.get().strip(),
                        "description": emb_desc.get("1.0", "end").strip(),
                        "color": emb_color.get().strip() or "#5865F2",
                        "footer": emb_footer.get().strip(),
                        "thumbnail": emb_thumb.get().strip(),
                        "fields": data.get("embed", {}).get("fields", []),
                    },
                    "ephemeral": bool(eph_var.get()),
                    "enabled": bool(en_var.get()),
                }

                if is_new:
                    all_commands.append(cmd_data)
                else:
                    all_commands[idx] = cmd_data

                if self._save_commander_commands(all_commands):
                    self.log_event("EVENT",
                                   f"[COMMANDER] {'Létrehozva' if is_new else 'Módosítva'}: /{name}")
                    refresh_list()
                    dlg.destroy()

            ctk.CTkButton(top_save, text="💾 Mentés", fg_color="#27ae60",
                          width=180, height=38, command=save).pack()

        # --- Alsó gombok ---
        btns = ctk.CTkFrame(win, fg_color="transparent")
        btns.pack(fill="x", padx=12, pady=10)
        ctk.CTkButton(btns, text="➕ Új parancs", fg_color="#27ae60",
                      hover_color="#2ecc71", command=lambda: edit_command(None),
                      width=140).pack(side="left", padx=4)
        ctk.CTkButton(btns, text="📤 Commander.py a botba",
                      fg_color="#8e44ad", hover_color="#9b59b6",
                      command=self.save_commander_to_bot,
                      width=200).pack(side="left", padx=4)
        ctk.CTkButton(btns, text="🔄 Frissítés", fg_color="#2980b9",
                      hover_color="#3498db", command=refresh_list,
                      width=120).pack(side="left", padx=4)
        ctk.CTkButton(btns, text="Bezárás", fg_color="#555555",
                      command=win.destroy, width=100).pack(side="right", padx=4)

        refresh_list()