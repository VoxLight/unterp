import tkinter as tk
from tkinter import scrolledtext, ttk
from PIL import Image, ImageTk
from pygments import lex
from pygments.lexers.python import PythonLexer
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

def apply_syntax_highlighting(text_widget, code, range_offset):
    text_widget.mark_set("range_start", f"{range_offset + 1}.0")
    tokens = lex(code, PythonLexer())
    
    for ttype, value in tokens:
        start_index = text_widget.index("range_start")
        end_index = f"range_start + {len(value)}c"
        text_widget.mark_set("range_end", end_index)
        text_widget.tag_add(str(ttype), "range_start", "range_end")
        text_widget.mark_set("range_start", "range_end")

def highlight_code(event=None, code_entry=None):
    if code_entry is None:
        return
    
    code = code_entry.get("1.0", tk.END)
    newline_count = len(code) - len(code.lstrip('\n'))
    
    # Clear existing tags
    for tag in code_entry.tag_names():
        code_entry.tag_remove(tag, "1.0", tk.END)

    apply_syntax_highlighting(code_entry, code.lstrip('\n'), newline_count)

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
    toolbar_frame = tk.Frame(code_entry_frame, bg=theme['input_bg'])
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

    # Load pygments style and apply it to the code_entry widget
    pygments_style = get_style_by_name('default')
    default_color = theme['foreground']  # Default color if not specified by pygments style

    for token, style in pygments_style:
        hex_color = style['color']
        if hex_color:
            color = f'#{hex_color}'
        else:
            color = default_color
        code_entry.tag_configure(str(token), foreground=color)
    
    # Ensure all text gets a default color if not matched by any token
    code_entry.tag_configure(str(Token), foreground=default_color)

    paned_window.add(code_entry_frame, stretch="always")

    root.mainloop()

if __name__ == "__main__":
    run_gui()
