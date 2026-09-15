import os
import importlib.util
from tkinter import messagebox

import customtkinter as ctk

import modules.config as config
from modules.config import PLUGINS_DIR


# =====================================================================
#  PLUGIN SABLONOK
#  A "name_key" a UI-ban megjelenő név (fordítva).
#  A "code" a plugin kódja — NEM fordítjuk, mert a user szerkeszti.
# =====================================================================
PLUGIN_TEMPLATES = {
    "empty": {
        "name_key": "plugin_tpl_empty_name",
        "code": '''def setup_panel(panel):
    """Ez a függvény fut le, amikor a panel betölti a plugint."""
    panel.log_event("EVENT", "Üres plugin betöltve.")
''',
    },
    "event_logger": {
        "name_key": "plugin_tpl_event_logger_name",
        "code": '''def setup_panel(panel):
    panel.log_event("EVENT", "Esemény loggoló plugin aktív.")

    def tick():
        panel.log_event("INFO", "[Plugin] Óra ketyeg...")
        panel.after(10000, tick)

    panel.after(5000, tick)
''',
    },
    "sidebar_button": {
        "name_key": "plugin_tpl_sidebar_button_name",
        "code": '''def setup_panel(panel):
    import customtkinter as ctk

    def on_click():
        panel.log_event("EVENT", "Egyedi gomb megnyomva!")

    btn = ctk.CTkButton(
        panel.sidebar_menu,
        text="Plugin gomb",
        fg_color="#9b59b6",
        command=on_click,
    )
    btn.pack(fill="x", padx=6, pady=2)
''',
    },
    "custom_window": {
        "name_key": "plugin_tpl_custom_window_name",
        "code": '''def setup_panel(panel):
    import customtkinter as ctk

    def open_custom_window():
        win = ctk.CTkToplevel(panel)
        win.title("Egyedi ablak")
        win.geometry("400x300")
        win.grab_set()
        ctk.CTkLabel(win, text="Szia! Ez a plugin ablaka.",
                     font=("Arial", 16, "bold")).pack(pady=20)
        ctk.CTkButton(win, text="Bezárás",
                      command=win.destroy).pack(pady=10)

    btn = ctk.CTkButton(
        panel.sidebar_menu,
        text="Egyedi ablak",
        fg_color="#e67e22",
        command=open_custom_window,
    )
    btn.pack(fill="x", padx=6, pady=2)
''',
    },
    "welcome_log": {
        "name_key": "plugin_tpl_welcome_log_name",
        "code": '''def setup_panel(panel):
    panel.append_log("SUCCESS", "🎉 Szia! A plugin sikeresen betöltődött.")
    panel.append_log("EVENT", "Verzió: 1.0.0")
''',
    },
    "bot_watcher": {
        "name_key": "plugin_tpl_bot_watcher_name",
        "code": '''def setup_panel(panel):
    panel.log_event("EVENT", "Bot figyelő plugin aktív.")
    state = {"last_running": {}}

    def check():
        for key, bot in panel.bots.items():
            was = state["last_running"].get(key, False)
            now = bot.get("is_running", False)
            if was and not now:
                panel.log_event("ERROR", f"[FIGYELŐ] A(z) '{key}' bot leállt!")
            elif not was and now:
                panel.log_event("SUCCESS", f"[FIGYELŐ] A(z) '{key}' bot elindult.")
            state["last_running"][key] = now
        panel.after(2000, check)

    panel.after(2000, check)
''',
    },
    "error_beep": {
        "name_key": "plugin_tpl_error_beep_name",
        "code": '''def setup_panel(panel):
    import winsound

    original_log = panel.append_log_to_bot

    def wrapped(bot_key, log_type, message):
        original_log(bot_key, log_type, message)
        if log_type == "ERROR":
            try:
                winsound.Beep(1500, 300)
            except Exception:
                pass

    panel.append_log_to_bot = wrapped
    panel.log_event("EVENT", "Hangjelzés plugin aktív.")
''',
    },
    "calculator": {
        "name_key": "plugin_tpl_calculator_name",
        "code": '''def setup_panel(panel):
    import customtkinter as ctk

    def open_calc():
        win = ctk.CTkToplevel(panel)
        win.title("Számológép")
        win.geometry("300x400")
        win.grab_set()

        entry = ctk.CTkEntry(win, width=260, font=("Arial", 18))
        entry.pack(pady=12, padx=20)

        def press(val):
            entry.insert("end", str(val))

        def calculate():
            try:
                result = eval(entry.get())
                entry.delete(0, "end")
                entry.insert(0, str(result))
            except Exception:
                entry.delete(0, "end")
                entry.insert(0, "Hiba")

        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=6)
        buttons = [
            ["7","8","9","/"],
            ["4","5","6","*"],
            ["1","2","3","-"],
            ["0",".","C","+"],
        ]
        for row in buttons:
            row_f = ctk.CTkFrame(btn_frame, fg_color="transparent")
            row_f.pack()
            for b in row:
                if b == "C":
                    cmd = lambda: entry.delete(0, "end")
                else:
                    cmd = lambda x=b: press(x)
                ctk.CTkButton(row_f, text=b, width=55, height=45,
                              command=cmd).pack(side="left", padx=2, pady=2)

        ctk.CTkButton(win, text="=", fg_color="#27ae60", width=240,
                      command=calculate).pack(pady=8)

    btn = ctk.CTkButton(
        panel.sidebar_menu,
        text="Számológép",
        fg_color="#16a085",
        command=open_calc,
    )
    btn.pack(fill="x", padx=6, pady=2)
''',
    },
    "theme_switcher": {
        "name_key": "plugin_tpl_theme_switcher_name",
        "code": '''def setup_panel(panel):
    import customtkinter as ctk

    def apply_dark():
        panel.apply_theme_setting("Discord Sötét (Alap)")

    def apply_green():
        panel.apply_theme_setting("Discord Zöld (Hacker)")

    frame = ctk.CTkFrame(panel.sidebar_menu, fg_color="transparent")
    frame.pack(fill="x", padx=6, pady=4)

    ctk.CTkButton(frame, text="🌑 Sötét", width=80,
                  command=apply_dark).pack(side="left", padx=2)
    ctk.CTkButton(frame, text="🟢 Zöld", width=80, fg_color="#2ecc71",
                  command=apply_green).pack(side="left", padx=2)
''',
    },
    "webhook": {
        "name_key": "plugin_tpl_webhook_name",
        "code": '''def setup_panel(panel):
    import urllib.request
    import json

    WEBHOOK_URL = "IDE_IRD_A_WEBHOOK_URL_T"

    if "IDE_IRD" in WEBHOOK_URL:
        panel.log_event("EVENT", "Webhook plugin: állítsd be a WEBHOOK_URL-t!")
        return

    original_log = panel.append_log_to_bot

    def wrapped(bot_key, log_type, message):
        original_log(bot_key, log_type, message)
        if log_type == "ERROR":
            try:
                data = json.dumps({"content": f"⚠️ [{bot_key}] {message}"}).encode()
                req = urllib.request.Request(
                    WEBHOOK_URL, data=data,
                    headers={"Content-Type": "application/json"}
                )
                urllib.request.urlopen(req, timeout=5)
            except Exception:
                pass

    panel.append_log_to_bot = wrapped
    panel.log_event("EVENT", "Webhook értesítés plugin aktív.")
''',
    },
}


class WindowPluginsMixin:
    """Plugin kezelő mixin."""

    def load_plugins(self):
        os.makedirs(PLUGINS_DIR, exist_ok=True)
        self.plugins = []
        for filename in sorted(os.listdir(PLUGINS_DIR)):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            path = os.path.join(PLUGINS_DIR, filename)
            try:
                module_name = "panel_plugin_" + os.path.splitext(filename)[0]
                spec = importlib.util.spec_from_file_location(module_name, path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "setup_panel"):
                    module.setup_panel(self)
                self.plugins.append(filename)
            except Exception as error:
                self.log_event("ERROR", self.tr("plugins_load_error",
                                                 file=filename, error=error))

    def open_plugins_window(self):
        win = ctk.CTkToplevel(self)
        win.title(self.tr("plugins"))
        win.geometry("980x640")
        win.minsize(760, 480)
        win.grab_set()

        win.update_idletasks()
        x = (win.winfo_screenwidth() - 980) // 2
        y = (win.winfo_screenheight() - 640) // 2
        win.geometry(f"980x640+{x}+{y}")

        ctk.CTkLabel(win, text="🧩 " + self.tr("plugins"),
                     font=("Arial", 18, "bold"), text_color="#7f8c8d").pack(pady=(12, 4))
        ctk.CTkLabel(win, text=self.tr("plugins_help"),
                     font=("Arial", 11), text_color="#aaaaaa").pack(pady=(0, 8))

        main = ctk.CTkFrame(win, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=12, pady=4)

        left = ctk.CTkFrame(main, width=240)
        left.pack(side="left", fill="y", padx=(0, 8))
        left.pack_propagate(False)

        ctk.CTkLabel(left, text=self.tr("plugins_list_lbl"),
                      font=("Arial", 12, "bold")).pack(pady=(8, 4))

        listbox = ctk.CTkTextbox(left, activate_scrollbars=True, wrap="none",
                                 font=("Consolas", 11))
        listbox.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        def render_list():
            listbox.configure(state="normal")
            listbox.delete("1.0", "end")
            os.makedirs(PLUGINS_DIR, exist_ok=True)
            for f in sorted(os.listdir(PLUGINS_DIR)):
                if f.endswith(".py") and not f.startswith("_"):
                    listbox.insert("end", f + "\n")
            listbox.configure(state="disabled")

        right = ctk.CTkFrame(main, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True)

        current_file = {"name": None}

        file_label = ctk.CTkLabel(right, text=self.tr("plugins_select_hint"),
                                  font=("Arial", 12, "bold"), anchor="w")
        file_label.pack(fill="x", padx=4, pady=(4, 2))

        editor = ctk.CTkTextbox(right, font=("Consolas", 11), wrap="none")
        editor.pack(fill="both", expand=True, padx=4, pady=4)

        status = ctk.CTkLabel(right, text="", font=("Arial", 10),
                              text_color="#aaaaaa", anchor="w")
        status.pack(fill="x", padx=4)

        def load_file(filename):
            path = os.path.join(PLUGINS_DIR, filename)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                messagebox.showerror(self.tr("common_error_title"),
                                       self.tr("plugins_read_error", error=e),
                                       parent=win)
                return
            current_file["name"] = filename
            file_label.configure(text=f"📄 {filename}")
            editor.delete("1.0", "end")
            editor.insert("1.0", content)
            status.configure(text=self.tr("plugins_loaded_status", name=filename))

        def save_file():
            if not current_file["name"]:
                messagebox.showwarning(self.tr("common_warning_title"),
                                        self.tr("plugins_need_select"), parent=win)
                return
            content = editor.get("1.0", "end").strip() + "\n"
            try:
                compile(content, current_file["name"], "exec")
            except SyntaxError as e:
                messagebox.showerror(
                    self.tr("plugins_syntax_error_title"),
                    self.tr("plugins_syntax_error_msg", line=e.lineno, msg=e.msg),
                    parent=win
                )
                return
            path = os.path.join(PLUGINS_DIR, current_file["name"])
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                status.configure(text=self.tr("plugins_saved_status",
                                                name=current_file['name']))
                self.log_event("EVENT",
                               self.tr("plugins_saved_log", name=current_file['name']))
            except Exception as e:
                messagebox.showerror(self.tr("common_error_title"),
                                       self.tr("plugins_save_error", error=e),
                                       parent=win)

        def new_plugin_dialog():
            dialog = ctk.CTkToplevel(win)
            dialog.title(self.tr("plugins_new_dialog_title"))
            dialog.geometry("420x280")
            dialog.grab_set()
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() - 420) // 2
            y = (dialog.winfo_screenheight() - 280) // 2
            dialog.geometry(f"420x280+{x}+{y}")

            ctk.CTkLabel(dialog, text=self.tr("plugins_new_dialog_header"),
                         font=("Arial", 14, "bold")).pack(pady=12)

            ctk.CTkLabel(dialog, text=self.tr("plugins_new_filename_lbl")).pack(
                anchor="w", padx=20)
            name_entry = ctk.CTkEntry(dialog, width=340)
            name_entry.insert(0, "sajat_plugin.py")
            name_entry.pack(padx=20, pady=4)

            ctk.CTkLabel(dialog, text=self.tr("plugins_new_template_lbl")).pack(
                anchor="w", padx=20, pady=(8, 2))

            # Fordított sablon-név → kulcs mapping
            tpl_name_to_key = {
                self.tr(t["name_key"]): k for k, t in PLUGIN_TEMPLATES.items()
            }
            tpl_display_names = list(tpl_name_to_key.keys())
            default_tpl_display = self.tr(PLUGIN_TEMPLATES["empty"]["name_key"])

            template_var = ctk.StringVar(value=default_tpl_display)
            ctk.CTkComboBox(dialog, values=tpl_display_names,
                            variable=template_var, width=340).pack(padx=20, pady=4)

            def do_create():
                fname = name_entry.get().strip()
                if not fname.endswith(".py"):
                    fname += ".py"
                if not fname or "/" in fname or "\\" in fname:
                    messagebox.showerror(self.tr("common_error_title"),
                                           self.tr("plugins_invalid_filename"),
                                           parent=dialog)
                    return
                path = os.path.join(PLUGINS_DIR, fname)
                if os.path.exists(path):
                    if not messagebox.askyesno(
                        self.tr("plugins_exists_title"),
                        self.tr("plugins_exists_confirm", name=fname),
                        parent=dialog
                    ):
                        return
                tpl_key = tpl_name_to_key.get(template_var.get(), "empty")
                try:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(PLUGIN_TEMPLATES[tpl_key]["code"])
                    render_list()
                    load_file(fname)
                    self.log_event("EVENT",
                                   self.tr("plugins_created_log", name=fname))
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror(self.tr("common_error_title"),
                                           str(e), parent=dialog)

            btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            btn_frame.pack(pady=12)
            ctk.CTkButton(btn_frame, text=self.tr("plugins_create_btn"),
                           fg_color="#27ae60",
                           command=do_create).pack(side="left", padx=4)
            ctk.CTkButton(btn_frame, text=self.tr("ui_cancel_btn"),
                           fg_color="#555555",
                           command=dialog.destroy).pack(side="left", padx=4)

        def delete_plugin():
            if not current_file["name"]:
                messagebox.showwarning(self.tr("common_warning_title"),
                                        self.tr("plugins_need_select"), parent=win)
                return
            if not messagebox.askyesno(
                self.tr("commander_delete_title"),
                self.tr("plugins_delete_confirm", name=current_file['name']),
                parent=win
            ):
                return
            try:
                os.remove(os.path.join(PLUGINS_DIR, current_file["name"]))
                self.log_event("EVENT",
                               self.tr("plugins_deleted_log", name=current_file['name']))
                current_file["name"] = None
                editor.delete("1.0", "end")
                file_label.configure(text=self.tr("plugins_select_hint"))
                status.configure(text="")
                render_list()
            except Exception as e:
                messagebox.showerror(self.tr("common_error_title"),
                                       str(e), parent=win)

        def reload_all():
            self.load_plugins()
            render_list()
            status.configure(text=self.tr("plugins_reloaded_status"))
            self.log_event("EVENT", self.tr("plugins_reloaded_log"))

        def on_left_click(event):
            index = listbox.index(f"@{event.x},{event.y}")
            line = int(index.split(".")[0])
            files = [f for f in sorted(os.listdir(PLUGINS_DIR))
                     if f.endswith(".py") and not f.startswith("_")]
            if 0 < line <= len(files):
                load_file(files[line - 1])

        listbox.bind("<Button-1>", on_left_click)

        btns = ctk.CTkFrame(win, fg_color="transparent")
        btns.pack(fill="x", padx=12, pady=10)

        ctk.CTkButton(btns, text=self.tr("plugins_new_btn"), fg_color="#27ae60",
                      hover_color="#2ecc71", command=new_plugin_dialog,
                      width=140).pack(side="left", padx=4)
        ctk.CTkButton(btns, text=self.tr("plugins_save_btn"), fg_color="#2980b9",
                      hover_color="#3498db", command=save_file,
                      width=120).pack(side="left", padx=4)
        ctk.CTkButton(btns, text=self.tr("plugins_delete_btn"), fg_color="#c0392b",
                      hover_color="#e74c3c", command=delete_plugin,
                      width=120).pack(side="left", padx=4)
        ctk.CTkButton(btns, text=self.tr("plugins_reload_btn"), fg_color="#8e44ad",
                      hover_color="#9b59b6", command=reload_all,
                      width=140).pack(side="left", padx=4)
        ctk.CTkButton(btns, text=self.tr("common_close_btn"), fg_color="#555555",
                      command=win.destroy, width=100).pack(side="right", padx=4)

        render_list()