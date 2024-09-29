import tkinter as tk
from tkinter import scrolledtext, filedialog, colorchooser, simpledialog
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import base64
import sys

class RedirectText:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)  # Scroll to the end

    def flush(self):
        pass  # Required for file-like objects, but not used here

# Function to hash the key
def generate_aes_key(raw_key):
    return SHA256.new(raw_key.encode()).digest()  # Create a 32-byte AES key

# Use the raw key string (no need to decode from base85 anymore)
raw_key = "BPL$m84GF30j/HnAPb'=EcsHA@5go$CILlj3)t5u/M2'XAS6$lE+N[)H(o1F)GQ1F\"V*>FD,f+/no5"
key = generate_aes_key(raw_key)

# Pad the data to be AES block size
def pad(data):
    return data + (AES.block_size - len(data) % AES.block_size) * chr(AES.block_size - len(data) % AES.block_size)

# Encrypt Python file content
def encrypt_content(content, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_content = pad(content)
    encrypted_bytes = cipher.encrypt(padded_content.encode())
    return base64.b64encode(encrypted_bytes).decode()

# Function to convert .py to .tggf (encrypted)
def convert_py_to_tggf(py_file_path, tggf_file_path, key):
    try:
        with open(py_file_path, 'r') as py_file:
            py_content = py_file.read()
        
        # Encrypt the content
        encrypted_content = encrypt_content(py_content, key)
        
        # Add a simple header to mark the .tggf file
        tggf_content = f"TGFFILE\nVersion: 1.0\n\n{encrypted_content}"
        
        # Write the encrypted content to the .tggf file
        with open(tggf_file_path, 'w') as tggf_file:
            tggf_file.write(tggf_content)

        output_text.insert(tk.END, f"Conversion to {tggf_file_path} completed.\n")
        output_text.see(tk.END)
    except Exception as e:
        output_text.insert(tk.END, f"\nError during conversion: {e}\n")
        output_text.see(tk.END)

def select_and_convert_file():
    # Open a file dialog to choose a .py file
    py_file_path = filedialog.askopenfilename(
        title="Select a Python File",
        filetypes=[("Python Files", "*.py")]
    )

    if py_file_path:
        # Set the output .tggf file path
        tggf_file_path = py_file_path.replace('.py', '.tggf')
        convert_py_to_tggf(py_file_path, tggf_file_path, key)

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("400x300")  # Increase the size of the settings window
    
    # Option to change background color
    def change_background_color():
        color = colorchooser.askcolor()[1]
        if color:
            root.config(bg=color)

    # Option to change terminal background color
    def change_terminal_color():
        color = colorchooser.askcolor()[1]
        if color:
            output_text.config(bg=color)

    # Option to change button color
    def change_button_color():
        color = colorchooser.askcolor()[1]
        if color:
            convert_button.config(bg=color)
            settings_button.config(bg=color)

    # Option to change resolution
    def change_resolution():
        width = simpledialog.askinteger("Resolution", "Enter width:", initialvalue=root.winfo_width())
        height = simpledialog.askinteger("Resolution", "Enter height:", initialvalue=root.winfo_height())
        if width and height:
            root.geometry(f"{width}x{height}")

    # Option to change aspect ratio
    def change_aspect_ratio():
        aspect_ratio = simpledialog.askstring("Aspect Ratio", "Enter aspect ratio (e.g., 16:9):", initialvalue="16:9")
        if aspect_ratio:
            width_ratio, height_ratio = map(int, aspect_ratio.split(":"))
            current_width = root.winfo_width()
            new_height = int(current_width * height_ratio / width_ratio)
            root.geometry(f"{current_width}x{new_height}")

    # Buttons for settings options
    tk.Button(settings_window, text="Change Background Color", command=change_background_color, width=30).pack(pady=5)
    tk.Button(settings_window, text="Change Terminal Color", command=change_terminal_color, width=30).pack(pady=5)
    tk.Button(settings_window, text="Change Button Color", command=change_button_color, width=30).pack(pady=5)
    tk.Button(settings_window, text="Change Resolution", command=change_resolution, width=30).pack(pady=5)
    tk.Button(settings_window, text="Change Aspect Ratio", command=change_aspect_ratio, width=30).pack(pady=5)

# Create the main application window
root = tk.Tk()
root.title("TGGF - GAME CONVERTER")

# Default window size
root.geometry("800x600")

# Create a frame for the buttons at the top and center-align them
button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

# Create a button to convert a Python file
convert_button = tk.Button(button_frame, text="Convert Python to TGGF", command=select_and_convert_file)
convert_button.pack(side=tk.LEFT, padx=10)

# Create a settings button to open the settings window
settings_button = tk.Button(button_frame, text="Settings", command=open_settings)
settings_button.pack(side=tk.LEFT, padx=10)

# Center-align the buttons
button_frame.pack(anchor=tk.CENTER)

# Create a scrolled text widget for output (terminal)
output_text = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD, bg="black", fg="white")
output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Redirect sys.stdout to the scrolled text widget
redirect = RedirectText(output_text)
sys.stdout = redirect

# Start the Tkinter main loop
root.mainloop()
