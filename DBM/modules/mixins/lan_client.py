import json
import threading
import urllib.request
import urllib.error
import time
import datetime

import customtkinter as ctk


class LANClientMixin:
    """LAN kliens — másik panelhez csatlakozás."""

    def init_lan_client(self):
        self._lan_client_win = None
        self._lan_client_config = {
            "host": getattr(self, "lan_client_host", ""),
            "port": getattr(self, "lan_client_port", 8765),
            "token": getattr(self, "lan_client_token", ""),
        }
        self._lan_client_cache = None
        self._lan_client_connected = False
        self._lan_client_running = False

    # ==================================================================
    #  Ablak megnyitása
    # ==================================================================
    def open_lan_client_window(self):
        if self._lan_client_win is not None:
            try:
                if self._lan_client_win.winfo_exists():
                    self._lan_client_win.focus_force()
                    return
            except Exception:
                pass

        win = ctk.CTkToplevel(self)
        self._lan_client_win = win
        win.title(self.tr("lan_client_title"))
        win.geometry("900x680")
        win.minsize(760, 520)
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 900) // 2
        y = (win.winfo_screenheight() - 680) // 2
        win.geometry(f"900x680+{x}+{y}")

        # --- Fejléc ---
        header = ctk.CTkFrame(win, fg_color="#0f1a3a", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkFrame(header, height=2, fg_color="#3b82f6",
                     corner_radius=0).pack(side="bottom", fill="x")

        ctk.CTkLabel(header, text="🔗  " + self.tr("lan_client_title"),
                      font=("Arial", 17, "bold"), text_color="#7dd3fc").pack(
            side="left", padx=22, pady=16)

        status_lbl = ctk.CTkLabel(header, text="⚪ " + self.tr("lan_disconnected"),
                                    font=("Arial", 11, "bold"),
                                    text_color="#e74c3c")
        status_lbl.pack(side="right", padx=22)

        # --- Kapcsolódási sáv ---
        conn = ctk.CTkFrame(win, fg_color="#1a1d26", corner_radius=0, height=70)
        conn.pack(fill="x")
        conn.pack_propagate(False)

        inner = ctk.CTkFrame(conn, fg_color="transparent")
        inner.pack(fill="x", padx=18, pady=16)

        ctk.CTkLabel(inner, text=self.tr("lan_host_lbl"),
                      font=("Arial", 11), text_color="#b8bcc6").pack(side="left")
        host_entry = ctk.CTkEntry(inner, width=160, height=32, font=("Consolas", 11))
        host_entry.insert(0, self._lan_client_config["host"])
        host_entry.pack(side="left", padx=(8, 12))

        ctk.CTkLabel(inner, text=self.tr("lan_port_lbl"),
                      font=("Arial", 11), text_color="#b8bcc6").pack(side="left")
        port_entry = ctk.CTkEntry(inner, width=80, height=32, font=("Consolas", 11))
        port_entry.insert(0, str(self._lan_client_config["port"]))
        port_entry.pack(side="left", padx=(8, 12))

        ctk.CTkLabel(inner, text=self.tr("lan_token_lbl"),
                      font=("Arial", 11), text_color="#b8bcc6").pack(side="left")
        token_entry = ctk.CTkEntry(inner, width=200, height=32, font=("Consolas", 11),
                                     show="•")
        token_entry.insert(0, self._lan_client_config["token"])
        token_entry.pack(side="left", padx=(8, 12))

        connect_btn = ctk.CTkButton(
            inner, text="🔌 " + self.tr("lan_connect_btn"),
            fg_color="#27ae60", hover_color="#2ecc71",
            width=130, height=32, font=("Arial", 11, "bold"),
            command=lambda: do_connect(),
        )
        connect_btn.pack(side="left")

        # --- Info sáv ---
        info = ctk.CTkFrame(win, fg_color="#0d0f14", corner_radius=0, height=32)
        info.pack(fill="x")
        info.pack_propagate(False)
        info_lbl = ctk.CTkLabel(info, text="", font=("Consolas", 10),
                                  text_color="#8a8e98", anchor="w")
        info_lbl.pack(side="left", padx=18, pady=6)

        # --- Bot lista ---
        bots_wrap = ctk.CTkScrollableFrame(win, fg_color="transparent")
        bots_wrap.pack(fill="both", expand=True, padx=16, pady=14)

        # --- Log ablak ---
        log_frame = ctk.CTkFrame(win, fg_color="#0a0c10", corner_radius=8,
                                   border_width=1, border_color="#2f3542", height=140)
        log_frame.pack(fill="x", padx=16, pady=(0, 12))
        log_frame.pack_propagate(False)

        log_header = ctk.CTkFrame(log_frame, fg_color="transparent")
        log_header.pack(fill="x", padx=12, pady=(8, 4))
        ctk.CTkLabel(log_header, text="📋  " + self.tr("lan_client_logs"),
                      font=("Arial", 11, "bold"), text_color="#7dd3fc").pack(side="left")

        log_box = ctk.CTkTextbox(log_frame, font=("Consolas", 10),
                                   fg_color="#050608", text_color="#b8bcc6")
        log_box.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        log_box.insert("1.0", self.tr("lan_client_logs_hint"))
        log_box.configure(state="disabled")

        def log_line(text):
            try:
                log_box.configure(state="normal")
                ts = datetime.datetime.now().strftime("%H:%M:%S")
                log_box.insert("end", f"[{ts}] {text}\n")
                log_box.see("end")
                log_box.configure(state="disabled")
            except Exception:
                pass

        # ==============================================================
        #  Kapcsolódás logika
        # ==============================================================
        client_state = {
            "running": False,
            "thread": None,
            "host": "",
            "port": 8765,
            "token": "",
        }

        def do_connect():
            host = host_entry.get().strip()
            try:
                port = int(port_entry.get().strip())
            except ValueError:
                log_line("❌ " + self.tr("lan_invalid_port"))
                return
            token = token_entry.get().strip()

            if not host:
                log_line("❌ " + self.tr("lan_invalid_host"))
                return

            # Ha már fut, állítsuk le
            if client_state["running"]:
                client_state["running"] = False
                time.sleep(0.3)

            client_state["host"] = host
            client_state["port"] = port
            client_state["token"] = token
            client_state["running"] = True

            # Mentés
            self.lan_client_host = host
            self.lan_client_port = port
            self.lan_client_token = token
            try:
                self.save_config()
            except Exception:
                pass

            connect_btn.configure(state="disabled",
                                    text="⏳ " + self.tr("lan_connecting"))
            log_line(f"🔌 {self.tr('lan_connecting_to', host=host, port=port)}")

            def worker():
                base = f"http://{host}:{port}"
                fail_count = 0

                while client_state["running"]:
                    try:
                        # Ping
                        req = urllib.request.Request(
                            f"{base}/api/status",
                            headers={"X-API-Key": token} if token else {},
                        )
                        with urllib.request.urlopen(req, timeout=4) as r:
                            data = json.loads(r.read().decode("utf-8"))
                        fail_count = 0

                        # Frissítés a main thread-en
                        self.after(0, lambda d=data: update_ui(d, True, base))

                    except Exception as e:
                        fail_count += 1
                        err_msg = str(e)
                        self.after(0, lambda em=err_msg, fc=fail_count:
                                    on_connection_fail(em, fc))

                    time.sleep(2)

                self.after(0, lambda: connect_btn.configure(
                    state="normal", text="🔌 " + self.tr("lan_connect_btn")))

            def update_ui(data, ok, base):
                nonlocal state_holder
                state_holder = {"ok": ok}
                # Státusz
                if ok:
                    status_lbl.configure(
                        text="🟢 " + self.tr("lan_connected"),
                        text_color="#2ecc71")
                    self._lan_client_cache = data
                    self._lan_client_connected = True
                # Info
                try:
                    info_lbl.configure(
                        text=f"Panel: {data.get('panel_id', '?')}  |  "
                              f"Active: {data.get('active_bot', '?')}  |  "
                              f"Temp: {data.get('temperature', '?')}"
                    )
                except Exception:
                    pass
                # Bot lista újraépítés
                render_bots(data.get("bots", []))

            def on_connection_fail(err_msg, fail_count):
                if fail_count == 1:
                    log_line(f"❌ {err_msg}")
                if fail_count >= 3:
                    status_lbl.configure(
                        text="⚪ " + self.tr("lan_disconnected"),
                        text_color="#e74c3c")
                    self._lan_client_connected = False
                    info_lbl.configure(text=self.tr("lan_host_offline"))

            state_holder = {"ok": False}

            def render_bots(bots):
                for w in bots_wrap.winfo_children():
                    w.destroy()

                if not bots:
                    ctk.CTkLabel(bots_wrap, text=self.tr("lan_no_bots"),
                                  font=("Arial", 12), text_color="#6a6e78").pack(pady=30)
                    return

                for bot in bots:
                    is_running = bot.get("is_running", False)
                    color = bot.get("color", "#5865F2")
                    emoji = bot.get("emoji", "🤖")

                    card = ctk.CTkFrame(bots_wrap, fg_color="#1a1d26",
                                          corner_radius=10)
                    card.pack(fill="x", pady=4)

                    # Bal oldal — ikon + név
                    left = ctk.CTkFrame(card, fg_color="transparent")
                    left.pack(side="left", fill="x", expand=True, padx=14, pady=12)

                    ctk.CTkLabel(left, text=f"{emoji}  {bot.get('name', '?')}",
                                  font=("Arial", 13, "bold"),
                                  text_color=color, anchor="w").pack(fill="x")

                    status_color = "#2ecc71" if is_running else "#e74c3c"
                    status_text = self.tr("lan_running") if is_running else self.tr("lan_stopped")
                    ctk.CTkLabel(
                        left,
                        text=f"{status_text}  •  "
                              f"RAM: {bot.get('ram_mb', 0)} MB  •  "
                              f"CPU: {bot.get('cpu_percent', 0)}%  •  "
                              f"Hibák: {bot.get('error_count', 0)}",
                        font=("Consolas", 10), text_color="#8a8e98",
                        anchor="w",
                    ).pack(fill="x", pady=(2, 0))

                    # Jobb oldal — gombok
                    right = ctk.CTkFrame(card, fg_color="transparent")
                    right.pack(side="right", padx=10, pady=10)

                    def send_cmd(action, bot_key=bot.get("key")):
                        def worker():
                            try:
                                base = f"http://{client_state['host']}:{client_state['port']}"
                                payload = json.dumps(
                                    {"action": action, "bot": bot_key}
                                ).encode("utf-8")
                                req = urllib.request.Request(
                                    f"{base}/api/command",
                                    data=payload,
                                    headers={
                                        "Content-Type": "application/json",
                                        "X-API-Key": client_state["token"],
                                    },
                                    method="POST",
                                )
                                with urllib.request.urlopen(req, timeout=6) as r:
                                    result = json.loads(r.read().decode("utf-8"))
                                msg = result.get("message", "?")
                                self.after(0, lambda: log_line(f"✅ {action} → {msg}"))
                            except Exception as e:
                                self.after(0, lambda err=str(e):
                                            log_line(f"❌ {action}: {err}"))

                        threading.Thread(target=worker, daemon=True).start()

                    ctk.CTkButton(
                        right, text="▶", width=36, height=32,
                        fg_color="#27ae60", hover_color="#2ecc71",
                        font=("Arial", 14, "bold"),
                        command=lambda bk=bot.get("key"): send_cmd("start", bk),
                    ).pack(side="left", padx=2)

                    ctk.CTkButton(
                        right, text="🔄", width=36, height=32,
                        fg_color="#d35400", hover_color="#e67e22",
                        font=("Arial", 12),
                        command=lambda bk=bot.get("key"): send_cmd("restart", bk),
                    ).pack(side="left", padx=2)

                    ctk.CTkButton(
                        right, text="⏸", width=36, height=32,
                        fg_color="#c0392b", hover_color="#e74c3c",
                        font=("Arial", 14, "bold"),
                        command=lambda bk=bot.get("key"): send_cmd("stop", bk),
                    ).pack(side="left", padx=2)

            client_state["thread"] = None

        # Bezárás
        def on_close():
            client_state["running"] = False
            try:
                win.destroy()
            except Exception:
                pass
            self._lan_client_win = None

        win.protocol("WM_DELETE_WINDOW", on_close)

        # Ha van mentett host → automatikus kapcsolódás
        if self._lan_client_config["host"]:
            win.after(500, do_connect)