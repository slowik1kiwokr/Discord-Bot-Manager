import http.server
import socketserver
import threading
import json
import secrets

import modules.config as config


class LANServerMixin:
    """LAN szerver — a panel kívülről vezérelhetővé tétele."""

    # ==================================================================
    #  Inicializálás
    # ==================================================================
    def init_lan_server(self):
        self._lan_server = None
        self._lan_thread = None
        self.lan_enabled = getattr(self, "lan_enabled", False)
        self.lan_port = getattr(self, "lan_port", 8765)
        self.lan_token = getattr(self, "lan_token", "")
        self.lan_allow_control = getattr(self, "lan_allow_control", True)
        self._lan_requests_log = []

        if self.lan_enabled:
            self.after(2000, self.start_lan_server)

    # ==================================================================
    #  Szerver indítás / leállítás
    # ==================================================================
    def start_lan_server(self):
        if self._lan_server is not None:
            return True

        if not self.lan_token:
            self.lan_token = secrets.token_hex(16)

        panel_ref = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def _send_json(self, data, code=200):
                try:
                    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
                    self.send_response(code)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                except Exception:
                    pass

            def _check_auth(self):
                expected = getattr(panel_ref, "lan_token", "")
                if not expected:
                    return True
                return self.headers.get("X-API-Key", "") == expected

            def _log_request(self, method, path, client_ip, status):
                try:
                    import datetime
                    entry = {
                        "time": datetime.datetime.now().strftime("%H:%M:%S"),
                        "method": method,
                        "path": path,
                        "ip": client_ip,
                        "status": status,
                    }
                    panel_ref._lan_requests_log.append(entry)
                    if len(panel_ref._lan_requests_log) > 30:
                        panel_ref._lan_requests_log.pop(0)
                except Exception:
                    pass

            def do_GET(self):
                client_ip = self.client_address[0]
                path = self.path.split("?")[0]

                # --- Ping: token nélkül is elérhető ---
                if path == "/api/ping":
                    self._log_request("GET", path, client_ip, 200)
                    self._send_json({
                        "ok": True,
                        "panel_id": config.PANEL_ID,
                        "version": config.VERSION,
                    })
                    return

                # --- Token ellenőrzés ---
                if not self._check_auth():
                    self._log_request("GET", path, client_ip, 401)
                    self._send_json({"error": "Invalid token"}, 401)
                    return

                if path == "/api/status":
                    self._log_request("GET", path, client_ip, 200)
                    self._send_json(panel_ref._lan_get_status())

                elif path == "/api/bots":
                    self._log_request("GET", path, client_ip, 200)
                    self._send_json(panel_ref._lan_get_bots())

                elif path == "/api/logs":
                    self._log_request("GET", path, client_ip, 200)
                    self._send_json(panel_ref._lan_get_logs())

                else:
                    self._log_request("GET", path, client_ip, 404)
                    self._send_json({"error": "Not found"}, 404)

            def do_POST(self):
                client_ip = self.client_address[0]
                path = self.path.split("?")[0]

                if not self._check_auth():
                    self._log_request("POST", path, client_ip, 401)
                    self._send_json({"error": "Invalid token"}, 401)
                    return

                if not getattr(panel_ref, "lan_allow_control", True):
                    self._log_request("POST", path, client_ip, 403)
                    self._send_json({"error": "Control disabled"}, 403)
                    return

                if path == "/api/command":
                    try:
                        length = int(self.headers.get("Content-Length", 0))
                        body = self.rfile.read(length).decode("utf-8")
                        data = json.loads(body)
                    except Exception:
                        self._log_request("POST", path, client_ip, 400)
                        self._send_json({"error": "Invalid JSON"}, 400)
                        return

                    result = panel_ref._lan_handle_command(data)
                    self._log_request("POST", path, client_ip,
                                      200 if result.get("ok") else 400)
                    self._send_json(result)
                else:
                    self._log_request("POST", path, client_ip, 404)
                    self._send_json({"error": "Not found"}, 404)

        try:
            server = socketserver.ThreadingTCPServer(("0.0.0.0", self.lan_port), Handler)
            server.allow_reuse_address = True
            server.daemon_threads = True
            self._lan_server = server
            self._lan_thread = threading.Thread(
                target=server.serve_forever, daemon=True
            )
            self._lan_thread.start()
            self.log_event("EVENT", self.tr("lan_server_started", port=self.lan_port))
            return True
        except OSError as e:
            self._lan_server = None
            self.log_event("ERROR", self.tr("lan_server_error", error=e))
            return False

    def stop_lan_server(self):
        if self._lan_server is None:
            return
        try:
            self._lan_server.shutdown()
            self._lan_server.server_close()
        except Exception:
            pass
        self._lan_server = None
        self._lan_thread = None
        self.log_event("EVENT", self.tr("lan_server_stopped"))

    def restart_lan_server(self):
        self.stop_lan_server()
        if self.lan_enabled:
            self.after(500, self.start_lan_server)

    # ==================================================================
    #  Adatok összeállítása
    # ==================================================================
    def _lan_get_status(self):
        import time
        bots_data = []
        for key, bot in self.bots.items():
            entry = {
                "key": key,
                "name": bot.get("name", key),
                "emoji": bot.get("emoji", "🤖"),
                "color": bot.get("color", "#5865F2"),
                "is_running": bot.get("is_running", False),
                "error_count": bot.get("error_count", 0),
                "total_commands": bot.get("total_commands", 0),
                "uptime_seconds": 0,
                "ram_mb": 0,
                "cpu_percent": 0,
            }
            if bot.get("is_running") and bot.get("start_time"):
                entry["uptime_seconds"] = int(time.time() - bot["start_time"])
                try:
                    import psutil
                    p = psutil.Process(bot["process"].pid)
                    entry["ram_mb"] = round(p.memory_info().rss / (1024 * 1024), 1)
                    entry["cpu_percent"] = round(p.cpu_percent(interval=None), 1)
                except Exception:
                    pass
            bots_data.append(entry)

        return {
            "ok": True,
            "panel_id": config.PANEL_ID,
            "version": config.VERSION,          # ← ÚJ
            "active_bot": self.active_bot_key,
            "bots": bots_data,
            "temperature": self.get_temperature_text(),
            "timestamp": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        }

    def _lan_get_bots(self):
        return {
            "ok": True,
            "bots": [
                {
                    "key": k,
                    "name": v.get("name", k),
                    "emoji": v.get("emoji", "🤖"),
                    "color": v.get("color", "#5865F2"),
                    "path": v.get("path", ""),
                }
                for k, v in self.bots.items()
            ],
        }

    def _lan_get_logs(self):
        active = self.active_bot_key
        bot = self.bots.get(active, {})
        logs = bot.get("raw_logs", [])[-50:]
        return {"ok": True, "bot": active, "logs": logs}

    # ==================================================================
    #  Parancsok feldolgozása
    # ==================================================================
    def _lan_handle_command(self, data):
        action = data.get("action", "").lower()
        bot_key = data.get("bot", self.active_bot_key)

        if bot_key not in self.bots:
            return {"ok": False, "message": f"Unknown bot: {bot_key}"}

        previous = self.active_bot_key
        try:
            self.switch_bot(bot_key)
            if action == "start":
                self.start_bot()
            elif action == "stop":
                self.stop_bot()
            elif action == "restart":
                self.restart_bot()
            else:
                return {"ok": False, "message": f"Unknown action: {action}"}
            return {"ok": True, "message": f"{action} → {bot_key}"}
        except Exception as e:
            return {"ok": False, "message": str(e)}
        finally:
            self.after(200, lambda: self.switch_bot(previous))