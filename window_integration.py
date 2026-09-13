import os
from tkinter import filedialog, messagebox

import customtkinter as ctk

import modules.config as config
from modules.languages import LANGUAGES
from modules.templates import (
    BOT_VEZERLO_CODE,
    PANEL_EXTENSION_CODE,
    VERSION_FILE_TEMPLATE,
    INFO_FILE_TEMPLATE,
)

class WindowIntegrationMixin:
    def open_alapok_window(self):
        win = ctk.CTkToplevel(self)
        win.title(self.tr("integration_title"))
        win.geometry("780x660")
        win.grab_set()

        ctk.CTkLabel(win, text=self.tr("integration_help"), font=("Arial", 16, "bold"), text_color="#8e44ad").pack(pady=(12, 5))

        ctk.CTkLabel(win, text=self.tr("integration_info"), justify="left", font=("Arial", 11)).pack(padx=15, anchor="w")

        tabview = ctk.CTkTabview(win, width=740, height=420)
        tabview.pack(padx=15, pady=10, fill="both", expand=True)
        
        tab_botpy = tabview.add(self.tr("integration_bot_template"))
        tab_vezerlo = tabview.add(self.tr("integration_panel_code"))
        tab_tutorial = tabview.add(self.tr("integration_tutorial"))

        box_bot = ctk.CTkTextbox(tab_botpy, font=("Consolas", 11), width=710, height=360)
        box_bot.pack(fill="both", expand=True, padx=5, pady=5)
        sablon_kod = (
            "# --- SABLON A SAJÁT BOT.PY FÁJLODHOZ ---\n"
            "import discord\n"
            "from discord.ext import commands\n\n"
            "from version import BOT_NAME, BOT_VERSION, BOT_TOKEN\n"
            "from info import BOT_INFO\n\n"
            "CURRENT_PREFIX = \"/\"\n\n"
            "async def get_prefix(bot, message):\n"
            "    return CURRENT_PREFIX\n\n"
            "intents = discord.Intents.default()\n"
            "intents.message_content = True\n\n"
            "bot = commands.Bot(command_prefix=get_prefix, intents=intents)\n\n"
            "@bot.event\n"
            "async def on_ready():\n"
            "    print(f'{BOT_NAME} v{BOT_VERSION} bejelentkezve: {bot.user}')\n"
            "    try:\n"
            "        await bot.load_extension('Panel')\n"
            "        await bot.tree.sync()\n"
            "        print('Panel integráció sikeresen betöltve.')\n"
            "    except Exception as e:\n"
            "        print(f'Hiba a vezérlő betöltésekor: {{e}}')\n\n"
            "@bot.command(name='teszt', aliases=['test'])\n"
            "async def teszt_parancs(ctx):\n"
            "    embed = discord.Embed(title=BOT_NAME, description=f'✅ A bot működik! Verzió: {BOT_VERSION}', color=discord.Color.green())\n"
            "    await ctx.send(embed=embed)\n"
            "\n"
            "@bot.command(name='parancsok', aliases=['menu'])\n"
            "async def parancsok_menu(ctx):\n"
            "    embed = discord.Embed(title='🤖 Parancsok', color=discord.Color.blue())\n"
            "    embed.add_field(name='/teszt', value='Bot tesztelése', inline=False)\n"
            "    embed.add_field(name='/parancsok', value='Ez a menü', inline=False)\n"
            "    embed.set_footer(text=f'Verzió: {BOT_VERSION}')\n"
            "    await ctx.send(embed=embed)\n"
            "\n"
            "bot.run(BOT_TOKEN)\n"
        )
        box_bot.insert("1.0", sablon_kod)
        box_bot.configure(state="disabled")

        box_vezerlo = ctk.CTkTextbox(tab_vezerlo, font=("Consolas", 11), width=710, height=360)
        box_vezerlo.pack(fill="both", expand=True, padx=5, pady=5)
        box_vezerlo.insert("1.0", BOT_VEZERLO_CODE)
        box_vezerlo.configure(state="disabled")

        ctk.CTkLabel(tab_tutorial, text=self.tr("tutorial_text"), justify="left", anchor="w").pack(fill="x", padx=12, pady=12)
        dependency_output = ctk.CTkTextbox(tab_tutorial, height=150, font=("Consolas", 10))
        dependency_output.pack(fill="both", expand=True, padx=12, pady=8)
        ctk.CTkButton(tab_tutorial, text=self.tr("install_dependencies"), command=lambda: self.install_panel_dependencies(dependency_output)).pack(anchor="w", padx=12, pady=8)

        def save_bot_vezerlo_file():
            script_path = self.entry_path.get().strip()
            if not script_path or not os.path.exists(script_path):
                messagebox.showwarning(self.tr("error_counter"), self.tr("choose_bot_file"), parent=win)
                return
            
            bot_dir = os.path.dirname(script_path)
            target_path = os.path.join(bot_dir, "bot_vezerlo.py")
            try:
                with open(target_path, "w", encoding="utf-8") as target_file:
                    target_file.write(BOT_VEZERLO_CODE)
                with open(os.path.join(bot_dir, "version.py"), "a", encoding="utf-8") as version_file:
                    if os.path.getsize(version_file.name) == 0:
                        version_file.write(VERSION_FILE_TEMPLATE)
                with open(os.path.join(bot_dir, "info.py"), "w", encoding="utf-8") as info_file:
                    info_file.write(INFO_FILE_TEMPLATE)
                messagebox.showinfo(self.tr("success"), f"{self.tr('saved_controller')}\n{bot_dir}", parent=win)
            except Exception as e:
                messagebox.showerror(self.tr("errors"), f"{self.tr('save_failed')}\n{e}", parent=win)

        def save_panel_extension():
            script_path = self.entry_path.get().strip()
            if not script_path or not os.path.exists(script_path):
                messagebox.showwarning(self.tr("error_counter"), self.tr("choose_bot_file"), parent=win)
                return
            bot_dir = os.path.dirname(script_path)
            try:
                with open(os.path.join(bot_dir, "Panel.py"), "w", encoding="utf-8") as panel_file:
                    panel_file.write(PANEL_EXTENSION_CODE)
                messagebox.showinfo(self.tr("success"), f"{self.tr('saved_panel')}\n{bot_dir}", parent=win)
            except OSError as error:
                messagebox.showerror(self.tr("errors"), f"{self.tr('save_failed')}\n{error}", parent=win)

        def choose_generation_folder():
            folder = filedialog.askdirectory(parent=win, title=self.tr("choose_bot_file"))
            return folder

        def save_generated_files():
            target_dir = choose_generation_folder()
            if not target_dir:
                return
            try:
                with open(os.path.join(target_dir, "bot.py"), "w", encoding="utf-8") as target_file:
                    target_file.write(sablon_kod)
                with open(os.path.join(target_dir, "bot_vezerlo.py"), "w", encoding="utf-8") as target_file:
                    target_file.write(BOT_VEZERLO_CODE)
                with open(os.path.join(target_dir, "Panel.py"), "w", encoding="utf-8") as panel_file:
                    panel_file.write(PANEL_EXTENSION_CODE)
                with open(os.path.join(target_dir, "version.py"), "w", encoding="utf-8") as version_file:
                    version_file.write(VERSION_FILE_TEMPLATE)
                with open(os.path.join(target_dir, "info.py"), "w", encoding="utf-8") as info_file:
                    info_file.write(INFO_FILE_TEMPLATE)
                messagebox.showinfo(self.tr("success"), f"{self.tr('generated_files')}\n{target_dir}", parent=win)
            except OSError as error:
                messagebox.showerror(self.tr("errors"), f"{self.tr('generation_failed')}\n{error}", parent=win)

        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(btn_frame, text=self.tr("save_controller"), fg_color="#27ae60", hover_color="#2ecc71", command=save_bot_vezerlo_file).pack(side="left", padx=5)
        self.btn_integrate_panel = ctk.CTkButton(btn_frame, text=self.tr("integrate_panel"), fg_color="#16a085", hover_color="#1abc9c", command=save_panel_extension)
        self.btn_integrate_panel.pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=self.tr("generate_template"), fg_color="#2980b9", hover_color="#3498db", command=save_generated_files).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=self.tr("close"), fg_color="#555555", command=win.destroy).pack(side="right", padx=5)
