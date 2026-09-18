# --- BOT MANAGER PANEL (Moduláris változat) ---
import os
import sys
import time
import threading
import psutil
import sqlite3
import ast
import logging
import datetime
import json
import uuid
import secrets
import importlib.util
import re
import webbrowser
import winsound
import ctypes
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import zipfile
import customtkinter as ctk
import pystray
from PIL import Image, ImageDraw
from version import version

# --- SAJÁT MODULOK ---
import modules.config as config
from modules.config import (
    SCRIPT_DIR, BOTS_FILE, SETTINGS_FILE, LANG_FILE,
    REMOTE_COMMANDS_FILE, REMOTE_RESPONSES_DIR,
    BROADCAST_REQUESTS_FILE, BACKUP_DIR, DISCORD_ICON_PATH,
    PLUGINS_DIR, LOG_DIR,
)
from modules.splash import SplashScreen
from modules.languages import LANGUAGES
from modules.templates import (
    VERSION_FILE_TEMPLATE,
    BOT_PY_TEMPLATE,
    PANEL_INTEGRITY_CODE,
)
from modules import logger  # logging beállítás mellékhatásként

# --- MIXINEK ---
from modules.mixins.window_activity import WindowActivityMixin
from modules.mixins.window_backup import WindowBackupMixin
from modules.mixins.window_bot_info import WindowBotInfoMixin
from modules.mixins.window_broadcast import WindowBroadcastMixin
from modules.mixins.window_github_update import WindowGithubMixin
from modules.mixins.window_integration import WindowIntegrationMixin
from modules.mixins.window_plugins import WindowPluginsMixin
from modules.mixins.window_servers import WindowServersMixin
from modules.mixins.window_settings import WindowSettingsMixin
from modules.mixins.window_sqlite import WindowSqliteMixin
from modules.mixins.window_stats import WindowStatsMixin
from modules.mixins.window_tutorial import WindowTutorialMixin
from modules.mixins.window_commander import WindowCommanderMixin
from modules.mixins.hotkeys import HotkeysMixin
from modules.mixins.ui_extras import UIExtrasMixin
from modules.mixins.window_report import WindowReportMixin
from modules.mixins.ui_enhancements import UIEnhancementsMixin
from modules.mixins.dashboard_widgets import DashboardWidgetsMixin
from modules.mixins.animated_charts import AnimatedChartsMixin
from modules.mixins.panel_stats import PanelStatsMixin
from modules.mixins.ai_assistant import AIAssistantMixin
from modules.mixins.achievements import AchievementsMixin
from modules.mixins.streak import StreakMixin
from modules.mixins.afk_screen import AfkScreenMixin
from modules.mixins.lan_server import LANServerMixin
from modules.mixins.lan_client import LANClientMixin
from modules.mixins.bot_startup_animation import BotStartupAnimationMixin
from modules.theme import (
    THEMES,
    DEFAULT_THEME,
    get_theme_names,
    get_theme,
    get_theme_colors,
    get_appearance_mode,
    get_default_color_theme,
)

# Matplotlib
try:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    MATPLOTLIB_ERROR = "A matplotlib csomag nem tölthető be."

# pypresence
try:
    from pypresence import Presence
    RPC_AVAILABLE = True
except ImportError:
    RPC_AVAILABLE = False

# Windows AppUserModelID
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "discord.bot.manager.panel.v2"
    )
except Exception:
    pass

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class BotManagerApp(
    WindowActivityMixin,
    WindowBackupMixin,
    WindowBotInfoMixin,
    WindowBroadcastMixin,
    WindowCommanderMixin,
    WindowGithubMixin,
    WindowIntegrationMixin,
    WindowPluginsMixin,
    WindowServersMixin,
    WindowSettingsMixin,
    WindowSqliteMixin,
    WindowStatsMixin,
    WindowTutorialMixin,
    WindowReportMixin,
    HotkeysMixin,
    UIExtrasMixin,
    UIEnhancementsMixin,
    DashboardWidgetsMixin,
    AnimatedChartsMixin,
    PanelStatsMixin,
    AIAssistantMixin,
    AchievementsMixin,
    StreakMixin,
    AfkScreenMixin,
    BotStartupAnimationMixin,
    LANServerMixin,       
    LANClientMixin,  
    ctk.CTk,
):
    def __init__(self):
        super().__init__()
        self.withdraw()

        # --- Splash létrehozása a panel Tk-jából (Toplevel) ---
        from modules.splash import SplashScreen
        try:
            self._splash = SplashScreen(self)
            self._splash.update()
        except Exception as e:
            print(f"[SPLASH] Hiba: {e}")
            self._splash = None

        self.sidebar_collapsed_sections = set()
        self.current_language = "English"
        self.selected_error_sound = "beep"
        self.minimize_to_tray_enabled = True
        self.current_theme = "DBM (Alap)"
        self.custom_icon_path = ""
        self.panel_password = ""
        self.update_check_interval_minutes = 60
        self._update_check_after_id = None
        self.ai_provider = "OpenAI (GPT)"
        self.ai_api_key = ""
        self.ai_model = ""
        self.log_save_level = "all"
        self.max_ram_mb = 200
        self.task_kill_enabled = False
        self.rpc_enabled = True
        self.backup_enabled = True
        self.backup_on_start = False
        self.backup_interval_hours = 24
        self.backup_last_run = ""
        self.plugins = []
        self.temperature_text = "-"
        self.temperature_last_update = 0
        self.stat_card_headers = []
        self.dual_stat_headers = []
        self.init_dashboard_widgets()
        self.init_panel_stats()
        self.afk_enabled = True
        self.afk_idle_seconds = 60
        self.init_afk_screen(idle_seconds=self.afk_idle_seconds)
        self.skipped_version = ""
        self._bot_tooltip = None
        self._watermark_base_image = None
        self._watermark_current_image = None
        self._watermark_size = (200, 200)
        self._watermark_fade_id = None
        self._watermark_debounce_id = None
        self.log_watermark_label = None
        self._bot_tooltip_key = None
        self._bot_tooltip_after_id = None
        self.is_loading = True
        self.bots = {}
        self.active_bot_key = "Main Bot"
        # --- Csendes órák ---
        self.quiet_hours_enabled = False
        self.quiet_hours_start = "22:00"
        self.quiet_hours_end = "06:00"

        self.load_config()

        if self.panel_password:
            self.withdraw()
            if self.prompt_startup_password():
                self.after(50, self.deiconify)
            else:
                sys.exit(0)

        self.apply_theme_setting(self.current_theme)
        self.apply_window_icon()

        self.title(self.tr("panel_title"))

        # Igazodás a képernyőhöz
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        win_w = min(1280, screen_w - 60)
        win_h = min(800, screen_h - 80)
        pos_x = max(0, (screen_w - win_w) // 2)
        pos_y = max(0, (screen_h - win_h) // 2)

        self.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
        self.minsize(1000, 620)

        self.protocol('WM_DELETE_WINDOW', self.on_window_close)

        self._build_tabs()
        self._build_sidebar()
        self._build_main_content()

        self.switch_bot(self.active_bot_key)
        self.is_loading = False
        self.save_config()

        self.render_tabs()
        self.update_stats_loop()

        self.is_monitoring = True
        threading.Thread(target=self.resource_monitor_loop, daemon=True).start()
        self.init_discord_rpc()
        self.load_plugins()
        threading.Thread(target=self.temperature_monitor_loop, daemon=True).start()

        self.after(1500, self.check_and_run_autostarts)
        self.after(3000, self.check_scheduled_backup)
        self.after(500, self.process_remote_commands)

        if getattr(self, "update_check_interval_minutes", 60) > 0:
            self.after(2000, lambda: self.schedule_update_check(
                interval_minutes=self.update_check_interval_minutes
            ))

        self.init_toast_system()
        self.init_collapsible_sidebar()
        self.init_animated_status()
        self.register_hotkeys()
        self.init_monthly_report()
        self.init_ui_enhancements()
        self.enable_scroll_support()
        self.init_achievements()
        self.init_streak()
        self._ui_built = True
        self.log_event("INFO", self.tr("panel_started_log"))
        self.notify(self.tr("toast_panel_started"), "success", 3000)
                # --- LAN szerver + kliens ---
        self.init_lan_server()
        self.init_lan_client()
        self._setup_done = True

    def prompt_startup_password(self):
        pwd_win = ctk.CTkToplevel(self)
        pwd_win.title(self.tr("password_title"))
        pwd_win.geometry("380x260")
        pwd_win.resizable(False, False)
        pwd_win.grab_set()

        pwd_win.update_idletasks()
        x = (pwd_win.winfo_screenwidth() - 380) // 2
        y = (pwd_win.winfo_screenheight() - 260) // 2
        pwd_win.geometry(f"380x260+{x}+{y}")

        def on_close():
            try:
                pwd_win.destroy()
            except Exception:
                pass
            sys.exit(0)

        pwd_win.protocol("WM_DELETE_WINDOW", on_close)

        ctk.CTkLabel(pwd_win, text=self.tr("password_protection_lbl"),
                    font=("Arial", 16, "bold"), text_color="#5865F2").pack(pady=(20, 5))
        ctk.CTkLabel(pwd_win, text=self.tr("password_prompt"),
                    font=("Arial", 12)).pack(pady=(0, 10))

        pwd_in = ctk.CTkEntry(pwd_win, show="*", width=280,
                            placeholder_text=self.tr("password_ph"))
        pwd_in.pack(pady=5)

        error_label = ctk.CTkLabel(pwd_win, text="", text_color="#e74c3c",
                                    font=("Arial", 11))
        error_label.pack(pady=(0, 4))

        success = [False]

        def verify(event=None):
            entered = pwd_in.get().strip()
            expected = (self.panel_password or "").strip()
            if entered == expected:
                success[0] = True
                pwd_win.destroy()
            else:
                error_label.configure(text=self.tr("wrong_password_msg"))
                pwd_in.delete(0, "end")
                pwd_in.focus_set()

        pwd_in.bind("<Return>", verify)

        ctk.CTkButton(pwd_win, text=self.tr("login_btn"), fg_color="#27ae60",
                    hover_color="#2ecc71", width=280,
                    command=verify).pack(pady=10)

        def force_focus():
            try:
                pwd_win.lift()
                pwd_win.focus_force()
                pwd_in.focus_set()
            except Exception:
                pass

        pwd_win.after(100, force_focus)
        pwd_win.after(400, force_focus)

        self.wait_window(pwd_win)
        return success[0]

    # ---------- LOG & AUDIT ----------

    def log_event(self, level, message):
        should_log = False
        if self.log_save_level == "all":
            should_log = True
        elif self.log_save_level == "errors" and level == "ERROR":
            should_log = True
        elif self.log_save_level == "events" and level == "EVENT":
            should_log = True
        elif self.log_save_level == "success" and level == "SUCCESS":
            should_log = True

        if should_log:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_line = f"{timestamp} [{level}] {message}\n"
            try:
                with open(config.LOG_FILE_PATH, "a", encoding="utf-8") as f:
                    f.write(log_line)
            except Exception as e:
                print(f"[LOG] Írási hiba: {e}")

    def audit_remote_action(self, user, source, action, result):
        audit_entry = {
            "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
            "user": user,
            "source": source,
            "action": action,
            "result": result,
            "panel_id": config.PANEL_ID
        }
        audit_path = os.path.join(LOG_DIR, "audit_log.jsonl")
        try:
            with open(audit_path, "a", encoding="utf-8") as audit_file:
                audit_file.write(json.dumps(audit_entry, ensure_ascii=False) + "\n")
            self.log_event("EVENT", f"[AUDIT] {user} ({source}) -> {action}: {result}")
        except Exception as error:
            self.log_event("ERROR", f"Audit naplózási hiba: {error}")

    def process_remote_commands(self):
        commands = []
        if os.path.exists(REMOTE_COMMANDS_FILE):
            try:
                with open(REMOTE_COMMANDS_FILE, "r", encoding="utf-8") as command_file:
                    commands = json.load(command_file)
                with open(REMOTE_COMMANDS_FILE, "w", encoding="utf-8") as command_file:
                    json.dump([], command_file)
            except (OSError, json.JSONDecodeError):
                commands = []

        for request in commands:
            response = self.execute_remote_command(request)
            response_path = os.path.join(REMOTE_RESPONSES_DIR, f"{request.get('id', uuid.uuid4().hex)}.json")
            try:
                with open(response_path, "w", encoding="utf-8") as response_file:
                    json.dump(response, response_file, ensure_ascii=False)
            except OSError as error:
                self.log_event("ERROR", f"Távoli válasz mentési hiba: {error}")
        self.after(500, self.process_remote_commands)

    def execute_remote_command(self, request):
        action = request.get("action", "").lower()
        user = request.get("user", "ismeretlen")
        source = request.get("source", "Discord")
        bot_key = request.get("bot", self.active_bot_key)
        if bot_key not in self.bots:
            result = f"Ismeretlen bot: {bot_key}"
            self.audit_remote_action(user, source, action, result)
            return {"ok": False, "message": result}

        previous_bot = self.active_bot_key
        self.switch_bot(bot_key)
        try:
            if action == "start":
                self.start_bot()
                result = f"{bot_key} indítási parancsa kiadva."
            elif action == "stop":
                self.stop_bot()
                result = f"{bot_key} leállítási parancsa kiadva."
            elif action == "restart":
                self.restart_bot()
                result = f"{bot_key} újraindítási parancsa kiadva."
            elif action == "stressz":
                result = f"Stresszteszt ellenőrzés kész: fut={self.bots[bot_key]['is_running']}, rendszer CPU={psutil.cpu_percent(interval=0.2):.1f}%, hőmérséklet={self.get_temperature_text()}."
            elif action in ("status", "info"):
                result = self.remote_status_text(bot_key)
            elif action == "log":
                recent = self.bots[bot_key]["raw_logs"][-8:]
                result = "\n".join(f"[{entry['time']}] {entry['type']}: {entry['msg']}" for entry in recent) or "Nincs naplóbejegyzés."
            elif action == "broadcast":
                result = "A broadcastot a BotVezerlo hajtja végre."
                return {"ok": True, "action": "broadcast", "data": request.get("data", {}), "message": result}
            else:
                result = "Ismeretlen parancs. Használható: start, stop, restart, info, status, stressz, log."
                self.audit_remote_action(user, source, action, result)
                return {"ok": False, "message": result}
            self.audit_remote_action(user, source, action, result)
            return {"ok": True, "message": result}
        finally:
            self.switch_bot(previous_bot)

    def remote_status_text(self, bot_key):
        bot = self.bots[bot_key]
        temperature = self.get_temperature_text()
        ram = "n/a"
        cpu = "n/a"
        if bot["is_running"] and bot["process"]:
            try:
                process = psutil.Process(bot["process"].pid)
                ram = f"{process.memory_info().rss / (1024 * 1024):.1f} MB"
                cpu = f"{process.cpu_percent(interval=None):.1f}%"
            except psutil.Error:
                pass
        return f"Panel {config.PANEL_ID} | {bot_key}: {'ONLINE' if bot['is_running'] else 'OFFLINE'} | RAM {ram} | CPU {cpu} | Hőmérséklet {temperature}"

    # ---------- HŐMÉRSÉKLET ----------

    def get_temperature_text(self):
        return self.temperature_text

    def read_temperature(self):
        try:
            sensors = psutil.sensors_temperatures()
            if sensors:
                values = [r.current for entries in sensors.values()
                        for r in entries if r.current is not None]
                if values:
                    return f"{max(values):.1f} C"
        except (AttributeError, OSError):
            pass

        if os.name != "nt":
            return self.tr("unavailable")

        for namespace in ("root/OpenHardwareMonitor", "root/LibreHardwareMonitor"):
            try:
                result = subprocess.run(
                    ["powershell", "-NoProfile", "-Command",
                    f"Get-CimInstance -Namespace {namespace} -ClassName Sensor "
                    f"| Where-Object {{ $_.SensorType -eq 'Temperature' -and $_.Name -like '*CPU*' }} "
                    f"| Select-Object -First 1 -ExpandProperty Value"],
                    capture_output=True, text=True, timeout=3,
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
                )
                out = result.stdout.strip().replace(",", ".")
                if out and out.replace(".", "").isdigit():
                    return f"{float(out):.1f} C"
            except (OSError, subprocess.SubprocessError, ValueError):
                pass

        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                "Get-CimInstance -Namespace root/wmi -ClassName MSAcpi_ThermalZoneTemperature "
                "| Select-Object -ExpandProperty CurrentTemperature"],
                capture_output=True, text=True, timeout=3,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )
            temperatures = []
            for line in result.stdout.splitlines():
                line = line.strip()
                if line.isdigit():
                    temperatures.append((int(line) / 10) - 273.15)
            if temperatures:
                return f"{max(temperatures):.1f} C"
        except (OSError, subprocess.SubprocessError, ValueError):
            pass

        try:
            import wmi
            w = wmi.WMI(namespace="root\\wmi")
            temps = w.MSAcpi_ThermalZoneTemperature()
            if temps:
                values = [(t.CurrentTemperature / 10) - 273.15 for t in temps]
                return f"{max(values):.1f} C"
        except ImportError:
            pass
        except Exception:
            pass

        try:
            cpu = psutil.cpu_percent(interval=0.3)
            return f"CPU: {cpu:.0f}%"
        except Exception:
            return self.tr("unavailable")

    def temperature_monitor_loop(self):
        while getattr(self, "is_monitoring", True):
            try:
                value = self.read_temperature()
                self.after(0, self.update_temperature_value, value)
            except Exception:
                pass
            time.sleep(30)

    def update_temperature_value(self, value):
        self.temperature_text = value
        if hasattr(self, "lbl_temperature"):
            self.lbl_temperature.configure(text=value)

    # ---------- PANEL PARANCS ----------

    def copy_panel_connect_command(self):
        command = f"/connect panel_id:{config.PANEL_ID} device:PC"
        self.clipboard_clear()
        self.clipboard_append(command)
        self.update()
        messagebox.showinfo(self.tr("copied_msg"), command)

    # ---------- FORDÍTÁS ----------

    def tr(self, key, **kwargs):
        """Szöveg lekérése a jelenlegi nyelven, helyettesítőkkel."""
        language = LANGUAGES.get(self.current_language, LANGUAGES.get("English", {}))
        text = language.get(key, LANGUAGES.get("English", {}).get(key, key))
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, IndexError):
                pass
        return text.replace("{version}", version)

    def apply_language(self, language):
        if language not in LANGUAGES:
            return
        self.current_language = language
        if hasattr(self, "sidebar"):
            self.update_ui_texts()

    # ---------- TÉMA & IKON ----------

    def apply_theme_setting(self, theme_name):
        try:
            from modules.theme import (
                THEMES, DEFAULT_THEME,
                get_theme_colors, get_appearance_mode, get_default_color_theme,
            )
        except ImportError:
            print("[THEME] Hiba: a modules/theme.py nem található!")
            return

        if theme_name not in THEMES:
            theme_name = DEFAULT_THEME

        self.current_theme = theme_name

        ctk.set_appearance_mode(get_appearance_mode(theme_name))
        ctk.set_default_color_theme(get_default_color_theme(theme_name))

        self.theme_colors = get_theme_colors(theme_name)

        try:
            self.configure(fg_color=self.theme_colors.get("bg_main", "#0f1420"))
        except Exception:
            pass

        if hasattr(self, "sidebar") and getattr(self, "_ui_built", False):
            try:
                self.after(50, self._rebuild_ui_for_theme)
            except Exception as e:
                print(f"[THEME] Rebuild ütemezés hiba: {e}")

        try:
            self.after(50, self._apply_log_styling)
        except Exception:
            pass

    def _apply_log_styling(self):
        if hasattr(self, "log_textbox"):
            try:
                self.log_textbox.configure(
                    fg_color=self.theme_colors.get("log_bg", "#131720"),
                    border_width=1,
                    border_color=self.theme_colors.get("log_border", "#5865F2"),
                )
            except Exception:
                pass

        if hasattr(self, "log_watermark_label") and self.log_watermark_label is not None:
            try:
                self.log_watermark_label.configure(
                    fg_color=self.theme_colors.get("log_bg", "#131720"),
                )
            except Exception:
                pass

        if hasattr(self, "log_container"):
            try:
                self.log_container.configure(
                    fg_color=self.theme_colors.get("card_bg", "#1e2330"),
                    border_width=1,
                    border_color=self.theme_colors.get("border", "#3a4258"),
                )
            except Exception:
                pass

        if hasattr(self, "settings_box"):
            try:
                self.settings_box.configure(
                    fg_color=self.theme_colors.get("settings_box_bg", "#1e2330"),
                    border_width=1,
                    border_color=self.theme_colors.get("border", "#3a4258"),
                )
            except Exception:
                pass

        if hasattr(self, "stats_panel"):
            try:
                self.stats_panel.configure(
                    fg_color=self.theme_colors.get("bg_main", "#0f1420"),
                )
            except Exception:
                pass

        if hasattr(self, "main_frame"):
            try:
                self.main_frame.configure(
                    fg_color=self.theme_colors.get("bg_main", "#0f1420"),
                )
            except Exception:
                pass

        if hasattr(self, "top_tab_frame"):
            try:
                self.top_tab_frame.configure(
                    fg_color=self.theme_colors.get("top_tab_bg", "#131720"),
                )
            except Exception:
                pass

        if hasattr(self, "sidebar"):
            try:
                self.sidebar.configure(
                    fg_color=self.theme_colors.get("sidebar_bg", "#131720"),
                )
            except Exception:
                pass

    def _rebuild_ui_for_theme(self):
        try:
            self.is_loading = True

            for attr in ("top_tab_frame", "sidebar", "main_frame"):
                w = getattr(self, attr, None)
                if w is not None:
                    try:
                        w.destroy()
                    except Exception:
                        pass

            self.stat_card_headers = []
            self.dual_stat_headers = []
            self.stats_section_labels = []

            self._build_tabs()
            self._build_sidebar()
            self._build_main_content()
            self.render_tabs()
            self.switch_bot(self.active_bot_key)

            self.update_ui_texts()

            self.is_loading = False

            try:
                self.notify(self.tr("toast_theme_changed", name=self.current_theme),
                            "success", 2000)
            except Exception:
                pass

            self.log_event("EVENT", f"[THEME] Új téma alkalmazva: {self.current_theme}")
            self._apply_log_styling()

        except Exception as e:
            self.is_loading = False
            print(f"[THEME] Rebuild hiba: {e}")
            import traceback
            traceback.print_exc()

    def apply_window_icon(self):
        if os.path.isfile(DISCORD_ICON_PATH):
            try:
                self.iconbitmap(DISCORD_ICON_PATH)
                return
            except Exception:
                pass
        if self.custom_icon_path and os.path.exists(self.custom_icon_path):
            try:
                self.iconbitmap(self.custom_icon_path)
                return
            except Exception:
                pass

        try:
            temp_icon_path = os.path.join(SCRIPT_DIR, "temp_app_icon.ico")
            if not os.path.exists(temp_icon_path):
                img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
                d = ImageDraw.Draw(img)
                d.rounded_rectangle([4, 4, 60, 60], radius=14, fill=(88, 101, 242))
                d.ellipse([20, 20, 44, 44], fill=(255, 255, 255))
                img.save(temp_icon_path, format='ICO', sizes=[(64, 64), (32, 32), (16, 16)])
            self.iconbitmap(temp_icon_path)
        except Exception:
            pass

    # ---------- UI ÉPÍTÉS ----------

    def _build_tabs(self):
        self.top_tab_frame = ctk.CTkFrame(
        self, height=40, corner_radius=0, fg_color=self.theme_colors.get("sidebar_bg", "#2b2b2b"))
        self.top_tab_frame.pack(side="top", fill="x")

        self.tab_buttons_frame = ctk.CTkFrame(self.top_tab_frame, fg_color="transparent")
        self.tab_buttons_frame.pack(side="left", fill="x")

        self.btn_add_bot = ctk.CTkButton(self.top_tab_frame, text="+", width=30, fg_color="#2b2b2b", command=self.add_bot_dialog)
        self.btn_add_bot.pack(side="left", padx=5, pady=5)

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, width=270, corner_radius=0,
            fg_color=self.theme_colors["sidebar_bg"]
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # ---------- Státuszjelző ----------
        self.lbl_status = ctk.CTkLabel(
            self.sidebar, text=self.tr("offline_status"),
            text_color="#e74c3c", font=("Arial", 14, "bold")
        )
        self.lbl_status.pack(padx=20, pady=(18, 10))

        # ---------- Görgethető menü ----------
        self.sidebar_menu = ctk.CTkScrollableFrame(
            self.sidebar, fg_color="transparent", corner_radius=0
        )
        self.sidebar_menu.pack(fill="both", expand=True, padx=2, pady=(0, 4))
        menu = self.sidebar_menu

        def make_section(title_key, accent="#0064D6", bg_tint="#1e2129", section_id=None):
            """Lenyitható szekció kártya. Visszaadja a TARTALOM frame-et."""
            #bot vezérlő
            card = ctk.CTkFrame(
                menu,
                fg_color=bg_tint,
                corner_radius=10,
                border_width=2,
                border_color=accent,
            )
            card.pack(fill="x", padx=6, pady=(8, 4))


            # --- Fejléc (kattintható) ---
            header = ctk.CTkFrame(card, fg_color="transparent", cursor="hand2")
            header.pack(fill="x", padx=8, pady=(8, 4))

            # Nyíl
            arrow_lbl = ctk.CTkLabel(
                header, text="▼",
                font=("Arial", 10, "bold"),
                text_color=accent,
                width=18,
                cursor="hand2",
            )
            arrow_lbl.pack(side="left", padx=(2, 4))

            # Cím
            title_lbl = ctk.CTkLabel(
                header,
                text=self.tr(title_key).upper(),
                font=("Arial", 9, "bold"),
                text_color=accent,
                anchor="w",
                cursor="hand2",
            )
            title_lbl.pack(side="left", fill="x", expand=True)

            # --- Tartalom ---
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="x", padx=4, pady=(0, 6))

            # --- Állapot ---
            collapsed = (
                section_id is not None
                and section_id in getattr(self, "sidebar_collapsed_sections", set())
            )

            state = {"collapsed": collapsed}

            def apply_state():
                if state["collapsed"]:
                    content.pack_forget()
                    arrow_lbl.configure(text="▶")
                else:
                    content.pack(fill="x", padx=4, pady=(0, 6))
                    arrow_lbl.configure(text="▼")

            def toggle(event=None):
                state["collapsed"] = not state["collapsed"]
                apply_state()

                # Mentés
                if section_id is not None:
                    if not hasattr(self, "sidebar_collapsed_sections"):
                        self.sidebar_collapsed_sections = set()
                    if state["collapsed"]:
                        self.sidebar_collapsed_sections.add(section_id)
                    else:
                        self.sidebar_collapsed_sections.discard(section_id)
                    try:
                        self.save_config()
                    except Exception:
                        pass

            # Kattintás kötések
            header.bind("<Button-1>", toggle)
            arrow_lbl.bind("<Button-1>", toggle)
            title_lbl.bind("<Button-1>", toggle)

            # Hover effekt
            def on_enter(e):
                try:
                    header.configure(fg_color="#2a2f3a")
                except Exception:
                    pass

            def on_leave(e):
                try:
                    header.configure(fg_color="transparent")
                except Exception:
                    pass

            header.bind("<Enter>", on_enter, add="+")
            header.bind("<Leave>", on_leave, add="+")

            # Kezdeti állapot
            apply_state()

            return content

        def nav_btn(parent, text, command, active=False, color=None, hover=None):
            if color:
                fg = color
                hv = hover or color
            elif active:
                fg = "#5865F2"
                hv = "#4752C4"
            else:
                fg = "transparent"
                hv = "#3a4155"

            b = ctk.CTkButton(
                parent, text=text, command=command, height=34,
                fg_color=fg,
                hover_color=hv,
                anchor="w",
                font=("Arial", 12),
                corner_radius=6,
                text_color="white",
            )
            b.pack(fill="x", padx=8, pady=1)
            return b

        def action_btn(parent, text, command, color):
            b = ctk.CTkButton(
                parent, text=text, command=command, height=34,
                fg_color=color, hover_color=color,
                anchor="w", font=("Arial", 12, "bold"),
                corner_radius=6,
            )
            b.pack(fill="x", padx=8, pady=2)
            return b

        def spacer(parent, h=4):
            ctk.CTkFrame(parent, height=h, fg_color="transparent").pack()

        # ============================================================
        #  VEZÉRLÉS
        # ============================================================
        card = make_section("control_section", accent="#03f70f", bg_tint="#0f1a24", section_id="control")
        self.btn_start = action_btn(card, "▶️   " + self.tr("bot_start_btn"), self.start_bot, "#27ae60")
        self.btn_restart = action_btn(card, "🔄   " + self.tr("bot_restart_btn"), self.restart_bot, "#d35400")
        self.btn_stop = action_btn(card, "⏸️   " + self.tr("bot_stop_btn"), self.stop_bot, "#c0392b")
        spacer(card, 6)

        # ============================================================
        #  TÖMEGES VEZÉRLÉS
        # ============================================================
        card = make_section("bulk_control_section", accent="#ca0303", bg_tint="#0f1a24", section_id="bulk_control")
        self.btn_start_all = nav_btn(card, "▶️   " + self.tr("start_all_btn"), self.start_all_bots, color="#27ae60")
        self.btn_restart_all = nav_btn(card, "🔄   " + self.tr("restart_all_btn"), self.restart_all_bots, color="#d35400")
        self.btn_stop_all = nav_btn(card, "⏸️   " + self.tr("stop_all_btn"), self.stop_all_bots, color="#c0392b")
        spacer(card, 6)

        # ============================================================
        #  BOT MANAGE
        # ============================================================
        card = make_section("bot_manage", accent="#b9fc02", bg_tint="#0f1a24", section_id="bot_manage")
        self.btn_commander = nav_btn(card, "🛠️  " + self.tr("commander_btn"), self.open_commander_window, color="#f39c12")
        self.btn_broadcast = nav_btn(card, "📢  " + self.tr("broadcast_btn"), self.open_broadcast_window, color="#cb4335")
        self.btn_backup = nav_btn(card, "💾  " + self.tr("backup_btn"), self.open_backup_manager, color="#9b59b6")
        self.btn_sqlite = nav_btn(card, "🗃️  " + self.tr("sqlite_btn"), self.open_sqlite_viewer, color="#795548")

        # ============================================================
        #  RENDSZER
        # ============================================================
        card = make_section("system_section", accent="#3498db", bg_tint="#0f1a24", section_id="system")
        self.btn_settings = nav_btn(card, "⚙️  " + self.tr("settings_btn"), self.open_settings_window_v2, active=True, color="#3498db")
        self.btn_tutorial = nav_btn(card, "🎓  " + self.tr("tutorial_btn"), self.open_tutorial_window, color="#e74c3c")
        self.btn_github_update = nav_btn(card, "🔄  " + self.tr("github_update_btn"), lambda: self.update_from_github("manual"), color="#2980b9")
        self.btn_lan_client = nav_btn(card, "🔗  " + self.tr("lan_client_btn"), self.open_lan_client_window, color="#16a085")
        spacer(card, 6)
        # ============================================================
        #  INTEGRÁCIÓ/panel
        # ============================================================
        card = make_section("tools_section", accent="#ffffff", bg_tint="#0f1a24", section_id="tools")
        self.btn_plugins = nav_btn(card, "🧩  " + self.tr("plugins_btn"), self.open_plugins_window, color="#8e44ad")
        self.btn_appearance = nav_btn(card, "🎨  " + self.tr("appearance_btn"), self.open_bot_appearance_editor, color="#bb8fce")
        self.btn_alapok = nav_btn(card, "🔗  " + self.tr("integration_btn"), self.open_alapok_window, color="#9b59b6")
        spacer(card, 6)

        # ============================================================
        #  STATISZTIKA
        # ============================================================
        card = make_section("stats_section", accent="#00ff80", bg_tint="#0f1a24", section_id="stats")
        self.btn_global_stats = nav_btn(card, "📈  " + self.tr("global_stats_btn"), self.open_global_stats_window, color="#2980b9")
        self.btn_dashboard = action_btn(card, "📐   " + self.tr("dashboard_widget_btn"), self.open_dashboard_window, "#5865F2")
        self.btn_animated = action_btn(card, "📈   " + self.tr("live_charts_btn"), self.open_animated_charts_window, "#e67e22")
        self.btn_panel_stats = action_btn(card, "📊   " + self.tr("panel_stats_btn"), self.open_panel_stats_window, "#8e44ad")
        self.btn_report = nav_btn(card, "📊  " + self.tr("monthly_report_btn"), self.open_monthly_report_window, color="#2ecc71")
        spacer(card, 6)


        # ============================================================
        #  AI FUNKCIOK
        # ============================================================
        card = make_section("ai_section", accent="#00bcd4", bg_tint="#0f1a24", section_id="ai")
        self.btn_ai_chat = action_btn(card, "🤖   " + self.tr("ai_assistant_btn"), self.open_ai_chat_window, "#5865F2")
        self.btn_ai_code = action_btn(card, "✨   " + self.tr("ai_code_gen_btn"), self.open_ai_code_generator, "#9b59b6")
        self.btn_ai_docs = action_btn(card, "📄   " + self.tr("ai_docs_btn"), self.open_ai_docs_generator, "#16a085")
        self.btn_achievements = action_btn(card, "🏆   " + self.tr("achievements_btn"), self.open_achievements_window, "#f39c12")
        spacer(card, 6)

        # ============================================================
        #  PANEL INFO KÁRTYA (NEM lenyitható!)
        # ============================================================
        info_card = ctk.CTkFrame(
            menu,
            fg_color="#1a1d26",
            corner_radius=10,
            border_width=1,
            border_color="#5865F2",
        )
        info_card.pack(fill="x", padx=6, pady=(10, 12))

        ctk.CTkLabel(
            info_card, text=self.tr("panel_id_lbl").upper(),
            font=("Arial", 9, "bold"),
            text_color="#7a8090",
            anchor="w",
        ).pack(fill="x", padx=12, pady=(10, 4))

        self.lbl_panel_id = ctk.CTkLabel(
            info_card,
            text=config.PANEL_ID,
            font=("Consolas", 12, "bold"),
            text_color="#5865F2",
            anchor="w",
        )
        self.lbl_panel_id.pack(fill="x", padx=12, pady=(0, 8))

        self.btn_copy_connect = ctk.CTkButton(
            info_card,
            text="📋  " + self.tr("copy_command_btn"),
            height=32, corner_radius=6,
            fg_color="#5865F2", hover_color="#4752C4",
            font=("Arial", 11, "bold"),
            command=self.copy_panel_connect_command,
        )
        self.btn_copy_connect.pack(fill="x", padx=10, pady=(0, 10))
        self.register_scrollable(self.sidebar_menu)

    def _build_main_content(self):
        self.main_frame = ctk.CTkFrame(
            self, corner_radius=0,
            fg_color=self.theme_colors.get("bg_main", "#0d0f14"),
        )
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # ============================================================
        #  FELSŐ SÁV — 3 KÁRTYA
        # ============================================================
        self.settings_box = ctk.CTkFrame(
            self.main_frame, fg_color="transparent",
        )
        self.settings_box.pack(fill="x", padx=10, pady=(10, 5))

        card_bg = self.theme_colors.get("card_bg", "#1e2330")

        def card_header(parent, icon, title, accent):
            header = ctk.CTkFrame(parent, fg_color="transparent")
            header.pack(fill="x", padx=14, pady=(10, 4))
            ctk.CTkLabel(
                header,
                text=f"{icon}   {title}",
                font=("Arial", 11, "bold"),
                text_color=accent,
                anchor="w",
            ).pack(side="left")
            ctk.CTkFrame(
                parent, height=1,
                fg_color=self.theme_colors.get("border", "#3a4258"),
            ).pack(fill="x", padx=12, pady=(0, 8))

        # ---------- 1. KÁRTYA — BOT FÁJLOK ----------
        self.card_files = ctk.CTkFrame(
            self.settings_box,
            fg_color=card_bg,
            corner_radius=10,
            border_width=2,
            border_color="#3498db",
        )
        self.card_files.pack(side="left", fill="both", expand=True, padx=(0, 5))

        card_header(self.card_files, "📁", self.tr("bot_files_section"), "#3498db")

        files_content = ctk.CTkFrame(self.card_files, fg_color="transparent")
        files_content.pack(fill="x", padx=14, pady=(0, 12))

        self.lbl_path_title = ctk.CTkLabel(
            files_content, text=self.tr("bot_file_lbl"),
            font=("Arial", 10),
            text_color=self.theme_colors.get("subtext", "#8a8e98"),
            anchor="w",
        )
        self.lbl_path_title.pack(fill="x", pady=(0, 2))

        self.entry_path = ctk.CTkEntry(
            files_content,
            placeholder_text=self.tr("bot_file_ph"),
            height=32,
        )
        self.entry_path.pack(fill="x", pady=(0, 6))

        self.lbl_env_status = ctk.CTkLabel(
            files_content,
            text=self.tr("env_na"),
            font=("Arial", 10, "bold"),
            text_color="#e74c3c",
            anchor="w",
        )
        self.lbl_env_status.pack(fill="x", pady=(0, 8))

        files_btns = ctk.CTkFrame(files_content, fg_color="transparent")
        files_btns.pack(fill="x")

        self.btn_save_path = ctk.CTkButton(
            files_btns, text="💾  " + self.tr("save_btn"),
            width=100, height=32,
            fg_color=self.theme_colors.get("save_btn", "#27ae60"),
            hover_color=self.theme_colors.get("save_hover", "#2ecc71"),
            font=("Arial", 11, "bold"),
            command=self.manual_save_path,
        )
        self.btn_save_path.pack(side="left", padx=(0, 4))

        self.btn_browse = ctk.CTkButton(
            files_btns, text="📂  " + self.tr("browse_btn"),
            width=110, height=32,
            fg_color="#3498db", hover_color="#5dade2",
            font=("Arial", 11, "bold"),
            command=self.browse_file,
        )
        self.btn_browse.pack(side="left", padx=4)

        # ---------- 2. KÁRTYA — PANEL VISELKEDÉS ----------
        self.card_behavior = ctk.CTkFrame(
            self.settings_box,
            fg_color=card_bg,
            corner_radius=10,
            border_width=2,
            border_color="#2ecc71",
        )
        self.card_behavior.pack(side="left", fill="both", expand=True, padx=5)

        card_header(self.card_behavior, "⚙️", self.tr("behavior_section"), "#2ecc71")

        behavior_content = ctk.CTkFrame(self.card_behavior, fg_color="transparent")
        behavior_content.pack(fill="x", padx=14, pady=(0, 12))

        self.autostart_var = ctk.BooleanVar(value=False)
        self.sound_var = ctk.BooleanVar(value=False)
        self.midnight_var = ctk.BooleanVar(value=False)

        self.chk_autostart = ctk.CTkSwitch(
            behavior_content, text="  " + self.tr("autostart_lbl"),
            variable=self.autostart_var,
            command=self.save_config,
            font=("Arial", 11),
        )
        self.chk_autostart.pack(anchor="w", pady=2)

        sound_row = ctk.CTkFrame(behavior_content, fg_color="transparent")
        sound_row.pack(fill="x", pady=2)
        self.chk_sound = ctk.CTkSwitch(
            sound_row, text="  " + self.tr("error_sound_lbl"),
            variable=self.sound_var,
            command=self.save_config,
            font=("Arial", 11),
        )
        self.chk_sound.pack(side="left")
        ctk.CTkLabel(sound_row, text="🔊", font=("Arial", 11)).pack(side="left", padx=(8, 2))
        self.slider_volume = ctk.CTkSlider(
            sound_row, from_=0, to=100, number_of_steps=10, width=80,
            command=lambda v: self.on_volume_change(),
        )
        self.slider_volume.pack(side="left")

        self.chk_midnight = ctk.CTkSwitch(
            behavior_content, text="  " + self.tr("midnight_restart_lbl"),
            variable=self.midnight_var,
            command=self.on_midnight_toggle,
            font=("Arial", 11),
        )
        self.chk_midnight.pack(anchor="w", pady=2)

        ctk.CTkLabel(
            behavior_content, text=self.tr("auto_restart_lbl"),
            font=("Arial", 10, "bold"),
            text_color=self.theme_colors.get("subtext", "#8a8e98"),
            anchor="w",
        ).pack(fill="x", pady=(8, 2))

        restart_row = ctk.CTkFrame(behavior_content, fg_color="transparent")
        restart_row.pack(fill="x")

        col1 = ctk.CTkFrame(restart_row, fg_color="transparent")
        col1.pack(side="left", padx=2)
        self.slider_r_days = ctk.CTkSlider(
            col1, from_=0, to=7, number_of_steps=7, width=60,
            command=lambda v: self.on_restart_slider_change(),
        )
        self.slider_r_days.pack()
        self.lbl_r_days = ctk.CTkLabel(col1, text="0" + self.tr("days_short"), font=("Arial", 9))
        self.lbl_r_days.pack()

        col2 = ctk.CTkFrame(restart_row, fg_color="transparent")
        col2.pack(side="left", padx=2)
        self.slider_r_hours = ctk.CTkSlider(
            col2, from_=0, to=24, number_of_steps=24, width=60,
            command=lambda v: self.on_restart_slider_change(),
        )
        self.slider_r_hours.pack()
        self.lbl_r_hours = ctk.CTkLabel(col2, text="0" + self.tr("hours_short"), font=("Arial", 9))
        self.lbl_r_hours.pack()

        col3 = ctk.CTkFrame(restart_row, fg_color="transparent")
        col3.pack(side="left", padx=2)
        self.slider_r_mins = ctk.CTkSlider(
            col3, from_=0, to=60, number_of_steps=60, width=60,
            command=lambda v: self.on_restart_slider_change(),
        )
        self.slider_r_mins.pack()
        self.lbl_r_mins = ctk.CTkLabel(col3, text="0" + self.tr("minutes_short"), font=("Arial", 9))
        self.lbl_r_mins.pack()

        # ---------- 3. KÁRTYA — BOT INFO ----------
        self.card_botinfo = ctk.CTkFrame(
            self.settings_box,
            fg_color=card_bg,
            corner_radius=10,
            border_width=2,
            border_color="#9b59b6",
        )
        self.card_botinfo.pack(side="left", fill="both", expand=True, padx=(5, 0))

        card_header(self.card_botinfo, "🤖", self.tr("bot_info_section"), "#9b59b6")

        botinfo_content = ctk.CTkFrame(self.card_botinfo, fg_color="transparent")
        botinfo_content.pack(fill="x", padx=14, pady=(0, 12))

        row1 = ctk.CTkFrame(botinfo_content, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 4))

        self.btn_servers = ctk.CTkButton(
            row1, text="🌐  " + self.tr("servers_btn"),
            height=32, fg_color="#16a085", hover_color="#1abc9c",
            font=("Arial", 11, "bold"),
            command=self.open_servers_window,
        )
        self.btn_servers.pack(side="left", fill="x", expand=True, padx=(0, 2))

        self.btn_bot_info = ctk.CTkButton(
            row1, text="🤖  " + self.tr("bot_data_btn"),
            height=32, fg_color="#8e44ad", hover_color="#9b59b6",
            font=("Arial", 11, "bold"),
            command=self.open_bot_info_editor,
        )
        self.btn_bot_info.pack(side="left", fill="x", expand=True, padx=2)

        self.btn_activity = ctk.CTkButton(
            botinfo_content, text="🎭  " + self.tr("activity_btn"),
            height=32, fg_color="#5865F2", hover_color="#4752C4",
            font=("Arial", 11, "bold"),
            command=self.open_activity_editor,
        )
        self.btn_activity.pack(fill="x", pady=4)

        self.test_mode_var = ctk.BooleanVar(value=False)
        self.chk_test_mode = ctk.CTkSwitch(
            botinfo_content, text="  " + self.tr("test_mode_lbl"),
            variable=self.test_mode_var,
            progress_color="#e67e22",
            command=self.on_test_mode_toggle,
            font=("Arial", 11),
        )
        self.chk_test_mode.pack(anchor="w", pady=(6, 0))

        self.middle_frame = ctk.CTkFrame(
            self.main_frame, fg_color="transparent",)
        self.middle_frame.pack(fill="both", expand=True, padx=0, pady=5)

        self.log_container = ctk.CTkFrame(
            self.middle_frame, fg_color=self.theme_colors.get("card_bg", "#1a1d24"), corner_radius=10, border_width=1, border_color=self.theme_colors.get("border", "#2f3542"), )
        self.log_container.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.log_header_frame = ctk.CTkFrame(self.log_container, fg_color="transparent")
        self.log_header_frame.pack(fill="x", padx=10, pady=(10, 0))

        self.lbl_logs_title = ctk.CTkLabel(self.log_header_frame, text=self.tr("live_logs_title"), font=("Arial", 14, "bold"))
        self.lbl_logs_title.pack(side="left")

        self.btn_filter_all = ctk.CTkButton(self.log_header_frame, text=self.tr("filter_all_btn"), width=60, command=lambda: self.filter_logs("ALL"))
        self.btn_filter_all.pack(side="left", padx=(10, 2))

        self.btn_filter_errors = ctk.CTkButton(self.log_header_frame, text=self.tr("filter_errors_btn"), width=70, fg_color="#c0392b", command=lambda: self.filter_logs("ERROR"))
        self.btn_filter_errors.pack(side="left", padx=2)

        self.btn_filter_success = ctk.CTkButton(self.log_header_frame, text=self.tr("filter_success_btn"), width=70, fg_color="#27ae60", command=lambda: self.filter_logs("SUCCESS"))
        self.btn_filter_success.pack(side="left", padx=2)

        self.btn_filter_events = ctk.CTkButton(self.log_header_frame, text=self.tr("filter_events_btn"), width=80, fg_color="#8e44ad", command=lambda: self.filter_logs("EVENT"))
        self.btn_filter_events.pack(side="left", padx=2)

        self.btn_clear = ctk.CTkButton(self.log_header_frame, text=self.tr("clear_logs_btn"), width=55, fg_color="#555555", command=self.clear_logs)
        self.btn_clear.pack(side="right", padx=5)

        self.chk_autoscroll = ctk.CTkCheckBox(self.log_header_frame, text=self.tr("autoscroll_lbl"))
        self.chk_autoscroll.pack(side="right", padx=5)
        self.chk_autoscroll.select()

        self.log_search_frame = ctk.CTkFrame(self.log_container, fg_color="transparent")
        self.log_search_frame.pack(fill="x", padx=10, pady=(5, 0))

        self.search_entry = ctk.CTkEntry(self.log_search_frame, placeholder_text=self.tr("log_search_ph"), font=("Arial", 12))
        self.search_entry.pack(fill="x", padx=0, pady=2)
        self.search_entry.bind("<KeyRelease>", lambda e: self.apply_log_search_and_filter())

        self.log_content_area = ctk.CTkFrame(
            self.log_container, fg_color="transparent",)
        self.log_content_area.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        self.log_textbox = ctk.CTkTextbox(
            self.log_content_area, font=("Consolas", 12), fg_color=self.theme_colors.get("log_bg", "#131720"), border_width=1, border_color=self.theme_colors.get("log_border", "#5865F2"), corner_radius=8,)
        self.log_textbox.pack(fill="both", expand=True)

        self.log_watermark_image = self._create_log_watermark_image()
        if self.log_watermark_image:
            self.log_watermark_label = ctk.CTkLabel(
                self.log_content_area,
                image=self.log_watermark_image,
                text="",
                fg_color=self.theme_colors.get("log_bg", "#131720"),
                corner_radius=0,
            )
            self.log_watermark_label.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.log_watermark_label = None

        self.stats_panel = ctk.CTkScrollableFrame(
            self.middle_frame,width=260, label_text=self.tr("metrics_section"), fg_color=self.theme_colors.get("bg_main", "#0d0f14"),)
        self.stats_panel.pack(side="right", fill="y", padx=(5, 0))

        self.btn_open_charts = ctk.CTkButton(self.stats_panel, text=self.tr("open_charts_btn"), fg_color="#e67e22", hover_color="#d35400", command=self.open_performance_charts_window)
        self.btn_open_charts.pack(fill="x", padx=5, pady=(2, 8))

        self.stats_section_labels = []
        bot_info_label = ctk.CTkLabel(self.stats_panel, text=self.tr("bot_information_section"), font=("Arial", 12, "bold"), text_color="#3498db")
        bot_info_label.pack(anchor="w", padx=8, pady=(4, 2))
        self.stats_section_labels.append((bot_info_label, "bot_information_section"))
        self.lbl_bot_name = self._create_stat_card(self.tr("bot_name_lbl"), "-", icon="🤖")
        self.lbl_bot_version = self._create_stat_card(self.tr("bot_version_lbl"), "-", icon="🏷️")
        self.lbl_uptime = self._create_stat_card(self.tr("uptime_lbl"), "00:00:00", icon="⏱️")
        self.lbl_weekly_uptime = self._create_stat_card(self.tr("weekly_uptime_lbl"), "0h 0m", icon="📅")
        self.lbl_api_ping, self.lbl_msg_ping = self._create_dual_stat_card(self.tr("ping_lbl"), "API: 0ms", "Msg: 0ms", icon="📡")
        self.lbl_commands = self._create_stat_card(self.tr("total_commands_lbl"), "0", icon="⚡")
        pc_info_label = ctk.CTkLabel(self.stats_panel, text=self.tr("pc_resources_section"), font=("Arial", 12, "bold"), text_color="#2ecc71")
        pc_info_label.pack(anchor="w", padx=8, pady=(8, 2))
        self.stats_section_labels.append((pc_info_label, "pc_resources_section"))
        self.lbl_ram = self._create_stat_card(self.tr("ram_lbl"), "0 MB", icon="💾")
        self.lbl_cpu = self._create_stat_card(self.tr("cpu_lbl"), "0 %", icon="💻")
        self.lbl_temperature = self._create_stat_card(self.tr("temperature_pc_lbl"), self.tr("unavailable"), icon="🌡️")
        self.lbl_servers = self._create_stat_card(self.tr("guilds_lbl"), "0", icon="🌐")
        self.lbl_users = self._create_stat_card(self.tr("users_lbl"), "0", icon="👥")
        self.lbl_errors = self._create_stat_card(self.tr("error_counter_lbl"), "0", text_color="#e74c3c", icon="⚠️")
        self.register_scrollable(self.stats_panel)

    def _create_log_watermark_image(self):
        try:
            from PIL import Image

            logo_path = os.path.join(SCRIPT_DIR, "logo_watermark.png")
            if not os.path.isfile(logo_path):
                logo_path = os.path.join(SCRIPT_DIR, "logo.png")
            if not os.path.isfile(logo_path):
                logo_path = os.path.join(SCRIPT_DIR, "logo.png")

            if not os.path.isfile(logo_path):
                return None

            print(f"[LOG] Watermark forrás: {logo_path}")

            img = Image.open(logo_path).convert("RGBA")

            max_size = 220
            if img.width > max_size or img.height > max_size:
                ratio = min(max_size / img.width, max_size / img.height)
                new_w = int(img.width * ratio)
                new_h = int(img.height * ratio)
                img = img.resize((new_w, new_h), Image.LANCZOS)

            self._watermark_base_image = img
            self._watermark_size = (img.width, img.height)

            transparent = img.copy()
            alpha = transparent.split()[3]
            alpha = alpha.point(lambda p: 0)
            transparent.putalpha(alpha)

            return ctk.CTkImage(
                light_image=transparent,
                dark_image=transparent,
                size=(img.width, img.height),
            )
        except Exception as e:
            print(f"[LOG] Watermark hiba: {e}")
            return None

    def _set_watermark_alpha(self, alpha_value):
        if not getattr(self, "_watermark_base_image", None):
            return
        if not hasattr(self, "log_watermark_label") or self.log_watermark_label is None:
            return

        try:
            from PIL import Image

            img = self._watermark_base_image.copy()
            alpha = img.split()[3]
            alpha = alpha.point(lambda p: int(p * alpha_value))
            img.putalpha(alpha)

            new_ctk = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=self._watermark_size,
            )
            self.log_watermark_label.configure(image=new_ctk)
            self._watermark_current_image = new_ctk
        except Exception as e:
            print(f"[LOG] Watermark alpha hiba: {e}")

    def _fade_in_log_watermark(self, duration_ms=500, target_alpha=1.0):
        if getattr(self, "_watermark_fade_id", None):
            try:
                self.after_cancel(self._watermark_fade_id)
            except Exception:
                pass
            self._watermark_fade_id = None

        if not hasattr(self, "log_watermark_label") or self.log_watermark_label is None:
            return

        self._set_watermark_alpha(0.0)
        self.log_watermark_label.place(relx=0.5, rely=0.5, anchor="center")
        self.log_watermark_label.lift()

        steps = 25
        step_delay = max(15, duration_ms // steps)

        def animate(step=0):
            try:
                if step > steps:
                    self._set_watermark_alpha(target_alpha)
                    self._watermark_fade_id = None
                    return
                progress = step / steps
                eased = 1 - (1 - progress) ** 2
                current_alpha = target_alpha * eased
                self._set_watermark_alpha(current_alpha)
                self._watermark_fade_id = self.after(
                    step_delay, lambda: animate(step + 1)
                )
            except Exception as e:
                print(f"[LOG] Fade hiba: {e}")
                self._watermark_fade_id = None

        animate(0)

    def _fade_out_log_watermark(self, duration_ms=250):
        if getattr(self, "_watermark_fade_id", None):
            try:
                self.after_cancel(self._watermark_fade_id)
            except Exception:
                pass
            self._watermark_fade_id = None

        if not hasattr(self, "log_watermark_label") or self.log_watermark_label is None:
            return

        try:
            if not self.log_watermark_label.winfo_ismapped():
                return
        except Exception:
            pass

        steps = 15
        step_delay = max(15, duration_ms // steps)
        start_alpha = 1.0

        def animate(step=0):
            try:
                if step > steps:
                    try:
                        self.log_watermark_label.place_forget()
                    except Exception:
                        pass
                    self._watermark_fade_id = None
                    return
                progress = step / steps
                current_alpha = start_alpha * (1 - progress)
                self._set_watermark_alpha(current_alpha)
                self._watermark_fade_id = self.after(
                    step_delay, lambda: animate(step + 1)
                )
            except Exception as e:
                print(f"[LOG] Fade-out hiba: {e}")
                self._watermark_fade_id = None

        animate(0)

    def _update_log_empty_state(self):
        if getattr(self, "_watermark_debounce_id", None):
            try:
                self.after_cancel(self._watermark_debounce_id)
            except Exception:
                pass
            self._watermark_debounce_id = None

        self._watermark_debounce_id = self.after(150, self._do_update_log_empty_state)

    def _do_update_log_empty_state(self):
        self._watermark_debounce_id = None

        if not hasattr(self, "log_watermark_label") or self.log_watermark_label is None:
            return

        try:
            content = self.log_textbox.get("1.0", "end").strip()
            has_content = bool(content)
        except Exception:
            return

        try:
            currently_visible = self.log_watermark_label.winfo_ismapped()
        except Exception:
            currently_visible = False

        if has_content and currently_visible:
            self._fade_out_log_watermark()
        elif not has_content and not currently_visible:
            self._fade_in_log_watermark()

    def _create_stat_card(self, title, default_val, text_color=None, icon=""):
        if text_color is None:
            text_color = self.theme_colors["text"]
        card = ctk.CTkFrame(self.stats_panel, fg_color=self.theme_colors["card_bg"], corner_radius=6)
        card.pack(fill="x", padx=5, pady=4)
        header_f = ctk.CTkFrame(card, fg_color="transparent")
        header_f.pack(fill="x", padx=8, pady=(4, 0))
        header = ctk.CTkLabel(header_f, text=f"{icon} {title}", font=("Arial", 11, "bold"), text_color=self.theme_colors["subtext"])
        header.pack(side="left")
        self.stat_card_headers.append((header, title))
        lbl_val = ctk.CTkLabel(card, text=default_val, font=("Arial", 13, "bold"), text_color=text_color)
        lbl_val.pack(anchor="w", padx=10, pady=(0, 6))
        return lbl_val

    def _create_dual_stat_card(self, title, val1, val2, icon=""):
        card = ctk.CTkFrame(self.stats_panel, fg_color=self.theme_colors["card_bg"], corner_radius=6)
        card.pack(fill="x", padx=5, pady=4)
        header = ctk.CTkLabel(card, text=f"{icon} {title}", font=("Arial", 11, "bold"), text_color=self.theme_colors["subtext"])
        header.pack(anchor="w", padx=8, pady=(4, 2))
        self.dual_stat_headers.append((header, title))
        sub_f = ctk.CTkFrame(card, fg_color="transparent")
        sub_f.pack(fill="x", padx=8, pady=(0, 6))
        lbl1 = ctk.CTkLabel(sub_f, text=val1, font=("Arial", 12, "bold"), text_color="#3498db")
        lbl1.pack(side="left", expand=True)
        lbl2 = ctk.CTkLabel(sub_f, text=val2, font=("Arial", 12, "bold"), text_color="#2ecc71")
        lbl2.pack(side="right", expand=True)
        return lbl1, lbl2

    # ---------- BOT METADATA ----------

    def read_bot_metadata(self, bot_key=None):
        bot = self.bots.get(bot_key or self.active_bot_key, {})
        script_path = bot.get("path", "")
        defaults = {
            "name": bot.get("name", bot_key or self.active_bot_key),
            "version": "1.0.0",
            "token": "",
            "prefix": "/",
        }
        if not script_path:
            return defaults
        version_path = os.path.join(os.path.dirname(script_path), "version.py")
        if not os.path.isfile(version_path):
            return defaults
        try:
            with open(version_path, "r", encoding="utf-8") as version_file:
                tree = ast.parse(version_file.read(), filename=version_path)
            mapping = {
                "BOT_NAME": "name",
                "BOT_VERSION": "version",
                "BOT_TOKEN": "token",
                "BOT_PREFIX": "prefix",
            }
            for node in tree.body:
                if (isinstance(node, ast.Assign) and
                        len(node.targets) == 1 and
                        isinstance(node.targets[0], ast.Name)):
                    key = node.targets[0].id
                    if key in mapping:
                        value = ast.literal_eval(node.value)
                        defaults[mapping[key]] = str(value)
        except (OSError, SyntaxError, ValueError):
            pass
        return defaults

    def save_bot_metadata(self, name, version, token, prefix="/"):
        old_key = self.active_bot_key
        bot = self.bots[old_key]
        name = name.strip() or old_key
        prefix = prefix.strip() or "/"
        script_path = bot.get("path", "")
        if not script_path or not os.path.isfile(script_path):
            messagebox.showwarning(self.tr("warning_title"), self.tr("bot_script_missing_msg"))
            return
        bot_dir = os.path.dirname(script_path)
        with open(os.path.join(bot_dir, "version.py"), "w", encoding="utf-8") as version_file:
            version_file.write(
                "BOT_NAME = %r\n"
                "BOT_VERSION = %r\n"
                "BOT_TOKEN = %r\n"
                "BOT_PREFIX = %r\n"
                % (name, version.strip(), token.strip(), prefix)
            )
        bot["name"] = name
        if name != old_key:
            self.rename_bot_key(old_key, name, persist=False)
        self.save_config()
        self.switch_bot(self.active_bot_key)
        self.notify(self.tr("bot_data_saved_msg", name=name), "success", 2000)

    def rename_bot_key(self, old_key, new_key, persist=True):
        new_key = new_key.strip()
        if not new_key or old_key not in self.bots:
            return False
        if new_key != old_key and new_key in self.bots:
            messagebox.showerror(self.tr("error_title"), self.tr("duplicate_bot_msg"))
            return False
        bot = self.bots.pop(old_key)
        bot["name"] = new_key
        self.bots[new_key] = bot
        if self.active_bot_key == old_key:
            self.active_bot_key = new_key
        self.render_tabs()
        if persist:
            self.save_config()
        return True

    # ---------- MONITOR LOOP ----------

    def resource_monitor_loop(self):
        while self.is_monitoring:
            time.sleep(5)
            for key, bot in self.bots.items():
                if bot["is_running"] and bot["process"]:
                    try:
                        p = psutil.Process(bot["process"].pid)
                        mem_mb = p.memory_info().rss / (1024 * 1024)
                        cpu_p = p.cpu_percent(interval=None)

                        if "history_ram" not in bot:
                            bot["history_ram"] = []
                            bot["history_cpu"] = []
                            bot["history_time"] = []

                        t_str = datetime.datetime.now().strftime("%H:%M:%S")
                        bot["history_ram"].append(mem_mb)
                        bot["history_cpu"].append(cpu_p)
                        bot["history_time"].append(t_str)

                        if len(bot["history_ram"]) > 17280:
                            bot["history_ram"].pop(0)
                            bot["history_cpu"].pop(0)
                            bot["history_time"].pop(0)

                        if mem_mb > self.max_ram_mb:
                            self.log_event("ERROR", f"A(z) '{key}' bot túllépte a RAM limitet: {mem_mb:.1f} MB / {self.max_ram_mb} MB")
                            if self.task_kill_enabled:
                                p.terminate()
                                bot["is_running"] = False
                                bot["process"] = None
                                self.log_event("ERROR", f"A(z) '{key}' bot automatikusan le lett lőve memóriatúllépés miatt.")
                    except Exception:
                        pass

    def init_discord_rpc(self):
        if not RPC_AVAILABLE or not self.rpc_enabled:
            return

        def rpc_worker():
            try:
                rpc = Presence("123456789012345678")
                rpc.connect()
                while self.rpc_enabled:
                    rpc.update(
                        details="Botokat kezel a DBM-ben",
                        state="DJ Baluss Panel",
                        large_image="icon",
                        start=time.time()
                    )
                    time.sleep(15)
            except Exception:
                pass

        threading.Thread(target=rpc_worker, daemon=True).start()

    # ---------- KAPCSOLÓK ----------

    def on_volume_change(self):
        if not self.is_loading:
            self.save_config()

    def on_test_mode_toggle(self):
        if not self.is_loading:
            self.save_config()
            status_str = self.tr("test_mode_on_status") if self.test_mode_var.get() else self.tr("test_mode_off_status")
            self.append_log("EVENT", self.tr("test_mode_changed_msg", status=status_str))

    def on_midnight_toggle(self):
        if self.midnight_var.get():
            self.slider_r_days.set(0)
            self.slider_r_hours.set(0)
            self.slider_r_mins.set(0)
            self.lbl_r_days.configure(text="0" + self.tr("days_short"))
            self.lbl_r_hours.configure(text="0" + self.tr("hours_short"))
            self.lbl_r_mins.configure(text="0" + self.tr("minutes_short"))
        if not self.is_loading:
            self.save_config()

    def on_restart_slider_change(self):
        d = int(self.slider_r_days.get())
        h = int(self.slider_r_hours.get())
        m = int(self.slider_r_mins.get())
        self.lbl_r_days.configure(text=f"{d}" + self.tr("days_short"))
        self.lbl_r_hours.configure(text=f"{h}" + self.tr("hours_short"))
        self.lbl_r_mins.configure(text=f"{m}" + self.tr("minutes_short"))

        if (d > 0 or h > 0 or m > 0) and self.midnight_var.get():
            self.midnight_var.set(False)

        if not self.is_loading:
            self.save_config()

    # ---------- UI SZÖVEG FRISSÍTÉS ----------

    def update_ui_texts(self):
        self.title(self.tr("panel_title"))

        stat_keys = [
            "bot_name_lbl", "bot_version_lbl", "uptime_lbl", "weekly_uptime_lbl",
            "total_commands_lbl", "ram_lbl", "cpu_lbl", "temperature_pc_lbl",
            "guilds_lbl", "users_lbl", "error_counter_lbl"
        ]
        for (header, _), key in zip(self.stat_card_headers, stat_keys):
            icon = header.cget("text").split(" ", 1)[0]
            header.configure(text=f"{icon} {self.tr(key)}")
        if self.dual_stat_headers:
            header, _ = self.dual_stat_headers[0]
            icon = header.cget("text").split(" ", 1)[0]
            header.configure(text=f"{icon} {self.tr('ping_lbl')}")
        self._refresh_stat_section_labels()
        self.btn_dashboard.configure(text="📐   " + self.tr("dashboard_widget_btn"))
        self.btn_start.configure(text="▶   " + self.tr("bot_start_btn"))
        self.btn_restart.configure(text="⟳   " + self.tr("bot_restart_btn"))
        self.btn_stop.configure(text="■   " + self.tr("bot_stop_btn"))
        self.btn_settings.configure(text=self.tr("settings_btn"))
        self.btn_global_stats.configure(text=self.tr("global_stats_btn"))
        if hasattr(self, "btn_broadcast"):
            self.btn_broadcast.configure(text=self.tr("broadcast_btn"))
        self.btn_servers.configure(text="🌐  " + self.tr("servers_btn"))
        self.lbl_panel_id.configure(text=config.PANEL_ID)
        self.btn_copy_connect.configure(text="📋  " + self.tr("copy_command_btn"))
        if hasattr(self, "btn_integrate_panel"):
            self.btn_integrate_panel.configure(text=self.tr("add_panel_btn"))
        self.btn_bot_info.configure(text="🤖  " + self.tr("bot_data_btn"))
        self.btn_start_all.configure(text="▶   " + self.tr("start_all_btn"))
        self.btn_restart_all.configure(text="⟳   " + self.tr("restart_all_btn"))
        self.btn_stop_all.configure(text="■   " + self.tr("stop_all_btn"))
        self.btn_alapok.configure(text=self.tr("integration_btn"))
        self.btn_tutorial.configure(text=self.tr("tutorial_btn"))
        if hasattr(self, "btn_lan_client"):
            self.btn_lan_client.configure(text="🔗  " + self.tr("lan_client_btn"))
        self.btn_backup.configure(text=self.tr("backup_btn"))
        self.btn_sqlite.configure(text=self.tr("sqlite_btn"))
        self.btn_plugins.configure(text=self.tr("plugins_btn"))
        self.entry_path.configure(placeholder_text=self.tr("bot_file_ph"))
        self.btn_activity.configure(text="🎭  " + self.tr("activity_btn"))
        self.lbl_path_title.configure(text=self.tr("bot_file_lbl"))
        self.btn_save_path.configure(text="💾  " + self.tr("save_btn"))
        self.btn_browse.configure(text="📂  " + self.tr("browse_btn"))
        self.chk_autostart.configure(text="  " + self.tr("autostart_lbl"))
        self.chk_sound.configure(text="  " + self.tr("error_sound_lbl"))
        self.chk_test_mode.configure(text="  " + self.tr("test_mode_lbl"))
        self.chk_midnight.configure(text="  " + self.tr("midnight_restart_lbl"))
        self.lbl_logs_title.configure(text=self.tr("live_logs_title"))
        self.btn_filter_all.configure(text=self.tr("filter_all_btn"))
        self.btn_filter_errors.configure(text=self.tr("filter_errors_btn"))
        self.btn_filter_success.configure(text=self.tr("filter_success_btn"))
        self.btn_filter_events.configure(text=self.tr("filter_events_btn"))
        self.search_entry.configure(placeholder_text=self.tr("log_search_ph"))
        self.btn_clear.configure(text=self.tr("clear_logs_btn"))
        self.chk_autoscroll.configure(text=self.tr("autoscroll_lbl"))
        self.btn_open_charts.configure(text=self.tr("open_charts_btn"))
        self.check_env_file()

    def _refresh_stat_section_labels(self):
        if hasattr(self, "stats_section_labels"):
            for label, key in self.stats_section_labels:
                label.configure(text=self.tr(key))

    # ---------- AUTOSTART & RESTART ----------

    def check_and_run_autostarts(self):
        for key, bot in self.bots.items():
            if bot["autostart"] and bot["path"] and os.path.exists(bot["path"]):
                if not bot["is_running"]:
                    try:
                        script_path = bot["path"]
                        bot_dir = os.path.dirname(script_path)
                        python_exe = sys.executable.lower().replace("pythonw.exe", "python.exe")
                        env = os.environ.copy()
                        env["PYTHONUNBUFFERED"] = "1"
                        env["PYTHONIOENCODING"] = "utf-8"
                        env["PYTHONUTF8"] = "1"
                        creationflags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0

                        bot["process"] = subprocess.Popen(
                            [python_exe, script_path], cwd=bot_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, env=env, creationflags=creationflags
                        )
                        bot["is_running"] = True
                        bot["start_time"] = time.time()

                        if key == self.active_bot_key:
                            self.lbl_status.configure(text=self.tr("online_status"), text_color="#2ecc71")

                        self.append_log_to_bot(key, "SUCCESS", self.tr("auto_start_process_started_msg", pid=bot['process'].pid))
                        threading.Thread(target=self._read_bot_output, args=(key,), daemon=True).start()
                    except Exception as e:
                        self.append_log_to_bot(key, "ERROR", self.tr("auto_start_error_msg", error=e))

    def check_auto_restarts(self):
        bot = self.bots.get(self.active_bot_key)
        if bot and bot["is_running"] and bot["start_time"]:
            if bot["midnight_restart"]:
                now = datetime.datetime.now()
                if now.hour == 0 and now.minute == 0 and now.second < 2:
                    self.append_log("EVENT", self.tr("midnight_restart_event_msg"))
                    self.restart_bot()
                    return

            total_seconds_limit = (bot["restart_days"] * 86400) + (bot["restart_hours"] * 3600) + (bot["restart_mins"] * 60)
            if total_seconds_limit > 0:
                elapsed = time.time() - bot["start_time"]
                if elapsed >= total_seconds_limit:
                    self.append_log("EVENT", self.tr("auto_restart_event_msg"))
                    self.restart_bot()

    def is_quiet_hours(self):
        """Igaz, ha épp csendes órák vannak (ne szóljon a hiba hang)."""
        if not getattr(self, "quiet_hours_enabled", False):
            return False

        start_str = getattr(self, "quiet_hours_start", "22:00")
        end_str = getattr(self, "quiet_hours_end", "06:00")

        try:
            sh, sm = map(int, start_str.split(":"))
            eh, em = map(int, end_str.split(":"))
        except (ValueError, AttributeError):
            return False

        now = datetime.datetime.now()
        now_min = now.hour * 60 + now.minute
        start_min = sh * 60 + sm
        end_min = eh * 60 + em

        if start_min == end_min:
            return False

        if start_min < end_min:
            return start_min <= now_min < end_min
        else:
            return now_min >= start_min or now_min < end_min

    def play_error_sound(self):
        if not self.sound_var.get():
            return
        # Csendes órák ellenőrzése
        if self.is_quiet_hours():
            return
        try:
            from modules.sounds import play_error_sound_by_name
            play_error_sound_by_name(self.selected_error_sound, async_play=True)
        except Exception:
            pass

    # ---------- BOT ADAT STRUKTÚRA ----------

    def create_bot_data(self, name, path=""):
        return {
            "name": name, "path": path, "emoji": "🤖", "color": "#5865F2",
            "autostart": False, "test_mode": False,
            "restart_days": 0, "restart_hours": 0, "restart_mins": 0,
            "midnight_restart": False, "error_sound": False, "volume": 50,
            "raw_logs": [], "is_running": False, "process": None,
            "start_time": None, "error_count": 0, "total_commands": 0,
            "allowed_discord_ids": [], "weekly_uptime_seconds": 0,
            "history_ram": [], "history_cpu": [], "history_time": [],
            "auto_restart_on_crash": False, "crash_restart_delay": 10,
            "manual_stop": False, "activity_enabled": True,
            "activity_type": "Playing", "activity_text": "",
            "activity_interval_minutes": 5, "activity_loop": [],
        }

    # ---------- TAB KEZELÉS ----------

    def render_tabs(self):
        for child in self.tab_buttons_frame.winfo_children():
            child.destroy()

        for i, key in enumerate(self.bots):
            bot = self.bots[key]
            emoji = bot.get("emoji", "🤖")
            custom_color = bot.get("color", None)

            if key == self.active_bot_key:
                color = custom_color or self.theme_colors["accent"]
            else:
                color = self.theme_colors["sidebar_bg"]

            is_first = (i == 0)
            base_text = key if (is_first or len(self.bots) <= 1) else f"{key}  ✕"
            btn_text = f"{emoji}  {base_text}"

            btn = ctk.CTkButton(
                self.tab_buttons_frame,
                text=btn_text, width=140, fg_color=color,
                hover_color=self.theme_colors["accent_hover"] if custom_color else "#3a3a3a",
                command=lambda k=key: self.switch_bot(k)
            )
            btn.bind("<Button-3>",
                     lambda e, k=key, first=is_first: self.show_tab_context_menu(e, k, first))
            btn.bind("<Enter>", lambda e, k=key: self._show_bot_tooltip(e, k), add="+")
            btn.bind("<Leave>", lambda e: self._hide_bot_tooltip(), add="+")
            btn.pack(side="left", padx=5, pady=5)

    def _show_bot_tooltip(self, event, bot_key):
        try:
            if getattr(self, "_bot_tooltip_key", None) == bot_key:
                return
            if getattr(self, "_bot_tooltip_after_id", None):
                try:
                    self.after_cancel(self._bot_tooltip_after_id)
                except Exception:
                    pass
                self._bot_tooltip_after_id = None
            self._bot_tooltip_key = bot_key
            self._bot_tooltip_after_id = self.after(
                400, lambda: self._really_show_bot_tooltip(bot_key)
            )
        except Exception as e:
            print(f"[TOOLTIP] show hiba: {e}")

    def _really_show_bot_tooltip(self, bot_key):
        if getattr(self, "_bot_tooltip_key", None) != bot_key:
            return
        self._hide_bot_tooltip(clear_key=False)
        try:
            bot = self.bots.get(bot_key)
            if not bot:
                return

            tip = ctk.CTkToplevel(self)
            tip.overrideredirect(True)
            try:
                tip.attributes("-topmost", True)
                tip.attributes("-alpha", 0.0)
            except Exception:
                pass
            tip.configure(fg_color="#0d0f14")

            border = ctk.CTkFrame(
                tip, fg_color="#0d0f14", corner_radius=10,
                border_width=2, border_color="#5865F2",
            )
            border.pack(fill="both", expand=True, padx=1, pady=1)

            emoji = bot.get("emoji", "🤖")
            ctk.CTkLabel(
                border, text=f"{emoji}  {bot_key}",
                font=("Arial", 13, "bold"), text_color="#ffffff",
            ).pack(padx=14, pady=(10, 6))

            ctk.CTkFrame(border, height=1, fg_color="#2f3542").pack(
                fill="x", padx=12, pady=(0, 6)
            )

            info = ctk.CTkFrame(border, fg_color="transparent")
            info.pack(padx=14, pady=(0, 10))

            is_running = bot.get("is_running", False)
            status_color = "#2ecc71" if is_running else "#e74c3c"
            status_text = self.tr("online_status") if is_running else self.tr("offline_status")

            def add_row(label, value, color="#ffffff"):
                row = ctk.CTkFrame(info, fg_color="transparent")
                row.pack(fill="x", pady=1)
                ctk.CTkLabel(
                    row, text=label, font=("Arial", 10),
                    text_color="#8a8e98", width=90, anchor="w",
                ).pack(side="left")
                ctk.CTkLabel(
                    row, text=value, font=("Consolas", 10, "bold"),
                    text_color=color, anchor="w",
                ).pack(side="left")

            add_row("State:", status_text, status_color)

            if is_running and bot.get("start_time"):
                sec = int(time.time() - bot["start_time"])
                h, rem = divmod(sec, 3600)
                m, s = divmod(rem, 60)
                add_row("Uptime:", f"{h:02d}:{m:02d}:{s:02d}", "#2ecc71")
            else:
                add_row("Uptime:", "—", "#6a6e78")

            ram_text = "—"
            cpu_text = "—"
            if is_running and bot.get("process"):
                try:
                    p = psutil.Process(bot["process"].pid)
                    ram_text = f"{p.memory_info().rss / (1024 * 1024):.1f} MB"
                    cpu_text = f"{p.cpu_percent(interval=None):.1f}%"
                except Exception:
                    pass

            add_row("RAM:", ram_text, "#3498db")
            add_row("CPU:", cpu_text, "#2ecc71")
            add_row("Errors:", str(bot.get("error_count", 0)),
                    "#e74c3c" if bot.get("error_count", 0) > 0 else "#6a6e78")
            add_row("Commands:", str(bot.get("total_commands", 0)), "#f39c12")

            tip.update_idletasks()
            tip_w = tip.winfo_reqwidth()
            tip_h = tip.winfo_reqheight()

            try:
                btn_widget = None
                for child in self.tab_buttons_frame.winfo_children():
                    if bot_key in str(child.cget("text")):
                        btn_widget = child
                        break
                if btn_widget:
                    x = btn_widget.winfo_rootx()
                    y = btn_widget.winfo_rooty() + btn_widget.winfo_height() + 6
                else:
                    x = self.winfo_pointerx() + 10
                    y = self.winfo_pointery() + 20
            except Exception:
                x = self.winfo_pointerx() + 10
                y = self.winfo_pointery() + 20

            screen_w = tip.winfo_screenwidth()
            screen_h = tip.winfo_screenheight()
            if x + tip_w > screen_w:
                x = screen_w - tip_w - 10
            if y + tip_h > screen_h:
                y = screen_h - tip_h - 10
            if x < 0:
                x = 10
            if y < 0:
                y = 10

            tip.geometry(f"{tip_w}x{tip_h}+{x}+{y}")
            self._bot_tooltip = tip

            def fade_in(alpha=0.0):
                try:
                    if not tip.winfo_exists():
                        return
                    new_alpha = min(1.0, alpha + 0.2)
                    tip.attributes("-alpha", new_alpha)
                    if new_alpha < 1.0:
                        tip.after(15, lambda: fade_in(new_alpha))
                except Exception:
                    pass

            tip.after(10, fade_in)
        except Exception as e:
            print(f"[TOOLTIP] megjelenítés hiba: {e}")

    def _hide_bot_tooltip(self, event=None, clear_key=True):
        try:
            if getattr(self, "_bot_tooltip_after_id", None):
                try:
                    self.after_cancel(self._bot_tooltip_after_id)
                except Exception:
                    pass
                self._bot_tooltip_after_id = None
            if clear_key:
                self._bot_tooltip_key = None
            tip = getattr(self, "_bot_tooltip", None)
            if tip is not None:
                try:
                    if tip.winfo_exists():
                        tip.destroy()
                except Exception:
                    pass
                self._bot_tooltip = None
        except Exception:
            pass

    def show_tab_context_menu(self, event, key, is_first):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="✏️ " + self.tr("rename_btn"), command=lambda: self.rename_bot(key))
        if not is_first and len(self.bots) > 1:
            menu.add_command(label="🗑️ " + self.tr("delete_btn"), command=lambda: self.delete_bot(key))
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def rename_bot(self, key):
        new_name = simpledialog.askstring(
            self.tr("rename_btn"),
            f"{self.tr('new_bot_prompt')} ({key}):",
            initialvalue=key
        )
        if new_name:
            new_name = new_name.strip()
            if not new_name or new_name in self.bots:
                messagebox.showerror(self.tr("error_title"), self.tr("duplicate_bot_msg"))
                return
            if not self.rename_bot_key(key, new_name, persist=False):
                return
            bot = self.bots[new_name]
            metadata = self.read_bot_metadata(new_name)
            script_path = bot.get("path", "")
            if script_path and os.path.isfile(script_path):
                with open(os.path.join(os.path.dirname(script_path), "version.py"),
                          "w", encoding="utf-8") as version_file:
                    version_file.write(
                        "BOT_NAME = %r\nBOT_VERSION = %r\nBOT_TOKEN = %r\n"
                        % (new_name, metadata["version"], metadata["token"])
                    )
            self.save_config()
            self.switch_bot(self.active_bot_key)

    def delete_bot(self, key):
        keys_list = list(self.bots.keys())
        if keys_list and keys_list[0] == key:
            messagebox.showwarning(self.tr("warning_title"), self.tr("default_bot_no_delete"))
            return
        if len(self.bots) <= 1:
            messagebox.showwarning(self.tr("warning_title"), self.tr("last_bot_no_delete_msg"))
            return
        if messagebox.askyesno(self.tr("confirm_btn"),
                                self.tr("delete_bot_confirm", name=key)):
            if self.bots[key]["is_running"]:
                try:
                    self.bots[key]["process"].terminate()
                except Exception:
                    pass
            del self.bots[key]
            if self.active_bot_key == key:
                self.active_bot_key = list(self.bots.keys())[0]
            self.switch_bot(self.active_bot_key)
            self.save_config()
            self.render_tabs()

    def check_env_file(self):
        script_path = self.entry_path.get().strip()
        if script_path and os.path.exists(script_path):
            bot_dir = os.path.dirname(script_path)
            if os.path.exists(os.path.join(bot_dir, ".env")):
                self.lbl_env_status.configure(text=self.tr("env_ok"), text_color="#2ecc71")
                return
        self.lbl_env_status.configure(text=self.tr("env_missing"), text_color="#e74c3c")

    def switch_bot(self, key):
        if key not in self.bots:
            return

        if not self.is_loading:
            if self.active_bot_key in self.bots:
                current_text = self.entry_path.get().strip()
                if current_text and current_text != self.tr("bot_file_ph"):
                    self.bots[self.active_bot_key]["path"] = current_text
                self.bots[self.active_bot_key]["autostart"] = self.autostart_var.get()
                self.bots[self.active_bot_key]["test_mode"] = self.test_mode_var.get()
                self.bots[self.active_bot_key]["restart_days"] = int(self.slider_r_days.get())
                self.bots[self.active_bot_key]["restart_hours"] = int(self.slider_r_hours.get())
                self.bots[self.active_bot_key]["restart_mins"] = int(self.slider_r_mins.get())
                self.bots[self.active_bot_key]["midnight_restart"] = self.midnight_var.get()
                self.bots[self.active_bot_key]["error_sound"] = self.sound_var.get()
                self.bots[self.active_bot_key]["volume"] = int(self.slider_volume.get())

        self.active_bot_key = key
        bot = self.bots[key]

        self.entry_path.delete(0, "end")
        if bot["path"]:
            self.entry_path.insert(0, bot["path"])

        self.autostart_var.set(bot["autostart"])
        self.test_mode_var.set(bot.get("test_mode", False))
        self.slider_r_days.set(bot["restart_days"])
        self.slider_r_hours.set(bot["restart_hours"])
        self.slider_r_mins.set(bot["restart_mins"])
        self.lbl_r_days.configure(text=f"{bot['restart_days']}" + self.tr("days_short"))
        self.lbl_r_hours.configure(text=f"{bot['restart_hours']}" + self.tr("hours_short"))
        self.lbl_r_mins.configure(text=f"{bot['restart_mins']}" + self.tr("minutes_short"))

        self.midnight_var.set(bot.get("midnight_restart", False))
        self.sound_var.set(bot["error_sound"])
        self.slider_volume.set(bot.get("volume", 50))

        self.check_env_file()
        metadata = self.read_bot_metadata(key)
        self.lbl_bot_name.configure(text=metadata["name"])
        self.lbl_bot_version.configure(text=metadata["version"])

        emoji = bot.get("emoji", "🤖")
        custom_color = bot.get("color", None)
        if bot["is_running"]:
            self.lbl_status.configure(text=f"{emoji} {self.tr('online_status')}",
                                       text_color=custom_color or "#2ecc71")
        else:
            self.lbl_status.configure(text=f"{emoji} {self.tr('offline_status')}",
                                       text_color="#e74c3c")

        self.lbl_errors.configure(text=str(bot["error_count"]))
        self.lbl_commands.configure(text=str(bot["total_commands"]) if bot["path"] and os.path.exists(bot["path"]) else "0")

        w_hours = bot["weekly_uptime_seconds"] // 3600
        w_mins = (bot["weekly_uptime_seconds"] % 3600) // 60
        self.lbl_weekly_uptime.configure(text=f"{w_hours}h {w_mins}m")

        self.search_entry.delete(0, "end")
        self.refresh_log_display()
        if not self.is_loading:
            self.render_tabs()

    def add_bot_dialog(self):
        bot_name = simpledialog.askstring(self.tr("new_bot_title"), self.tr("new_bot_prompt"))
        if bot_name:
            bot_name = bot_name.strip()
            if bot_name in self.bots:
                messagebox.showerror(self.tr("error_title"), self.tr("duplicate_bot_msg"))
                return
            self.bots[bot_name] = self.create_bot_data(bot_name)
            self.switch_bot(bot_name)
            self.save_config()
            self.render_tabs()

    # ---------- BOT VEZÉRLÉS ----------

    def start_all_bots(self):
        for key in self.bots:
            self.switch_bot(key)
            self.start_bot()
        self.log_event("SUCCESS", self.tr("all_bots_start_log"))
        messagebox.showinfo(self.tr("panel_title"), self.tr("all_bots_start_msg"))

    def restart_all_bots(self):
        for key in self.bots:
            self.switch_bot(key)
            self.restart_bot()
        self.log_event("SUCCESS", self.tr("all_bots_restart_log"))
        messagebox.showinfo(self.tr("panel_title"), self.tr("all_bots_restart_msg"))

    def stop_all_bots(self):
        for key in self.bots:
            self.switch_bot(key)
            self.stop_bot()
        self.log_event("WARNING", self.tr("all_bots_stop_log"))
        messagebox.showwarning(self.tr("panel_title"), self.tr("all_bots_stop_msg"))

    def start_bot(self):
        script_path = self.entry_path.get().strip()
        if not script_path or not os.path.exists(script_path):
            self.append_log("ERROR", self.tr("bot_script_missing_msg"))
            return

        bot = self.bots[self.active_bot_key]
        if not bot["is_running"]:
            try:
                bot_dir = os.path.dirname(script_path)
                python_exe = sys.executable.lower().replace("pythonw.exe", "python.exe")
                env = os.environ.copy()
                env["PYTHONUNBUFFERED"] = "1"
                creationflags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0

                bot["process"] = subprocess.Popen(
                    [python_exe, script_path], cwd=bot_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, env=env, creationflags=creationflags
                )
                bot["is_running"] = True
                bot["manual_stop"] = False
                bot["start_time"] = time.time()
                bot["path"] = script_path
                self.lbl_status.configure(text=self.tr("online_status"), text_color="#2ecc71")
                self.append_log("SUCCESS", self.tr("bot_process_started_msg", pid=bot['process'].pid))
                self.show_bot_startup_animation(
                    self.active_bot_key,
                    bot.get("emoji", "🤖"),
                )
                threading.Thread(target=self._read_bot_output, args=(self.active_bot_key,), daemon=True).start()
                self.save_config()
            except Exception as e:
                self.append_log("ERROR", self.tr("start_error_msg", error=e))

    def _read_bot_output(self, bot_key):
        bot = self.bots[bot_key]
        proc = bot["process"]
        while bot["is_running"] and proc:
            line = proc.stdout.readline()
            if line:
                cleaned_line = line.strip()
                lower_l = cleaned_line.lower()
                if "error" in lower_l or "exception" in lower_l:
                    log_type = "ERROR"
                elif "[debug]" in lower_l or "[info]" in lower_l or "event" in lower_l:
                    log_type = "EVENT"
                else:
                    log_type = "INFO"

                self.after(0, self.append_log_to_bot, bot_key, log_type, cleaned_line)
            if proc.poll() is not None:
                break
        return_code = proc.poll()
        if bot.get("is_running"):
            bot["is_running"] = False
            self.after(0, self.handle_bot_exit, bot_key, return_code)

    def handle_bot_exit(self, bot_key, return_code):
        bot = self.bots.get(bot_key)
        if not bot:
            return
        bot["process"] = None
        bot["start_time"] = None
        self.append_log_to_bot(bot_key,
                                "ERROR" if return_code not in (0, None) else "EVENT",
                                self.tr("bot_unexpected_stop_msg", code=return_code))
        if bot.get("auto_restart_on_crash") and not bot.get("manual_stop") and return_code not in (0, None):
            delay = max(1, int(bot.get("crash_restart_delay", 10)))
            self.append_log_to_bot(bot_key, "EVENT", self.tr("crash_watchdog_msg", n=delay))
            self.after(delay * 1000, lambda: self.restart_crashed_bot(bot_key))

    def restart_crashed_bot(self, bot_key):
        if bot_key not in self.bots or self.bots[bot_key].get("is_running"):
            return
        previous_key = self.active_bot_key
        self.switch_bot(bot_key)
        self.start_bot()
        self.switch_bot(previous_key)

    def stop_bot(self):
        bot = self.bots[self.active_bot_key]
        if bot["is_running"] and bot["process"]:
            bot["manual_stop"] = True
            bot["process"].terminate()
            bot["process"] = None
            bot["is_running"] = False
            bot["start_time"] = None
            self.lbl_status.configure(text=self.tr("offline_status"), text_color="#e74c3c")
            self.append_log("EVENT", self.tr("bot_process_stopped_msg"))
            self.save_config()

    def restart_bot(self):
        self.append_log("EVENT", self.tr("bot_restart_msg"))
        self.stop_bot()
        self.after(1500, self.start_bot)

    def browse_file(self):
        file_selected = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_selected:
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, file_selected)
            self.manual_save_path()

    # ---------- LOG KEZELÉS ----------

    def append_log(self, log_type, message):
        self.append_log_to_bot(self.active_bot_key, log_type, message)

    def append_log_to_bot(self, bot_key, log_type, message):
        if bot_key not in self.bots:
            return
        bot = self.bots[bot_key]
        if log_type == "ERROR":
            bot["error_count"] += 1
            if bot_key == self.active_bot_key:
                self.lbl_errors.configure(text=str(bot["error_count"]))
            self.play_error_sound()

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        entry = {"time": timestamp, "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                  "type": log_type, "msg": message}
        bot["raw_logs"].append(entry)
        self.log_event(log_type, f"[{bot_key}] {message}")

        if bot_key == self.active_bot_key:
            query = self.search_entry.get().strip().lower()
            if not query or query in message.lower() or query in log_type.lower() or query in timestamp.lower():
                self._write_to_textbox(entry)

    def refresh_log_display(self):
        self.log_textbox.delete("1.0", "end")
        for entry in self.bots[self.active_bot_key]["raw_logs"]:
            self._write_to_textbox(entry)
        self._update_log_empty_state()

    def _write_to_textbox(self, entry):
        self.log_textbox.insert("end", f"[{entry['time']}][{entry['type']:<7}] {entry['msg']}\n")
        if self.chk_autoscroll.get():
            self.log_textbox.see("end")
        self._update_log_empty_state()

    def filter_logs(self, cat):
        self.search_entry.delete(0, "end")
        self.log_textbox.delete("1.0", "end")
        for entry in self.bots[self.active_bot_key]["raw_logs"]:
            if cat == "ALL" or entry["type"] == cat:
                self._write_to_textbox(entry)
        self._update_log_empty_state()

    def apply_log_search_and_filter(self):
        query = self.search_entry.get().strip().lower()
        self.log_textbox.delete("1.0", "end")
        for entry in self.bots[self.active_bot_key]["raw_logs"]:
            if not query or query in entry["msg"].lower() or query in entry["type"].lower() or query in entry["time"].lower():
                self._write_to_textbox(entry)
        self._update_log_empty_state()

    def clear_logs(self):
        bot = self.bots[self.active_bot_key]
        bot["raw_logs"].clear()
        bot["error_count"] = 0
        self.lbl_errors.configure(text="0")
        self.log_textbox.delete("1.0", "end")
        self._update_log_empty_state()
        self.save_config()

    # ---------- CONFIG MENTÉS / BETÖLTÉS ----------

    def manual_save_path(self):
        path_val = self.entry_path.get().strip()
        if path_val and path_val != self.tr("bot_file_ph"):
            if not os.path.exists(path_val):
                messagebox.showerror(self.tr("error_title"),
                                      self.tr("file_not_found_msg", path=path_val))
                return
            self.bots[self.active_bot_key]["path"] = path_val

        if self.active_bot_key in self.bots:
            self.bots[self.active_bot_key]["autostart"] = self.autostart_var.get()
            self.bots[self.active_bot_key]["test_mode"] = self.test_mode_var.get()
            self.bots[self.active_bot_key]["restart_days"] = int(self.slider_r_days.get())
            self.bots[self.active_bot_key]["restart_hours"] = int(self.slider_r_hours.get())
            self.bots[self.active_bot_key]["restart_mins"] = int(self.slider_r_mins.get())
            self.bots[self.active_bot_key]["midnight_restart"] = self.midnight_var.get()
            self.bots[self.active_bot_key]["error_sound"] = self.sound_var.get()
            self.bots[self.active_bot_key]["volume"] = int(self.slider_volume.get())

        self.save_config()
        self.check_env_file()
        messagebox.showinfo(self.tr("success_title"), self.tr("save_msg"))
        self.append_log("EVENT", self.tr("settings_manually_saved_msg"))

    def save_config(self):
        if getattr(self, "is_loading", False):
            return

        current_text = self.entry_path.get().strip()
        if self.active_bot_key in self.bots:
            if current_text and current_text != self.tr("bot_file_ph"):
                self.bots[self.active_bot_key]["path"] = current_text

            curr = self.bots[self.active_bot_key]
            curr["autostart"] = self.autostart_var.get()
            curr["test_mode"] = self.test_mode_var.get()
            curr["restart_days"] = int(self.slider_r_days.get())
            curr["restart_hours"] = int(self.slider_r_hours.get())
            curr["restart_mins"] = int(self.slider_r_mins.get())
            curr["midnight_restart"] = self.midnight_var.get()
            curr["error_sound"] = self.sound_var.get()
            curr["volume"] = int(self.slider_volume.get())

            script_path = curr["path"]
            if script_path and os.path.exists(script_path):
                bot_dir = os.path.dirname(script_path)
                bot_config_path = os.path.join(bot_dir, "bot_config.json")
                try:
                    cfg_data = {
                        "test_mode": curr["test_mode"],
                        "panel_id": config.PANEL_ID,
                        "panel_dir": SCRIPT_DIR,
                        "version": "1.0.0",
                        "allowed_discord_ids": curr.get("allowed_discord_ids", []),
                        "activity_enabled": curr.get("activity_enabled", True),
                        "activity_type": curr.get("activity_type", "Playing"),
                        "activity_text": curr.get("activity_text", ""),
                        "activity_interval_minutes": curr.get("activity_interval_minutes", 5),
                        "activity_loop": curr.get("activity_loop", [])
                    }
                    with open(bot_config_path, "w", encoding="utf-8") as f:
                        json.dump(cfg_data, f, ensure_ascii=False, indent=4)
                except Exception as e:
                    print(f"Hiba a bot_config.json mentésekor: {e}")

        bots_data = {"active_bot": self.active_bot_key, "bots": {}}
        for k, v in self.bots.items():
            stored_path = v["path"]
            if stored_path:
                try:
                    stored_path = os.path.relpath(stored_path, SCRIPT_DIR)
                except ValueError:
                    pass
            bots_data["bots"][k] = {
                "name": v["name"], "path": stored_path,
                "emoji": v.get("emoji", "🤖"), "color": v.get("color", "#5865F2"),
                "autostart": v["autostart"], "test_mode": v.get("test_mode", False),
                "restart_days": v["restart_days"], "restart_hours": v["restart_hours"],
                "restart_mins": v["restart_mins"],
                "midnight_restart": v.get("midnight_restart", False),
                "error_sound": v["error_sound"], "volume": v.get("volume", 50),
                "allowed_discord_ids": v.get("allowed_discord_ids", []),
                "total_commands": v["total_commands"],
                "weekly_uptime_seconds": v["weekly_uptime_seconds"],
                "auto_restart_on_crash": v.get("auto_restart_on_crash", False),
                "crash_restart_delay": v.get("crash_restart_delay", 10),
                "activity_enabled": v.get("activity_enabled", True),
                "activity_type": v.get("activity_type", "Playing"),
                "activity_text": v.get("activity_text", ""),
                "activity_interval_minutes": v.get("activity_interval_minutes", 5),
                "activity_loop": v.get("activity_loop", [])
            }

        try:
            with open(BOTS_FILE, "w", encoding="utf-8") as f:
                json.dump(bots_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Hiba bots.json mentéskor: {e}")

        settings_data = {
            "sidebar_collapsed_sections": list(getattr(self, "sidebar_collapsed_sections", set())),
            "panel_id": config.PANEL_ID, "language": self.current_language,
            "minimize_to_tray": self.minimize_to_tray_enabled,
            "panel_password": self.panel_password,
            "error_sound_type": self.selected_error_sound,
            "theme": self.current_theme,
            "custom_icon": os.path.relpath(self.custom_icon_path, SCRIPT_DIR) if self.custom_icon_path else "",
            "log_save_level": self.log_save_level, "max_ram_mb": self.max_ram_mb,
            "task_kill_enabled": self.task_kill_enabled, "rpc_enabled": self.rpc_enabled,
            "backup_enabled": self.backup_enabled, "backup_on_start": self.backup_on_start,
            "backup_interval_hours": self.backup_interval_hours,
            "backup_last_run": self.backup_last_run,
            "last_report_month": getattr(self, "last_report_month", ""),
            "dashboard_layout": getattr(self, "dashboard_layout", []),
            "ai_provider": getattr(self, "ai_provider", "OpenAI (GPT)"),
            "ai_api_key": getattr(self, "ai_api_key", ""),
            "ai_model": getattr(self, "ai_model", ""),
            "afk_enabled": getattr(self, "afk_enabled", True),
            "afk_idle_seconds": getattr(self, "afk_idle_seconds", 60),
            "skipped_version": getattr(self, "skipped_version", ""),
            "update_check_interval_minutes": getattr(self, "update_check_interval_minutes", 60),
            "quiet_hours_enabled": getattr(self, "quiet_hours_enabled", False),
            "quiet_hours_start": getattr(self, "quiet_hours_start", "22:00"),
            "quiet_hours_end": getattr(self, "quiet_hours_end", "06:00"),
            # --- LAN ---
            "lan_enabled": getattr(self, "lan_enabled", False),
            "lan_port": getattr(self, "lan_port", 8765),
            "lan_token": getattr(self, "lan_token", ""),
            "lan_allow_control": getattr(self, "lan_allow_control", True),
            "lan_client_host": getattr(self, "lan_client_host", ""),
            "lan_client_port": getattr(self, "lan_client_port", 8765),
            "lan_client_token": getattr(self, "lan_client_token", ""),
        }
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(settings_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Hiba settings.json mentéskor: {e}")

    # ---------- ÉRTÉK NORMALIZÁLÁS (visszafele kompatibilitás) ----------

    def _normalize_log_level(self, value):
        """A régi magyar értékeket átalakítja fix kulcsokra.

        Régi → új:
            "Mindent mentse"        → "all"
            "Csak hibák"            → "errors"
            "Csak események"        → "events"
            "Sikeres interakciók"   → "success"
        """
        legacy_map = {
            "Mindent mentse": "all",
            "Csak hibák": "errors",
            "Csak események": "events",
            "Sikeres interakciók": "success",
        }
        if value in legacy_map:
            return legacy_map[value]
        if value in ("all", "errors", "events", "success"):
            return value
        return "all"

    def _normalize_sound_key(self, value):
        """A régi magyar hangneveket átalakítja fix kulcsokra."""
        try:
            from modules.sounds import _normalize_key
            return _normalize_key(value)
        except Exception:
            return "beep"
            
    def load_config(self):
        if os.path.exists(BOTS_FILE):
            try:
                with open(BOTS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for k, v in data.get("bots", {}).items():
                    configured_path = v.get("path", "")
                    if configured_path and not os.path.isabs(configured_path):
                        configured_path = os.path.abspath(os.path.join(SCRIPT_DIR, configured_path))
                    b_data = self.create_bot_data(v.get("name", k), configured_path)
                    b_data["emoji"] = v.get("emoji", "🤖")
                    b_data["color"] = v.get("color", "#5865F2")
                    b_data["autostart"] = v.get("autostart", False)
                    b_data["test_mode"] = v.get("test_mode", False)
                    b_data["restart_days"] = v.get("restart_days", 0)
                    b_data["restart_hours"] = v.get("restart_hours", 0)
                    b_data["restart_mins"] = v.get("restart_mins", 0)
                    b_data["midnight_restart"] = v.get("midnight_restart", False)
                    b_data["error_sound"] = v.get("error_sound", False)
                    b_data["volume"] = v.get("volume", 50)
                    b_data["allowed_discord_ids"] = v.get("allowed_discord_ids", [])
                    b_data["total_commands"] = v.get("total_commands", 0)
                    b_data["weekly_uptime_seconds"] = v.get("weekly_uptime_seconds", 0)
                    b_data["auto_restart_on_crash"] = v.get("auto_restart_on_crash", False)
                    b_data["crash_restart_delay"] = v.get("crash_restart_delay", 10)
                    b_data["activity_enabled"] = v.get("activity_enabled", True)
                    b_data["activity_type"] = v.get("activity_type", "Playing")
                    b_data["activity_text"] = v.get("activity_text", "")
                    b_data["activity_interval_minutes"] = v.get("activity_interval_minutes", 5)
                    b_data["activity_loop"] = v.get("activity_loop", [])
                    self.bots[k] = b_data
                self.active_bot_key = data.get("active_bot", list(self.bots.keys())[0] if self.bots else "Main Bot")
            except Exception as e:
                print(f"Hiba bots.json betöltéskor: {e}")

        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    s_data = json.load(f)
                stored_panel_id = s_data.get("panel_id", "")
                if isinstance(stored_panel_id, str) and stored_panel_id.startswith("#") and stored_panel_id != "#00001":
                    config.PANEL_ID = stored_panel_id
                else:
                    config.PANEL_ID = "#" + secrets.token_hex(8).upper()
                self.current_language = s_data.get("language", "English")
                if self.current_language not in LANGUAGES:
                    self.current_language = "English"
                self.minimize_to_tray_enabled = s_data.get("minimize_to_tray", True)
                self.panel_password = s_data.get("panel_password", "")
                self.selected_error_sound = self._normalize_sound_key(s_data.get("error_sound_type", "beep"))
                self.current_theme = s_data.get("theme", DEFAULT_THEME)
                self.custom_icon_path = s_data.get("custom_icon", "")
                if self.custom_icon_path and not os.path.isabs(self.custom_icon_path):
                    self.custom_icon_path = os.path.abspath(os.path.join(SCRIPT_DIR, self.custom_icon_path))
                self.log_save_level = self._normalize_log_level(s_data.get("log_save_level", "all"))
                self.max_ram_mb = s_data.get("max_ram_mb", 200)
                self.task_kill_enabled = s_data.get("task_kill_enabled", False)
                self.rpc_enabled = s_data.get("rpc_enabled", True)
                self.backup_enabled = s_data.get("backup_enabled", True)
                self.backup_on_start = s_data.get("backup_on_start", False)
                self.backup_interval_hours = max(0, int(s_data.get("backup_interval_hours", 24)))
                self.backup_last_run = s_data.get("backup_last_run", "")
                self.last_report_month = s_data.get("last_report_month", "")
                self.dashboard_layout = s_data.get("dashboard_layout", [])
                self.ai_provider = s_data.get("ai_provider", "OpenAI (GPT)")
                self.ai_api_key = s_data.get("ai_api_key", "")
                self.ai_model = s_data.get("ai_model", "")
                self.afk_enabled = s_data.get("afk_enabled", True)
                self.afk_idle_seconds = s_data.get("afk_idle_seconds", 60)
                self.skipped_version = s_data.get("skipped_version", "")
                self.update_check_interval_minutes = s_data.get("update_check_interval_minutes", 60)
                self.quiet_hours_enabled = s_data.get("quiet_hours_enabled", False)
                self.quiet_hours_start = s_data.get("quiet_hours_start", "22:00")
                self.quiet_hours_end = s_data.get("quiet_hours_end", "06:00")
                # --- LAN ---
                self.lan_enabled = s_data.get("lan_enabled", False)
                self.lan_port = s_data.get("lan_port", 8765)
                self.lan_token = s_data.get("lan_token", "")
                self.lan_allow_control = s_data.get("lan_allow_control", True)
                self.lan_client_host = s_data.get("lan_client_host", "")
                self.lan_client_port = s_data.get("lan_client_port", 8765)
                self.lan_client_token = s_data.get("lan_client_token", "")
                # --- Lenyitható szekciók betöltése ---
                collapsed = s_data.get("sidebar_collapsed_sections", [])
                if isinstance(collapsed, list):
                    self.sidebar_collapsed_sections = set(collapsed)
                else:
                    self.sidebar_collapsed_sections = set()

            except Exception as e:
                print(f"Hiba settings.json betöltéskor: {e}")

        if not self.bots:
            self.bots["Main Bot"] = self.create_bot_data("Main Bot")
            self.active_bot_key = "Main Bot"

    # ---------- ABLAK BEZÁRÁS / TÁLCA ----------

    def on_window_close(self):
        if not self.minimize_to_tray_enabled:
            self.perform_exit()
            return
        self.withdraw()
        if hasattr(self, "tray_icon"):
            return
        try:
            image = Image.open(DISCORD_ICON_PATH).convert("RGBA") if os.path.isfile(DISCORD_ICON_PATH) else Image.new("RGBA", (64, 64), color=(88, 101, 242))
        except Exception:
            image = Image.new("RGBA", (64, 64), color=(88, 101, 242))

        def show_panel(icon, item):
            icon.stop()
            self.tray_icon = None
            self.after(0, self.authenticate_and_show)

        def quit_panel(icon, item):
            icon.stop()
            self.after(0, self.perform_exit)

        menu = pystray.Menu(
            pystray.MenuItem(self.tr("tray_open"), show_panel, default=True),
            pystray.MenuItem(self.tr("tray_quit"), quit_panel)
        )
        self.tray_icon = pystray.Icon("BotManager", image, "Bot Manager", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def authenticate_and_show(self):
        if not self.panel_password:
            self.deiconify()
            return
        self.prompt_startup_password()

    def stop_tray(self):
        tray = getattr(self, "tray_icon", None)
        if tray:
            tray.stop()
            self.tray_icon = None

    def _reveal(self):
        """A panel megjelenítése a splash után."""
        try:
            self.deiconify()
            self.lift()
            self.focus_force()
        except Exception as e:
            print(f"[REVEAL] Hiba: {e}")

    def perform_exit(self, icon=None, item=None):
        self.is_monitoring = False
        self.rpc_enabled = False
        self.stop_afk_screen()
        if hasattr(self, 'tray_icon'):
            self.stop_tray()
        self.save_config()
        for bot in self.bots.values():
            if bot["is_running"] and bot["process"]:
                bot["process"].terminate()
        self.destroy()


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", category=ResourceWarning)

    app = BotManagerApp()

    def finish_splash():
        """A splash befejezése és a panel megjelenítése."""
        try:
            if getattr(app, "_splash", None) is not None:
                app._splash.finish()
        except Exception:
            pass

        # 1.2 sec múlva jelenjen meg a panel (fade-out közben)
        app.after(1200, app._reveal)

    # 1.5 sec animáció után jöhet a panel
    app.after(1500, finish_splash)
    app.mainloop()