import tkinter as tk
from tkinter import scrolledtext, ttk
from PIL import Image, ImageTk
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
from pygments.token import Token
from .interpreter import interpreter
import os

# Define a theming kit
theme = {
    'background': '#282c34',
    'foreground': '#abb2bf',
    'cursor': 'white',
    'button_bg': '#3e4451',
    'button_fg': 'white',
    'secondary_bg': '#3c4049',
    'font': ('Courier New', 12),
    'input_bg': '#383c4a',
    'output_bg': '#21252b'
}

def create_tooltip(widget, text):
    tooltip = tk.Toplevel(widget, bg="black", padx=1, pady=1)
    tooltip.withdraw()
    tooltip.overrideredirect(True)
    label = tk.Label(tooltip, text=text, bg="black", fg="white", font=("Arial", 10))
    label.pack()

    def show_tooltip(event):
        x = widget.winfo_rootx() + event.x + 20
        y = widget.winfo_rooty() + event.y
        tooltip.geometry(f"+{x}+{y}")
        tooltip.deiconify()

    def hide_tooltip(event):
        tooltip.withdraw()

    widget.bind("<Enter>", show_tooltip)
    widget.bind("<Leave>", hide_tooltip)

def apply_syntax_highlighting(code_entry, code, lexer):
    tokens = lex(code, lexer)
    for ttype, value in tokens:
        start_index = code_entry.index("range_start")
        end_index = f"range_start + {len(value)}c"
        code_entry.mark_set("range_end", end_index)
        code_entry.tag_add(str(ttype), "range_start", "range_end")
        code_entry.mark_set("range_start", "range_end")

def highlight_code(event=None, code_entry=None):
    if code_entry is None:
        return
    
    code = code_entry.get("1.0", tk.END)
    code_entry.mark_set("range_start", "1.0")

    # Clear existing tags
    for tag in code_entry.tag_names():
        code_entry.tag_remove(tag, "1.0", tk.END)

    apply_syntax_highlighting(code_entry, code, PythonLexer())

def run_gui():
    current_code = []

    def on_submit(event=None):
        code = code_entry.get("1.0", tk.END).strip()
        if code:
            current_code.append(code)
            code_entry.delete("1.0", tk.END)

        complete_code = '\n'.join(current_code)
        try:
            output = interpreter.execute_code(complete_code)
            current_code.clear()

            code_display.config(state=tk.NORMAL)
            code_display.insert(tk.END, f">>> {complete_code}\n{output}\n")
            code_display.config(state=tk.DISABLED)
        except SyntaxError:
            # Incomplete code block; continue input
            return

    def clear_console():
        code_display.config(state=tk.NORMAL)
        code_display.delete("1.0", tk.END)
        code_display.config(state=tk.DISABLED)

    def restart_interpreter():
        interpreter.namespace.clear()
        clear_console()

    root = tk.Tk()
    root.title('Unterp - Minimalistic Python Interpreter')

    # Find the icon file
    icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'unterp-removebg-preview.ico')
    root.iconbitmap(icon_path)

    # Set the theme colors
    root.configure(bg=theme['background'])

    # Configure ttk style for scrollbars and other ttk widgets
    style = ttk.Style()
    style.configure("TScrollbar", background=theme['secondary_bg'], troughcolor=theme['secondary_bg'], arrowcolor=theme['button_fg'])

    paned_window = tk.PanedWindow(root, orient=tk.VERTICAL, bg=theme['secondary_bg'])
    paned_window.pack(fill=tk.BOTH, expand=True)

    code_display = scrolledtext.ScrolledText(paned_window, wrap=tk.WORD)
    code_display.config(state=tk.DISABLED, font=theme['font'], bg=theme['output_bg'], fg=theme['foreground'], insertbackground=theme['cursor'], padx=10, pady=10)
    paned_window.add(code_display, stretch="always")

    code_entry_frame = tk.Frame(paned_window, bg=theme['secondary_bg'])
    
    # Add the toolbar frame inside the code entry frame, at the top
    toolbar_frame = tk.Frame(code_entry_frame, bg=theme['input_bg'], container=True)
    toolbar_frame.pack(side=tk.TOP, anchor='ne', padx=5, pady=5)

    # Load button icons
    icons_path = os.path.join(os.path.dirname(__file__), 'icons')
    play_icon = ImageTk.PhotoImage(Image.open(os.path.join(icons_path, "play.png")).resize((20, 20), Image.Resampling.LANCZOS))
    clear_icon = ImageTk.PhotoImage(Image.open(os.path.join(icons_path, "clear.png")).resize((16, 16), Image.Resampling.LANCZOS))
    restart_icon = ImageTk.PhotoImage(Image.open(os.path.join(icons_path, "restart.png")).resize((16, 16), Image.Resampling.LANCZOS))

    submit_button = tk.Button(toolbar_frame, image=play_icon, command=on_submit, bg=theme['button_bg'], fg=theme['button_fg'], width=30, height=30)
    submit_button.pack(side=tk.LEFT, padx=5)
    create_tooltip(submit_button, "Run Code")

    clear_button = tk.Button(toolbar_frame, image=clear_icon, command=clear_console, bg=theme['button_bg'], fg=theme['button_fg'], width=24, height=24)
    clear_button.pack(side=tk.LEFT, padx=(5, 2))
    create_tooltip(clear_button, "Clear Console")

    restart_button = tk.Button(toolbar_frame, image=restart_icon, command=restart_interpreter, bg=theme['button_bg'], fg=theme['button_fg'], width=24, height=24)
    restart_button.pack(side=tk.LEFT, padx=(2, 5))
    create_tooltip(restart_button, "Restart Interpreter")

    code_entry = tk.Text(code_entry_frame, wrap=tk.WORD, height=5, font=theme['font'])
    code_entry.pack(fill=tk.BOTH, expand=True)
    code_entry.bind("<KeyRelease>", lambda event: highlight_code(event, code_entry))
    code_entry.bind("<Control-Return>", on_submit)
    code_entry.configure(bg=theme['input_bg'], fg=theme['foreground'], insertbackground=theme['cursor'], padx=10, pady=10)

    paned_window.add(code_entry_frame, stretch="always")

    # Update the layout periodically to ensure smooth resizing
    def update_layout():
        root.update_idletasks()
        root.after(50, update_layout)

    update_layout()

    root.mainloop()

if __name__ == "__main__":
    run_gui()
