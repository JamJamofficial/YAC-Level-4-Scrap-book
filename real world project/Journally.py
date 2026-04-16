import tkinter as tk
from tkinter import font, filedialog, messagebox, colorchooser
from tkinter import ttk
from pathlib import Path

THEMES = {
    "Light": {"bg": "#ECECEC", "card": "#FFFFFF", "text": "#222222", "accent": "#5B73FF", "button_text": "#000000"},
    "Dark": {"bg": "#1E1E1E", "card": "#2A2A2A", "text": "#EAEAEA", "accent": "#6C83FF", "button_text": "#FFFFFF"},
    "High Contrast": {"bg": "#000000", "card": "#000000", "text": "#FFFF00", "accent": "#FFFFFF", "button_text": "#000000"},
}

class JournalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Journally")
        self.geometry("1000x650")
        self.resizable(False, False)

        self.journal_dir = Path("journals")
        self.journal_dir.mkdir(exist_ok=True)

        self.theme_name = "Light"
        self.theme = THEMES[self.theme_name]

        self.font_size = 15
        self.available_fonts = sorted(font.families())
        self.current_font_family = "Segoe UI"

        self.text_font = font.Font(family=self.current_font_family, size=self.font_size)
        self.bold_font = font.Font(family=self.current_font_family, size=self.font_size, weight="bold")
        self.italic_font = font.Font(family=self.current_font_family, size=self.font_size, slant="italic")

        self.text_color = self.theme["text"]

        self.tabs = {}
        self.untitled_count = 1
        self.toolbar_buttons = []

        self.build_ui()
        self.apply_theme()
        self.create_new_tab()
        self.load_files()

    def build_ui(self):
        self.sidebar = tk.Frame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.sidebar_label = tk.Label(self.sidebar, text="Your Journals", font=("Segoe UI", 12, "bold"))
        self.sidebar_label.pack(pady=10)

        self.file_list = tk.Listbox(self.sidebar)
        self.file_list.pack(fill="both", expand=True, padx=10, pady=10)
        self.file_list.bind("<<ListboxSelect>>", self.open_selected_file)

        self.main = tk.Frame(self)
        self.main.pack(fill="both", expand=True)

        self.toolbar = tk.Frame(self.main)
        self.toolbar.pack(fill="x", pady=5)

        self.new_tab_btn = tk.Button(self.toolbar, text="New Tab", command=self.create_new_tab)
        self.new_tab_btn.pack(side="left", padx=5)
        self.toolbar_buttons.append(self.new_tab_btn)

        self.close_tab_btn = tk.Button(self.toolbar, text="Close Tab", command=self.close_current_tab)
        self.close_tab_btn.pack(side="left", padx=5)
        self.toolbar_buttons.append(self.close_tab_btn)

        self.bold_btn = tk.Button(self.toolbar, text="Bold", command=self.make_bold)
        self.bold_btn.pack(side="left", padx=5)
        self.toolbar_buttons.append(self.bold_btn)

        self.italic_btn = tk.Button(self.toolbar, text="Italic", command=self.make_italic)
        self.italic_btn.pack(side="left", padx=5)
        self.toolbar_buttons.append(self.italic_btn)

        self.save_btn = tk.Button(self.toolbar, text="Save", command=self.save_file)
        self.save_btn.pack(side="left", padx=5)
        self.toolbar_buttons.append(self.save_btn)

        self.open_btn = tk.Button(self.toolbar, text="Open File", command=self.open_any_file)
        self.open_btn.pack(side="left", padx=5)
        self.toolbar_buttons.append(self.open_btn)

        self.font_var = tk.StringVar(value=self.current_font_family)
        self.font_menu = tk.OptionMenu(self.toolbar, self.font_var, *self.available_fonts, command=self.change_font)
        self.font_menu.pack(side="left", padx=5)
        self.toolbar_buttons.append(self.font_menu)

        self.size_var = tk.IntVar(value=self.font_size)
        self.font_slider = tk.Scale(
            self.toolbar,
            from_=8,
            to=40,
            orient="horizontal",
            variable=self.size_var,
            command=self.change_font_size_wrapper,
            length=150
        )
        self.font_slider.pack(side="left", padx=5)

        self.color_btn = tk.Button(self.toolbar, text="Text Colour", command=self.pick_text_color)
        self.color_btn.pack(side="left", padx=5)
        self.toolbar_buttons.append(self.color_btn)

        self.theme_var = tk.StringVar(value=self.theme_name)
        self.theme_menu = tk.OptionMenu(self.toolbar, self.theme_var, *THEMES.keys(), command=self.change_theme)
        self.theme_menu.pack(side="right", padx=10)
        self.toolbar_buttons.append(self.theme_menu)

        self.notebook = ttk.Notebook(self.main)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

    def create_new_tab(self, path=None, content=""):
        frame = tk.Frame(self.notebook)
        text = tk.Text(frame, wrap="word", font=self.text_font, insertbackground=self.text_color)
        text.pack(fill="both", expand=True)

        text.tag_configure("bold", font=self.bold_font)
        text.tag_configure("italic", font=self.italic_font)

        text.insert("1.0", content)
        text.configure(fg=self.text_color, bg=self.theme["card"])

        self.notebook.add(frame, text=self._tab_title_for_path(path))
        self.notebook.select(frame)

        self.tabs[frame] = {"text": text, "path": path}

    def _tab_title_for_path(self, path):
        if path is None:
            title = f"Untitled {self.untitled_count}"
            self.untitled_count += 1
            return title
        return Path(path).name

    def get_current_tab(self):
        tab_id = self.notebook.select()
        if not tab_id:
            return None, None
        frame = self.nametowidget(tab_id)
        return frame, self.tabs.get(frame)

    def close_current_tab(self):
        frame, meta = self.get_current_tab()
        if not meta:
            return
        if meta["path"]:
            self._save_tab_to_path(frame, meta["path"])
        self.notebook.forget(frame)
        del self.tabs[frame]
        if not self.tabs:
            self.create_new_tab()

    def _save_tab_to_path(self, frame, path):
        text = self.tabs[frame]["text"]
        content = text.get("1.0", tk.END).rstrip("\n")
        Path(path).write_text(content, encoding="utf-8")

    def save_file(self):
        frame, meta = self.get_current_tab()
        if not meta:
            return
        if not meta["path"]:
            meta["path"] = filedialog.asksaveasfilename(
                initialdir=self.journal_dir, 
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")]
            )
            if not meta["path"]:
                return
            self.notebook.tab(frame, text=Path(meta["path"]).name)

        self._save_tab_to_path(frame, meta["path"])
        self.load_files()

    def open_file_in_tab(self, path):
        path = Path(path)
        
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {str(e)}")
            return

        self.create_new_tab(path=str(path), content=content)

    def open_any_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )
        if path:
            self.open_file_in_tab(path)

    def open_selected_file(self, event):
        if not self.file_list.curselection():
            return
        filename = self.file_list.get(self.file_list.curselection())
        path = self.journal_dir / filename
        if path.exists():
            self.open_file_in_tab(path)

    def load_files(self):
        self.file_list.delete(0, tk.END)
        for f in sorted(self.journal_dir.glob("*.txt")):
            self.file_list.insert(tk.END, f.name)

    def change_font(self, font_name):
        self.current_font_family = font_name
        self.text_font.configure(family=font_name)
        self.bold_font.configure(family=font_name)
        self.italic_font.configure(family=font_name)

        for meta in self.tabs.values():
            text_widget = meta["text"]
            text_widget.configure(font=self.text_font)
            text_widget.tag_configure("bold", font=self.bold_font)
            text_widget.tag_configure("italic", font=self.italic_font)

    def change_font_size_wrapper(self, value):
        size = int(float(value))
        self.font_size = size

        self.text_font.configure(size=size)
        self.bold_font.configure(size=size)
        self.italic_font.configure(size=size)

        for meta in self.tabs.values():
            text_widget = meta["text"]
            text_widget.configure(font=self.text_font)
            text_widget.tag_configure("bold", font=self.bold_font)
            text_widget.tag_configure("italic", font=self.italic_font)

    def pick_text_color(self):
        color = colorchooser.askcolor(initialcolor=self.text_color)[1]
        if color:
            self.text_color = color
            for meta in self.tabs.values():
                meta["text"].configure(fg=color, insertbackground=color)

    def apply_theme(self):
        t = self.theme
        
        self.configure(bg=t["bg"])
        
        self.sidebar.configure(bg=t["accent"])
        self.sidebar_label.configure(bg=t["accent"], fg=t["text"])
        self.file_list.configure(bg=t["card"], fg=t["text"], selectbackground=t["accent"])
        
        self.toolbar.configure(bg=t["bg"])
        
        for button in self.toolbar_buttons:
            try:
                button.configure(bg=t["accent"], fg=t["button_text"], activebackground=t["card"])
            except:
                pass
        
        self.font_slider.configure(bg=t["bg"], fg=t["text"], troughcolor=t["card"])
        
        for meta in self.tabs.values():
            meta["text"].configure(bg=t["card"], fg=self.text_color, insertbackground=self.text_color)
        
        style = ttk.Style()
        style.theme_use('default')
        
        if self.theme_name == "High Contrast":
            style.configure('TNotebook', background=t["bg"], borderwidth=0)
            style.configure('TNotebook.Tab', background=t["card"], foreground=t["text"], 
                          padding=[10, 2], borderwidth=2)
            style.map('TNotebook.Tab', 
                     background=[('selected', t["accent"])],
                     foreground=[('selected', t["button_text"])],
                     borderwidth=[('selected', 2)])
        else:
            style.configure('TNotebook', background=t["bg"])
            style.configure('TNotebook.Tab', background=t["card"], foreground=t["text"])
            style.map('TNotebook.Tab', 
                     background=[('selected', t["accent"])],
                     foreground=[('selected', t["text"])])

    def change_theme(self, name):
        self.theme_name = name
        self.theme = THEMES[name]
        
        if name == "High Contrast":
            
            self.text_color = "#FFFF00"
        else:
            self.text_color = self.theme.get("text", self.text_color)
        
        for meta in self.tabs.values():
            meta_text = meta["text"]
            meta_text.configure(fg=self.text_color, insertbackground=self.text_color)
        
        self.apply_theme()

    def toggle_tag(self, tag):
        frame, meta = self.get_current_tab()
        if not meta:
            return
        text = meta["text"]
        try:
            if text.tag_ranges(tk.SEL):
                start, end = text.tag_ranges(tk.SEL)
                if tag in text.tag_names("sel.first"):
                    text.tag_remove(tag, start, end)
                else:
                    text.tag_add(tag, start, end)
        except ValueError:
            pass

    def make_bold(self):
        self.toggle_tag("bold")

    def make_italic(self):
        self.toggle_tag("italic")

if __name__ == "__main__":
    JournalApp().mainloop()