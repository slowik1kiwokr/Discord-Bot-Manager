import os
import json
import uuid
import datetime
import threading

import customtkinter as ctk
from tkinter import messagebox, filedialog

import modules.config as config
from modules.config import BROADCAST_REQUESTS_FILE


# =====================================================================
#  BROADCAST SABLONOK (minden szöveg kulcs!)
# =====================================================================
BROADCAST_TEMPLATES = {
    "simple": {
        "name_key": "bc_tpl_simple_name",
        "type": "message",
        "content_key": "bc_tpl_simple_content",
        "embed": {},
    },
    "maintenance": {
        "name_key": "bc_tpl_maintenance_name",
        "type": "embed",
        "content_key": None,
        "embed": {
            "title_key": "bc_tpl_maintenance_title",
            "description_key": "bc_tpl_maintenance_desc",
            "color": "#f39c12",
            "footer_key": "bc_tpl_maintenance_footer",
            "thumbnail": "",
            "fields": [],
        },
    },
    "new_version": {
        "name_key": "bc_tpl_new_version_name",
        "type": "embed",
        "content_key": None,
        "embed": {
            "title_key": "bc_tpl_new_version_title",
            "description_key": "bc_tpl_new_version_desc",
            "color": "#2ecc71",
            "footer_key": "bc_tpl_new_version_footer",
            "thumbnail": "",
            "fields": [],
        },
    },
    "event": {
        "name_key": "bc_tpl_event_name",
        "type": "embed",
        "content_key": None,
        "embed": {
            "title_key": "bc_tpl_event_title",
            "description_key": "bc_tpl_event_desc",
            "color": "#e91e63",
            "footer_key": "bc_tpl_event_footer",
            "thumbnail": "",
            "fields": [],
        },
    },
    "warning": {
        "name_key": "bc_tpl_warning_name",
        "type": "embed",
        "content_key": None,
        "embed": {
            "title_key": "bc_tpl_warning_title",
            "description_key": "bc_tpl_warning_desc",
            "color": "#e74c3c",
            "footer_key": "bc_tpl_warning_footer",
            "thumbnail": "",
            "fields": [],
        },
    },
    "outage": {
        "name_key": "bc_tpl_outage_name",
        "type": "embed",
        "content_key": None,
        "embed": {
            "title_key": "bc_tpl_outage_title",
            "description_key": "bc_tpl_outage_desc",
            "color": "#c0392b",
            "footer_key": "bc_tpl_outage_footer",
            "thumbnail": "",
            "fields": [],
        },
    },
    "custom": {
        "name_key": "bc_tpl_custom_name",
        "type": "embed",
        "content_key": None,
        "embed": {
            "title_key": "bc_tpl_custom_title",
            "description_key": "bc_tpl_custom_desc",
            "color": "#9b59b6",
            "footer_key": None,
            "thumbnail": "",
            "fields": [],
        },
    },
    "sysinfo": {
        "name_key": "bc_tpl_sysinfo_name",
        "type": "embed",
        "content_key": None,
        "embed": {
            "title_key": "bc_tpl_sysinfo_title",
            "description_key": "bc_tpl_sysinfo_desc",
            "color": "#3498db",
            "footer_key": "bc_tpl_sysinfo_footer",
            "thumbnail": "",
            "fields": [
                {"name_key": "bc_tpl_sysinfo_field1_name",
                 "value_key": "bc_tpl_sysinfo_field1_value", "inline": False},
                {"name_key": "bc_tpl_sysinfo_field2_name",
                 "value_key": "bc_tpl_sysinfo_field2_value", "inline": False},
            ],
        },
    },
}


# Időzítés opciók: (fordítási kulcs, másodpercek)
SCHEDULE_OPTIONS = [
    ("sched_1min", 60),
    ("sched_5min", 300),
    ("sched_10min", 600),
    ("sched_30min", 1800),
    ("sched_1hour", 3600),
    ("sched_6hour", 21600),
    ("sched_24hour", 86400),
]


class WindowBroadcastMixin:
    """Broadcast ablak — szerverek + csatornák + sablonok + időzítés."""

    # ==================================================================
    #  Segéd
    # ==================================================================
    def _bot_dir(self):
        bot = self.bots.get(self.active_bot_key, {})
        sp = bot.get("path", "")
        return os.path.dirname(sp) if sp else None

    def _load_channels(self):
        """Betölti a bot által küldött csatorna listát."""
        bot_dir = self._bot_dir()
        if not bot_dir:
            return []
        path = os.path.join(bot_dir, "bot_channels.json")
        if not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return []

    def _resolve_template(self, tpl_key):
        """A sablon kulcsait a jelenlegi nyelvre fordítja."""
        tpl = BROADCAST_TEMPLATES.get(tpl_key)
        if not tpl:
            return None

        content = self.tr(tpl["content_key"]) if tpl.get("content_key") else ""

        emb = {}
        raw_emb = tpl.get("embed", {}) or {}
        if raw_emb:
            fields = []
            for f in raw_emb.get("fields", []):
                fields.append({
                    "name": self.tr(f.get("name_key", "")),
                    "value": self.tr(f.get("value_key", "")),
                    "inline": f.get("inline", False),
                })
            emb = {
                "title": self.tr(raw_emb.get("title_key", "")) if raw_emb.get("title_key") else "",
                "description": self.tr(raw_emb.get("description_key", "")) if raw_emb.get("description_key") else "",
                "color": raw_emb.get("color", "#5865F2"),
                "footer": self.tr(raw_emb.get("footer_key", "")) if raw_emb.get("footer_key") else "",
                "thumbnail": raw_emb.get("thumbnail", ""),
                "fields": fields,
            }

        return {
            "type": tpl["type"],
            "content": content,
            "embed": emb,
        }

    # ==================================================================
    #  Fő ablak
    # ==================================================================
    def open_broadcast_window(self):
        bot_dir = self._bot_dir()
        if not bot_dir:
            messagebox.showwarning(
                self.tr("warning_title"),
                self.tr("broadcast_need_bot_msg")
            )
            return

        channels_data = self._load_channels()

        # Fordított sablon-név → kulcs mapping
        tpl_name_to_key = {
            self.tr(t["name_key"]): k for k, t in BROADCAST_TEMPLATES.items()
        }
        tpl_display_names = list(tpl_name_to_key.keys())
        default_tpl_display = self.tr(BROADCAST_TEMPLATES["simple"]["name_key"])

        # Időzítés opciók fordítva
        sched_display_values = [self.tr(k) for k, _ in SCHEDULE_OPTIONS]

        win = ctk.CTkToplevel(self)
        win.title(self.tr("broadcast_title"))
        win.geometry("1100x780")
        win.minsize(900, 560)
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 1100) // 2
        y = (win.winfo_screenheight() - 780) // 2
        win.geometry(f"1100x780+{x}+{y}")

        # Fejléc
        header = ctk.CTkFrame(win, fg_color="#c0392b", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text=self.tr("broadcast_header"),
            font=("Arial", 18, "bold"), text_color="white"
        ).pack(side="left", padx=24, pady=16)
        ctk.CTkLabel(
            header, text=self.tr("broadcast_servers_count", count=len(channels_data)),
            font=("Arial", 11), text_color="#ffd0d0"
        ).pack(side="right", padx=20)

        # Fő terület
        main = ctk.CTkFrame(win, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # ============================================================
        #  BAL: Szerverek + csatornák listája
        # ============================================================
        left = ctk.CTkFrame(main, width=380)
        left.pack(side="left", fill="y", padx=(0, 8))
        left.pack_propagate(False)

        ctk.CTkLabel(left, text=self.tr("broadcast_servers_section"),
                      font=("Arial", 13, "bold")).pack(pady=(8, 4))

        ctk.CTkLabel(
            left,
            text=self.tr("broadcast_channels_hint"),
            font=("Arial", 10), text_color="#8a8e98",
            justify="left",
        ).pack(padx=8, pady=(0, 8))

        # Görgethető csatorna lista
        ch_scroll = ctk.CTkScrollableFrame(left, fg_color="#1e2129")
        ch_scroll.pack(fill="both", expand=True, padx=8, pady=4)

        channel_vars = {}  # "guild_id:channel_id" -> BooleanVar

        if not channels_data:
            ctk.CTkLabel(
                ch_scroll,
                text=self.tr("broadcast_no_channels_msg"),
                font=("Arial", 11), text_color="#e67e22",
                justify="center",
            ).pack(pady=30)
        else:
            for guild in channels_data:
                # Szerver fejléc
                g_frame = ctk.CTkFrame(ch_scroll, fg_color="#252932", corner_radius=8)
                g_frame.pack(fill="x", pady=(6, 2))

                ctk.CTkLabel(
                    g_frame,
                    text=f"🌐  {guild['guild_name']}",
                    font=("Arial", 12, "bold"),
                    text_color="#5865F2",
                    anchor="w",
                ).pack(fill="x", padx=10, pady=6)

                # Csatornák
                for ch in guild.get("channels", []):
                    key = f"{guild['guild_id']}:{ch['id']}"
                    can_send = ch.get("can_send", True)

                    row = ctk.CTkFrame(ch_scroll, fg_color="transparent")
                    row.pack(fill="x", padx=12, pady=1)

                    var = ctk.BooleanVar(value=False)
                    channel_vars[key] = var

                    cb = ctk.CTkCheckBox(
                        row,
                        text=f"  #{ch['name']}",
                        variable=var,
                        font=("Arial", 11),
                        state="normal" if can_send else "disabled",
                    )
                    cb.pack(side="left", padx=4, pady=2)

                    # Jogosultság jelző
                    if not can_send:
                        ctk.CTkLabel(row, text="🚫",
                                      font=("Arial", 10)).pack(side="right", padx=4)
                    elif not ch.get("can_embed", True):
                        ctk.CTkLabel(row, text="⚠️",
                                      font=("Arial", 10)).pack(side="right", padx=4)

        # Gyors gombok
        quick_btns = ctk.CTkFrame(left, fg_color="transparent")
        quick_btns.pack(fill="x", padx=8, pady=(4, 8))

        def select_all():
            for var in channel_vars.values():
                var.set(True)

        def deselect_all():
            for var in channel_vars.values():
                var.set(False)

        ctk.CTkButton(quick_btns, text=self.tr("broadcast_select_all_btn"),
                       fg_color="#27ae60", hover_color="#2ecc71",
                       width=100, height=30, font=("Arial", 11),
                       command=select_all).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(quick_btns, text=self.tr("broadcast_deselect_all_btn"),
                       fg_color="#7f8c8d", hover_color="#95a5a6",
                       width=100, height=30, font=("Arial", 11),
                       command=deselect_all).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(quick_btns, text=self.tr("refresh_btn"),
                       fg_color="#3498db", hover_color="#5dade2",
                       width=110, height=30, font=("Arial", 11),
                       command=lambda: (win.destroy(), self.open_broadcast_window())
                       ).pack(side="left", padx=2, expand=True, fill="x")

        # ============================================================
        #  JOBB: üzenet szerkesztő
        # ============================================================
        right = ctk.CTkFrame(main, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True)

        # Felső sáv: sablon + típus
        top_bar = ctk.CTkFrame(right, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(top_bar, text=self.tr("broadcast_template_lbl"),
                      font=("Arial", 11, "bold")).pack(side="left", padx=(0, 6))

        template_var = ctk.StringVar(value=default_tpl_display)

        # Alsó mentés sáv
        bottom = ctk.CTkFrame(right, fg_color="transparent")
        bottom.pack(side="bottom", fill="x", pady=(8, 0))

        # Scrollozható tartalom
        content_scroll = ctk.CTkScrollableFrame(right, fg_color="transparent")
        content_scroll.pack(fill="both", expand=True)

        # Típus
        ctk.CTkLabel(content_scroll, text=self.tr("common_type_lbl"),
                      font=("Arial", 11, "bold"), anchor="w").pack(fill="x", pady=(4, 2))

        # Fix belső értékek
        TYPE_MESSAGE_LABEL = self.tr("common_type_message")
        TYPE_EMBED_LABEL = self.tr("common_type_embed")
        type_var = ctk.StringVar(value=TYPE_MESSAGE_LABEL)
        ctk.CTkComboBox(content_scroll,
                         values=[TYPE_MESSAGE_LABEL, TYPE_EMBED_LABEL],
                         variable=type_var, width=180, height=34).pack(anchor="w")

        # Üzenet frame
        msg_frame = ctk.CTkFrame(content_scroll, fg_color="transparent")
        ctk.CTkLabel(msg_frame, text=self.tr("common_content_lbl"),
                      font=("Arial", 11), anchor="w").pack(fill="x", pady=(0, 2))
        content_box = ctk.CTkTextbox(msg_frame, height=140, font=("Consolas", 11))
        content_box.pack(fill="x")

        # Embed frame
        embed_frame = ctk.CTkFrame(content_scroll, fg_color="transparent")

        ctk.CTkLabel(embed_frame, text=self.tr("common_embed_title_lbl"),
                      font=("Arial", 11), anchor="w").pack(fill="x", pady=(0, 2))
        emb_title = ctk.CTkEntry(embed_frame, width=500, height=34)
        emb_title.pack(anchor="w")

        ctk.CTkLabel(embed_frame, text=self.tr("common_embed_desc_lbl"),
                      font=("Arial", 11), anchor="w").pack(fill="x", pady=(8, 2))
        emb_desc = ctk.CTkTextbox(embed_frame, height=120, font=("Arial", 11))
        emb_desc.pack(fill="x")

        # Szín sor
        color_row = ctk.CTkFrame(embed_frame, fg_color="transparent")
        color_row.pack(fill="x", pady=(8, 0))

        ctk.CTkLabel(color_row, text=self.tr("common_color_lbl"),
                      font=("Arial", 11)).pack(side="left")
        emb_color = ctk.CTkEntry(color_row, width=120, height=32)
        emb_color.insert(0, "#5865F2")
        emb_color.pack(side="left", padx=6)

        color_preview = ctk.CTkFrame(
            color_row, width=32, height=32, corner_radius=6,
            fg_color="#5865F2",
        )
        color_preview.pack(side="left", padx=4)
        color_preview.pack_propagate(False)

        def update_color(*_):
            try:
                color_preview.configure(fg_color=emb_color.get().strip() or "#5865F2")
            except Exception:
                pass

        emb_color.bind("<KeyRelease>", update_color)

        # Gyors színek — meglévő color_* kulcsokat használjuk
        quick_colors = [
            ("color_blurple", "#5865F2"),
            ("color_green",   "#2ecc71"),
            ("color_red",     "#e74c3c"),
            ("color_orange",  "#f39c12"),
            ("color_blue",    "#3498db"),
        ]
        color_quick = ctk.CTkFrame(embed_frame, fg_color="transparent")
        color_quick.pack(fill="x", pady=(4, 0))
        ctk.CTkLabel(color_quick, text=self.tr("common_quick_colors_lbl"),
                      font=("Arial", 10)).pack(side="left", padx=(0, 4))
        for name_key, hexcode in quick_colors:
            ctk.CTkButton(
                color_quick, text=self.tr(name_key), width=64, height=24,
                fg_color=hexcode, hover_color=hexcode,
                text_color="white", font=("Arial", 10),
                command=lambda h=hexcode: (
                    emb_color.delete(0, "end"),
                    emb_color.insert(0, h),
                    update_color(),
                ),
            ).pack(side="left", padx=2)

        ctk.CTkLabel(embed_frame, text=self.tr("common_embed_footer_lbl"),
                      font=("Arial", 11), anchor="w").pack(fill="x", pady=(8, 2))
        emb_footer = ctk.CTkEntry(embed_frame, width=500, height=34)
        emb_footer.pack(anchor="w")

        ctk.CTkLabel(embed_frame, text=self.tr("common_embed_thumb_lbl"),
                      font=("Arial", 11), anchor="w").pack(fill="x", pady=(8, 2))
        emb_thumb = ctk.CTkEntry(embed_frame, width=500, height=34,
                                   placeholder_text="https://...")
        emb_thumb.pack(anchor="w")

        # Szeckiók ki/be
        def toggle_sections(*_):
            if type_var.get() == TYPE_EMBED_LABEL:
                msg_frame.pack_forget()
                embed_frame.pack(fill="x", pady=(10, 0))
            else:
                embed_frame.pack_forget()
                msg_frame.pack(fill="x", pady=(10, 0))

        type_var.trace_add("write", toggle_sections)
        toggle_sections()

        # Sablon alkalmazó
        def apply_template(choice):
            tpl_key = tpl_name_to_key.get(choice)
            if not tpl_key:
                return
            resolved = self._resolve_template(tpl_key)
            if not resolved:
                return

            type_var.set(
                TYPE_EMBED_LABEL if resolved["type"] == "embed" else TYPE_MESSAGE_LABEL
            )
            content_box.delete("1.0", "end")
            content_box.insert("1.0", resolved.get("content", ""))

            emb = resolved.get("embed", {})
            emb_title.delete(0, "end")
            emb_title.insert(0, emb.get("title", ""))
            emb_desc.delete("1.0", "end")
            emb_desc.insert("1.0", emb.get("description", ""))
            emb_color.delete(0, "end")
            emb_color.insert(0, emb.get("color", "#5865F2"))
            update_color()
            emb_footer.delete(0, "end")
            emb_footer.insert(0, emb.get("footer", ""))
            emb_thumb.delete(0, "end")
            emb_thumb.insert(0, emb.get("thumbnail", ""))
            toggle_sections()

        template_combo = ctk.CTkComboBox(
            top_bar, values=tpl_display_names,
            variable=template_var, width=280, height=32,
            command=apply_template,
        )
        template_combo.pack(side="left")

        # Időzítés
        ctk.CTkLabel(
            content_scroll, text=self.tr("broadcast_schedule_section"),
            font=("Arial", 12, "bold"), anchor="w"
        ).pack(fill="x", pady=(16, 4))

        schedule_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            content_scroll,
            text=self.tr("broadcast_schedule_check"),
            variable=schedule_var,
            font=("Arial", 11),
        ).pack(anchor="w", pady=2)

        sched_row = ctk.CTkFrame(content_scroll, fg_color="transparent")
        sched_row.pack(fill="x", pady=(6, 0))

        ctk.CTkLabel(sched_row, text=self.tr("broadcast_when_lbl"),
                      font=("Arial", 11)).pack(side="left")
        when_var = ctk.StringVar(value=sched_display_values[1])  # 5 perc
        ctk.CTkComboBox(
            sched_row,
            values=sched_display_values,
            variable=when_var, width=180, height=32,
        ).pack(side="left", padx=8)

        # Alkalmazás inicializálás (sablont alkalmazunk)
        apply_template(default_tpl_display)

        # ============================================================
        #  KÜLDÉS
        # ============================================================
        def send_broadcast():
            # Csatornák összegyűjtése
            selected = {}
            for key, var in channel_vars.items():
                if var.get():
                    g_id, c_id = key.split(":", 1)
                    selected[g_id] = c_id  # utolsó csatorna nyer per szerver

            if not selected:
                messagebox.showwarning(
                    self.tr("warning_title"),
                    self.tr("broadcast_no_channel_msg"),
                    parent=win,
                )
                return

            # Üzenet vagy embed tartalom
            is_embed = (type_var.get() == TYPE_EMBED_LABEL)
            msg_type = "embed" if is_embed else "message"

            if msg_type == "message":
                content = content_box.get("1.0", "end-1c").strip()
                if not content:
                    messagebox.showwarning(self.tr("warning_title"),
                                             self.tr("broadcast_msg_empty_msg"),
                                             parent=win)
                    return
                message_payload = {"type": "message", "content": content}
            else:
                embed_data = {
                    "title": emb_title.get().strip(),
                    "description": emb_desc.get("1.0", "end-1c").strip(),
                    "color": emb_color.get().strip() or "#5865F2",
                    "footer": emb_footer.get().strip(),
                    "thumbnail": emb_thumb.get().strip(),
                    "fields": [],
                }
                if not embed_data["title"] and not embed_data["description"]:
                    messagebox.showwarning(self.tr("warning_title"),
                                             self.tr("broadcast_embed_empty_msg"),
                                             parent=win)
                    return
                message_payload = {"type": "embed", "embed": embed_data}

            # Időzítés — index alapján
            delay_seconds = 0
            if schedule_var.get():
                try:
                    idx = sched_display_values.index(when_var.get())
                    delay_seconds = SCHEDULE_OPTIONS[idx][1]
                except (ValueError, IndexError):
                    delay_seconds = 0
                scheduled_time = (datetime.datetime.now()
                                    + datetime.timedelta(seconds=delay_seconds))
            else:
                scheduled_time = None

            # Broadcast request írása
            request = {
                "id": uuid.uuid4().hex,
                "bot": self.active_bot_key,
                "message": message_payload.get("content", ""),  # legacy
                "channels": selected,
                "payload": message_payload,
                "delay_seconds": delay_seconds,
                "scheduled_time": scheduled_time.isoformat(timespec="seconds") if scheduled_time else "",
                "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
            }

            # Módosítsuk a payload alapján a "message" mezőt
            if msg_type == "embed":
                request["message"] = "[EMBED]"

            try:
                pending = []
                if os.path.exists(BROADCAST_REQUESTS_FILE):
                    with open(BROADCAST_REQUESTS_FILE, "r", encoding="utf-8") as f:
                        try:
                            pending = json.load(f)
                        except json.JSONDecodeError:
                            pending = []

                pending.append(request)

                tmp = BROADCAST_REQUESTS_FILE + ".tmp"
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(pending, f, ensure_ascii=False)
                os.replace(tmp, BROADCAST_REQUESTS_FILE)

                if delay_seconds > 0:
                    self.notify(
                        self.tr("broadcast_scheduled_toast",
                                minutes=delay_seconds // 60),
                        "success", 3000
                    )
                    self.log_event("EVENT",
                                   self.tr("broadcast_scheduled_log",
                                           bot=self.active_bot_key,
                                           count=len(selected)))
                else:
                    self.notify(
                        self.tr("broadcast_sent_toast", count=len(selected)),
                        "success", 3000
                    )
                    self.log_event("EVENT",
                                   self.tr("broadcast_sent_log",
                                           bot=self.active_bot_key,
                                           count=len(selected)))

                win.destroy()

            except (OSError, json.JSONDecodeError) as e:
                messagebox.showerror(self.tr("error_title"),
                                       self.tr("broadcast_send_error_msg", error=e),
                                       parent=win)

        # Előnézet gomb
        ctk.CTkButton(
            bottom,
            text=self.tr("broadcast_preview_btn"),
            fg_color="#7f8c8d", hover_color="#95a5a6",
            width=140, height=44, font=("Arial", 12),
            command=lambda: self._broadcast_preview(
                type_var.get(), content_box, emb_title, emb_desc,
                emb_color, emb_footer, emb_thumb, win,
                TYPE_EMBED_LABEL,
            ),
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            bottom,
            text=self.tr("broadcast_send_btn"),
            fg_color="#c0392b", hover_color="#e74c3c",
            width=220, height=44, font=("Arial", 13, "bold"),
            command=send_broadcast,
        ).pack(side="right", padx=4)

    # ==================================================================
    #  Előnézet ablak
    # ==================================================================
    def _broadcast_preview(self, msg_type, content_box, emb_title, emb_desc,
                            emb_color, emb_footer, emb_thumb, parent,
                            type_embed_label):
        preview = ctk.CTkToplevel(parent)
        preview.title(self.tr("broadcast_preview_title"))
        preview.geometry("560x460")
        preview.grab_set()
        preview.update_idletasks()
        x = (preview.winfo_screenwidth() - 560) // 2
        y = (preview.winfo_screenheight() - 460) // 2
        preview.geometry(f"560x460+{x}+{y}")

        header = ctk.CTkFrame(preview, fg_color="#2b2d31", corner_radius=8)
        header.pack(fill="x", padx=14, pady=(14, 8))

        ctk.CTkLabel(header, text="🤖  MainBot",
                      font=("Arial", 12, "bold"),
                      text_color="#5865F2").pack(anchor="w", padx=12, pady=(8, 0))
        ctk.CTkLabel(header, text=self.tr("broadcast_preview_time"),
                      font=("Arial", 9), text_color="#888").pack(anchor="w", padx=12, pady=(0, 8))

        body = ctk.CTkFrame(preview, fg_color="#2b2d31", corner_radius=8)
        body.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        if msg_type == type_embed_label:
            color = emb_color.get().strip() or "#5865F2"
            try:
                stripe = ctk.CTkFrame(body, width=5, fg_color=color, corner_radius=2)
                stripe.pack(side="left", fill="y", padx=(10, 0), pady=10)
            except Exception:
                pass

            inner = ctk.CTkFrame(body, fg_color="transparent")
            inner.pack(side="left", fill="both", expand=True, padx=12, pady=10)

            title = emb_title.get().strip()
            if title:
                ctk.CTkLabel(inner, text=title,
                              font=("Arial", 13, "bold"),
                              text_color="white",
                              anchor="w", justify="left",
                              wraplength=440).pack(fill="x", pady=(0, 6))

            desc = emb_desc.get("1.0", "end-1c").strip()
            if desc:
                ctk.CTkLabel(inner, text=desc,
                              font=("Arial", 11),
                              text_color="#dcddde",
                              anchor="w", justify="left",
                              wraplength=440).pack(fill="x")

            footer = emb_footer.get().strip()
            if footer:
                ctk.CTkLabel(inner, text=footer,
                              font=("Arial", 9),
                              text_color="#888",
                              anchor="w").pack(fill="x", pady=(10, 0))
        else:
            content = content_box.get("1.0", "end-1c").strip()
            ctk.CTkLabel(body, text=content or self.tr("broadcast_empty_msg"),
                          font=("Arial", 11),
                          text_color="#dcddde",
                          anchor="w", justify="left",
                          wraplength=490).pack(fill="both", expand=True, padx=14, pady=14)

        ctk.CTkButton(preview, text=self.tr("close_btn"),
                       fg_color="#555555", hover_color="#666666",
                       width=120, height=36,
                       command=preview.destroy).pack(pady=(0, 14))