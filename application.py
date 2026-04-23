import customtkinter as ctk
import json
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image
import cairosvg
import io
import sys
from pathlib import Path

# Tên ứng dụng của bạn
APP_NAME = "PromptManager"

# Tìm đường dẫn AppData của Windows (thường là C:\Users\<User>\AppData\Roaming)
def get_data_dir():
    # Tạo đường dẫn: %APPDATA%/PromptManager
    data_dir = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), APP_NAME)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir


# CONFIG
if getattr(sys, 'frozen', False):
    # Nếu đang chạy từ file .exe
    APPLICATION_PATH = os.path.dirname(sys.executable)
else:
    # Nếu đang chạy script .py
    APPLICATION_PATH = os.path.dirname(os.path.abspath(__file__))

# CẬP NHẬT CONFIG
DATA_FILE = os.path.join(get_data_dir(), "prompts.json")
SETTINGS_FILE = os.path.join(get_data_dir(), "settings.json")
ICON_DIR = "icons"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

from functools import lru_cache

@lru_cache(maxsize=32)
def get_cached_icon(name, size=(18, 18), color=(255, 255, 255)):
    return load_svg_icon(name, size, color)

def resource_path(path):
    """ Lấy đường dẫn tuyệt đối đến tài nguyên, dùng cho cả dev và PyInstaller """
    try:
        # PyInstaller tạo thư mục tạm và lưu đường dẫn ở _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, path)

# SVG ICON (FORCE WHITE)
def load_svg_icon(name, size=(18, 18), color=(255, 255, 255)):
    path = resource_path(os.path.join(ICON_DIR, name))

    png_data = cairosvg.svg2png(
        url=path,
        output_width=size[0],
        output_height=size[1]
    )

    img = Image.open(io.BytesIO(png_data)).convert("RGBA")

    # FORCE WHITE COLOR
    pixels = img.getdata()
    new_pixels = []

    def normalize_color(color):
        if isinstance(color, str):
            color = color.lstrip("#")
            return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

        if isinstance(color, tuple) and len(color) >= 3:
            return color[:3]

        return (255, 255, 255)


    r, g, b = normalize_color(color)

    for p in pixels:
        if p[3] > 0:
            new_pixels.append((r, g, b, p[3]))
        else:
            new_pixels.append(p)

    img.putdata(new_pixels)

    return ctk.CTkImage(light_image=img, dark_image=img, size=size)

# STORAGE
class Storage:
    def __init__(self):
        self.prompts = []
        self.settings = {"theme": "Dark"}
        self.load()

    def load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.prompts = json.load(f)
            except:
                self.prompts = self.sample_data()
        else:
            self.prompts = self.sample_data()

        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    self.settings = json.load(f)
            except:
                self.settings = {"theme": "Dark"}

    def save(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.prompts, f, indent=2, ensure_ascii=False)

        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=2)

    def sample_data(self):
        return [
            {
                "title": "Explain Code",
                "content": "Explain step by step:\n<CODE HERE>",
                "pinned": False
            },
            {
                "title": "Summarize",
                "content": "Summarize in simple terms:\n<TEXT HERE>",
                "pinned": False
            }
        ]

# PROMPT CARD
class PromptCard(ctk.CTkFrame):
    def __init__(self, parent, app, prompt, index):
        super().__init__(
            parent,
            corner_radius=14,
            border_width=2,
            border_color=app.get_border_color(),
            fg_color=("white", "#2a2a2a")
        )

        self.app = app
        self.prompt = prompt
        self.index = index

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.pin_icon = load_svg_icon(
            "pin.svg",
            size=(18, 18),
            color=self.app.get_border_color()
    )
        # ---------------- TITLE ----------------
        self.title_label = ctk.CTkLabel(
            self,
            text=prompt.get("title", ""),
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=12, pady=(10, 2))

        # ---------------- DIVIDER ----------------
        self.divider = ctk.CTkFrame(
            self,
            height=2,
            fg_color=app.get_border_color()
        )
        self.divider.grid(row=1, column=0, sticky="ew", padx=12, pady=(4, 6))

        # ---------------- CONTENT ----------------
        self.content_label = ctk.CTkLabel(
            self,
            text=prompt.get("content", ""),
            justify="left",
            anchor="w",
            wraplength=520,
            font=ctk.CTkFont(family="Segoe UI", size=15)
        )
        self.content_label.grid(row=2, column=0, sticky="w", padx=12, pady=(0, 10))

        # ---------------- BUTTON AREA ----------------
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="ne")

        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        # COPY (FULL WIDTH TOP)
        self.copy_icon = get_cached_icon("copy.svg", (18, 18))
        self.copy_btn = ctk.CTkButton(
            btn_frame,
            text="",
            image=self.copy_icon,
            width=80,
            command=self.copy_prompt
        )
        self.copy_btn.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 6))

        # EDIT + DELETE (BOTTOM ROW)
        self.edit_btn = ctk.CTkButton(
            btn_frame,
            text="",
            image=load_svg_icon("edit.svg"),
            width=40,
            fg_color="#444444",
            hover_color="#555555",
            command=self.edit_prompt
        )
        self.edit_btn.grid(row=1, column=0, padx=(0, 4))

        self.delete_btn = ctk.CTkButton(
            btn_frame,
            text="",
            image=load_svg_icon("trash-2.svg"),
            width=40,
            fg_color="#aa3333",
            hover_color="#bb4444",
            command=self.delete_prompt
        )
        self.delete_btn.grid(row=1, column=1, padx=(4, 0))

    # ---------------- PIN AREA ----------------
        pin_frame = ctk.CTkFrame(self, fg_color="transparent")
        pin_frame.grid(row=3, column=1, sticky="se", padx=10, pady=(0, 8))

        self.pin_var = tk.BooleanVar(value=self.prompt.get("pinned", False))

        self.pin_checkbox = ctk.CTkCheckBox(
            pin_frame,
            text="",
            variable=self.pin_var,
            width=15,
            hover_color="#444444",
            command=self.toggle_pin
        )
        self.pin_checkbox.pack(side="right")

        self.pin_label = ctk.CTkLabel(
            pin_frame,
            image=self.pin_icon,
            text=""
        )
        self.pin_label.pack(side="right", padx=(0, 4))

    # ---------------- ACTIONS ----------------
    def copy_prompt(self):
        self.clipboard_clear()
        self.clipboard_append(self.prompt["content"])

        # hiển thị copied + giữ icon
        self.copy_btn.configure(text="Copied", compound="left")

        # reset sau 1.5s
        self.after(750, lambda: self.copy_btn.configure(
            text="",
            compound="center"
        ))

    def edit_prompt(self):
        self.app.open_editor(self.index)

    def delete_prompt(self):
        if messagebox.askyesno("Delete", "Remove this prompt?"):
            self.app.delete_prompt(self.index)
    def toggle_pin(self):
        self.prompt["pinned"] = self.pin_var.get()
        self.app.storage.save()
        self.app.refresh()

# EDITOR
class Editor(ctk.CTkToplevel):
    def __init__(self, app, index=None):
        super().__init__(app)
        self.app = app
        self.index = index

        self.bind("<Escape>", lambda e: self.close_editor())

        self.transient(app)   # gắn cửa sổ con vào main window
        self.grab_set()       # bắt toàn bộ input vào editor
        self.lift()           # đưa lên trên cùng
        self.focus_force()    # ép focus vào editor
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))

        self.title("Prompt Editor")
        self.geometry("520x420")

        self.title_entry = ctk.CTkEntry(self, placeholder_text="Title")
        self.title_entry.pack(fill="x", padx=10, pady=10)
      
        self.textbox = ctk.CTkTextbox(self,font=ctk.CTkFont(family="Segoe UI", size=14))
        self.textbox.pack(fill="both", expand=True, padx=10, pady=10)

        save_btn = ctk.CTkButton(
            self,
            text="Save",
            image=load_svg_icon("plus-circle.svg"),
            compound="left",
            command=self.save
        )
        save_btn.pack(pady=10)

        self.bind("<Return>", lambda e: self.save())

        if index is not None:
            p = app.storage.prompts[index]
            self.title_entry.insert(0, p["title"])
            self.textbox.insert("1.0", p["content"])


    def save(self):
        title = self.title_entry.get()
        content = self.textbox.get("1.0", "end").strip()

        if not content:
            return

        if self.index is None:
            self.app.storage.prompts.append({
                "title": title,
                "content": content,
                "pinned": False
            })
        else:
            old = self.app.storage.prompts[self.index]
            self.app.storage.prompts[self.index] = {
                "title": title,
                "content": content,
                "pinned": old.get("pinned", False)
            }
        self.app.storage.save()
        self.app.refresh()
        self.destroy()

    def close_editor(self):
        self.destroy()

# Info APP
class InfoWindow(ctk.CTkToplevel):
    def __init__(self, app):
        super().__init__(app)
        self.title("About")
        self.geometry("300x200")

        self.transient(app)
        self.grab_set()
        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)

        self.after(100, lambda: self.attributes("-topmost", False))

        label = ctk.CTkLabel(
            self,
            text="Prompt Manager\n\nVersion 1.0.0\n" \
            "\n\nAuthor: Ngo Van Tuan\n\n" \
            "Email feedback: ngovantuan060606@gmail.com"        
            ,

            justify="center"
        )
        label.pack(expand=True, pady=20)

# MAIN APP
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        icon_path = resource_path("app.ico")

        # Thiết lập Icon
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                try:
                    from PIL import ImageTk
                    icon_img = ImageTk.PhotoImage(Image.open(icon_path))
                    self.wm_iconphoto(True, icon_img)
                except Exception as e:
                    print(f"Lỗi hiển thị icon: {e}")

        self.after(100, lambda: self.iconbitmap(icon_path))
        self.after(100, lambda: self.wm_iconbitmap(icon_path))

        self.storage = Storage()
        self.menu = None

        self.title("Prompt Manager")
        self.geometry("720x650")

        ctk.set_appearance_mode(self.storage.settings.get("theme", "Dark"))

        # ---------------- TOP BAR ----------------
        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=10, pady=10)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self.refresh())

        self.search_entry = ctk.CTkEntry(
            top,
            placeholder_text="Search"
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)

        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh())

        add_btn = ctk.CTkButton(
            top,
            text="",
            image=load_svg_icon("plus-circle.svg"),
            width=40,
            command=self.open_editor
        )
        add_btn.pack(side="left", padx=5)

        menu_btn = ctk.CTkButton(
            top,
            text="",
            image=load_svg_icon("settings.svg"),
            width=40,
            command=self.open_menu
        )
        menu_btn.pack(side="left", padx=5)

        # ---------------- LIST ----------------
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh()

    # ---------------- MENU ----------------
    def open_menu(self):
        if self.menu is not None and self.menu.winfo_exists():
            self.menu.destroy()
            self.menu = None
            return

        self.menu = ctk.CTkFrame(self, corner_radius=10)
        self.menu.place(x=520, y=55)

        theme_btn = ctk.CTkButton(
            self.menu,
            text="Toggle Theme",
            image=load_svg_icon("sun.svg"),
            compound="left",
            command=self.toggle_theme
        )
        theme_btn.pack(padx=10, pady=10)

        info_btn = ctk.CTkButton(
            self.menu,
            text="Info",
            command=self.open_info
        )
        info_btn.pack(padx=10, pady=10)

    # ---------------- INFO ----------------
    def open_info(self):
        InfoWindow(self)
    # ---------------- THEME ----------------
    def toggle_theme(self):
        current = self.storage.settings.get("theme", "Dark")
        new = "Light" if current == "Dark" else "Dark"

        ctk.set_appearance_mode(new)
        self.storage.settings["theme"] = new
        self.storage.save()

        self.refresh()

    def get_border_color(self):
        return "#000000" if ctk.get_appearance_mode() == "Light" else "#ffffff"

    # ---------------- CORE ----------------
    def refresh(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        q = self.search_entry.get().lower()

        filtered = []
        for i, p in enumerate(self.storage.prompts):
            if q in p["title"].lower() or q in p["content"].lower():
                filtered.append((i, p))

        # sort pinned lên trên
        filtered.sort(key=lambda x: x[1].get("pinned", False), reverse=True)

        for i, p in filtered:
            card = PromptCard(self.scroll, self, p, i)
            card.pack(fill="x", pady=6, padx=6)

    def open_editor(self, index=None):
        Editor(self, index)

    def delete_prompt(self, index):
        del self.storage.prompts[index]
        self.storage.save()
        self.refresh()

# RUN
if __name__ == "__main__":
    App().mainloop()