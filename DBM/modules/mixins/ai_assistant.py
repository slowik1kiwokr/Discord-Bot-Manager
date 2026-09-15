import os
import json
import threading
import urllib.request
import urllib.error

import customtkinter as ctk
from tkinter import messagebox

import modules.config as config


AI_PROVIDERS = {
    "OpenAI (GPT)": {
        "url": "https://api.openai.com/v1/chat/completions",
        "model": "gpt-4o-mini",
        "needs_key": True,
    },
    "Anthropic (Claude)": {
        "url": "https://api.anthropic.com/v1/messages",
        "model": "claude-3-5-sonnet-20241022",
        "needs_key": True,
    },
    "Ollama (local)": {
        "url": "http://localhost:11434/api/chat",
        "model": "llama3.2",
        "needs_key": False,
    },
    "LM Studio (local)": {
        "url": "http://localhost:1234/v1/chat/completions",
        "model": "local-model",
        "needs_key": False,
    },
}


class AIAssistantMixin:
    """AI chatbot, kódgenerátor, hibaelemzés, dokumentáció."""

    # Chat szerep-kulcsok
    _AI_ROLE_KEYS = {
        "user": "ai_role_user",
        "assistant": "ai_role_assistant",
    }

    def _ai_call(self, messages, system_prompt="", callback=None):
        """Háttérszálban hívja az AI-t és visszaadja a választ."""
        provider = getattr(self, "ai_provider", "OpenAI (GPT)")
        api_key = getattr(self, "ai_api_key", "")
        cfg = AI_PROVIDERS.get(provider, AI_PROVIDERS["OpenAI (GPT)"])

        if cfg["needs_key"] and not api_key:
            if callback:
                callback(self.tr("ai_err_no_key"))
            return

        def worker():
            try:
                url = cfg["url"]
                model = getattr(self, "ai_model", cfg["model"])

                if "OpenAI" in provider or "LM Studio" in provider:
                    body = {
                        "model": model,
                        "messages": (
                            ([{"role": "system", "content": system_prompt}]
                             if system_prompt else []) + messages
                        ),
                        "temperature": 0.7,
                    }
                    headers = {"Content-Type": "application/json"}
                    if api_key:
                        headers["Authorization"] = f"Bearer {api_key}"

                elif "Anthropic" in provider:
                    body = {
                        "model": model,
                        "max_tokens": 2048,
                        "system": system_prompt or "You are a helpful assistant.",
                        "messages": messages,
                    }
                    headers = {
                        "Content-Type": "application/json",
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01",
                    }

                elif "Ollama" in provider:
                    body = {
                        "model": model,
                        "messages": (
                            ([{"role": "system", "content": system_prompt}]
                             if system_prompt else []) + messages
                        ),
                        "stream": False,
                    }
                    headers = {"Content-Type": "application/json"}
                else:
                    body = {}
                    headers = {}

                req = urllib.request.Request(
                    url,
                    data=json.dumps(body).encode("utf-8"),
                    headers=headers,
                    method="POST",
                )

                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = json.loads(resp.read().decode("utf-8"))

                # Válasz kinyerése provider-től függően
                if "OpenAI" in provider or "LM Studio" in provider:
                    text = data["choices"][0]["message"]["content"]
                elif "Anthropic" in provider:
                    text = data["content"][0]["text"]
                elif "Ollama" in provider:
                    text = data.get("message", {}).get("content", "")
                else:
                    text = str(data)

                if callback:
                    callback(text)

            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8", errors="replace")
                if callback:
                    callback(self.tr("ai_err_http", code=e.code, body=err_body[:500]))
            except Exception as e:
                if callback:
                    callback(self.tr("ai_err_generic", error=e))

        threading.Thread(target=worker, daemon=True).start()

    # ------------------------------------------------------------------
    #  AI Chatbot ablak
    # ------------------------------------------------------------------
    def open_ai_chat_window(self):
        # Ha már van nyitott AI chat ablak, zárjuk be
        if hasattr(self, "_ai_chat_window") and self._ai_chat_window is not None:
            try:
                if self._ai_chat_window.winfo_exists():
                    self._ai_chat_window.destroy()
            except Exception:
                pass

        win = ctk.CTkToplevel(self)
        self._ai_chat_window = win
        win.title(self.tr("ai_chat_title"))
        win.geometry("820x680")
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 820) // 2
        y = (win.winfo_screenheight() - 680) // 2
        win.geometry(f"820x680+{x}+{y}")

        header = ctk.CTkFrame(win, fg_color="#5865F2", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text=self.tr("ai_chat_header"),
                     font=("Arial", 17, "bold"), text_color="white").pack(side="left", padx=20, pady=14)

        provider_lbl = ctk.CTkLabel(header,
                                     text=self.tr("ai_chat_provider_lbl",
                                                  provider=getattr(self, "ai_provider", "N/A")),
                                     font=("Arial", 10), text_color="#c0c8ff")
        provider_lbl.pack(side="right", padx=20)

        chat_box = ctk.CTkTextbox(win, font=("Consolas", 11), wrap="word")
        chat_box.pack(fill="both", expand=True, padx=12, pady=(12, 6))

        chat_box.insert("end", self.tr("ai_chat_welcome") + "\n")
        chat_box.configure(state="disabled")

        input_frame = ctk.CTkFrame(win, fg_color="transparent")
        input_frame.pack(fill="x", padx=12, pady=(0, 12))

        msg_entry = ctk.CTkEntry(input_frame, placeholder_text=self.tr("ai_chat_placeholder"))
        msg_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        msg_entry.bind("<Return>", lambda e: send_message())

        send_btn = ctk.CTkButton(input_frame, text=self.tr("ai_send_btn"),
                                  fg_color="#27ae60", hover_color="#2ecc71",
                                  width=110)
        send_btn.pack(side="right")

        self._ai_chat_history = []

        def append_chat(role, text):
            """Chat üzenet hozzáadása — CSAK main thread-en hívható!"""
            try:
                if not chat_box.winfo_exists():
                    return
                chat_box.configure(state="normal")
                icon = "👤" if role == "user" else "🤖"
                role_label = self.tr(self._AI_ROLE_KEYS.get(role, role))
                chat_box.insert("end", f"{icon} {role_label}:\n{text}\n\n")
                chat_box.insert("end", "─" * 40 + "\n\n")
                chat_box.see("end")
                chat_box.configure(state="disabled")
            except Exception as e:
                print(f"[AI] append_chat hiba: {e}")

        def on_ai_response(text):
            """Callback a háttérszálból — a UI-t main thread-en frissítjük."""
            print(f"[AI] Válasz megérkezett: {text[:150]}")

            def update_ui():
                try:
                    if not win.winfo_exists():
                        return
                    send_btn.configure(state="normal", text=self.tr("ai_send_btn"))
                    append_chat("assistant", text)
                except Exception as e:
                    print(f"[AI] UI update hiba: {e}")

            # ⚠️ EZ A LÉNYEG: a main thread-re ütemezzük
            self.after(0, update_ui)

        def send_message():
            msg = msg_entry.get().strip()
            if not msg:
                return
            msg_entry.delete(0, "end")
            append_chat("user", msg)
            self._ai_chat_history.append({"role": "user", "content": msg})

            send_btn.configure(state="disabled", text="⏳...")

            system = (
                "You are a helpful assistant for a Discord bot management panel. "
                "Answer in Hungarian, concisely and helpfully. "
                "If the user asks about code, provide code examples in Python."
            )
            self._ai_call(self._ai_chat_history[-10:], system, on_ai_response)

            # A választ is elmentjük majd, ha megjön — placeholder
            self._ai_chat_history.append({"role": "assistant", "content": "(pending)"})

        send_btn.configure(command=send_message)

    # ------------------------------------------------------------------
    #  AI Kód generátor
    # ------------------------------------------------------------------
    def open_ai_code_generator(self):
        win = ctk.CTkToplevel(self)
        win.title(self.tr("ai_codegen_title"))
        win.geometry("780x680")
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 780) // 2
        y = (win.winfo_screenheight() - 680) // 2
        win.geometry(f"780x680+{x}+{y}")

        header = ctk.CTkFrame(win, fg_color="#9b59b6", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text=self.tr("ai_codegen_header"),
                     font=("Arial", 17, "bold"), text_color="white").pack(side="left", padx=20, pady=14)

        ctk.CTkLabel(win, text=self.tr("ai_codegen_prompt_lbl"),
                     font=("Arial", 12), anchor="w").pack(fill="x", padx=14, pady=(14, 4))

        prompt_entry = ctk.CTkTextbox(win, height=80, font=("Arial", 11))
        prompt_entry.pack(fill="x", padx=14, pady=(0, 8))

        ctk.CTkLabel(win, text=self.tr("ai_codegen_output_lbl"),
                     font=("Arial", 12, "bold"), anchor="w").pack(fill="x", padx=14, pady=(4, 4))

        output_box = ctk.CTkTextbox(win, font=("Consolas", 11), wrap="none")
        output_box.pack(fill="both", expand=True, padx=14, pady=(0, 8))

        status = ctk.CTkLabel(win, text="", font=("Arial", 10), text_color="#888")
        status.pack(pady=2)

        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(fill="x", padx=14, pady=(4, 14))

        gen_btn = ctk.CTkButton(btn_frame, text=self.tr("ai_codegen_generate_btn"),
                                 fg_color="#9b59b6", hover_color="#8e44ad",
                                 width=160, height=40)
        gen_btn.pack(side="left", padx=4)

        def save_code():
            code = output_box.get("1.0", "end").strip()
            if not code:
                messagebox.showwarning(self.tr("common_warning_title"),
                                       self.tr("ai_codegen_nothing_to_save"), parent=win)
                return
            # Bot mappájába mentjük?
            bot = self.bots.get(self.active_bot_key, {})
            script_path = bot.get("path", "")
            if not script_path:
                messagebox.showwarning(self.tr("common_warning_title"),
                                       self.tr("ai_codegen_need_bot_file"), parent=win)
                return
            bot_dir = os.path.dirname(script_path)
            target = os.path.join(bot_dir, "ai_generated.py")
            try:
                with open(target, "w", encoding="utf-8") as f:
                    f.write(code)
                self.notify(self.tr("ai_codegen_saved"), "success")
                self.log_event("EVENT", self.tr("ai_codegen_log_saved", path=target))
            except Exception as e:
                messagebox.showerror(self.tr("common_error_title"), str(e), parent=win)

        ctk.CTkButton(btn_frame, text=self.tr("ai_codegen_save_btn"),
                       fg_color="#27ae60", hover_color="#2ecc71",
                       width=200, height=40, command=save_code).pack(side="left", padx=4)

        ctk.CTkButton(btn_frame, text=self.tr("common_close_btn"), fg_color="#555555",
                       width=100, height=40, command=win.destroy).pack(side="right", padx=4)

        def on_code(text):
            output_box.delete("1.0", "end")
            # Kód blokk kinyerése
            if "```" in text:
                blocks = text.split("```")
                code = ""
                for i, b in enumerate(blocks):
                    if i % 2 == 1:
                        # nyelv jelző eltávolítása
                        lines = b.split("\n")
                        if lines and lines[0].strip() in (
                            "python", "py", "python3", ""
                        ):
                            b = "\n".join(lines[1:])
                        code += b
                output_box.insert("1.0", code.strip() if code else text)
            else:
                output_box.insert("1.0", text)
            gen_btn.configure(state="normal", text=self.tr("ai_codegen_generate_btn"))
            status.configure(text=self.tr("ai_codegen_status_done"))

        def generate():
            prompt = prompt_entry.get("1.0", "end").strip()
            if not prompt:
                messagebox.showwarning(self.tr("common_warning_title"),
                                       self.tr("ai_codegen_need_prompt"), parent=win)
                return
            gen_btn.configure(state="disabled", text="⏳...")
            status.configure(text=self.tr("ai_codegen_status_thinking"))

            system = (
                "You are a Python expert for Discord bots using discord.py. "
                "Generate clean, working code. Only output the code, no explanation. "
                "Use `discord.ext.commands` or `app_commands` as appropriate. "
                "Reply with the code inside a ```python code block."
            )
            self._ai_call([{"role": "user", "content": prompt}], system, on_code)

        gen_btn.configure(command=generate)

    # ------------------------------------------------------------------
    #  AI Hibaelemzés
    # ------------------------------------------------------------------
    def analyze_error_with_ai(self, error_text, parent=None):
        if not error_text.strip():
            messagebox.showwarning(self.tr("common_warning_title"),
                                   self.tr("ai_error_nothing"))
            return

        win = ctk.CTkToplevel(self if not parent else parent)
        win.title(self.tr("ai_error_title"))
        win.geometry("780x620")
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 780) // 2
        y = (win.winfo_screenheight() - 620) // 2
        win.geometry(f"780x620+{x}+{y}")

        header = ctk.CTkFrame(win, fg_color="#e74c3c", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text=self.tr("ai_error_header"),
                     font=("Arial", 17, "bold"), text_color="white").pack(side="left", padx=20, pady=14)

        ctk.CTkLabel(win, text=self.tr("ai_error_input_lbl"),
                     font=("Arial", 11), anchor="w").pack(fill="x", padx=14, pady=(14, 4))

        err_box = ctk.CTkTextbox(win, height=140, font=("Consolas", 10))
        err_box.pack(fill="x", padx=14, pady=(0, 8))
        err_box.insert("1.0", error_text[:5000])

        ctk.CTkLabel(win, text=self.tr("ai_error_output_lbl"),
                     font=("Arial", 11, "bold"), anchor="w").pack(fill="x", padx=14, pady=(4, 4))

        result_box = ctk.CTkTextbox(win, font=("Arial", 11), wrap="word")
        result_box.pack(fill="both", expand=True, padx=14, pady=(0, 8))
        result_box.insert("1.0", self.tr("ai_error_analyzing"))
        result_box.configure(state="disabled")

        def on_result(text):
            result_box.configure(state="normal")
            result_box.delete("1.0", "end")
            result_box.insert("1.0", text)
            result_box.configure(state="disabled")

        system = (
            "You are a Python error analysis expert. Analyze the given error/stack trace. "
            "Explain in Hungarian: 1) What is the root cause? 2) How to fix it? "
            "3) Provide a code example if relevant. Be concise but complete."
        )
        self._ai_call(
            [{"role": "user", "content": f"Elemezd ezt a hibát:\n\n{error_text}"}],
            system, on_result
        )

        ctk.CTkButton(win, text=self.tr("common_close_btn"), fg_color="#555555",
                       width=120, command=win.destroy).pack(pady=(0, 12))

    # ------------------------------------------------------------------
    #  AI Dokumentáció generátor
    # ------------------------------------------------------------------
    def open_ai_docs_generator(self):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title=self.tr("ai_docs_select_file"),
            filetypes=[(self.tr("ai_docs_filetype"), "*.py")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            messagebox.showerror(self.tr("common_error_title"),
                                 self.tr("ai_docs_read_error", error=e))
            return

        win = ctk.CTkToplevel(self)
        win.title(self.tr("ai_docs_title"))
        win.geometry("800x640")
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 800) // 2
        y = (win.winfo_screenheight() - 640) // 2
        win.geometry(f"800x640+{x}+{y}")

        header = ctk.CTkFrame(win, fg_color="#16a085", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header,
                     text=self.tr("ai_docs_header", filename=os.path.basename(file_path)),
                     font=("Arial", 15, "bold"), text_color="white").pack(side="left", padx=20, pady=14)

        result_box = ctk.CTkTextbox(win, font=("Consolas", 11), wrap="word")
        result_box.pack(fill="both", expand=True, padx=14, pady=14)
        result_box.insert("1.0", self.tr("ai_docs_generating"))
        result_box.configure(state="disabled")

        def on_docs(text):
            result_box.configure(state="normal")
            result_box.delete("1.0", "end")
            result_box.insert("1.0", text)
            result_box.configure(state="disabled")

        system = (
            "You are a technical documentation writer. Given Python code, produce a clear "
            "Markdown documentation in Hungarian. Include: 1) Purpose of the file, "
            "2) List of functions/classes with descriptions, 3) Usage examples if relevant. "
            "Format as clean Markdown."
        )
        self._ai_call(
            [{"role": "user", "content": f"Készíts dokumentációt erről a kódról:\n\n```python\n{code[:6000]}\n```"}],
            system, on_docs
        )

        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(fill="x", padx=14, pady=(0, 14))

        def save_docs():
            docs = result_box.get("1.0", "end").strip()
            target = filedialog.asksaveasfilename(
                defaultextension=".md",
                filetypes=[("Markdown", "*.md"), ("Text", "*.txt")],
                initialfile=os.path.basename(file_path).replace(".py", "_DOCS.md")
            )
            if target:
                try:
                    with open(target, "w", encoding="utf-8") as f:
                        f.write(docs)
                    self.notify(self.tr("ai_docs_saved"), "success")
                except Exception as e:
                    messagebox.showerror(self.tr("common_error_title"), str(e))

        ctk.CTkButton(btn_frame, text=self.tr("ai_docs_save_btn"),
                       fg_color="#27ae60", width=140, height=38,
                       command=save_docs).pack(side="left", padx=4)

        ctk.CTkButton(btn_frame, text=self.tr("common_close_btn"), fg_color="#555555",
                       width=120, height=38, command=win.destroy).pack(side="right", padx=4)

    # ------------------------------------------------------------------
    #  Settings ablak AI szekciója
    # ------------------------------------------------------------------
    def _build_ai_settings(self, parent):
        """AI beállítások szekció — a Settings ablakba kerül."""
        frame = ctk.CTkFrame(parent, fg_color="#1e2129", corner_radius=10)
        frame.pack(fill="x", padx=20, pady=(12, 4))

        ctk.CTkLabel(frame, text=self.tr("ai_settings_section"),
                     font=("Arial", 12, "bold"), anchor="w").pack(fill="x", padx=14, pady=(10, 4))

        ctk.CTkLabel(frame, text=self.tr("ai_settings_provider_lbl")).pack(anchor="w", padx=14)
        provider_var = ctk.StringVar(value=getattr(self, "ai_provider", "OpenAI (GPT)"))
        ctk.CTkComboBox(frame, values=list(AI_PROVIDERS.keys()),
                        variable=provider_var, width=280).pack(anchor="w", padx=14, pady=2)

        ctk.CTkLabel(frame, text=self.tr("ai_settings_key_lbl")).pack(anchor="w", padx=14, pady=(6, 0))
        key_entry = ctk.CTkEntry(frame, show="*", width=380, placeholder_text="sk-...")
        if getattr(self, "ai_api_key", ""):
            key_entry.insert(0, self.ai_api_key)
        key_entry.pack(anchor="w", padx=14, pady=2)

        ctk.CTkLabel(frame, text=self.tr("ai_settings_model_lbl")).pack(anchor="w", padx=14, pady=(6, 0))
        model_entry = ctk.CTkEntry(frame, width=380,
                                    placeholder_text=getattr(self, "ai_model", ""))
        model_entry.pack(anchor="w", padx=14, pady=(2, 10))

        def save_ai():
            self.ai_provider = provider_var.get()
            self.ai_api_key = key_entry.get().strip()
            self.ai_model = model_entry.get().strip()
            self.save_config()
            self.notify(self.tr("ai_settings_saved"), "success")

        ctk.CTkButton(frame, text=self.tr("ai_settings_save_btn"), width=140,
                       fg_color="#27ae60", command=save_ai).pack(anchor="w", padx=14, pady=(0, 12))