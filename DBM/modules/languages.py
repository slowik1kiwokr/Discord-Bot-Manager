"""
Központi nyelvi szótár — minden panel szöveg egy helyen.
Konvenció:
    _btn    = gomb
    _title  = cím / ablak cím
    _section = szekció fejléc
    _lbl    = label
    _ph     = placeholder (bemeneti mező)
    _msg    = üzenet (messagebox, toast)
    _status = állapot szöveg
    _hint   = tipp / leírás
    _cat    = kategória
"""

import json
from modules.config import LANG_FILE


LANGUAGES = {
    "English": {
        # =============================================================
        #  PANEL / ÁLTALÁNOS
        # =============================================================
        "panel_title": "Discord Bot Manager - Professional Multi-Bot Panel",
        "online_status": "● ONLINE",
        "offline_status": "● OFFLINE",
        "unavailable": "N/A",
        "warning_title": "Warning",
        "error_title": "Error",
        "info_title": "Information",
        "success_title": "Success",
        "confirm_btn": "Confirm",
        "close_btn": "Close",
        "cancel_btn": "Cancel",
        "save_btn": "Save",
        "delete_btn": "Delete",
        "edit_btn": "Edit",
        "rename_btn": "Rename",
        "refresh_btn": "Refresh",
        "save_msg": "Saved successfully!",
        "copied_msg": "Copied",
        "days_short": "d",
        "hours_short": "h",
        "minutes_short": "m",

        # =============================================================
        #  SIDEBAR — SZEKCIÓK
        # =============================================================
        "control_section": "Control",
        "bulk_control_section": "Bulk Control",
        "tools_section": "Tools & Integration",
        "stats_section": "Statistics & System",
        "system_section": "System",
        "ai_section": "AI & Extras",

        # =============================================================
        #  SIDEBAR — GOMBOK
        # =============================================================
        "dashboard_btn": "Dashboard",
        "bot_start_btn": "Start Bot",
        "bot_restart_btn": "Restart",
        "bot_stop_btn": "Stop",
        "start_all_btn": "Start All",
        "restart_all_btn": "Restart All",
        "stop_all_btn": "Stop All",
        "commander_btn": "Commander",
        "plugins_btn": "Plugins",
        "appearance_btn": "Appearance",
        "integration_btn": "Basics / Integration",
        "global_stats_btn": "Global Statistics",
        "dashboard_widget_btn": "Dashboard",
        "live_charts_btn": "Live Charts",
        "panel_stats_btn": "Panel Statistics",
        "monthly_report_btn": "Monthly Report",
        "broadcast_btn": "Broadcast",
        "backup_btn": "Backups",
        "sqlite_btn": "SQLite Viewer",
        "settings_btn": "Settings",
        "tutorial_btn": "Tutorial",
        "github_update_btn": "GitHub Update",
        "ai_assistant_btn": "AI Assistant",
        "ai_code_gen_btn": "AI Code Generator",
        "ai_docs_btn": "AI Documentation",
        "achievements_btn": "Achievements",
        "copy_command_btn": "Copy command",
        "add_bot_btn": "+",
        "toggle_sidebar_btn": "☰",

        # =============================================================
        #  FELSŐ SÁV — BOT FÁJLOK KÁRTYA
        # =============================================================
        "bot_files_section": "BOT FILES",
        "bot_file_lbl": "Main bot file:",
        "bot_file_ph": "Browse for the main .py file...",
        "env_ok": "🔑 .env: OK",
        "env_missing": "🔑 .env: Missing",
        "env_na": "🔑 .env: N/A",
        "browse_btn": "Browse",

        # =============================================================
        #  FELSŐ SÁV — PANEL VISELKEDÉS KÁRTYA
        # =============================================================
        "behavior_section": "PANEL BEHAVIOR",
        "autostart_lbl": "Auto-start",
        "error_sound_lbl": "Error sound",
        "midnight_restart_lbl": "Midnight Restart",
        "auto_restart_lbl": "Auto Restart:",

        # =============================================================
        #  FELSŐ SÁV — BOT INFO KÁRTYA
        # =============================================================
        "bot_info_section": "BOT INFO",
        "servers_btn": "Servers",
        "bot_data_btn": "Bot Data",
        "activity_btn": "Activity",
        "test_mode_lbl": "Test Mode",

        # =============================================================
        #  NAPLÓK
        # =============================================================
        "live_logs_title": "Live Logs",
        "filter_all_btn": "ALL",
        "filter_errors_btn": "ERRORS",
        "filter_success_btn": "SUCCESS",
        "filter_events_btn": "EVENTS",
        "autoscroll_lbl": "Auto-scroll",
        "clear_logs_btn": "Clear",
        "log_search_ph": "🔍 Search logs...",
        "log_write_error": "[LOG] Write error: {error}",
        "remote_response_save_error": "Remote response save error: {error}",

        # =============================================================
        #  PRO METRIKÁK
        # =============================================================
        "metrics_section": "📊 Pro Metrics",
        "open_charts_btn": "📈 Performance Chart",
        "bot_information_section": "Bot Information",
        "pc_resources_section": "PC Resources",
        "bot_name_lbl": "Bot Name",
        "bot_version_lbl": "Bot Version",
        "uptime_lbl": "Uptime (Session)",
        "weekly_uptime_lbl": "Weekly Uptime",
        "ping_lbl": "Ping Response",
        "total_commands_lbl": "Total Commands",
        "ram_lbl": "RAM Usage",
        "cpu_lbl": "CPU Usage",
        "temperature_pc_lbl": "PC Temperature",
        "guilds_lbl": "Servers (Guilds)",
        "users_lbl": "Users Reached",
        "error_counter_lbl": "Error Counter",

        # =============================================================
        #  SETTINGS ABLAK
        # =============================================================
        "settings_title": "Settings",
        "settings_header": "⚙️  Settings",
        "settings_tab_panel": "Panel Settings",
        "settings_tab_bot": "Bot Settings",
        "settings_save_close_btn": "💾  Save & Close",
        "settings_saved_status": "✅ Settings saved",
        "settings_saved_toast": "💾 Settings saved",

        # Settings — szekciók
        "settings_sec_security": "Security",
        "settings_sec_appearance": "Appearance",
        "settings_sec_notifications": "Notifications",
        "settings_sec_logs": "Logs",
        "settings_sec_afk": "AFK Screen",
        "settings_sec_backup": "Backup",
        "settings_sec_github": "GitHub Updates",
        "settings_sec_ai": "AI Settings",
        "settings_sec_resources": "Resources",
        "settings_sec_test_mode": "Test Mode",
        "settings_sec_crash": "Crash Handling",

        # Settings — mezők
        "settings_password_lbl": "Panel password (empty = disabled)",
        "settings_language_lbl": "Language:",
        "settings_theme_lbl": "Theme:",
        "settings_tray_switch": "Minimize to tray on close",
        "settings_rpc_switch": "Discord Rich Presence",
        "settings_error_sound_lbl": "Error sound:",
        "settings_sound_test_btn": "🔊 Test",
        "settings_log_level_lbl": "File log level:",
        "settings_log_all": "Save everything",
        "settings_log_errors": "Only errors",
        "settings_log_events": "Only events",
        "settings_log_success": "Successful interactions",
        "settings_afk_hint": "Shows a fullscreen bot status view when idle.",
        "settings_afk_switch": "Enable AFK screen",
        "settings_afk_timeout_lbl": "Idle time:",
        "settings_afk_preview_btn": "👁 Preview",
        "settings_backup_switch": "Automatic backup",
        "settings_backup_start_switch": "Backup on panel startup",
        "settings_backup_interval_lbl": "Scheduled backup interval (hours, 0 = off):",
        "settings_backup_manager_btn": "📂 Open backup manager",
        "settings_github_hint": "The panel checks GitHub for updates automatically.",
        "settings_update_interval_lbl": "Update check interval:",
        "settings_update_check_now_btn": "🔄 Check now",
        "settings_update_history_btn": "📜 Update history",
        "settings_ai_model_lbl": "Model:",
        "settings_max_ram_lbl": "Maximum RAM usage (MB):",
        "settings_max_ram_hint": "If the bot exceeds this, the panel warns you.",
        "settings_test_switch": "Enable Test Mode",
        "settings_testers_lbl": "Tester Discord IDs (comma-separated):",
        "settings_testers_hint": "Only these IDs can use the bot while test mode is active.",
        "settings_crash_switch": "Auto-Restart on Crash",
        "settings_crash_delay_lbl": "Restart delay (seconds):",
        "settings_err_backup_interval": "❌ Invalid backup interval",
        "settings_err_crash_delay": "❌ Invalid crash delay",
        "settings_err_ram": "❌ Invalid RAM value",

        # =============================================================
        #  HANG NEVEK
        # =============================================================
        "sound_beep": "Basic (Beep)",
        "sound_double_beep": "Double Beep",
        "sound_buzz": "Deep Error (Buzz)",
        "sound_triple_beep": "Triple Beep",
        "sound_slow_buzz": "Slow Buzz",
        "sound_fast_double": "Fast Double",
        "sound_long_cry": "Long Cry",
        "sound_none": "No sound",

        # =============================================================
        #  AFK IDŐZÍTŐ OPCIÓK
        # =============================================================
        "afk_timeout_15s": "15 seconds",
        "afk_timeout_30s": "30 seconds",
        "afk_timeout_1m": "1 minute",
        "afk_timeout_2m": "2 minutes",
        "afk_timeout_5m": "5 minutes",
        "afk_timeout_10m": "10 minutes",
        "afk_timeout_30m": "30 minutes",

        # =============================================================
        #  UPDATE ELLENŐRZÉSI OPCIÓK
        # =============================================================
        "update_interval_never": "Never",
        "update_interval_1min": "Every minute",
        "update_interval_10min": "Every 10 minutes",
        "update_interval_1hour": "Every hour",
        "update_interval_1day": "Every day",

        # =============================================================
        #  DIALÓGUS ABLAKOK — ÚJ BOT / TÖRLÉS
        # =============================================================
        "new_bot_title": "New Bot",
        "new_bot_prompt": "Enter the new bot name:",
        "duplicate_bot_msg": "A bot with this name already exists.",
        "delete_bot_confirm": "Are you sure you want to delete '{name}' bot?",
        "default_bot_no_delete": "The default bot cannot be deleted!",
        "last_bot_no_delete_msg": "The last bot cannot be deleted!",
        "delete_bot_confirm_short": "Are you sure you want to delete this bot?",
        "bot_script_missing_msg": "The bot's .py file is missing!",
        "bot_data_saved_msg": "✅ Bot data saved: {name}",

        # =============================================================
        #  BOT ADATAI ABLAK
        # =============================================================
        "bot_data_title": "Bot Data",
        "bot_data": "Bot Data",
        "bot_name": "Bot Name",
        "bot_version": "Bot Version",
        "bot_prefix": "Bot Prefix",
        "bot_info_hint": "⚠️ The token is sensitive data. Do not share it!",
        "bot_info_token_placeholder": "Enter bot token...",
        "save": "Save",
        "close": "Close",

        # =============================================================
        #  BROADCAST
        # =============================================================
        "broadcast_title": "Broadcast",
        "broadcast_header": "📢  Broadcast",
        "broadcast_servers_count": "🌐 Servers: {count}",
        "broadcast_servers_section": "Servers and channels",
        "broadcast_channels_hint": "Check the channels you want to send to.\nGrayed channels = bot cannot write there.",
        "broadcast_no_channels_msg": "No servers found.\nRun the bot first!",
        "broadcast_select_all_btn": "✅ All",
        "broadcast_deselect_all_btn": "❌ None",
        "broadcast_template_lbl": "Template:",
        "broadcast_schedule_section": "⏰ Schedule (optional)",
        "broadcast_schedule_check": "Delayed sending",
        "broadcast_when_lbl": "Send in:",
        "broadcast_preview_btn": "👁 Preview",
        "broadcast_preview_title": "Preview",
        "broadcast_preview_time": "Today at 12:00",
        "broadcast_send_btn": "📢 Send Broadcast",
        "broadcast_empty_msg": "(empty message)",
        "broadcast_need_bot_msg": "Browse a valid bot .py file first!",
        "broadcast_no_channel_msg": "Select at least one channel!",
        "broadcast_msg_empty_msg": "The message cannot be empty!",
        "broadcast_embed_empty_msg": "The embed needs a title or description!",
        "broadcast_send_error_msg": "Send error: {error}",
        "broadcast_scheduled_toast": "⏰ Broadcast scheduled: {minutes} min",
        "broadcast_scheduled_log": "Broadcast scheduled ({bot}) — {count} channels",
        "broadcast_sent_toast": "✅ Broadcast sent to {count} channels",
        "broadcast_sent_log": "Broadcast sent ({bot}) — {count} channels",

        # =============================================================
        #  BROADCAST — KÖZÖS MEZŐK (commander is használja)
        # =============================================================
        "broadcast_type_lbl": "Type:",
        "broadcast_type_message": "Message",
        "broadcast_type_embed": "Embed",
        "broadcast_content_lbl": "Message content:",
        "broadcast_embed_title_lbl": "Embed title:",
        "broadcast_embed_desc_lbl": "Embed description:",
        "broadcast_footer_lbl": "Footer:",
        "broadcast_thumb_lbl": "Thumbnail URL:",
        "broadcast_color_lbl": "Color:",
        "broadcast_quick_lbl": "Quick:",

        # =============================================================
        #  BROADCAST SABLONOK
        # =============================================================
        "bc_tpl_simple_name": "📝 Simple message",
        "bc_tpl_simple_content": "Hello everyone! 👋\nThis is a test message.",

        "bc_tpl_maintenance_name": "🔧 Maintenance",
        "bc_tpl_maintenance_title": "🔧 Scheduled Maintenance",
        "bc_tpl_maintenance_desc": "The bot will be temporarily unavailable due to maintenance.\nWe'll be back soon!",
        "bc_tpl_maintenance_footer": "Thank you for your patience!",

        "bc_tpl_new_version_name": "🚀 New version",
        "bc_tpl_new_version_title": "🚀 New Version Available!",
        "bc_tpl_new_version_desc": "A new version of the bot has been released.\nCheck the changelog for details!",
        "bc_tpl_new_version_footer": "Update now!",

        "bc_tpl_event_name": "🎉 Event",
        "bc_tpl_event_title": "🎉 Special Event!",
        "bc_tpl_event_desc": "Join us for a special event!\nDon't miss out!",
        "bc_tpl_event_footer": "See you there!",

        "bc_tpl_warning_name": "⚠️ Warning",
        "bc_tpl_warning_title": "⚠️ Important Warning",
        "bc_tpl_warning_desc": "Please read this important notice carefully.",
        "bc_tpl_warning_footer": "Thank you for your attention!",

        "bc_tpl_outage_name": "🚨 Outage",
        "bc_tpl_outage_title": "🚨 Service Outage",
        "bc_tpl_outage_desc": "We are currently experiencing technical difficulties.\nWe're working on it!",
        "bc_tpl_outage_footer": "We apologize for the inconvenience.",

        "bc_tpl_custom_name": "✏️ Custom embed",
        "bc_tpl_custom_title": "Custom Title",
        "bc_tpl_custom_desc": "Write your own description here...",

        "bc_tpl_sysinfo_name": "🖥️ System info",
        "bc_tpl_sysinfo_title": "🖥️ System Information",
        "bc_tpl_sysinfo_desc": "Current bot and system status:",
        "bc_tpl_sysinfo_footer": "Auto-generated",
        "bc_tpl_sysinfo_field1_name": "Bot Status",
        "bc_tpl_sysinfo_field1_value": "🟢 Online",
        "bc_tpl_sysinfo_field2_name": "Uptime",
        "bc_tpl_sysinfo_field2_value": "0h 0m",

        # =============================================================
        #  IDŐZÍTÉS OPCIÓK
        # =============================================================
        "sched_1min": "1 minute",
        "sched_5min": "5 minutes",
        "sched_10min": "10 minutes",
        "sched_30min": "30 minutes",
        "sched_1hour": "1 hour",
        "sched_6hour": "6 hours",
        "sched_24hour": "24 hours",

        # =============================================================
        #  COMMANDER
        # =============================================================
        "commander_title": "Commander & File Manager",
        "commander_header": "⚡  Commander",
        "commander_bot_folder_lbl": "Bot folder",
        "commander_tab_editor": "Editor",
        "commander_tab_commands": "Commander",
        "commander_tab_extensions": "Extensions",
        "commander_select_file_lbl": "Select a file from the tree",
        "commander_save_editor_btn": "💾 Save",
        "commander_new_file_btn": "➕ File",
        "commander_new_folder_btn": "📁 Folder",
        "commander_rename_btn": "✏️ Rename",
        "commander_delete_btn": "🗑️ Delete",
        "commander_commands_lbl": "Custom commands (commander_commands.json)",
        "commander_new_command_btn": "➕ New command",
        "commander_extensions_lbl": "Extensions",
        "commander_extensions_hint": "Extensions loaded automatically from bot_extensions.txt.",
        "commander_add_extension_btn": "➕ Add",
        "commander_save_extensions_btn": "💾 Save",
        "commander_need_bot_msg": "Browse a valid bot .py file first!",

        # Commander — parancs szerkesztő
        "commander_editor_title_new": "➕ New Command",
        "commander_editor_title_edit": "✏️ Edit Command",
        "commander_templates_section": "🎨 Templates",
        "commander_templates_hint": "Pick a template — fields fill automatically, then edit freely.",
        "commander_data_section": "📋 Command Data",
        "commander_options_section": "⚙️ Options",
        "commander_name_lbl": "Command name (without slash):",
        "commander_desc_lbl": "Description (shown in Discord / menu):",
        "commander_ephemeral_lbl": "Visible only to caller (ephemeral)",
        "commander_enabled_lbl": "Command enabled",
        "commander_save_command_btn": "💾 Save Command",
        "commander_default_description": "Custom command",

        # Commander — üzenetek
        "commander_binary_file_msg": "Cannot open binary file!",
        "commander_no_open_file_msg": "No file is open!",
        "commander_syntax_error_title": "Syntax Error",
        "commander_syntax_error_msg": "Line {line}: {msg}\n\nSave anyway?",
        "commander_saved_status": "✅ Saved: {name}",
        "commander_saved_toast": "✅ Saved: {name}",
        "commander_created_toast": "✅ Created: {name}",
        "commander_file_exists_msg": "A file with this name already exists!",
        "commander_add_extension_title": "New extension",
        "commander_add_extension_prompt": "Extension name (e.g. cogs.commands):",
        "commander_add_extension_confirm": "Add '{ext}' extension to auto-load list?",
        "commander_name_empty_msg": "Command name cannot be empty!",
        "commander_name_invalid_msg": "Only letters, numbers and underscore allowed!",
        "commander_name_exists_msg": "A command named '{name}' already exists!",
        "commander_no_commands_msg": "No custom commands yet.",
        "commander_no_extensions_msg": "No extensions added yet.",
        "commander_extensions_saved_msg": "✅ Extensions saved",
        "commander_rename_title": "Rename",
        "commander_rename_prompt": "New name:",
        "commander_new_file_title": "New File",
        "commander_new_file_prompt": "File name (e.g. command.py):",
        "commander_new_folder_title": "New Folder",
        "commander_new_folder_prompt": "Folder name:",
        "commander_delete_item_title": "Delete",
        "commander_delete_item_confirm": "Are you sure you want to delete '{name}'?",
        "commander_delete_command_title": "Delete Command",
        "commander_delete_command_confirm": "Are you sure you want to delete command '{name}'?",

        # =============================================================
        #  COMMANDER SABLONOK
        # =============================================================
        "cmd_tpl_simple_name": "📝 Simple message",
        "cmd_tpl_simple_desc": "Simple text command",
        "cmd_tpl_simple_content": "Hello! 👋",

        "cmd_tpl_welcome_name": "👋 Welcome",
        "cmd_tpl_welcome_desc": "Welcome message",
        "cmd_tpl_welcome_content": "Welcome to the server! 🎉",

        "cmd_tpl_announcement_name": "📢 Announcement",
        "cmd_tpl_announcement_desc": "Server announcement",
        "cmd_tpl_announcement_content": "📢 Important announcement!",

        "cmd_tpl_simple_embed_name": "📄 Simple embed",
        "cmd_tpl_simple_embed_desc": "Basic embed message",
        "cmd_tpl_simple_embed_title": "Hello!",
        "cmd_tpl_simple_embed_description": "This is a simple embed.",
        "cmd_tpl_simple_embed_footer": "Powered by DBM",

        "cmd_tpl_error_embed_name": "❌ Error embed",
        "cmd_tpl_error_embed_desc": "Error message (ephemeral)",
        "cmd_tpl_error_embed_title": "❌ Error",
        "cmd_tpl_error_embed_description": "Something went wrong.",
        "cmd_tpl_error_embed_footer": "Please try again",

        "cmd_tpl_success_embed_name": "✅ Success embed",
        "cmd_tpl_success_embed_desc": "Success message (ephemeral)",
        "cmd_tpl_success_embed_title": "✅ Success",
        "cmd_tpl_success_embed_description": "Operation completed successfully.",

        "cmd_tpl_warning_embed_name": "⚠️ Warning embed",
        "cmd_tpl_warning_embed_desc": "Warning message",
        "cmd_tpl_warning_embed_title": "⚠️ Warning",
        "cmd_tpl_warning_embed_description": "Please read this carefully.",

        "cmd_tpl_help_name": "❓ Help menu",
        "cmd_tpl_help_desc": "Help with commands",
        "cmd_tpl_help_title": "❓ Help",
        "cmd_tpl_help_description": "Available commands:",
        "cmd_tpl_help_footer": "Type /help for more",
        "cmd_tpl_help_f1_name": "/test",
        "cmd_tpl_help_f1_value": "Test the bot",
        "cmd_tpl_help_f2_name": "/info",
        "cmd_tpl_help_f2_value": "Bot information",
        "cmd_tpl_help_f3_name": "/help",
        "cmd_tpl_help_f3_value": "This menu",

        "cmd_tpl_rules_name": "📜 Server rules",
        "cmd_tpl_rules_desc": "Server rules list",
        "cmd_tpl_rules_title": "📜 Server Rules",
        "cmd_tpl_rules_description": "Please follow these rules:",
        "cmd_tpl_rules_footer": "Breaking rules = ban",
        "cmd_tpl_rules_f1_name": "1. Be respectful",
        "cmd_tpl_rules_f1_value": "Treat everyone with respect.",
        "cmd_tpl_rules_f2_name": "2. No spam",
        "cmd_tpl_rules_f2_value": "Don't spam messages.",
        "cmd_tpl_rules_f3_name": "3. No NSFW",
        "cmd_tpl_rules_f3_value": "No inappropriate content.",
        "cmd_tpl_rules_f4_name": "4. Follow Discord ToS",
        "cmd_tpl_rules_f4_value": "Obey Discord's Terms of Service.",

        "cmd_tpl_info_name": "ℹ️ Info embed",
        "cmd_tpl_info_desc": "General information",
        "cmd_tpl_info_title": "ℹ️ Information",
        "cmd_tpl_info_description": "General info:",
        "cmd_tpl_info_footer": "Last updated today",
        "cmd_tpl_info_f1_name": "Members",
        "cmd_tpl_info_f1_value": "0",
        "cmd_tpl_info_f2_name": "Online",
        "cmd_tpl_info_f2_value": "0",
        "cmd_tpl_info_f3_name": "Bots",
        "cmd_tpl_info_f3_value": "1",

        "cmd_tpl_giveaway_name": "🎁 Giveaway",
        "cmd_tpl_giveaway_desc": "Giveaway announcement",
        "cmd_tpl_giveaway_title": "🎁 Giveaway!",
        "cmd_tpl_giveaway_description": "React to enter the giveaway!",
        "cmd_tpl_giveaway_footer": "Good luck!",
        "cmd_tpl_giveaway_f1_name": "Prize",
        "cmd_tpl_giveaway_f1_value": "Nitro",
        "cmd_tpl_giveaway_f2_name": "Winners",
        "cmd_tpl_giveaway_f2_value": "1",
        "cmd_tpl_giveaway_f3_name": "Ends",
        "cmd_tpl_giveaway_f3_value": "Tomorrow",

        "cmd_tpl_ticket_name": "🎫 Ticket",
        "cmd_tpl_ticket_desc": "Support ticket",
        "cmd_tpl_ticket_title": "🎫 Support Ticket",
        "cmd_tpl_ticket_description": "Need help? Open a ticket!",
        "cmd_tpl_ticket_footer": "Support team",
        "cmd_tpl_ticket_f1_name": "How to open",
        "cmd_tpl_ticket_f1_value": "React with 🎫",
        "cmd_tpl_ticket_f2_name": "Response time",
        "cmd_tpl_ticket_f2_value": "Within 24 hours",
        "cmd_tpl_ticket_f3_name": "Support hours",
        "cmd_tpl_ticket_f3_value": "9:00 - 18:00",

        "cmd_tpl_event_name": "🎉 Event",
        "cmd_tpl_event_desc": "Event announcement",
        "cmd_tpl_event_title": "🎉 Special Event!",
        "cmd_tpl_event_description": "Join us for a special event!",
        "cmd_tpl_event_footer": "Don't miss it!",
        "cmd_tpl_event_f1_name": "Date",
        "cmd_tpl_event_f1_value": "This Saturday",
        "cmd_tpl_event_f2_name": "Time",
        "cmd_tpl_event_f2_value": "20:00",
        "cmd_tpl_event_f3_name": "Place",
        "cmd_tpl_event_f3_value": "Voice channel",

        "cmd_tpl_botinfo_name": "🤖 Bot info",
        "cmd_tpl_botinfo_desc": "Bot information embed",
        "cmd_tpl_botinfo_title": "🤖 Bot Information",
        "cmd_tpl_botinfo_description": "All about the bot:",
        "cmd_tpl_botinfo_footer": "Powered by DBM",
        "cmd_tpl_botinfo_f1_name": "Version",
        "cmd_tpl_botinfo_f1_value": "1.0.0",
        "cmd_tpl_botinfo_f2_name": "Servers",
        "cmd_tpl_botinfo_f2_value": "0",
        "cmd_tpl_botinfo_f3_name": "Uptime",
        "cmd_tpl_botinfo_f3_value": "0h",

        "cmd_tpl_music_name": "🎵 Music list",
        "cmd_tpl_music_desc": "Music commands list",
        "cmd_tpl_music_title": "🎵 Music Commands",
        "cmd_tpl_music_description": "Available music commands:",
        "cmd_tpl_music_f1_name": "/play",
        "cmd_tpl_music_f1_value": "Play a song",
        "cmd_tpl_music_f2_name": "/pause",
        "cmd_tpl_music_f2_value": "Pause playback",
        "cmd_tpl_music_f3_name": "/skip",
        "cmd_tpl_music_f3_value": "Skip current song",
        "cmd_tpl_music_f4_name": "/queue",
        "cmd_tpl_music_f4_value": "Show queue",

        "cmd_tpl_moderation_name": "🔨 Moderation",
        "cmd_tpl_moderation_desc": "Moderation commands",
        "cmd_tpl_moderation_title": "🔨 Moderation",
        "cmd_tpl_moderation_description": "Available moderation commands:",
        "cmd_tpl_moderation_footer": "Use responsibly",
        "cmd_tpl_moderation_f1_name": "/kick",
        "cmd_tpl_moderation_f1_value": "Kick a member",
        "cmd_tpl_moderation_f2_name": "/ban",
        "cmd_tpl_moderation_f2_value": "Ban a member",
        "cmd_tpl_moderation_f3_name": "/clear",
        "cmd_tpl_moderation_f3_value": "Clear messages",

        "cmd_tpl_notification_name": "🔔 Notification",
        "cmd_tpl_notification_desc": "Simple notification",
        "cmd_tpl_notification_title": "🔔 Notification",
        "cmd_tpl_notification_description": "This is a notification.",
        "cmd_tpl_notification_footer": "Read carefully",

        "cmd_tpl_custom_color_name": "🎨 Custom color",
        "cmd_tpl_custom_color_desc": "Embed with custom color",
        "cmd_tpl_custom_color_title": "🎨 Custom Color",
        "cmd_tpl_custom_color_description": "This embed has a custom color.",

        "cmd_tpl_image_name": "🖼️ Image embed",
        "cmd_tpl_image_desc": "Embed with image",
        "cmd_tpl_image_title": "🖼️ Image",
        "cmd_tpl_image_description": "Embed with image:",

        "cmd_tpl_links_name": "🔗 Links",
        "cmd_tpl_links_desc": "Useful links",
        "cmd_tpl_links_title": "🔗 Useful Links",
        "cmd_tpl_links_description": "Important links:",
        "cmd_tpl_links_f1_name": "Website",
        "cmd_tpl_links_f1_value": "https://example.com",
        "cmd_tpl_links_f2_name": "Support",
        "cmd_tpl_links_f2_value": "https://discord.gg/example",
        "cmd_tpl_links_f3_name": "GitHub",
        "cmd_tpl_links_f3_value": "https://github.com/example",

        # =============================================================
        #  SZÍNEK
        # =============================================================
        "color_blurple": "Blurple",
        "color_blue": "Blue",
        "color_green": "Green",
        "color_red": "Red",
        "color_orange": "Orange",
        "color_purple": "Purple",
        "color_teal": "Teal",
        "color_rose": "Rose",
        "color_cyan": "Cyan",
        "color_gold": "Gold",
        "color_mauve": "Mauve",
        "color_graphite": "Graphite",

        # =============================================================
        #  INTEGRÁCIÓ
        # =============================================================
        "integration_title": "Panel Integration",
        "integration_header": "📌  Panel Integration",
        "integration_welcome": "Welcome to the panel integration! 🎉",
        "integration_intro": "The panel uses 3 files on the bot side:\n   • bot.py — the bot main file\n   • panel_integrity.py — all panel functions\n   • version.py — bot name, version, token",
        "integration_have_bot_q": "Do you already have a working bot?",
        "integration_btn_existing": "✅ I have a bot\n(just add integration)",
        "integration_btn_new": "🆕 I'm creating a new bot\n(full template)",
        "integration_steps_title": "📋 Steps",
        "integration_step1": "1. Browse for your bot's main .py file on the panel (📁 Browse).",
        "integration_step2": "2. Click '📥 Add panel integration' below — creates panel_integrity.py.",
        "integration_step3": "3. Open bot.py and add in on_ready():",
        "integration_step4": "4. Restart the bot.",
        "integration_step5": "5. In Discord type: /connect panel_id:<panel ID>",
        "integration_code_title": "📄 panel_integrity.py content",
        "integration_add_btn": "📥 Add panel integration",
        "integration_existing_title": "Existing bot",
        "integration_existing_header": "✅  Add integration to existing bot",
        "integration_new_title": "New bot",
        "integration_new_header": "🆕  Create new bot",
        "integration_new_intro": "The panel generates 3 files. Choose a target folder, or save each file separately.",
        "integration_file_bot_lbl": "📄 1. bot.py — the bot main file",
        "integration_file_panel_lbl": "📄 2. panel_integrity.py — all panel functions",
        "integration_file_version_lbl": "📄 3. version.py — bot name, version, token",
        "integration_token_card_title": "🔑 Bot Token Setup",
        "integration_token_card_hint": "The bot token can be set in the 'Bot Data' window.\nYou can also edit name, version and prefix.",
        "integration_token_edit_btn": "🔑 Edit bot data",
        "integration_generate_all_btn": "📁 Generate all files to a folder",
        "integration_need_bot": "Browse a valid bot .py file first!",
        "integration_saved_title": "Success",
        "integration_saved_msg": "Panel integration saved:\n{dir}",
        "integration_log_saved": "Panel integration saved: {path}",
        "integration_saved_toast": "✅ Integration saved",
        "integration_generated_msg": "Files generated to:\n{folder}",
        "integration_log_generated": "Template generated: {folder}",
        "integration_generated_toast": "✅ Files generated",
        "integration_choose_folder": "Choose target folder",
        "integration_token_need_bot": "Browse a valid bot .py file first!",

        # =============================================================
        #  FÜGGŐSÉGEK
        # =============================================================
        "deps_title": "🔧 Dependencies",
        "deps_header": "🔧  Dependencies",
        "deps_intro": "Check if all required Python packages are installed.",
        "deps_check_btn": "🔍 Check",
        "deps_install_missing_btn": "📥 Install missing",
        "deps_reinstall_btn": "🔄 Reinstall",
        "deps_version": "v{version}",
        "deps_missing": "— missing —",
        "deps_all_ok": "✅ All {total} packages installed ({ok}/{total})",
        "deps_some_missing": "❌ {missing} missing of {total} ({ok}/{total} installed)",
        "deps_info_title": "Information",
        "deps_all_installed": "All required packages are installed!",
        "deps_log_start": "▶ Starting installation ({count} packages)...\n",
        "deps_log_item": "▶ [{idx}/{total}] {pkg}\n",
        "deps_log_error": "❌ {pkg}: {error}\n",
        "deps_log_done": "\n✅ Installation complete!\n",
        "deps_status_installing": "⏳ Installing...",
        "deps_status_item": "⏳ [{idx}/{total}] {pkg}",
        "deps_status_done": "✅ Done",
        "deps_reinstall_title": "Reinstall",
        "deps_reinstall_confirm": "Reinstall all required packages?",
        "deps_output_hint": "— Output will appear here —",
        "integration_deps_btn": "🔧 Dependencies",

        # Függőség leírások
        "dep_customtkinter_desc": "Modern UI toolkit",
        "dep_psutil_desc": "System and process utilities",
        "dep_matplotlib_desc": "Charts and graphs",
        "dep_pystray_desc": "System tray icon",
        "dep_pillow_desc": "Image processing",
        "dep_pypresence_desc": "Discord Rich Presence",
        "dep_discord_desc": "Discord API library",
        "dep_wmi_desc": "Windows temperature info (optional)",
        "dep_requests_desc": "HTTP library (optional)",

        # =============================================================
        #  GITHUB UPDATE
        # =============================================================
        "update_title": "Update",
        "update_window_title": "🚀 Update Available",
        "update_header": "🚀 Update Available!",
        "update_news_default": "📝 What's new",
        "update_changelog_general": "Changes",
        "update_no_changelog": "No changelog available.",
        "update_safe_info": "ℹ️ Backups, plugins, settings and bots are preserved.",
        "update_download_btn": "✅ Download update",
        "update_later_btn": "⏰ Later",
        "update_skip_btn": "❌ Skip",
        "update_history_btn": "📜 Previous updates",
        "update_skip_title": "Skip version",
        "update_skip_confirm": "Skip version {version} until restart?",
        "update_history_window_title": "📜 Update History",
        "update_history_header": "📜  Update History",
        "update_history_current": "Current: v{version}",
        "update_history_current_badge": "CURRENT",
        "update_history_empty": "No update history available.",
        "update_history_no_desc": "(no description)",
        "update_history_refresh_btn": "🔄 Check for updates",
        "update_status_downloading": "⬇️ Downloading...",
        "update_status_extracting": "📦 Extracting...",
        "update_status_preparing": "🔧 Preparing...",
        "update_status_stopping_bots": "🛑 Stopping bots...",
        "update_status_updating_files": "📂 Updating files...",
        "update_status_version": "🏷️ Updating version...",
        "update_status_done": "✅ Update complete!",
        "update_status_error": "❌ Error",
        "update_error_title": "Update error",
        "update_error_msg": "Error during update:\n{error}",
        "update_conn_error": "❌ Could not connect to GitHub!",
        "update_up_to_date": "✅ You have the latest version (v{version})",
        "update_restart_title": "Restart required",
        "update_restart_success": "🎉 Update complete!",
        "update_restart_version": "New version: v{version}",
        "update_restart_msg": "The panel needs to restart to apply the update.",
        "update_restart_safe_info": "ℹ️ Your settings and bots are preserved.",
        "update_restart_now_btn": "🔄 Restart now",
        "update_restart_exit_btn": "🚪 Exit",
        "update_restart_error_title": "Restart error",
        "update_log_version_fetch_error": "[UPDATE] Version fetch error: {error}",
        "update_log_manual_check": "[UPDATE] Manual check started",
        "update_log_auto_disabled": "[UPDATE] Auto-check disabled",
        "update_log_skipped": "[UPDATE] Version skipped: {version}",
        "update_log_installed": "[UPDATE] Installed: v{version}",
        "update_log_restart": "[UPDATE] Restarting panel",
        "update_log_version_write_error": "[UPDATE] Version write error: {error}",

        # =============================================================
        #  BACKUP
        # =============================================================
        "backup_title": "Backup Manager",
        "backup_new": "New backup",
        "backup_restore": "Restore selected",
        "backup_done_title": "Backup",
        "backup_done_msg": "Backup created:\n{path}",
        "backup_error_title": "Backup error",
        "backup_select_title": "Select",
        "backup_select_msg": "Select a backup from the list!",
        "backup_restore_title": "Restore",
        "backup_restore_confirm": "Are you sure you want to restore this backup?\nExisting files will be overwritten!",
        "backup_invalid_path": "Invalid path in archive!",
        "backup_restore_done": "✅ Backup restored!\nRestart the panel.",
        "backup_restore_error_title": "Restore error",
        "refresh": "Refresh",

        # =============================================================
        #  SQLITE
        # =============================================================
        "sqlite_title": "SQLite Database Viewer",
        "sqlite_file": "SQLite .db / .sqlite file",
        "sqlite_file_ph": "SQLite .db / .sqlite file",
        "quick_sql": "Quick SQL query",
        "quick_sql_ph": "Quick SQL query: SELECT * FROM users LIMIT 100",
        "open_table": "Open Table",
        "open_table_btn": "Open Table",
        "run_sql": "Run SQL",
        "run_sql_btn": "Run SQL",
        "browse": "Browse",

        # =============================================================
        #  SERVERS
        # =============================================================
        "server_settings": "Server Settings",
        "servers_title": "Server Settings",
        "servers_need_bot": "Browse a valid bot .py file first!",
        "servers_folder_missing": "No server data folder found:\n{path}",
        "no_servers": "No server JSON files found.",
        "no_servers_msg": "No server JSON files found.",
        "servers_info_line": "{name} | ID: {id} | Members: {members} | v{version}",
        "servers_edit_title": "Edit: {name}",
        "servers_edit_server_lbl": "Edit server: {name}",
        "servers_edit_btn": "Edit",
        "servers_read_error": "Read error: {error}",
        "servers_saved_title": "Save",
        "servers_saved_msg": "Server data saved!",
        "servers_json_error_title": "JSON Error",
        "servers_json_error_msg": "Invalid JSON:\n{error}",
        "servers_save_error": "Save error: {error}",
        "servers_json_unreadable": "(unreadable)",
        "servers_unknown_server": "Unknown server",
        "servers_unknown_id": "?",

        # =============================================================
        #  ACTIVITY
        # =============================================================
        "activity_title": "Discord Activity Loop",
        "activity_loop": "Activity Loop",
        "activity_enabled": "Enable Activity",
        "activity_enabled_lbl": "Enable Activity",
        "activity_interval": "Switch interval (minutes):",
        "activity_interval_lbl": "Switch interval (minutes):",
        "activity_interval_invalid": "Invalid interval value!",
        "activity_text": "Activity text",
        "activity_text_ph": "Activity text",
        "activity_add_btn": "+ Add Activity",
        "add_activity": "+ Add Activity",
        "activity_remove_btn": "-",
        "remove": "-",
        "activity_save_btn": "Save",

        # =============================================================
        #  TUTORIAL
        # =============================================================
        "tutorial_title": "📖 Tutorial",
        "tutorial_window_title": "📖 Tutorial",
        "tutorial_header_text": "📖  Tutorial",
        "tutorial_categories": "📚 Categories",
        "tutorial_categories_lbl": "📚 Categories",
        "tutorial_hint": "💡 Choose a category\n      from the left",
        "github_btn": "🌐 GitHub",
        "tutorial_github_btn": "🌐 GitHub",

        # =============================================================
        #  ACHIEVEMENTS
        # =============================================================
        "achievements_title": "🏆 Achievements",
        "achievements_header_text": "🏆 Achievements — {unlocked}/{total}",
        "achievements_btn": "Achievements",
        "ach_unlocked_toast": "{icon} Achievement unlocked: {name}",
        "ach_unlocked_log": "Achievement unlocked: {name} — {desc}",

        # Achievement nevek + leírások
        "ach_first_start_name": "First Step",
        "ach_first_start_desc": "You started a bot",
        "ach_first_backup_name": "Safe & Sound",
        "ach_first_backup_desc": "You created a backup",
        "ach_first_plugin_name": "Extender",
        "ach_first_plugin_desc": "You created a plugin",
        "ach_first_commander_name": "Commander",
        "ach_first_commander_desc": "You created a Commander command",
        "ach_three_bots_name": "Multitude",
        "ach_three_bots_desc": "You registered 3 bots",
        "ach_five_bots_name": "Fleet",
        "ach_five_bots_desc": "You registered 5 bots",
        "ach_ten_bots_name": "Armada",
        "ach_ten_bots_desc": "You registered 10 bots",
        "ach_uptime_1h_name": "Persistent",
        "ach_uptime_1h_desc": "A bot ran for 1 hour",
        "ach_uptime_10h_name": "Long-runner",
        "ach_uptime_10h_desc": "A bot ran for 10 hours",
        "ach_uptime_100h_name": "Marathoner",
        "ach_uptime_100h_desc": "A bot ran for 100 hours",
        "ach_ten_backups_name": "Collector",
        "ach_ten_backups_desc": "You made 10 backups",
        "ach_error_free_day_name": "Flawless Day",
        "ach_error_free_day_desc": "No errors for a day",
        "ach_appearance_user_name": "Artist",
        "ach_appearance_user_desc": "You set a bot emoji/color",
        "ach_hotkey_user_name": "Quick-fingered",
        "ach_hotkey_user_desc": "You used a hotkey",
        "ach_theme_switcher_name": "Versatile",
        "ach_theme_switcher_desc": "You switched themes",

        # =============================================================
        #  STREAK
        # =============================================================
        "streak_lbl": "🔥 Streak",
        "streak_header": "🔥 STREAK",
        "streak_days": "{days} days",
        "streak_days_lbl": "days",
        "streak_best": "Best: {days} days",
        "streak_best_lbl": "Best: {n} days",
        "streak_short": "🔥 {days}d",
        "streak_started": "🔥 Streak started!",
        "streak_milestone": "🔥 {days} day streak!",
        "streak_progress": "🔥 {days} day streak",
        "streak_log": "Streak: {days} days (best: {best})",

        # =============================================================
        #  AI
        # =============================================================
        "ai_chat_title": "🤖 AI Assistant",
        "ai_chat_header": "🤖  AI Assistant",
        "ai_chat_provider_lbl": "Provider: {provider}",
        "ai_chat_welcome": "👋 Hello! How can I help you today?",
        "ai_chat_placeholder": "Type your question...",
        "ai_send_btn": "📤 Send",
        "ai_input_ph": "Type your question...",
        "ai_generate_btn": "✨ Generate",
        "ai_save_btn": "💾 Save",
        "ai_code_title": "✨ AI Code Generator",
        "ai_codegen_title": "✨ AI Code Generator",
        "ai_codegen_header": "✨  AI Code Generator",
        "ai_codegen_prompt_lbl": "Describe what you need:",
        "ai_codegen_output_lbl": "Generated code:",
        "ai_codegen_generate_btn": "✨ Generate",
        "ai_codegen_save_btn": "💾 Save to bot folder",
        "ai_codegen_status_done": "✅ Code generated",
        "ai_codegen_status_thinking": "⏳ Thinking...",
        "ai_codegen_nothing_to_save": "Nothing to save!",
        "ai_codegen_need_bot_file": "Browse a bot .py file first!",
        "ai_codegen_need_prompt": "Enter a description!",
        "ai_codegen_saved": "✅ Code saved",
        "ai_codegen_log_saved": "AI code saved: {path}",
        "ai_error_title": "🔍 AI Error Analysis",
        "ai_error_header": "🔍  Error Analysis",
        "ai_error_input_lbl": "Error / stack trace:",
        "ai_error_output_lbl": "AI Analysis:",
        "ai_error_analyzing": "⏳ Analyzing...",
        "ai_error_nothing": "No error to analyze!",
        "ai_docs_title": "📄 AI Documentation",
        "ai_docs_header": "📄  Documentation: {filename}",
        "ai_docs_select_file": "Select Python file",
        "ai_docs_filetype": "Python Files",
        "ai_docs_read_error": "Read error: {error}",
        "ai_docs_generating": "⏳ Generating documentation...",
        "ai_docs_save_btn": "💾 Save",
        "ai_docs_saved": "✅ Documentation saved",
        "ai_role_user": "You",
        "ai_role_assistant": "AI",
        "ai_err_no_key": "❌ No API key set! Go to Settings → AI.",
        "ai_err_http": "❌ HTTP Error {code}:\n{body}",
        "ai_err_generic": "❌ Error: {error}",
        "ai_settings_provider_lbl": "Provider:",
        "ai_settings_key_lbl": "API key (OpenAI/Claude):",
        "ai_settings_saved": "✅ AI settings saved",
        "ai_settings_save_btn": "💾 Save",

        # =============================================================
        #  AFK SCREEN
        # =============================================================
        "afk_hint": "💡 Move the mouse or press a key to return",
        "afk_return_hint": "💡 Move the mouse or press a key to return",
        "afk_stat_running": "Running",
        "afk_stat_stopped": "Stopped",
        "afk_stat_error": "Errors",
        "afk_status_stopped": "Stopped",
        "afk_date_format": "{year}. {month} {day}. ({day_name})",
        "afk_no_bots": "No bots registered.",

        # =============================================================
        #  TOAST / ÉRTESÍTÉSEK
        # =============================================================
        "toast_panel_started": "🚀 Panel started!",
        "toast_settings_saved": "💾 Settings saved",
        "toast_backup_created": "💾 Backup created",
        "toast_theme_changed": "🎨 Theme: {name}",
        "toast_bot_started": "▶️ Bot started: {name}",
        "toast_bot_stopped": "🛑 Bot stopped: {name}",
        "toast_bot_crashed": "❌ Bot crashed: {name}",
        "panel_started_log": "Panel started",

        # =============================================================
        #  PASSWORD
        # =============================================================
        "password_title": "Password Required",
        "password_protection_lbl": "🔒 Panel Password Protection",
        "password_prompt": "Enter your password:",
        "password_ph": "Password...",
        "login_btn": "Login",
        "wrong_password_msg": "❌ Wrong password! Try again.",

        # =============================================================
        #  HOTKEYS
        # =============================================================
        "hotkeys_registered_log": "Hotkeys registered",
        "hotkeys_saved": "💾 Saved (hotkey)",
        "hotkeys_save_error": "❌ Error: {error}",
        "hotkeys_backup_done": "💾 Backup created (hotkey)",
        "hotkeys_confirm_title": "Confirm",
        "hotkeys_restart_all_confirm": "Restart all bots?",
        "hotkeys_restart_all_done": "🔄 All bots restarted",
        "hotkeys_error": "❌ Error: {error}",
        "hotkeys_logs_cleared": "🗑️ Logs cleared",
        "hotkeys_help_title": "⌨️ Hotkeys",
        "hotkeys_help_text": (
            "⌨️ Keyboard Shortcuts\n\n"
            "Ctrl+S — Save settings\n"
            "Ctrl+B — Create backup\n"
            "Ctrl+R — Restart all bots\n"
            "Ctrl+F — Search logs\n"
            "Ctrl+L — Clear logs\n"
            "Ctrl+T — Tutorial\n"
            "Ctrl+, — Settings\n"
            "Ctrl+W — Close panel\n"
            "Ctrl+1…9 — Switch bot\n"
            "F1 — Tutorial\n"
            "F2 — This help\n"
            "F5 — Refresh stats"
        ),

        # =============================================================
        #  CHARTS
        # =============================================================
        "charts_title": "📈 Live Performance Charts",
        "charts_header": "📈  Live Charts",
        "charts_hint": "🖱️ Hover • 🔍 Zoom • ✋ Drag",
        "charts_cpu_title": "CPU Usage (%)",
        "charts_ram_title": "RAM Usage (%)",
        "charts_hover_cpu": "CPU: {value}%",
        "charts_hover_ram": "RAM: {value}%",
        "charts_status_collecting": "⏳ Collecting data...",
        "charts_status_last": "📊 CPU: {cpu}% | RAM: {ram}% | Points: {points}",
        "charts_mpl_missing": "matplotlib package is not installed!",

        # =============================================================
        #  DASHBOARD WIDGETEK
        # =============================================================
        "dashboard_title": "📐 Dashboard",
        "dashboard_header": "📐  Dashboard",
        "dashboard_widgets_btn": "⚙️ Widgets",
        "dashboard_refresh_btn": "🔄 Refresh",
        "dashboard_no_widgets": "No widgets enabled.\nClick '⚙️ Widgets' to add some.",
        "dashboard_manager_title": "⚙️ Widget Manager",
        "dashboard_manager_header": "⚙️  Widget Manager",
        "dashboard_manager_hint": "Check the widgets you want to see on the dashboard.",
        "dashboard_save_btn": "💾 Save",
        "dashboard_recent_logs_count": "{count} entries",

        # Widget nevek + leírások
        "widget_uptime_name": "Uptime",
        "widget_uptime_desc": "Session uptime",
        "widget_cpu_name": "CPU",
        "widget_cpu_desc": "System CPU usage",
        "widget_ram_name": "RAM",
        "widget_ram_desc": "System RAM usage",
        "widget_active_bots_name": "Active Bots",
        "widget_active_bots_desc": "Running bots / total",
        "widget_total_bots_name": "Total Bots",
        "widget_total_bots_desc": "Registered bots",
        "widget_error_count_name": "Errors",
        "widget_error_count_desc": "Total errors",
        "widget_commands_name": "Commands",
        "widget_commands_desc": "Total commands",
        "widget_temperature_name": "Temperature",
        "widget_temperature_desc": "PC temperature",
        "widget_server_count_name": "Servers",
        "widget_server_count_desc": "Discord servers",
        "widget_user_count_name": "Users",
        "widget_user_count_desc": "Reached users",
        "widget_recent_logs_name": "Recent Logs",
        "widget_recent_logs_desc": "Last log entries",

        # =============================================================
        #  PANEL STATS
        # =============================================================
        "pstats_title": "📊 Panel Statistics",
        "pstats_header": "📊  Panel Statistics",
        "pstats_overview": "📈 Overview",
        "pstats_card_opens": "Opens",
        "pstats_card_total": "Total time",
        "pstats_card_session": "This session",
        "pstats_dates_section": "📅 Dates",
        "pstats_first_opened": "First opened: {value}",
        "pstats_last_opened": "Last opened: {value}",
        "pstats_top_features": "🔥 Most Used Features",
        "pstats_no_data": "No usage data yet.",
        "pstats_time_format": "{hours}h {minutes}m",
        "pstats_save_btn": "💾 Save",
        "pstats_saved": "✅ Statistics saved",
        "pstats_reset_btn": "🗑️ Reset",
        "pstats_reset_title": "Reset",
        "pstats_reset_confirm": "Reset all panel statistics?",

        # Feature nevek
        "feat_settings": "Settings",
        "feat_backup": "Backup Manager",
        "feat_sqlite": "SQLite Viewer",
        "feat_broadcast": "Broadcast",
        "feat_commander": "Commander",
        "feat_plugins": "Plugins",
        "feat_servers": "Servers",
        "feat_global_stats": "Global Statistics",
        "feat_monthly_report": "Monthly Report",
        "feat_tutorial": "Tutorial",
        "feat_basics": "Basics / Integration",
        "feat_bot_info": "Bot Data",
        "feat_activity": "Activity",
        "feat_perf_charts": "Performance Chart",
        "feat_appearance": "Appearance",
        "feat_animated_charts": "Live Charts",
        "feat_dashboard": "Dashboard",

        # =============================================================
        #  REPORT
        # =============================================================
        "report_title": "Monthly Report",
        "report_header": "📅  Monthly Report",
        "report_month_lbl": "Month:",
        "report_new_month_msg": "A new month has started! Do you want to generate the monthly report for {month}?",
        "report_prev_month_format": "{year}. {month}",
        "report_card_errors": "Errors",
        "report_card_commands": "Commands",
        "report_card_logs": "Log entries",
        "report_card_uptime": "Uptime",
        "report_hours_short": "{hours}h",
        "report_per_bot": "🤖 Per Bot",
        "report_no_data": "No data for this month.",
        "report_bot_stats_line": "⚠️ {errors} errors | ⚡ {commands} commands | 📝 {logs} logs",
        "report_top_commands": "🔥 Top Commands",
        "report_daily_activity": "📊 Daily Activity",
        "report_data_status": "📊 Data from: {month}",
        "report_export_json_btn": "📤 JSON",
        "report_export_text_btn": "📄 Text",
        "report_export_title": "Export",
        "report_export_saved": "✅ Saved: {path}",
        "report_exported_toast": "✅ JSON exported",
        "report_text_exported_toast": "✅ Text exported",
        "report_txt_title": "Monthly Report — {month}",
        "report_txt_total_errors": "Total errors: {count}",
        "report_txt_total_commands": "Total commands: {count}",
        "report_txt_total_uptime": "Total uptime: {hours}h",
        "report_txt_per_bot": "PER BOT",
        "report_txt_bot_header": "Bot: {name}",
        "report_txt_bot_errors": "  Errors: {count}",
        "report_txt_bot_commands": "  Commands: {count}",
        "report_txt_bot_logs": "  Log entries: {count}",
        "report_txt_bot_first": "  First log: {value}",
        "report_txt_bot_last": "  Last log: {value}",
        "report_txt_top_commands": "TOP COMMANDS",
        "report_txt_cmd_line": "  {cmd}: {count}x",
        "report_txt_filetype": "Text file",

        # =============================================================
        #  PLUGINS
        # =============================================================
        "plugins": "Plugins",
        "plugins_help": "Extend the panel with plugins",
        "plugins_list_lbl": "Installed Plugins",
        "plugins_select_hint": "Select a plugin from the list",
        "plugins_loaded_status": "✅ Loaded: {name}",
        "plugins_saved_status": "✅ Saved: {name}",
        "plugins_saved_log": "Plugin saved: {name}",
        "plugins_reloaded_status": "✅ Plugins reloaded",
        "plugins_reloaded_log": "Plugins reloaded",
        "plugins_read_error": "Read error: {error}",
        "plugins_save_error": "Save error: {error}",
        "plugins_syntax_error_title": "Syntax Error",
        "plugins_syntax_error_msg": "Line {line}: {msg}",
        "plugins_new_dialog_title": "New Plugin",
        "plugins_new_dialog_header": "🧩  Create New Plugin",
        "plugins_new_filename_lbl": "Filename:",
        "plugins_new_template_lbl": "Template:",
        "plugins_invalid_filename": "Invalid filename!",
        "plugins_exists_title": "File exists",
        "plugins_exists_confirm": "Overwrite '{name}'?",
        "plugins_created_log": "Plugin created: {name}",
        "plugins_delete_confirm": "Delete plugin '{name}'?",
        "plugins_deleted_log": "Plugin deleted: {name}",
        "plugins_need_select": "Select a plugin first!",
        "plugins_new_btn": "➕ New",
        "plugins_save_btn": "💾 Save",
        "plugins_delete_btn": "🗑️ Delete",
        "plugins_reload_btn": "🔄 Reload",
        "plugins_create_btn": "Create",
        "plugins_load_error": "Failed to load plugin: {file} — {error}",

        # Plugin sablonok
        "plugin_tpl_empty_name": "Empty",
        "plugin_tpl_event_logger_name": "Event Logger",
        "plugin_tpl_sidebar_button_name": "Sidebar Button",
        "plugin_tpl_custom_window_name": "Custom Window",
        "plugin_tpl_welcome_log_name": "Welcome Log",
        "plugin_tpl_bot_watcher_name": "Bot Watcher",
        "plugin_tpl_error_beep_name": "Error Beep",
        "plugin_tpl_calculator_name": "Calculator",
        "plugin_tpl_theme_switcher_name": "Theme Switcher",
        "plugin_tpl_webhook_name": "Webhook",

        # =============================================================
        #  UI ENHANCEMENTS
        # =============================================================
        "ui_search_placeholder": "🔍 Search bots...",
        "ui_status_online_spinner": "● {char} ONLINE",
        "ui_switch_toast": "🤖 Switched to: {name}",
        "ui_appearance_title": "Appearance: {name}",
        "ui_appearance_header": "🎨  Appearance: {name}",
        "ui_emoji_lbl": "Emoji",
        "ui_color_lbl": "Color",
        "ui_custom_hex_lbl": "Custom hex:",
        "ui_apply_btn": "Apply",
        "ui_appearance_saved": "✅ Appearance saved: {name}",
        "ui_save_btn": "💾 Save",
        "ui_cancel_btn": "Cancel",
        "ui_sidebar_opened": "📂 Sidebar opened",
        "ui_sidebar_collapsed": "📁 Sidebar collapsed",

        # =============================================================
        #  SPLASH
        # =============================================================
        "splash_title": "Discord Bot Manager",
        "splash_title_text": "Discord Bot Manager",
        "splash_subtitle": "Professional Multi-Bot Panel",
        "splash_status_loading": "Loading...",
        "splash_status_init": "Initializing...",
        "splash_status_config": "Loading configuration...",
        "splash_status_modules": "Loading modules...",
        "splash_status_bots": "Preparing bots...",
        "splash_status_ui": "Building interface...",
        "splash_status_done": "Ready!",
        "splash_tip_1": "💡 Tip: Ctrl+S saves settings quickly",
        "splash_tip_2": "💡 Tip: Use Bulk Control to start all bots at once",
        "splash_tip_3": "💡 Tip: Create backups regularly",
        "splash_tip_4": "💡 Tip: Customize bot colors with the Appearance editor",
        "splash_tip_5": "💡 Tip: AI Assistant can help debug crashes",
        "splash_tip_6": "💡 Tip: Use /connect in Discord to link your bot",
        "splash_tip_7": "💡 Tip: Set up scheduled restarts for stability",
        "splash_tip_8": "💡 Tip: Enable AFK screen to see bot status",
        "splash_tip_9": "💡 Tip: Check monthly reports for insights",
        "splash_tip_10": "💡 Tip: Use Commander to create commands without code",

        # =============================================================
        #  DÁTUM — NAPOK / HÓNAPOK
        # =============================================================
        "day_monday": "Monday",
        "day_tuesday": "Tuesday",
        "day_wednesday": "Wednesday",
        "day_thursday": "Thursday",
        "day_friday": "Friday",
        "day_saturday": "Saturday",
        "day_sunday": "Sunday",
        "month_january": "January",
        "month_february": "February",
        "month_march": "March",
        "month_april": "April",
        "month_may": "May",
        "month_june": "June",
        "month_july": "July",
        "month_august": "August",
        "month_september": "September",
        "month_october": "October",
        "month_november": "November",
        "month_december": "December",

        # =============================================================
        #  REMOTE COMMANDS
        # =============================================================
        "remote_unknown_bot_msg": "Unknown bot: {bot}",
        "remote_start_issued": "{bot} start command issued.",
        "remote_stop_issued": "{bot} stop command issued.",
        "remote_restart_issued": "{bot} restart command issued.",
        "remote_stress_result": "Stress test done: running={running}, CPU={cpu}%, temp={temp}.",
        "remote_no_log": "No log entries.",
        "remote_broadcast_handled": "Broadcast handled by BotVezerlo.",
        "remote_unknown_cmd": "Unknown command. Available: start, stop, restart, info, status, stressz, log.",
        "remote_status_line": "Panel {panel_id} | {bot}: {status} | RAM {ram} | CPU {cpu} | Temp {temp}",
        "remote_invalid_panel": "❌ Invalid panel ID.",
        "remote_connected": "✅ Connected to panel.",
        "remote_use_connect": "Use /connect first.",
        "remote_test_mode": "🧪 Bot is in test mode. Only testers can use it.",

        # =============================================================
        #  EGYÉB
        # =============================================================
        "temp_cpu_fallback": "CPU: {cpu}%",
        "tray_open": "Open panel",
        "tray_quit": "Quit",
        "tray_tooltip": "Bot Manager",
        "rpc_details": "Managing bots in DBM",
        "rpc_state": "DJ Baluss Panel",
        "log_manual_save": "Settings manually saved",
        "settings_manually_saved_msg": "Settings manually saved",
        "auto_start_process_started_msg": "✅ Bot process started (PID: {pid})",
        "auto_start_error_msg": "❌ Auto-start error: {error}",
        "bot_process_started_msg": "✅ Bot process started (PID: {pid})",
        "start_error_msg": "❌ Start error: {error}",
        "bot_process_stopped_msg": "🛑 Bot stopped",
        "bot_restart_msg": "🔄 Restarting bot...",
        "bot_unexpected_stop_msg": "❌ Bot stopped unexpectedly (code: {code})",
        "crash_watchdog_msg": "🔄 Crash watchdog: restarting in {n} seconds",
        "midnight_restart_event_msg": "🌙 Midnight restart triggered",
        "auto_restart_event_msg": "⏰ Scheduled restart triggered",
        "all_bots_start_log": "All bots started",
        "all_bots_start_msg": "✅ All bots started!",
        "all_bots_restart_log": "All bots restarted",
        "all_bots_restart_msg": "🔄 All bots restarted!",
        "all_bots_stop_log": "All bots stopped",
        "all_bots_stop_msg": "🛑 All bots stopped!",
        "test_mode_on_status": "ON",
        "test_mode_off_status": "OFF",
        "test_mode_changed_msg": "Test mode: {status}",
        "settings_manually_saved_msg": "✅ Settings saved",
        "file_not_found_msg": "File not found:\n{path}",
        # --- Common ---
        "common_close_btn": "Close",

        # --- Global Stats (window_stats.py) ---
        "global_stats_title": "Global Bot Statistics",
        "global_stats": "Global Statistics",
        "command_stats": "Command Statistics",
        "total_commands": "Total Commands",
        "errors": "Errors",
        "offline": "Offline",
    },
    "Magyar": {
        # =============================================================
        #  PANEL / ÁLTALÁNOS
        # =============================================================
        # --- Common ---
        "common_close_btn": "Bezárás",

        # --- Global Stats (window_stats.py) ---
        "global_stats_title": "Globális bot statisztika",
        "global_stats": "Globális statisztika",
        "command_stats": "Parancs statisztika",
        "total_commands": "Összes parancs",
        "errors": "Hibák",
        "offline": "Offline",
        "panel_title": "Discord Bot Manager - Professzionális Multi-Bot Panel",
        "online_status": "● ONLINE",
        "offline_status": "● OFFLINE",
        "unavailable": "N/A",
        "warning_title": "Figyelem",
        "error_title": "Hiba",
        "info_title": "Információ",
        "success_title": "Siker",
        "confirm_btn": "Megerősítés",
        "close_btn": "Bezárás",
        "cancel_btn": "Mégse",
        "save_btn": "Mentés",
        "delete_btn": "Törlés",
        "edit_btn": "Szerkesztés",
        "rename_btn": "Átnevezés",
        "refresh_btn": "Frissítés",
        "save_msg": "Sikeres mentés!",
        "copied_msg": "Vágólapra másolva",
        "days_short": "n",
        "hours_short": "ó",
        "minutes_short": "p",

        # =============================================================
        #  SIDEBAR — SZEKCIÓK
        # =============================================================
        "control_section": "Vezérlés",
        "bulk_control_section": "Tömeges vezérlés",
        "tools_section": "Eszközök és integráció",
        "stats_section": "Statisztika és rendszer",
        "system_section": "Rendszer",
        "ai_section": "AI és extrák",

        # =============================================================
        #  SIDEBAR — GOMBOK
        # =============================================================
        "dashboard_btn": "Vezérlőpult",
        "bot_start_btn": "Bot indítása",
        "bot_restart_btn": "Újraindítás",
        "bot_stop_btn": "Leállítás",
        "start_all_btn": "Összes indítása",
        "restart_all_btn": "Összes újraindítása",
        "stop_all_btn": "Összes leállítása",
        "commander_btn": "Commander",
        "plugins_btn": "Pluginok",
        "appearance_btn": "Megjelenés",
        "integration_btn": "Alapok / Integráció",
        "global_stats_btn": "Globális statisztika",
        "dashboard_widget_btn": "Dashboard",
        "live_charts_btn": "Élő grafikonok",
        "panel_stats_btn": "Panel statisztika",
        "monthly_report_btn": "Havi riport",
        "broadcast_btn": "Broadcast",
        "backup_btn": "Biztonsági mentések",
        "sqlite_btn": "SQLite nézegető",
        "settings_btn": "Beállítások",
        "tutorial_btn": "Tutorial",
        "github_update_btn": "GitHub Frissítés",
        "ai_assistant_btn": "AI Asszisztens",
        "ai_code_gen_btn": "AI Kód Generátor",
        "ai_docs_btn": "AI Dokumentáció",
        "achievements_btn": "Achievementek",
        "copy_command_btn": "Parancs másolása",
        "add_bot_btn": "+",
        "toggle_sidebar_btn": "☰",

        # =============================================================
        #  FELSŐ SÁV — BOT FÁJLOK KÁRTYA
        # =============================================================
        "bot_files_section": "BOT FÁJLOK",
        "bot_file_lbl": "Fő bot fájl:",
        "bot_file_ph": "Tallózd be a fő .py fájlt...",
        "env_ok": "🔑 .env: OK",
        "env_missing": "🔑 .env: Hiányzik",
        "env_na": "🔑 .env: N/A",
        "browse_btn": "Tallózás",

        # =============================================================
        #  FELSŐ SÁV — PANEL VISELKEDÉS KÁRTYA
        # =============================================================
        "behavior_section": "PANEL VISELKEDÉS",
        "autostart_lbl": "Auto-indítás",
        "error_sound_lbl": "Hiba hang",
        "midnight_restart_lbl": "Éjféli újraindítás",
        "auto_restart_lbl": "Auto Restart:",

        # =============================================================
        #  FELSŐ SÁV — BOT INFO KÁRTYA
        # =============================================================
        "bot_info_section": "BOT INFO",
        "servers_btn": "Szerverek",
        "bot_data_btn": "Bot adatai",
        "activity_btn": "Activity",
        "test_mode_lbl": "Teszt mód",

        # =============================================================
        #  NAPLÓK
        # =============================================================
        "live_logs_title": "Élő naplók",
        "filter_all_btn": "ÖSSZES",
        "filter_errors_btn": "HIBÁK",
        "filter_success_btn": "SIKER",
        "filter_events_btn": "ESEMÉNYEK",
        "autoscroll_lbl": "Automatikus görgetés",
        "clear_logs_btn": "Törlés",
        "log_search_ph": "🔍 Keresés a logokban...",
        "log_write_error": "[LOG] Írási hiba: {error}",
        "remote_response_save_error": "Távoli válasz mentési hiba: {error}",

        # =============================================================
        #  PRO METRIKÁK
        # =============================================================
        "metrics_section": "📊 Pro metrikák",
        "open_charts_btn": "📈 Teljesítmény grafikon",
        "bot_information_section": "Bot információ",
        "pc_resources_section": "PC erőforrások",
        "bot_name_lbl": "Bot neve",
        "bot_version_lbl": "Bot verziója",
        "uptime_lbl": "Futási idő (munkamenet)",
        "weekly_uptime_lbl": "Heti futási idő",
        "ping_lbl": "Ping válaszidő",
        "total_commands_lbl": "Összes parancs",
        "ram_lbl": "RAM használat",
        "cpu_lbl": "CPU használat",
        "temperature_pc_lbl": "PC hőmérséklete",
        "guilds_lbl": "Szerverek (Guilds)",
        "users_lbl": "Elért felhasználók",
        "error_counter_lbl": "Hiba számláló",

        # =============================================================
        #  SETTINGS ABLAK
        # =============================================================
        "settings_title": "Beállítások",
        "settings_header": "⚙️  Beállítások",
        "settings_tab_panel": "Panel beállítások",
        "settings_tab_bot": "Botonkénti beállítások",
        "settings_save_close_btn": "💾  Mentés és bezárás",
        "settings_saved_status": "✅ Beállítások mentve",
        "settings_saved_toast": "💾 Beállítások mentve",

        # Settings — szekciók
        "settings_sec_security": "Biztonság",
        "settings_sec_appearance": "Megjelenés",
        "settings_sec_notifications": "Értesítések",
        "settings_sec_logs": "Naplók",
        "settings_sec_afk": "AFK képernyő",
        "settings_sec_backup": "Biztonsági mentés",
        "settings_sec_github": "GitHub frissítések",
        "settings_sec_ai": "AI beállítások",
        "settings_sec_resources": "Erőforrások",
        "settings_sec_test_mode": "Teszt mód",
        "settings_sec_crash": "Crash kezelés",

        # Settings — mezők
        "settings_password_lbl": "Panel jelszó (üresen hagyva nincs védelem)",
        "settings_language_lbl": "Nyelv:",
        "settings_theme_lbl": "Téma:",
        "settings_tray_switch": "Kicsinyítés a tálcára bezáráskor",
        "settings_rpc_switch": "Discord Rich Presence",
        "settings_error_sound_lbl": "Hiba hang:",
        "settings_sound_test_btn": "🔊 Teszt",
        "settings_log_level_lbl": "Napló mentési szint:",
        "settings_log_all": "Mindent mentse",
        "settings_log_errors": "Csak hibák",
        "settings_log_events": "Csak események",
        "settings_log_success": "Sikeres interakciók",
        "settings_afk_hint": "Tétlenség esetén teljes képernyős bot állapot nézetet mutat.",
        "settings_afk_switch": "AFK képernyő engedélyezése",
        "settings_afk_timeout_lbl": "Tétlenség:",
        "settings_afk_preview_btn": "👁 Előnézet",
        "settings_backup_switch": "Automatikus biztonsági mentés",
        "settings_backup_start_switch": "Mentés panelindításkor",
        "settings_backup_interval_lbl": "Időzített mentés gyakorisága (óra, 0 = ki):",
        "settings_backup_manager_btn": "📂 Backup kezelő megnyitása",
        "settings_github_hint": "A panel automatikusan ellenőrzi a GitHub frissítéseket.",
        "settings_update_interval_lbl": "Ellenőrzés gyakorisága:",
        "settings_update_check_now_btn": "🔄 Azonnali ellenőrzés",
        "settings_update_history_btn": "📜 Előző frissítések",
        "settings_ai_model_lbl": "Modell:",
        "settings_max_ram_lbl": "Maximális RAM használat (MB):",
        "settings_max_ram_hint": "Ha a bot túllépi, a panel figyelmeztet.",
        "settings_test_switch": "Teszt mód engedélyezése",
        "settings_testers_lbl": "Tesztelők Discord azonosítói (vesszővel):",
        "settings_testers_hint": "Teszt módban csak ezek az azonosítók használhatják a botot.",
        "settings_crash_switch": "Automatikus újraindítás összeomlás után",
        "settings_crash_delay_lbl": "Újraindítás várakozása (másodperc):",
        "settings_err_backup_interval": "❌ Érvénytelen backup intervallum",
        "settings_err_crash_delay": "❌ Érvénytelen crash várakozási idő",
        "settings_err_ram": "❌ Érvénytelen RAM érték",

        # =============================================================
        #  HANG NEVEK
        # =============================================================
        "sound_beep": "Alap (Beep)",
        "sound_double_beep": "Dupla Pittyogás",
        "sound_buzz": "Mély Hiba (Buzz)",
        "sound_triple_beep": "Hármas Sípjel",
        "sound_slow_buzz": "Lassú Búgás",
        "sound_fast_double": "Gyors Dupla",
        "sound_long_cry": "Hosszú Sírás",
        "sound_none": "Nincs hang",

        # =============================================================
        #  AFK IDŐZÍTŐ OPCIÓK
        # =============================================================
        "afk_timeout_15s": "15 másodperc",
        "afk_timeout_30s": "30 másodperc",
        "afk_timeout_1m": "1 perc",
        "afk_timeout_2m": "2 perc",
        "afk_timeout_5m": "5 perc",
        "afk_timeout_10m": "10 perc",
        "afk_timeout_30m": "30 perc",

        # =============================================================
        #  UPDATE ELLENŐRZÉSI OPCIÓK
        # =============================================================
        "update_interval_never": "Soha",
        "update_interval_1min": "Percenként",
        "update_interval_10min": "10 percenként",
        "update_interval_1hour": "Óránként",
        "update_interval_1day": "Naponta",

        # =============================================================
        #  DIALÓGUS ABLAKOK — ÚJ BOT / TÖRLÉS
        # =============================================================
        "new_bot_title": "Új bot",
        "new_bot_prompt": "Add meg az új bot nevét:",
        "duplicate_bot_msg": "Már létezik ilyen nevű bot.",
        "delete_bot_confirm": "Biztosan törlöd a(z) '{name}' botot?",
        "default_bot_no_delete": "Az alapértelmezett (fő) bot nem törölhető!",
        "last_bot_no_delete_msg": "Az utolsó bot nem törölhető!",
        "delete_bot_confirm_short": "Biztosan törlöd ezt a botot?",
        "bot_script_missing_msg": "A bot .py fájlja hiányzik!",
        "bot_data_saved_msg": "✅ Bot adatai mentve: {name}",

        # =============================================================
        #  BOT ADATAI ABLAK
        # =============================================================
        "bot_data_title": "Bot adatai",
        "bot_data": "Bot adatai",
        "bot_name": "Bot neve",
        "bot_version": "Bot verziója",
        "bot_prefix": "Bot prefix",
        "bot_info_hint": "⚠️ A token érzékeny adat, ne oszd meg senkivel!",
        "bot_info_token_placeholder": "Írd be a bot tokent...",
        "save": "Mentés",
        "close": "Bezárás",

        # =============================================================
        #  BROADCAST
        # =============================================================
        "broadcast_title": "Broadcast",
        "broadcast_header": "📢  Broadcast",
        "broadcast_servers_count": "🌐 Szerverek: {count}",
        "broadcast_servers_section": "Szerverek és csatornák",
        "broadcast_channels_hint": "Pipáld be, mely csatornákra menjen az üzenet.\nA szürke csatornákra a bot NEM tud írni.",
        "broadcast_no_channels_msg": "Nincsenek szerverek.\nIndítsd el előbb a botot!",
        "broadcast_select_all_btn": "✅ Összes",
        "broadcast_deselect_all_btn": "❌ Egyik sem",
        "broadcast_template_lbl": "Sablon:",
        "broadcast_schedule_section": "⏰ Időzítés (opcionális)",
        "broadcast_schedule_check": "Késleltetett küldés",
        "broadcast_when_lbl": "Küldés:",
        "broadcast_preview_btn": "👁 Előnézet",
        "broadcast_preview_title": "Előnézet",
        "broadcast_preview_time": "Ma 12:00-kor",
        "broadcast_send_btn": "📢 Broadcast indítása",
        "broadcast_empty_msg": "(üres üzenet)",
        "broadcast_need_bot_msg": "Előbb tallózd be a bot érvényes .py fájlját!",
        "broadcast_no_channel_msg": "Válassz ki legalább egy csatornát!",
        "broadcast_msg_empty_msg": "Az üzenet nem lehet üres!",
        "broadcast_embed_empty_msg": "Az embedhez kell cím vagy leírás!",
        "broadcast_send_error_msg": "Küldési hiba: {error}",
        "broadcast_scheduled_toast": "⏰ Broadcast időzítve: {minutes} perc",
        "broadcast_scheduled_log": "Broadcast időzítve ({bot}) — {count} csatorna",
        "broadcast_sent_toast": "✅ Broadcast elküldve {count} csatornára",
        "broadcast_sent_log": "Broadcast elküldve ({bot}) — {count} csatorna",

        # =============================================================
        #  BROADCAST — KÖZÖS MEZŐK
        # =============================================================
        "broadcast_type_lbl": "Típus:",
        "broadcast_type_message": "Üzenet",
        "broadcast_type_embed": "Embed",
        "broadcast_content_lbl": "Üzenet tartalma:",
        "broadcast_embed_title_lbl": "Embed cím:",
        "broadcast_embed_desc_lbl": "Embed leírás:",
        "broadcast_footer_lbl": "Footer:",
        "broadcast_thumb_lbl": "Thumbnail URL:",
        "broadcast_color_lbl": "Szín:",
        "broadcast_quick_lbl": "Gyors:",

        # =============================================================
        #  BROADCAST SABLONOK
        # =============================================================
        "bc_tpl_simple_name": "📝 Egyszerű üzenet",
        "bc_tpl_simple_content": "Sziasztok! 👋\nEz egy teszt üzenet.",

        "bc_tpl_maintenance_name": "🔧 Karbantartás",
        "bc_tpl_maintenance_title": "🔧 Tervezett karbantartás",
        "bc_tpl_maintenance_desc": "A bot átmenetileg nem elérhető karbantartás miatt.\nHamarosan visszatérünk!",
        "bc_tpl_maintenance_footer": "Köszönjük a türelmedet!",

        "bc_tpl_new_version_name": "🚀 Új verzió",
        "bc_tpl_new_version_title": "🚀 Új verzió érhető el!",
        "bc_tpl_new_version_desc": "Megjelent a bot új verziója.\nNézd meg a changelogot a részletekért!",
        "bc_tpl_new_version_footer": "Frissíts most!",

        "bc_tpl_event_name": "🎉 Esemény",
        "bc_tpl_event_title": "🎉 Különleges esemény!",
        "bc_tpl_event_desc": "Csatlakozz hozzánk egy különleges eseményre!\nNe maradj le!",
        "bc_tpl_event_footer": "Találkozunk ott!",

        "bc_tpl_warning_name": "⚠️ Figyelmeztetés",
        "bc_tpl_warning_title": "⚠️ Fontos figyelmeztetés",
        "bc_tpl_warning_desc": "Kérjük, olvasd el figyelmesen ezt a fontos értesítést.",
        "bc_tpl_warning_footer": "Köszönjük a figyelmedet!",

        "bc_tpl_outage_name": "🚨 Kiesés",
        "bc_tpl_outage_title": "🚨 Szolgáltatás kiesés",
        "bc_tpl_outage_desc": "Jelenleg technikai nehézségekkel küzdünk.\nDolgozunk a megoldáson!",
        "bc_tpl_outage_footer": "Elnézést kérünk a kellemetlenségért.",

        "bc_tpl_custom_name": "✏️ Egyedi embed",
        "bc_tpl_custom_title": "Egyedi cím",
        "bc_tpl_custom_desc": "Írd ide a saját leírásodat...",

        "bc_tpl_sysinfo_name": "🖥️ Rendszer info",
        "bc_tpl_sysinfo_title": "🖥️ Rendszer információ",
        "bc_tpl_sysinfo_desc": "Jelenlegi bot és rendszer állapot:",
        "bc_tpl_sysinfo_footer": "Automatikusan generálva",
        "bc_tpl_sysinfo_field1_name": "Bot állapot",
        "bc_tpl_sysinfo_field1_value": "🟢 Online",
        "bc_tpl_sysinfo_field2_name": "Futási idő",
        "bc_tpl_sysinfo_field2_value": "0ó 0p",

        # =============================================================
        #  IDŐZÍTÉS OPCIÓK
        # =============================================================
        "sched_1min": "1 perc",
        "sched_5min": "5 perc",
        "sched_10min": "10 perc",
        "sched_30min": "30 perc",
        "sched_1hour": "1 óra",
        "sched_6hour": "6 óra",
        "sched_24hour": "24 óra",

        # =============================================================
        #  COMMANDER
        # =============================================================
        "commander_title": "Commander & Fájlkezelő",
        "commander_header": "⚡  Commander",
        "commander_bot_folder_lbl": "Bot mappa",
        "commander_tab_editor": "Szerkesztő",
        "commander_tab_commands": "Commander",
        "commander_tab_extensions": "Extension",
        "commander_select_file_lbl": "Válassz fájlt a fáról",
        "commander_save_editor_btn": "💾 Mentés",
        "commander_new_file_btn": "➕ Fájl",
        "commander_new_folder_btn": "📁 Mappa",
        "commander_rename_btn": "✏️ Átnevezés",
        "commander_delete_btn": "🗑️ Törlés",
        "commander_commands_lbl": "Egyedi parancsok (commander_commands.json)",
        "commander_new_command_btn": "➕ Új parancs",
        "commander_extensions_lbl": "Extension-ök",
        "commander_extensions_hint": "A bot indulásakor a panel_integrity.py betölti az itt listázott extension-öket.",
        "commander_add_extension_btn": "➕ Hozzáadás",
        "commander_save_extensions_btn": "💾 Mentés",
        "commander_need_bot_msg": "Előbb tallózd be a bot érvényes .py fájlját!",

        # Commander — parancs szerkesztő
        "commander_editor_title_new": "➕ Új parancs",
        "commander_editor_title_edit": "✏️ Parancs szerkesztése",
        "commander_templates_section": "🎨 Sablonok",
        "commander_templates_hint": "Válassz egy kész sablont — a mezők automatikusan kitöltődnek, utána szabadon módosíthatod őket.",
        "commander_data_section": "📋 Parancs adatok",
        "commander_options_section": "⚙️ Opciók",
        "commander_name_lbl": "Parancs neve (per jel nélkül):",
        "commander_desc_lbl": "Leírás (megjelenik a Discord / menüben):",
        "commander_ephemeral_lbl": "Csak a hívónak látszódjon (ephemeral)",
        "commander_enabled_lbl": "Parancs engedélyezve",
        "commander_save_command_btn": "💾 Parancs mentése",
        "commander_default_description": "Egyedi parancs",

        # Commander — üzenetek
        "commander_binary_file_msg": "Bináris fájl nem nyitható meg!",
        "commander_no_open_file_msg": "Nincs megnyitott fájl!",
        "commander_syntax_error_title": "Szintaktikai hiba",
        "commander_syntax_error_msg": "{line}. sor: {msg}\n\nMentés mindenképp?",
        "commander_saved_status": "✅ Mentve: {name}",
        "commander_saved_toast": "✅ Mentve: {name}",
        "commander_created_toast": "✅ Létrehozva: {name}",
        "commander_file_exists_msg": "Már létezik ilyen nevű fájl!",
        "commander_add_extension_title": "Új extension",
        "commander_add_extension_prompt": "Extension neve (pl. cogs.parancsok):",
        "commander_add_extension_confirm": "Hozzáadod a(z) '{ext}' extension-t az automatikusan betöltendő listához?",
        "commander_name_empty_msg": "A parancs neve nem lehet üres!",
        "commander_name_invalid_msg": "Csak betű, szám és alulvonás engedélyezett!",
        "commander_name_exists_msg": "Már létezik '{name}' nevű parancs!",
        "commander_no_commands_msg": "Még nincsenek egyedi parancsok.",
        "commander_no_extensions_msg": "Még nincsenek extension-ök.",
        "commander_extensions_saved_msg": "✅ Extension-ök mentve",
        "commander_rename_title": "Átnevezés",
        "commander_rename_prompt": "Új név:",
        "commander_new_file_title": "Új fájl",
        "commander_new_file_prompt": "Fájlnév (pl. parancs.py):",
        "commander_new_folder_title": "Új mappa",
        "commander_new_folder_prompt": "Mappa neve:",
        "commander_delete_item_title": "Törlés",
        "commander_delete_item_confirm": "Biztosan törlöd: '{name}'?",
        "commander_delete_command_title": "Parancs törlése",
        "commander_delete_command_confirm": "Biztosan törlöd a(z) '{name}' parancsot?",

        # =============================================================
        #  COMMANDER SABLONOK
        # =============================================================
        "cmd_tpl_simple_name": "📝 Egyszerű üzenet",
        "cmd_tpl_simple_desc": "Egyszerű szöveges parancs",
        "cmd_tpl_simple_content": "Szia! 👋",

        "cmd_tpl_welcome_name": "👋 Üdvözlés",
        "cmd_tpl_welcome_desc": "Üdvözlő üzenet",
        "cmd_tpl_welcome_content": "Üdvözlünk a szerveren! 🎉",

        "cmd_tpl_announcement_name": "📢 Bejelentés",
        "cmd_tpl_announcement_desc": "Szerver bejelentés",
        "cmd_tpl_announcement_content": "📢 Fontos bejelentés!",

        "cmd_tpl_simple_embed_name": "📄 Egyszerű embed",
        "cmd_tpl_simple_embed_desc": "Alap embed üzenet",
        "cmd_tpl_simple_embed_title": "Szia!",
        "cmd_tpl_simple_embed_description": "Ez egy egyszerű embed.",
        "cmd_tpl_simple_embed_footer": "DBM által",

        "cmd_tpl_error_embed_name": "❌ Hiba embed",
        "cmd_tpl_error_embed_desc": "Hibaüzenet (ephemeral)",
        "cmd_tpl_error_embed_title": "❌ Hiba",
        "cmd_tpl_error_embed_description": "Valami hiba történt.",
        "cmd_tpl_error_embed_footer": "Próbáld újra",

        "cmd_tpl_success_embed_name": "✅ Siker embed",
        "cmd_tpl_success_embed_desc": "Sikeres üzenet (ephemeral)",
        "cmd_tpl_success_embed_title": "✅ Sikeres",
        "cmd_tpl_success_embed_description": "A művelet sikeresen befejeződött.",

        "cmd_tpl_warning_embed_name": "⚠️ Figyelmeztetés embed",
        "cmd_tpl_warning_embed_desc": "Figyelmeztető üzenet",
        "cmd_tpl_warning_embed_title": "⚠️ Figyelem",
        "cmd_tpl_warning_embed_description": "Kérjük, olvasd el figyelmesen.",

        "cmd_tpl_help_name": "❓ Súgó menü",
        "cmd_tpl_help_desc": "Segítség a parancsokhoz",
        "cmd_tpl_help_title": "❓ Súgó",
        "cmd_tpl_help_description": "Elérhető parancsok:",
        "cmd_tpl_help_footer": "Írd be: /help",
        "cmd_tpl_help_f1_name": "/teszt",
        "cmd_tpl_help_f1_value": "Bot tesztelése",
        "cmd_tpl_help_f2_name": "/info",
        "cmd_tpl_help_f2_value": "Bot információ",
        "cmd_tpl_help_f3_name": "/help",
        "cmd_tpl_help_f3_value": "Ez a menü",

        "cmd_tpl_rules_name": "📜 Szerver szabályok",
        "cmd_tpl_rules_desc": "Szerver szabályok listája",
        "cmd_tpl_rules_title": "📜 Szerver szabályok",
        "cmd_tpl_rules_description": "Kérjük, tartsd be a szabályokat:",
        "cmd_tpl_rules_footer": "Szabályszegés = ban",
        "cmd_tpl_rules_f1_name": "1. Tiszteld a többieket",
        "cmd_tpl_rules_f1_value": "Bánj mindenkivel tisztelettel.",
        "cmd_tpl_rules_f2_name": "2. Ne spamolj",
        "cmd_tpl_rules_f2_value": "Ne küldj spam üzeneteket.",
        "cmd_tpl_rules_f3_name": "3. Semmi NSFW",
        "cmd_tpl_rules_f3_value": "Nem megfelelő tartalom tilos.",
        "cmd_tpl_rules_f4_name": "4. Discord ToS betartása",
        "cmd_tpl_rules_f4_value": "Tartsd be a Discord Felhasználási Feltételeit.",

        "cmd_tpl_info_name": "ℹ️ Info embed",
        "cmd_tpl_info_desc": "Általános információ",
        "cmd_tpl_info_title": "ℹ️ Információ",
        "cmd_tpl_info_description": "Általános infó:",
        "cmd_tpl_info_footer": "Utoljára frissítve ma",
        "cmd_tpl_info_f1_name": "Tagok",
        "cmd_tpl_info_f1_value": "0",
        "cmd_tpl_info_f2_name": "Online",
        "cmd_tpl_info_f2_value": "0",
        "cmd_tpl_info_f3_name": "Botok",
        "cmd_tpl_info_f3_value": "1",

        "cmd_tpl_giveaway_name": "🎁 Nyereményjáték",
        "cmd_tpl_giveaway_desc": "Nyereményjáték bejelentés",
        "cmd_tpl_giveaway_title": "🎁 Nyereményjáték!",
        "cmd_tpl_giveaway_description": "Reagálj, hogy részt vegyél!",
        "cmd_tpl_giveaway_footer": "Sok szerencsét!",
        "cmd_tpl_giveaway_f1_name": "Nyeremény",
        "cmd_tpl_giveaway_f1_value": "Nitro",
        "cmd_tpl_giveaway_f2_name": "Nyertesek",
        "cmd_tpl_giveaway_f2_value": "1",
        "cmd_tpl_giveaway_f3_name": "Vége",
        "cmd_tpl_giveaway_f3_value": "Holnap",

        "cmd_tpl_ticket_name": "🎫 Ticket",
        "cmd_tpl_ticket_desc": "Support ticket",
        "cmd_tpl_ticket_title": "🎫 Support Ticket",
        "cmd_tpl_ticket_description": "Segítség kell? Nyiss egy ticketet!",
        "cmd_tpl_ticket_footer": "Support csapat",
        "cmd_tpl_ticket_f1_name": "Hogyan nyisd",
        "cmd_tpl_ticket_f1_value": "Reagálj 🎫-vel",
        "cmd_tpl_ticket_f2_name": "Válaszidő",
        "cmd_tpl_ticket_f2_value": "24 órán belül",
        "cmd_tpl_ticket_f3_name": "Support idő",
        "cmd_tpl_ticket_f3_value": "9:00 - 18:00",

        "cmd_tpl_event_name": "🎉 Esemény",
        "cmd_tpl_event_desc": "Esemény bejelentés",
        "cmd_tpl_event_title": "🎉 Különleges esemény!",
        "cmd_tpl_event_description": "Csatlakozz hozzánk egy különleges eseményre!",
        "cmd_tpl_event_footer": "Ne maradj le!",
        "cmd_tpl_event_f1_name": "Dátum",
        "cmd_tpl_event_f1_value": "Szombaton",
        "cmd_tpl_event_f2_name": "Idő",
        "cmd_tpl_event_f2_value": "20:00",
        "cmd_tpl_event_f3_name": "Helyszín",
        "cmd_tpl_event_f3_value": "Hangcsatorna",

        "cmd_tpl_botinfo_name": "🤖 Bot info",
        "cmd_tpl_botinfo_desc": "Bot információ embed",
        "cmd_tpl_botinfo_title": "🤖 Bot információ",
        "cmd_tpl_botinfo_description": "Minden a botról:",
        "cmd_tpl_botinfo_footer": "DBM által",
        "cmd_tpl_botinfo_f1_name": "Verzió",
        "cmd_tpl_botinfo_f1_value": "1.0.0",
        "cmd_tpl_botinfo_f2_name": "Szerverek",
        "cmd_tpl_botinfo_f2_value": "0",
        "cmd_tpl_botinfo_f3_name": "Futási idő",
        "cmd_tpl_botinfo_f3_value": "0ó",

        "cmd_tpl_music_name": "🎵 Zene lista",
        "cmd_tpl_music_desc": "Zene parancsok listája",
        "cmd_tpl_music_title": "🎵 Zene parancsok",
        "cmd_tpl_music_description": "Elérhető zene parancsok:",
        "cmd_tpl_music_f1_name": "/play",
        "cmd_tpl_music_f1_value": "Zene lejátszása",
        "cmd_tpl_music_f2_name": "/pause",
        "cmd_tpl_music_f2_value": "Szüneteltetés",
        "cmd_tpl_music_f3_name": "/skip",
        "cmd_tpl_music_f3_value": "Következő szám",
        "cmd_tpl_music_f4_name": "/queue",
        "cmd_tpl_music_f4_value": "Sor megjelenítése",

        "cmd_tpl_moderation_name": "🔨 Moderáció",
        "cmd_tpl_moderation_desc": "Moderációs parancsok",
        "cmd_tpl_moderation_title": "🔨 Moderáció",
        "cmd_tpl_moderation_description": "Elérhető moderációs parancsok:",
        "cmd_tpl_moderation_footer": "Használd felelősségteljesen",
        "cmd_tpl_moderation_f1_name": "/kick",
        "cmd_tpl_moderation_f1_value": "Tag kirúgása",
        "cmd_tpl_moderation_f2_name": "/ban",
        "cmd_tpl_moderation_f2_value": "Tag kitiltása",
        "cmd_tpl_moderation_f3_name": "/clear",
        "cmd_tpl_moderation_f3_value": "Üzenetek törlése",

        "cmd_tpl_notification_name": "🔔 Értesítés",
        "cmd_tpl_notification_desc": "Egyszerű értesítés",
        "cmd_tpl_notification_title": "🔔 Értesítés",
        "cmd_tpl_notification_description": "Ez egy értesítés.",
        "cmd_tpl_notification_footer": "Olvasd el figyelmesen",

        "cmd_tpl_custom_color_name": "🎨 Egyedi szín",
        "cmd_tpl_custom_color_desc": "Embed egyedi színnel",
        "cmd_tpl_custom_color_title": "🎨 Egyedi szín",
        "cmd_tpl_custom_color_description": "Ez az embed egyedi színű.",

        "cmd_tpl_image_name": "🖼️ Kép embed",
        "cmd_tpl_image_desc": "Embed képpel",
        "cmd_tpl_image_title": "🖼️ Kép",
        "cmd_tpl_image_description": "Embed képpel:",

        "cmd_tpl_links_name": "🔗 Linkek",
        "cmd_tpl_links_desc": "Hasznos linkek",
        "cmd_tpl_links_title": "🔗 Hasznos linkek",
        "cmd_tpl_links_description": "Fontos linkek:",
        "cmd_tpl_links_f1_name": "Weboldal",
        "cmd_tpl_links_f1_value": "https://example.com",
        "cmd_tpl_links_f2_name": "Support",
        "cmd_tpl_links_f2_value": "https://discord.gg/example",
        "cmd_tpl_links_f3_name": "GitHub",
        "cmd_tpl_links_f3_value": "https://github.com/example",

        # =============================================================
        #  SZÍNEK
        # =============================================================
        "color_blurple": "Blurple",
        "color_blue": "Kék",
        "color_green": "Zöld",
        "color_red": "Piros",
        "color_orange": "Narancs",
        "color_purple": "Lila",
        "color_teal": "Türkiz",
        "color_rose": "Rózsa",
        "color_cyan": "Cián",
        "color_gold": "Arany",
        "color_mauve": "Mályva",
        "color_graphite": "Grafit",

        # =============================================================
        #  INTEGRÁCIÓ
        # =============================================================
        "integration_title": "Panel Integráció",
        "integration_header": "📌  Panel Integráció",
        "integration_welcome": "Üdvözlünk a panel integrációban! 🎉",
        "integration_intro": "A panel 3 fájlt használ a bot oldalán:\n   • bot.py — a bot fő fájlja\n   • panel_integrity.py — a panel összes funkciója\n   • version.py — bot név, verzió, token",
        "integration_have_bot_q": "Van már működő botod?",
        "integration_btn_existing": "✅ Van már botom\n(csak integrációt adok hozzá)",
        "integration_btn_new": "🆕 Új botot készítek\n(teljes sablon)",
        "integration_steps_title": "📋 Lépések",
        "integration_step1": "1. Tallózd be a botod fő .py fájlját a panelen (📁 Tallózás).",
        "integration_step2": "2. Kattints az alábbi „📥 Panel integráció hozzáadása” gombra.",
        "integration_step3": "3. Nyisd meg a bot.py fájlt, és az on_ready() függvényben add hozzá:",
        "integration_step4": "4. Indítsd újra a botot.",
        "integration_step5": "5. Discordban írd be: /connect panel_id:<a panel azonosítója>",
        "integration_code_title": "📄 panel_integrity.py tartalma",
        "integration_add_btn": "📥 Panel integráció hozzáadása",
        "integration_existing_title": "Meglévő bot",
        "integration_existing_header": "✅  Integráció hozzáadása meglévő bothoz",
        "integration_new_title": "Új bot",
        "integration_new_header": "🆕  Új bot készítése",
        "integration_new_intro": "A panel 3 fájlt generál. Válaszd ki a célmappát, vagy mentsd külön-külön.",
        "integration_file_bot_lbl": "📄 1. bot.py — a bot fő fájlja",
        "integration_file_panel_lbl": "📄 2. panel_integrity.py — a panel összes funkciója",
        "integration_file_version_lbl": "📄 3. version.py — bot név, verzió, token",
        "integration_token_card_title": "🔑 Bot Token beállítása",
        "integration_token_card_hint": "A bot tokent a „Bot adatai” ablakban tudod beállítani.\nOtt a nevet, verziót és prefixet is szerkesztheted.",
        "integration_token_edit_btn": "🔑 Bot adatai szerkesztése",
        "integration_generate_all_btn": "📁 Összes fájl generálása egy mappába",
        "integration_need_bot": "Előbb tallózd be a bot érvényes .py fájlját!",
        "integration_saved_title": "Siker",
        "integration_saved_msg": "Panel integráció elmentve:\n{dir}",
        "integration_log_saved": "Panel integráció mentve: {path}",
        "integration_saved_toast": "✅ Integráció mentve",
        "integration_generated_msg": "Fájlok generálva:\n{folder}",
        "integration_log_generated": "Sablon generálva: {folder}",
        "integration_generated_toast": "✅ Fájlok generálva",
        "integration_choose_folder": "Válaszd ki a célmappát",
        "integration_token_need_bot": "Előbb tallózd be a bot érvényes .py fájlját!",

        # =============================================================
        #  FÜGGŐSÉGEK
        # =============================================================
        "deps_title": "🔧 Függőségek",
        "deps_header": "🔧  Függőségek",
        "deps_intro": "Ellenőrizd, hogy minden szükséges Python csomag telepítve van-e.",
        "deps_check_btn": "🔍 Ellenőrzés",
        "deps_install_missing_btn": "📥 Hiányzók telepítése",
        "deps_reinstall_btn": "🔄 Újratelepít",
        "deps_version": "v{version}",
        "deps_missing": "— hiányzik —",
        "deps_all_ok": "✅ Mind a(z) {total} csomag telepítve ({ok}/{total})",
        "deps_some_missing": "❌ {missing} hiányzik {total}-ból ({ok}/{total} telepítve)",
        "deps_info_title": "Információ",
        "deps_all_installed": "Minden szükséges csomag telepítve van!",
        "deps_log_start": "▶ Telepítés indítása ({count} csomag)...\n",
        "deps_log_item": "▶ [{idx}/{total}] {pkg}\n",
        "deps_log_error": "❌ {pkg}: {error}\n",
        "deps_log_done": "\n✅ Telepítés befejezve!\n",
        "deps_status_installing": "⏳ Telepítés...",
        "deps_status_item": "⏳ [{idx}/{total}] {pkg}",
        "deps_status_done": "✅ Kész",
        "deps_reinstall_title": "Újratelepítés",
        "deps_reinstall_confirm": "Újratelepíted az összes szükséges csomagot?",
        "deps_output_hint": "— A kimenet itt jelenik meg —",
        "integration_deps_btn": "🔧 Függőségek",

        # Függőség leírások
        "dep_customtkinter_desc": "Modern UI eszköztár",
        "dep_psutil_desc": "Rendszer- és folyamatkezelés",
        "dep_matplotlib_desc": "Grafikonok és diagramok",
        "dep_pystray_desc": "Rendszertálca ikon",
        "dep_pillow_desc": "Képfeldolgozás",
        "dep_pypresence_desc": "Discord Rich Presence",
        "dep_discord_desc": "Discord API könyvtár",
        "dep_wmi_desc": "Windows hőmérséklet info (opcionális)",
        "dep_requests_desc": "HTTP könyvtár (opcionális)",

        # =============================================================
        #  GITHUB UPDATE
        # =============================================================
        "update_title": "Frissítés",
        "update_window_title": "🚀 Új verzió érhető el",
        "update_header": "🚀 Új verzió érhető el!",
        "update_news_default": "📝 Újdonságok",
        "update_changelog_general": "Változások",
        "update_no_changelog": "Nincs elérhető changelog.",
        "update_safe_info": "ℹ️ A mentések, pluginok, beállítások és botok megmaradnak.",
        "update_download_btn": "✅ Frissítés letöltése",
        "update_later_btn": "⏰ Később",
        "update_skip_btn": "❌ Kihagyás",
        "update_history_btn": "📜 Előző frissítések",
        "update_skip_title": "Verzió kihagyása",
        "update_skip_confirm": "Kihagyod a(z) {version} verziót újraindításig?",
        "update_history_window_title": "📜 Frissítések története",
        "update_history_header": "📜  Frissítések története",
        "update_history_current": "Jelenlegi: v{version}",
        "update_history_current_badge": "JELENLEGI",
        "update_history_empty": "Nincs frissítési előzmény.",
        "update_history_no_desc": "(nincs leírás)",
        "update_history_refresh_btn": "🔄 Frissítések keresése",
        "update_status_downloading": "⬇️ Letöltés...",
        "update_status_extracting": "📦 Kicsomagolás...",
        "update_status_preparing": "🔧 Előkészítés...",
        "update_status_stopping_bots": "🛑 Botok leállítása...",
        "update_status_updating_files": "📂 Fájlok frissítése...",
        "update_status_version": "🏷️ Verzió frissítése...",
        "update_status_done": "✅ Frissítés kész!",
        "update_status_error": "❌ Hiba",
        "update_error_title": "Frissítési hiba",
        "update_error_msg": "Hiba a frissítés során:\n{error}",
        "update_conn_error": "❌ Nem sikerült csatlakozni a GitHubhoz!",
        "update_up_to_date": "✅ A legfrissebb verziód van (v{version})",
        "update_restart_title": "Újraindítás szükséges",
        "update_restart_success": "🎉 Frissítés kész!",
        "update_restart_version": "Új verzió: v{version}",
        "update_restart_msg": "A panelnek újra kell indulnia a frissítés alkalmazásához.",
        "update_restart_safe_info": "ℹ️ A beállításaid és botjaid megmaradnak.",
        "update_restart_now_btn": "🔄 Újraindítás most",
        "update_restart_exit_btn": "🚪 Kilépés",
        "update_restart_error_title": "Újraindítási hiba",
        "update_log_version_fetch_error": "[UPDATE] Verzió lekérési hiba: {error}",
        "update_log_manual_check": "[UPDATE] Manuális ellenőrzés indítva",
        "update_log_auto_disabled": "[UPDATE] Auto-ellenőrzés kikapcsolva",
        "update_log_skipped": "[UPDATE] Verzió kihagyva: {version}",
        "update_log_installed": "[UPDATE] Telepítve: v{version}",
        "update_log_restart": "[UPDATE] Panel újraindítása",
        "update_log_version_write_error": "[UPDATE] Verzió írási hiba: {error}",

        # =============================================================
        #  BACKUP
        # =============================================================
        "backup_title": "Biztonsági mentéskezelő",
        "backup_new": "Új mentés",
        "backup_restore": "Kijelölt visszaállítása",
        "backup_done_title": "Biztonsági mentés",
        "backup_done_msg": "A mentés elkészült:\n{path}",
        "backup_error_title": "Mentési hiba",
        "backup_select_title": "Kiválasztás",
        "backup_select_msg": "Válassz ki egy mentést a listából!",
        "backup_restore_title": "Visszaállítás",
        "backup_restore_confirm": "Biztosan visszaállítod ezt a mentést?\nA meglévő fájlok felülíródnak!",
        "backup_invalid_path": "Érvénytelen útvonal az archívumban!",
        "backup_restore_done": "✅ Mentés visszaállítva!\nIndítsd újra a panelt.",
        "backup_restore_error_title": "Visszaállítási hiba",
        "refresh": "Frissítés",

        # =============================================================
        #  SQLITE
        # =============================================================
        "sqlite_title": "SQLite adatbázis nézegető",
        "sqlite_file": "SQLite .db / .sqlite fájl",
        "sqlite_file_ph": "SQLite .db / .sqlite fájl",
        "quick_sql": "Gyors SQL lekérdezés",
        "quick_sql_ph": "Gyors SQL lekérdezés: SELECT * FROM users LIMIT 100",
        "open_table": "Tábla megnyitása",
        "open_table_btn": "Tábla megnyitása",
        "run_sql": "SQL futtatása",
        "run_sql_btn": "SQL futtatása",
        "browse": "Tallózás",

        # =============================================================
        #  SERVERS
        # =============================================================
        "server_settings": "Szerverek beállításai",
        "servers_title": "Szerverek beállításai",
        "servers_need_bot": "Előbb tallózd be a bot érvényes .py fájlját!",
        "servers_folder_missing": "Nincs szerver adat mappa:\n{path}",
        "no_servers": "Nincsenek szerver JSON fájlok.",
        "no_servers_msg": "Nincsenek szerver JSON fájlok.",
        "servers_info_line": "{name} | ID: {id} | Tagok: {members} | v{version}",
        "servers_edit_title": "Szerkesztés: {name}",
        "servers_edit_server_lbl": "Szerver szerkesztése: {name}",
        "servers_edit_btn": "Szerkesztés",
        "servers_read_error": "Olvasási hiba: {error}",
        "servers_saved_title": "Mentés",
        "servers_saved_msg": "Szerver adatok mentve!",
        "servers_json_error_title": "JSON hiba",
        "servers_json_error_msg": "Érvénytelen JSON:\n{error}",
        "servers_save_error": "Mentési hiba: {error}",
        "servers_json_unreadable": "(olvashatatlan)",
        "servers_unknown_server": "Ismeretlen szerver",
        "servers_unknown_id": "?",

        # =============================================================
        #  ACTIVITY
        # =============================================================
        "activity_title": "Discord Activity Loop",
        "activity_loop": "Activity Loop",
        "activity_enabled": "Activity engedélyezése",
        "activity_enabled_lbl": "Activity engedélyezése",
        "activity_interval": "Váltás gyakorisága (perc):",
        "activity_interval_lbl": "Váltás gyakorisága (perc):",
        "activity_interval_invalid": "Érvénytelen intervallum érték!",
        "activity_text": "Activity szöveg",
        "activity_text_ph": "Activity szöveg",
        "activity_add_btn": "+ Activity hozzáadása",
        "add_activity": "+ Activity hozzáadása",
        "activity_remove_btn": "-",
        "remove": "-",
        "activity_save_btn": "Mentés",

        # =============================================================
        #  TUTORIAL
        # =============================================================
        "tutorial_title": "📖 Tutorial",
        "tutorial_window_title": "📖 Tutorial",
        "tutorial_header_text": "📖  Tutorial",
        "tutorial_categories": "📚 Kategóriák",
        "tutorial_categories_lbl": "📚 Kategóriák",
        "tutorial_hint": "💡 Válassz kategóriát\n      a bal oldalról",
        "github_btn": "🌐 GitHub",
        "tutorial_github_btn": "🌐 GitHub",

        # =============================================================
        #  ACHIEVEMENTS
        # =============================================================
        "achievements_title": "🏆 Achievementek",
        "achievements_header_text": "🏆 Achievementek — {unlocked}/{total}",
        "achievements_btn": "Achievementek",
        "ach_unlocked_toast": "{icon} Achievement feloldva: {name}",
        "ach_unlocked_log": "Achievement feloldva: {name} — {desc}",

        # Achievement nevek + leírások
        "ach_first_start_name": "Első lépés",
        "ach_first_start_desc": "Elindítottál egy botot",
        "ach_first_backup_name": "Biztonságos",
        "ach_first_backup_desc": "Készítettél egy backupot",
        "ach_first_plugin_name": "Bővítő",
        "ach_first_plugin_desc": "Létrehoztál egy plugint",
        "ach_first_commander_name": "Parancsnok",
        "ach_first_commander_desc": "Létrehoztál egy Commander parancsot",
        "ach_three_bots_name": "Sokaság",
        "ach_three_bots_desc": "3 botot regisztráltál",
        "ach_five_bots_name": "Flotta",
        "ach_five_bots_desc": "5 botot regisztráltál",
        "ach_ten_bots_name": "Armada",
        "ach_ten_bots_desc": "10 botot regisztráltál",
        "ach_uptime_1h_name": "Kitartó",
        "ach_uptime_1h_desc": "Egy bot 1 órán át futott",
        "ach_uptime_10h_name": "Hosszútávfutó",
        "ach_uptime_10h_desc": "Egy bot 10 órán át futott",
        "ach_uptime_100h_name": "Maratonista",
        "ach_uptime_100h_desc": "Egy bot 100 órán át futott",
        "ach_ten_backups_name": "Gyűjtögető",
        "ach_ten_backups_desc": "10 backupot készítettél",
        "ach_error_free_day_name": "Hibátlan nap",
        "ach_error_free_day_desc": "Egy napig nem volt hiba",
        "ach_appearance_user_name": "Művész",
        "ach_appearance_user_desc": "Beállítottad egy bot emoji-ját/színét",
        "ach_hotkey_user_name": "Gyorsujjú",
        "ach_hotkey_user_desc": "Használtál egy gyorsgombot",
        "ach_theme_switcher_name": "Változatos",
        "ach_theme_switcher_desc": "Váltottál témát",

        # =============================================================
        #  STREAK
        # =============================================================
        "streak_lbl": "🔥 Streak",
        "streak_header": "🔥 STREAK",
        "streak_days": "{days} nap",
        "streak_days_lbl": "nap",
        "streak_best": "Legjobb: {days} nap",
        "streak_best_lbl": "Legjobb: {n} nap",
        "streak_short": "🔥 {days} nap",
        "streak_started": "🔥 Streak elindult!",
        "streak_milestone": "🔥 {days} napos streak!",
        "streak_progress": "🔥 {days} napos streak",
        "streak_log": "Streak: {days} nap (legjobb: {best})",

        # =============================================================
        #  AI
        # =============================================================
        "ai_chat_title": "🤖 AI Asszisztens",
        "ai_chat_header": "🤖  AI Asszisztens",
        "ai_chat_provider_lbl": "Provider: {provider}",
        "ai_chat_welcome": "👋 Szia! Miben segíthetek ma?",
        "ai_chat_placeholder": "Írd be a kérdést...",
        "ai_send_btn": "📤 Küldés",
        "ai_input_ph": "Írd be a kérdést...",
        "ai_generate_btn": "✨ Generálás",
        "ai_save_btn": "💾 Mentés",
        "ai_code_title": "✨ AI Kód Generátor",
        "ai_codegen_title": "✨ AI Kód Generátor",
        "ai_codegen_header": "✨  AI Kód Generátor",
        "ai_codegen_prompt_lbl": "Írd le, mire van szükséged:",
        "ai_codegen_output_lbl": "Generált kód:",
        "ai_codegen_generate_btn": "✨ Generálás",
        "ai_codegen_save_btn": "💾 Mentés a bot mappájába",
        "ai_codegen_status_done": "✅ Kód generálva",
        "ai_codegen_status_thinking": "⏳ Gondolkodom...",
        "ai_codegen_nothing_to_save": "Nincs mit menteni!",
        "ai_codegen_need_bot_file": "Előbb tallózd be a bot .py fájlját!",
        "ai_codegen_need_prompt": "Adj meg egy leírást!",
        "ai_codegen_saved": "✅ Kód elmentve",
        "ai_codegen_log_saved": "AI kód mentve: {path}",
        "ai_error_title": "🔍 AI Hibaelemzés",
        "ai_error_header": "🔍  Hibaelemzés",
        "ai_error_input_lbl": "Hiba / stack trace:",
        "ai_error_output_lbl": "AI elemzés:",
        "ai_error_analyzing": "⏳ Elemzés...",
        "ai_error_nothing": "Nincs elemzendő hiba!",
        "ai_docs_title": "📄 AI Dokumentáció",
        "ai_docs_header": "📄  Dokumentáció: {filename}",
        "ai_docs_select_file": "Válassz Python fájlt",
        "ai_docs_filetype": "Python fájlok",
        "ai_docs_read_error": "Olvasási hiba: {error}",
        "ai_docs_generating": "⏳ Dokumentáció generálása...",
        "ai_docs_save_btn": "💾 Mentés",
        "ai_docs_saved": "✅ Dokumentáció mentve",
        "ai_role_user": "Te",
        "ai_role_assistant": "AI",
        "ai_err_no_key": "❌ Nincs beállítva API kulcs! Menj a Beállítások → AI menüpontra.",
        "ai_err_http": "❌ HTTP hiba {code}:\n{body}",
        "ai_err_generic": "❌ Hiba: {error}",
        "ai_settings_provider_lbl": "Provider:",
        "ai_settings_key_lbl": "API kulcs (OpenAI/Claude):",
        "ai_settings_saved": "✅ AI beállítások mentve",
        "ai_settings_save_btn": "💾 Mentés",

        # =============================================================
        #  AFK SCREEN
        # =============================================================
        "afk_hint": "💡 Mozgasd meg az egeret, vagy nyomj meg egy gombot a visszatéréshez",
        "afk_return_hint": "💡 Mozgasd meg az egeret, vagy nyomj meg egy gombot a visszatéréshez",
        "afk_stat_running": "Fut",
        "afk_stat_stopped": "Áll",
        "afk_stat_error": "Hibák",
        "afk_status_stopped": "Leállítva",
        "afk_date_format": "{year}. {month} {day}. ({day_name})",
        "afk_no_bots": "Nincsenek regisztrált botok.",

        # =============================================================
        #  TOAST / ÉRTESÍTÉSEK
        # =============================================================
        "toast_panel_started": "🚀 Panel elindult!",
        "toast_settings_saved": "💾 Beállítások mentve",
        "toast_backup_created": "💾 Biztonsági mentés elkészült",
        "toast_theme_changed": "🎨 Téma: {name}",
        "toast_bot_started": "▶️ Bot elindítva: {name}",
        "toast_bot_stopped": "🛑 Bot leállítva: {name}",
        "toast_bot_crashed": "❌ Bot összeomlott: {name}",
        "panel_started_log": "Panel elindult",

        # =============================================================
        #  PASSWORD
        # =============================================================
        "password_title": "Jelszó szükséges",
        "password_protection_lbl": "🔒 Panel jelszóvédelem",
        "password_prompt": "Add meg a belépési jelszót:",
        "password_ph": "Jelszó...",
        "login_btn": "Belépés",
        "wrong_password_msg": "❌ Hibás jelszó! Próbáld újra.",

        # =============================================================
        #  HOTKEYS
        # =============================================================
        "hotkeys_registered_log": "Gyorsgombok regisztrálva",
        "hotkeys_saved": "💾 Mentve (gyorsgombbal)",
        "hotkeys_save_error": "❌ Hiba: {error}",
        "hotkeys_backup_done": "💾 Mentés kész (gyorsgombbal)",
        "hotkeys_confirm_title": "Megerősítés",
        "hotkeys_restart_all_confirm": "Újraindítod az összes botot?",
        "hotkeys_restart_all_done": "🔄 Összes bot újraindítva",
        "hotkeys_error": "❌ Hiba: {error}",
        "hotkeys_logs_cleared": "🗑️ Naplók törölve",
        "hotkeys_help_title": "⌨️ Gyorsgombok",
        "hotkeys_help_text": (
            "⌨️ Billentyűparancsok\n\n"
            "Ctrl+S — Beállítások mentése\n"
            "Ctrl+B — Biztonsági mentés\n"
            "Ctrl+R — Összes bot újraindítása\n"
            "Ctrl+F — Keresés a naplókban\n"
            "Ctrl+L — Naplók törlése\n"
            "Ctrl+T — Tutorial\n"
            "Ctrl+, — Beállítások\n"
            "Ctrl+W — Panel bezárása\n"
            "Ctrl+1…9 — Botváltás\n"
            "F1 — Tutorial\n"
            "F2 — Ez a súgó\n"
            "F5 — Statisztikák frissítése"
        ),

        # =============================================================
        #  CHARTS
        # =============================================================
        "charts_title": "📈 Élő teljesítmény grafikonok",
        "charts_header": "📈  Élő grafikonok",
        "charts_hint": "🖱️ Hover • 🔍 Zoom • ✋ Húzás",
        "charts_cpu_title": "CPU használat (%)",
        "charts_ram_title": "RAM használat (%)",
        "charts_hover_cpu": "CPU: {value}%",
        "charts_hover_ram": "RAM: {value}%",
        "charts_status_collecting": "⏳ Adatgyűjtés...",
        "charts_status_last": "📊 CPU: {cpu}% | RAM: {ram}% | Pontok: {points}",
        "charts_mpl_missing": "A matplotlib csomag nincs telepítve!",

        # =============================================================
        #  DASHBOARD WIDGETEK
        # =============================================================
        "dashboard_title": "📐 Dashboard",
        "dashboard_header": "📐  Dashboard",
        "dashboard_widgets_btn": "⚙️ Widgetek",
        "dashboard_refresh_btn": "🔄 Frissítés",
        "dashboard_no_widgets": "Nincs engedélyezett widget.\nKattints a '⚙️ Widgetek' gombra.",
        "dashboard_manager_title": "⚙️ Widget kezelő",
        "dashboard_manager_header": "⚙️  Widget kezelő",
        "dashboard_manager_hint": "Pipáld be, mely widgetek jelenjenek meg a dashboardon.",
        "dashboard_save_btn": "💾 Mentés",
        "dashboard_recent_logs_count": "{count} bejegyzés",

        # Widget nevek + leírások
        "widget_uptime_name": "Futási idő",
        "widget_uptime_desc": "Munkamenet futási idő",
        "widget_cpu_name": "CPU",
        "widget_cpu_desc": "Rendszer CPU használat",
        "widget_ram_name": "RAM",
        "widget_ram_desc": "Rendszer RAM használat",
        "widget_active_bots_name": "Aktív botok",
        "widget_active_bots_desc": "Futó botok / összes",
        "widget_total_bots_name": "Összes bot",
        "widget_total_bots_desc": "Regisztrált botok",
        "widget_error_count_name": "Hibák",
        "widget_error_count_desc": "Összes hiba",
        "widget_commands_name": "Parancsok",
        "widget_commands_desc": "Összes parancs",
        "widget_temperature_name": "Hőmérséklet",
        "widget_temperature_desc": "PC hőmérséklet",
        "widget_server_count_name": "Szerverek",
        "widget_server_count_desc": "Discord szerverek",
        "widget_user_count_name": "Felhasználók",
        "widget_user_count_desc": "Elért felhasználók",
        "widget_recent_logs_name": "Friss naplók",
        "widget_recent_logs_desc": "Utolsó naplóbejegyzések",

        # =============================================================
        #  PANEL STATS
        # =============================================================
        "pstats_title": "📊 Panel statisztika",
        "pstats_header": "📊  Panel statisztika",
        "pstats_overview": "📈 Áttekintés",
        "pstats_card_opens": "Megnyitások",
        "pstats_card_total": "Össz idő",
        "pstats_card_session": "Ez a session",
        "pstats_dates_section": "📅 Dátumok",
        "pstats_first_opened": "Első megnyitás: {value}",
        "pstats_last_opened": "Utolsó megnyitás: {value}",
        "pstats_top_features": "🔥 Legtöbbet használt funkciók",
        "pstats_no_data": "Még nincs használati adat.",
        "pstats_time_format": "{hours}ó {minutes}p",
        "pstats_save_btn": "💾 Mentés",
        "pstats_saved": "✅ Statisztika mentve",
        "pstats_reset_btn": "🗑️ Visszaállítás",
        "pstats_reset_title": "Visszaállítás",
        "pstats_reset_confirm": "Visszaállítod az összes panel statisztikát?",

        # Feature nevek
        "feat_settings": "Beállítások",
        "feat_backup": "Backup kezelő",
        "feat_sqlite": "SQLite nézegető",
        "feat_broadcast": "Broadcast",
        "feat_commander": "Commander",
        "feat_plugins": "Pluginok",
        "feat_servers": "Szerverek",
        "feat_global_stats": "Globális statisztika",
        "feat_monthly_report": "Havi riport",
        "feat_tutorial": "Tutorial",
        "feat_basics": "Alapok / Integráció",
        "feat_bot_info": "Bot adatai",
        "feat_activity": "Activity",
        "feat_perf_charts": "Teljesítmény grafikon",
        "feat_appearance": "Megjelenés",
        "feat_animated_charts": "Élő grafikonok",
        "feat_dashboard": "Dashboard",

        # =============================================================
        #  REPORT
        # =============================================================
        "report_title": "Havi riport",
        "report_header": "📅  Havi riport",
        "report_month_lbl": "Hónap:",
        "report_new_month_msg": "Új hónap kezdődött! Szeretnéd elkészíteni a(z) {month} hónap riportját?",
        "report_prev_month_format": "{year}. {month}",
        "report_card_errors": "Hibák",
        "report_card_commands": "Parancsok",
        "report_card_logs": "Napló bejegyzések",
        "report_card_uptime": "Futási idő",
        "report_hours_short": "{hours}ó",
        "report_per_bot": "🤖 Botonkénti bontás",
        "report_no_data": "Nincs adat erre a hónapra.",
        "report_bot_stats_line": "⚠️ {errors} hiba | ⚡ {commands} parancs | 📝 {logs} napló",
        "report_top_commands": "🔥 Top parancsok",
        "report_daily_activity": "📊 Napi aktivitás",
        "report_data_status": "📊 Adatok: {month}",
        "report_export_json_btn": "📤 JSON",
        "report_export_text_btn": "📄 Szöveg",
        "report_export_title": "Exportálás",
        "report_export_saved": "✅ Mentve: {path}",
        "report_exported_toast": "✅ JSON exportálva",
        "report_text_exported_toast": "✅ Szöveg exportálva",
        "report_txt_title": "Havi riport — {month}",
        "report_txt_total_errors": "Összes hiba: {count}",
        "report_txt_total_commands": "Összes parancs: {count}",
        "report_txt_total_uptime": "Összes futási idő: {hours}ó",
        "report_txt_per_bot": "BOTONKÉNT",
        "report_txt_bot_header": "Bot: {name}",
        "report_txt_bot_errors": "  Hibák: {count}",
        "report_txt_bot_commands": "  Parancsok: {count}",
        "report_txt_bot_logs": "  Napló bejegyzések: {count}",
        "report_txt_bot_first": "  Első napló: {value}",
        "report_txt_bot_last": "  Utolsó napló: {value}",
        "report_txt_top_commands": "TOP PARANCSOK",
        "report_txt_cmd_line": "  {cmd}: {count}x",
        "report_txt_filetype": "Szöveges fájl",

        # =============================================================
        #  PLUGINS
        # =============================================================
        "plugins": "Pluginok",
        "plugins_help": "Bővítsd a panelt pluginokkal",
        "plugins_list_lbl": "Telepített pluginok",
        "plugins_select_hint": "Válassz egy plugint a listából",
        "plugins_loaded_status": "✅ Betöltve: {name}",
        "plugins_saved_status": "✅ Mentve: {name}",
        "plugins_saved_log": "Plugin mentve: {name}",
        "plugins_reloaded_status": "✅ Pluginok újratöltve",
        "plugins_reloaded_log": "Pluginok újratöltve",
        "plugins_read_error": "Olvasási hiba: {error}",
        "plugins_save_error": "Mentési hiba: {error}",
        "plugins_syntax_error_title": "Szintaktikai hiba",
        "plugins_syntax_error_msg": "{line}. sor: {msg}",
        "plugins_new_dialog_title": "Új plugin",
        "plugins_new_dialog_header": "🧩  Új plugin készítése",
        "plugins_new_filename_lbl": "Fájlnév:",
        "plugins_new_template_lbl": "Sablon:",
        "plugins_invalid_filename": "Érvénytelen fájlnév!",
        "plugins_exists_title": "Fájl létezik",
        "plugins_exists_confirm": "Felülírod: '{name}'?",
        "plugins_created_log": "Plugin létrehozva: {name}",
        "plugins_delete_confirm": "Törlöd a(z) '{name}' plugint?",
        "plugins_deleted_log": "Plugin törölve: {name}",
        "plugins_need_select": "Előbb válassz ki egy plugint!",
        "plugins_new_btn": "➕ Új",
        "plugins_save_btn": "💾 Mentés",
        "plugins_delete_btn": "🗑️ Törlés",
        "plugins_reload_btn": "🔄 Újratöltés",
        "plugins_create_btn": "Létrehozás",
        "plugins_load_error": "Plugin betöltési hiba: {file} — {error}",

        # Plugin sablonok
        "plugin_tpl_empty_name": "Üres",
        "plugin_tpl_event_logger_name": "Esemény loggoló",
        "plugin_tpl_sidebar_button_name": "Sidebar gomb",
        "plugin_tpl_custom_window_name": "Egyedi ablak",
        "plugin_tpl_welcome_log_name": "Üdvözlő üzenet",
        "plugin_tpl_bot_watcher_name": "Bot figyelő",
        "plugin_tpl_error_beep_name": "Hangjelzés hibánál",
        "plugin_tpl_calculator_name": "Számológép",
        "plugin_tpl_theme_switcher_name": "Téma váltó",
        "plugin_tpl_webhook_name": "Webhook",

        # =============================================================
        #  UI ENHANCEMENTS
        # =============================================================
        "ui_search_placeholder": "🔍 Bot keresése...",
        "ui_status_online_spinner": "● {char} ONLINE",
        "ui_switch_toast": "🤖 Váltás: {name}",
        "ui_appearance_title": "Megjelenés: {name}",
        "ui_appearance_header": "🎨  Megjelenés: {name}",
        "ui_emoji_lbl": "Emoji",
        "ui_color_lbl": "Szín",
        "ui_custom_hex_lbl": "Egyedi hex:",
        "ui_apply_btn": "Alkalmaz",
        "ui_appearance_saved": "✅ Megjelenés mentve: {name}",
        "ui_save_btn": "💾 Mentés",
        "ui_cancel_btn": "Mégse",
        "ui_sidebar_opened": "📂 Sidebar kinyitva",
        "ui_sidebar_collapsed": "📁 Sidebar összecsukva",

        # =============================================================
        #  SPLASH
        # =============================================================
        "splash_title": "Discord Bot Manager",
        "splash_title_text": "Discord Bot Manager",
        "splash_subtitle": "Professzionális Multi-Bot Panel",
        "splash_status_loading": "Betöltés...",
        "splash_status_init": "Inicializálás...",
        "splash_status_config": "Konfiguráció betöltése...",
        "splash_status_modules": "Modulok betöltése...",
        "splash_status_bots": "Botok előkészítése...",
        "splash_status_ui": "Felület építése...",
        "splash_status_done": "Kész!",
        "splash_tip_1": "💡 Tipp: Ctrl+S gyorsan menti a beállításokat",
        "splash_tip_2": "💡 Tipp: Használd a Tömeges vezérlést az összes bot indításához",
        "splash_tip_3": "💡 Tipp: Készíts rendszeresen biztonsági mentést",
        "splash_tip_4": "💡 Tipp: Testreszabhatod a botok színét a Megjelenés szerkesztővel",
        "splash_tip_5": "💡 Tipp: Az AI Asszisztens segít a crash-ek elemzésében",
        "splash_tip_6": "💡 Tipp: Használd a /connect parancsot Discordban a bot összekötéséhez",
        "splash_tip_7": "💡 Tipp: Állíts be időzített újraindítást a stabilitásért",
        "splash_tip_8": "💡 Tipp: Kapcsold be az AFK képernyőt a bot állapot megtekintéséhez",
        "splash_tip_9": "💡 Tipp: Nézd meg a havi riportokat az elemzésekhez",
        "splash_tip_10": "💡 Tipp: Használd a Commandert parancsok kód nélküli létrehozásához",

        # =============================================================
        #  DÁTUM — NAPOK / HÓNAPOK
        # =============================================================
        "day_monday": "Hétfő",
        "day_tuesday": "Kedd",
        "day_wednesday": "Szerda",
        "day_thursday": "Csütörtök",
        "day_friday": "Péntek",
        "day_saturday": "Szombat",
        "day_sunday": "Vasárnap",
        "month_january": "Január",
        "month_february": "Február",
        "month_march": "Március",
        "month_april": "Április",
        "month_may": "Május",
        "month_june": "Június",
        "month_july": "Július",
        "month_august": "Augusztus",
        "month_september": "Szeptember",
        "month_october": "Október",
        "month_november": "November",
        "month_december": "December",

        # =============================================================
        #  REMOTE COMMANDS
        # =============================================================
        "remote_unknown_bot_msg": "Ismeretlen bot: {bot}",
        "remote_start_issued": "{bot} indítási parancsa kiadva.",
        "remote_stop_issued": "{bot} leállítási parancsa kiadva.",
        "remote_restart_issued": "{bot} újraindítási parancsa kiadva.",
        "remote_stress_result": "Stresszteszt kész: fut={running}, CPU={cpu}%, hőmérséklet={temp}.",
        "remote_no_log": "Nincs naplóbejegyzés.",
        "remote_broadcast_handled": "A broadcastot a BotVezerlo hajtja végre.",
        "remote_unknown_cmd": "Ismeretlen parancs. Elérhető: start, stop, restart, info, status, stressz, log.",
        "remote_status_line": "Panel {panel_id} | {bot}: {status} | RAM {ram} | CPU {cpu} | Hőmérséklet {temp}",
        "remote_invalid_panel": "❌ Érvénytelen panel azonosító.",
        "remote_connected": "✅ Csatlakozva a panelhez.",
        "remote_use_connect": "Előbb használd a /connect parancsot.",
        "remote_test_mode": "🧪 A bot teszt módban van. Csak tesztelők használhatják.",

        # =============================================================
        #  EGYÉB
        # =============================================================
        "temp_cpu_fallback": "CPU: {cpu}%",
        "tray_open": "Panel megnyitása",
        "tray_quit": "Kilépés",
        "tray_tooltip": "Bot Manager",
        "rpc_details": "Botokat kezel a DBM-ben",
        "rpc_state": "DJ Baluss Panel",
        "log_manual_save": "Beállítások manuálisan mentve",
        "settings_manually_saved_msg": "Beállítások manuálisan mentve",
        "auto_start_process_started_msg": "✅ Bot folyamat elindult (PID: {pid})",
        "auto_start_error_msg": "❌ Auto-indítási hiba: {error}",
        "bot_process_started_msg": "✅ Bot folyamat elindult (PID: {pid})",
        "start_error_msg": "❌ Indítási hiba: {error}",
        "bot_process_stopped_msg": "🛑 Bot leállítva",
        "bot_restart_msg": "🔄 Bot újraindítása...",
        "bot_unexpected_stop_msg": "❌ Bot váratlanul leállt (kód: {code})",
        "crash_watchdog_msg": "🔄 Crash watchdog: újraindítás {n} másodperc múlva",
        "midnight_restart_event_msg": "🌙 Éjféli újraindítás aktiválva",
        "auto_restart_event_msg": "⏰ Időzített újraindítás aktiválva",
        "all_bots_start_log": "Összes bot elindítva",
        "all_bots_start_msg": "✅ Összes bot elindult!",
        "all_bots_restart_log": "Összes bot újraindítva",
        "all_bots_restart_msg": "🔄 Összes bot újraindult!",
        "all_bots_stop_log": "Összes bot leállítva",
        "all_bots_stop_msg": "🛑 Összes bot leállt!",
        "test_mode_on_status": "BE",
        "test_mode_off_status": "KI",
        "test_mode_changed_msg": "Teszt mód: {status}",
        "settings_manually_saved_msg": "✅ Beállítások mentve",
        "file_not_found_msg": "Fájl nem található:\n{path}",
    },
}


# =====================================================================
#  KÜLSŐ lang.json FELÜLÍRÁS (ha van)
# =====================================================================
try:
    with open(LANG_FILE, "r", encoding="utf-8") as language_file:
        _external = json.load(language_file)
        for lang_key in _external:
            if lang_key in LANGUAGES:
                LANGUAGES[lang_key].update(_external[lang_key])
            else:
                LANGUAGES[lang_key] = _external[lang_key]
except (OSError, json.JSONDecodeError):
    pass


# =====================================================================
#  SEGÉDFÜGGVÉNY
# =====================================================================
def get_text(lang, key, **kwargs):
    """Egy szöveg lekérése nyelven, helyettesítőkkel."""
    language = LANGUAGES.get(lang, LANGUAGES.get("English", {}))
    text = language.get(key, LANGUAGES.get("English", {}).get(key, key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text