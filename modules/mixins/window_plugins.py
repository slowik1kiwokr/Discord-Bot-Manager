import os
import importlib.util
from tkinter import messagebox

import customtkinter as ctk

import modules.config as config
from modules.config import PLUGINS_DIR
from modules.languages import LANGUAGES
les.languages import LANGUAGES


class WindowPluginsMixin:
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
                self.log_event("ERROR", "Plugin betöltési hiba (%s): %s" % (filename, error))

    def open_plugins_window(self):
        win = ctk.CTkToplevel(self)
        win.title(self.tr("plugins"))
        win.geometry("520x380")
        ctk.CTkLabel(win, text=self.tr("plugins_help"), wraplength=470).pack(pady=12)
        box = ctk.CTkTextbox(win, height=180)
        box.pack(fill="both", expand=True, padx=12, pady=8)
        box.insert("1.0", "\n".join(self.plugins) or "Nincs betöltött plugin.")
        box.configure(state="disabled")
        def create_plugin():
            os.makedirs(PLUGINS_DIR, exist_ok=True)
            path = os.path.join(PLUGINS_DIR, "example_plugin.py")
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as plugin_file:
                    plugin_file.write("def setup_panel(panel):\n    panel.log_event('EVENT', 'Example plugin betöltve.')\n")
            self.load_plugins()
            win.destroy()
        ctk.CTkButton(win, text=self.tr("create_plugin"), command=create_plugin).pack(pady=10)