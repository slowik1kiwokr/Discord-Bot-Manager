import os
import json
from tkinter import filedialog, messagebox

import customtkinter as ctk

import modules.config as config


class WindowServersMixin:
    def open_servers_window(self):
        script_path = self.entry_path.get()
        if not script_path or not os.path.exists(script_path):
            messagebox.showwarning(self.tr("common_warning_title"),
                                     self.tr("servers_need_bot"))
            return

        servers_dir = os.path.join(os.path.dirname(script_path), "data", "servers")
        win = ctk.CTkToplevel(self)
        win.title(self.tr("server_settings"))
        win.geometry("750x500")
        win.grab_set()

        ctk.CTkLabel(win, text=self.tr("server_settings"),
                     font=("Arial", 16, "bold"),
                     text_color="#16a085").pack(pady=15)

        if not os.path.exists(servers_dir):
            ctk.CTkLabel(win,
                         text=self.tr("servers_folder_missing", path=servers_dir),
                         font=("Arial", 12)).pack(pady=30)
            return

        json_files = [f for f in os.listdir(servers_dir) if f.endswith(".json")]

        if not json_files:
            ctk.CTkLabel(win, text=self.tr("no_servers"),
                         font=("Arial", 12)).pack(pady=30)
            return

        scroll_f = ctk.CTkScrollableFrame(win, width=700, height=350)
        scroll_f.pack(padx=20, pady=10, fill="both", expand=True)

        for filename in json_files:
            file_path = os.path.join(servers_dir, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    s_data = json.load(f)
            except Exception:
                s_data = {"error": self.tr("servers_json_unreadable")}

            server_name = s_data.get(
                "server_name",
                s_data.get("name", self.tr("servers_unknown_server"))
            )
            member_count = s_data.get("member_count", 0)
            guild_id = s_data.get(
                "guild_id",
                s_data.get("server_id", self.tr("servers_unknown_id"))
            )
            version = s_data.get("version", self.tr("servers_unknown_id"))

            card = ctk.CTkFrame(scroll_f, fg_color=self.theme_colors["card_bg"])
            card.pack(fill="x", padx=5, pady=5)

            info_text = self.tr(
                "servers_info_line",
                name=server_name,
                id=guild_id,
                members=member_count,
                version=version,
            )
            ctk.CTkLabel(card, text=info_text,
                          font=("Consolas", 11),
                          text_color=self.theme_colors["text"]).pack(
                side="left", padx=10, pady=10)

            def open_json_editor(fp=file_path, s_name=server_name):
                ed_win = ctk.CTkToplevel(win)
                ed_win.edit_file_path = fp
                ed_win.title(self.tr("servers_edit_title", name=s_name))
                ed_win.geometry("500x400")
                ed_win.grab_set()

                ctk.CTkLabel(ed_win,
                             text=self.tr("servers_edit_server_lbl", name=s_name),
                             font=("Arial", 12, "bold")).pack(pady=10)

                txt_box = ctk.CTkTextbox(ed_win, font=("Consolas", 11),
                                           width=460, height=260)
                txt_box.pack(padx=20, pady=5)

                try:
                    with open(fp, "r", encoding="utf-8") as f:
                        content_str = f.read()
                    txt_box.insert("1.0", content_str)
                except Exception as e:
                    txt_box.insert("1.0",
                                    self.tr("servers_read_error", error=e))

                def save_json_file():
                    try:
                        new_content = txt_box.get("1.0", "end").strip()
                        json.loads(new_content)
                        with open(ed_win.edit_file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        messagebox.showinfo(self.tr("servers_saved_title"),
                                              self.tr("servers_saved_msg"),
                                              parent=ed_win)
                        ed_win.destroy()
                    except json.JSONDecodeError as err:
                        messagebox.showerror(self.tr("servers_json_error_title"),
                                               self.tr("servers_json_error_msg", error=err),
                                               parent=ed_win)
                    except Exception as err:
                        messagebox.showerror(self.tr("common_error_title"),
                                               self.tr("servers_save_error", error=err),
                                               parent=ed_win)

                ctk.CTkButton(ed_win, text=self.tr("common_save_btn"),
                               fg_color="#27ae60",
                               command=save_json_file).pack(pady=10)

            ctk.CTkButton(card, text=self.tr("servers_edit_btn"),
                           width=90, fg_color="#16a085",
                           command=open_json_editor).pack(
                side="right", padx=10, pady=10)