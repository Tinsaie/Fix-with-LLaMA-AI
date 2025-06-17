import tkinter as tk
from tkinter import scrolledtext, messagebox
from main import generate_fixed_code
import threading
import time
import keyword

"""
# This big list of keywords is OPTIONAL.
# It contains keywords from different programming languages and web languages.
# You can use it later if you want to add syntax highlighting.

MULTI_LANG_KEYWORDS = {
    # C keywords
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default',
    'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto',
    'if', 'inline', 'int', 'long', 'register', 'restrict', 'return',
    'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef',
    'union', 'unsigned', 'void', 'volatile', 'while', '_Alignas', '_Alignof',
    '_Atomic', '_Bool', '_Complex', '_Generic', '_Imaginary', '_Noreturn',
    '_Static_assert', '_Thread_local',

    # Python keywords
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
    'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
    'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
    'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
    'try', 'while', 'with', 'yield',

    # Java keywords
    'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char',
    'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
    'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements',
    'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new',
    'package', 'private', 'protected', 'public', 'return', 'short', 'static',
    'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws',
    'transient', 'try', 'void', 'volatile', 'while',

    # HTML tags (basic set)
    'html', 'head', 'title', 'body', 'div', 'span', 'h1', 'h2', 'h3', 'h4',
    'h5', 'h6', 'p', 'a', 'img', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th',
    'form', 'input', 'button', 'script', 'style', 'link', 'meta', 'header',
    'footer', 'nav', 'section', 'article', 'aside', 'main',

    # CSS properties (basic set)
    'color', 'background', 'margin', 'padding', 'border', 'font-size',
    'font-weight', 'display', 'position', 'top', 'bottom', 'left', 'right',
    'width', 'height', 'overflow', 'visibility', 'z-index', 'flex', 'grid',
    'align-items', 'justify-content', 'text-align', 'vertical-align'
}
"""

# Define colors for light theme
LIGHT_THEME = {
    "bg": "#f0f0f0",             # background color of window
    "fg": "#000000",             # text color (foreground)
    "section_bg": "#ffffff",     # background for input/output sections
    "button_bg": "#3b82f6",      # button color
    "button_hover": "#2563eb",   # button color when mouse is over it
    "input_bg": "#ffffff",       # input box background
    "input_fg": "#000000",       # input box text color
    "footer_bg": "#dddddd",      # footer background color
    "insert_bg": "#000000",      # cursor color inside text box
}

# Define colors for dark theme
DARK_THEME = {
    "bg": "#1c1c1c",
    "fg": "#ffffff",
    "section_bg": "#2a2a2a",
    "button_bg": "#3b82f6",
    "button_hover": "#120D0D",
    "input_bg": "#1e1e1e",
    "input_fg": "#ffffff",
    "footer_bg": "#111111",
    "insert_bg": "#ffffff",
}

current_theme = DARK_THEME

# Function to fix the code when user clicks SEND
def fix_code():
    input_code = input_text.get("1.0", tk.END).strip()  
    if not input_code:
        messagebox.showwarning("⚠️ Warning", "Please enter some code.")
        return

    def task():
        # Disable the SEND button while working
        fix_button.config(state=tk.DISABLED)
        progress_label.config(text="⏳ Fixing... please wait...")

        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)  # clear previous output

        start_time = time.time()
        try:
            # Call function to fix code (from main.py)
            fixed = generate_fixed_code(input_code)
            end_time = time.time()

            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, fixed)
            # Uncomment next line if you want syntax highlighting later
            # highlight_syntax()

            # Show how long fixing took(optional)
            # output_text.insert(tk.END, f"\n\n time take: {end_time - start_time:.2f} seconds")
        except Exception as e:
            # Show error message if fixing fails
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, f"❌ Error:\n{str(e)}")
            output_text.tag_add("error", "1.0", tk.END)
        finally:
            output_text.config(state=tk.DISABLED)  
            fix_button.config(state=tk.NORMAL)
            progress_label.config(text="")

    threading.Thread(target=task).start()

# Function to clear both input and output boxes
def clear_fields():
    input_text.delete("1.0", tk.END)
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)

# Function to copy output text to clipboard
def copy_output():
    output_text.config(state=tk.NORMAL)
    result = output_text.get("1.0", tk.END).strip()
    output_text.config(state=tk.DISABLED)
    if result:
        window.clipboard_clear()
        window.clipboard_append(result)
        messagebox.showinfo("Copied", "Repaired code copied to clipboard.")
    else:
        messagebox.showwarning("Nothing to Copy", "Output is empty.")

"""
# This function is for syntax highlighting keywords (optional)
def highlight_syntax():
    output_text.tag_remove("keyword", "1.0", tk.END)
    output_text.tag_configure("keyword", foreground="#569CD6")  # Blue color for keywords

    for keyword in MULTI_LANG_KEYWORDS:
        start_index = "1.0"
        while True:
            pos_start = output_text.search(r'\b' + keyword + r'\b', start_index, stopindex=tk.END, regexp=True)
            if not pos_start:
                break
            pos_end = f"{pos_start}+{len(keyword)}c"
            output_text.tag_add("keyword", pos_start, pos_end)
            start_index = pos_end
"""

# Button hover effects (change color when mouse over)
def on_enter(e): e.widget.config(bg=current_theme["button_hover"])
def on_leave(e): e.widget.config(bg=current_theme["button_bg"])

# Switch between dark and light theme
def toggle_theme():
    global current_theme
    current_theme = LIGHT_THEME if current_theme == DARK_THEME else DARK_THEME
    apply_theme()

# Apply the current theme colors to all widgets
def apply_theme():
    window.config(bg=current_theme["bg"])
    header.config(bg=current_theme["footer_bg"])
    footer.config(bg=current_theme["footer_bg"])
    main_frame.config(bg=current_theme["bg"])
    input_frame.config(bg=current_theme["section_bg"])
    output_frame.config(bg=current_theme["section_bg"])
    button_frame.config(bg=current_theme["bg"])

    for label in [header_label, input_label, output_label, footer_label]:
        label.config(bg=current_theme["footer_bg"] if label in (header_label, footer_label) else current_theme["section_bg"], fg=current_theme["fg"])

    for text_widget in [input_text, output_text]:
        text_widget.config(
            bg=current_theme["input_bg"],
            fg=current_theme["input_fg"],
            insertbackground=current_theme["insert_bg"]
        )

    for btn in [fix_button, clear_button, copy_button, theme_button]:
        btn.config(bg=current_theme["button_bg"], fg="white", activebackground=current_theme["button_hover"])

    progress_label.config(bg=current_theme["bg"], fg=current_theme["fg"])

    footer_label.config(bg=current_theme["footer_bg"], fg="#aaaaaa")

    output_text.tag_config("keyword", foreground="#569CD6")
    output_text.tag_config("error", foreground="#FF5555")

# Start of GUI window
window = tk.Tk()
window.title("🔧FixWithLlama AI")
window.state("zoomed")  # start maximized

FONT_HEADER = ("Segoe UI", 20, "bold")
FONT_LABEL = ("Segoe UI", 13)
FONT_CODE = ("Consolas", 11)

# Top header bar
header = tk.Frame(window, height=60)
header.pack(fill=tk.X)

header_label = tk.Label(header, text="🛠️FixWithLlama AI   🛠️",
                        font=FONT_HEADER, anchor="w")
header_label.pack(side=tk.LEFT, padx=20, pady=10)

theme_button = tk.Button(header, text="🌙 Dark/Light", font=("Segoe UI", 10, "bold"),
                         relief=tk.FLAT, padx=10, pady=6, cursor="hand2", command=toggle_theme)
theme_button.pack(side=tk.RIGHT, padx=20, pady=12)
theme_button.bind("<Enter>", on_enter)
theme_button.bind("<Leave>", on_leave)

# Main area
main_frame = tk.Frame(window)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Input code section
input_frame = tk.Frame(main_frame)
input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
input_label = tk.Label(input_frame, text="🔍Paste code to check:", font=FONT_LABEL, anchor="w")
input_label.pack(anchor="w", padx=10, pady=(10, 0))
input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=15, font=FONT_CODE, bd=1, relief=tk.FLAT)
input_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Buttons: SEND, Clear, Copy Output
button_frame = tk.Frame(window)
button_frame.pack(pady=(0,10))

fix_button = tk.Button(button_frame, text="📤SEND ", command=fix_code,
                       font=("Segoe UI", 12,), relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
fix_button.grid(row=0, column=0, padx=5)
fix_button.bind("<Enter>", on_enter)
fix_button.bind("<Leave>", on_leave)

clear_button = tk.Button(button_frame, text="🧹Clear ", command=clear_fields,
                         font=("Segoe UI", 12), relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
clear_button.grid(row=0, column=1, padx=5)
clear_button.bind("<Enter>", lambda e: clear_button.config(bg=current_theme["button_hover"]))
clear_button.bind("<Leave>", lambda e: clear_button.config(bg=current_theme["button_bg"]))

copy_button = tk.Button(button_frame, text="📋Copy Output", command=copy_output,
                        font=("Segoe UI", 12), relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
copy_button.grid(row=0, column=2, padx=5)
copy_button.bind("<Enter>", lambda e: copy_button.config(bg=current_theme["button_hover"]))
copy_button.bind("<Leave>", lambda e: copy_button.config(bg=current_theme["button_bg"]))

# Label to show progress messages
progress_label = tk.Label(window, text="", font=("Segoe UI", 11, "italic"))
progress_label.pack()

# Output repaired code section
output_frame = tk.Frame(main_frame)
output_frame.pack(fill=tk.BOTH, expand=True)
output_label = tk.Label(output_frame, text="✅Repaired Code: ", font=FONT_LABEL, anchor="w")
output_label.pack(anchor="w", padx=10, pady=(10, 0))
output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=15, font=FONT_CODE, bd=1, relief=tk.FLAT, state=tk.DISABLED)
output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Footer section
footer = tk.Frame(window, height=30)
footer.pack(fill=tk.X, side=tk.BOTTOM)
footer_label = tk.Label(footer, text="© buggy | TINSAE ", font=("Segoe UI", 9), anchor="e")
footer_label.pack(side=tk.RIGHT, padx=10)

# Apply colors based on current theme
apply_theme()

# Run the GUI window loop (start the app)
window.mainloop()
