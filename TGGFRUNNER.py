import tkinter as tk
from tkinter import scrolledtext, filedialog, colorchooser, simpledialog, StringVar
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import base64
import sys
import threading
import time

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

# Use the raw key string
raw_key = "BPL$m84GF30j/HnAPb'=EcsHA@5go$CILlj3)t5u/M2'XAS6$lE+N[)H(o1F)GQ1F\"V*>FD,f+/no5"
key = generate_aes_key(raw_key)

# Unpad the data after decryption
def unpad(data):
    padding_length = ord(data[-1])
    return data[:-padding_length]

# Decrypt the content of a .TGGF file
def decrypt_content(encrypted_content, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_bytes = base64.b64decode(encrypted_content)
    decrypted_padded_bytes = cipher.decrypt(encrypted_bytes)
    return unpad(decrypted_padded_bytes.decode('utf-8'))

def run_game():
    # Open a file dialog to choose a .TGGF (Python file)
    file_path = filedialog.askopenfilename(
        title="Select a .TGGF File",
        filetypes=[("TGGF Files", "*.tggf")]
    )
    
    if file_path:
        with open(file_path, 'r') as file:
            file_content = file.read()
            
            if "TGFFILE" in file_content:
                encrypted_content = file_content.split("\n\n", 1)[1]
                try:
                    # Decrypt the content
                    decrypted_code = decrypt_content(encrypted_content, key)
                    
                    # Print the decrypted code to the terminal (for demonstration purposes)
                    output_text.insert(tk.END, f"\n--- Running Game from: {file_path} ---\n")
                    output_text.see(tk.END)

                    # Execute the game code in a separate thread
                    threading.Thread(target=execute_game_code, args=(decrypted_code,)).start()
                    
                except Exception as e:
                    output_text.insert(tk.END, f"\nError running game: {e}\n")
                    output_text.see(tk.END)
            else:
                output_text.insert(tk.END, "\nInvalid .TGGF file format.\n")
                output_text.see(tk.END)

def execute_game_code(code):
    # Prepare a local namespace with necessary imports
    local_namespace = {}
    exec("import time\n"  # Add any other imports your game code needs here
         "import sys\n"
         "import os\n", local_namespace)

    # Execute the decrypted code within the local namespace
    try:
        exec(code, local_namespace)
    except Exception as e:
        output_text.insert(tk.END, f"\nError executing game code: {e}\n")
        output_text.see(tk.END)

    # Simulate output being processed in chunks like IDLE
    for output in local_namespace.get('outputs', []):  # Assuming your game code uses an 'outputs' list
        output_text.insert(tk.END, output)
        output_text.see(tk.END)
        time.sleep(0.5)  # Adjust sleep time as needed

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    
    # Create a frame for buttons and dropdowns
    settings_frame = tk.Frame(settings_window)
    settings_frame.pack(side=tk.TOP, anchor=tk.CENTER, pady=20)  # Center the frame in the window

    # Option to change background color
    def change_background_color():
        color = colorchooser.askcolor()[1]
        if color:
            root.config(bg=color)
            output_text.insert(tk.END, f"Background color changed to {color}\n")
            output_text.see(tk.END)

    # Option to change terminal background color
    def change_terminal_color():
        color = colorchooser.askcolor()[1]
        if color:
            output_text.config(bg=color)
            output_text.insert(tk.END, f"Terminal color changed to {color}\n")
            output_text.see(tk.END)

    # Option to change button color
    def change_button_color():
        color = colorchooser.askcolor()[1]
        if color:
            run_button.config(bg=color)
            settings_button.config(bg=color)
            output_text.insert(tk.END, f"Button color changed to {color}\n")
            output_text.see(tk.END)

    # Options for resolution
    resolutions = ["800x600", "1024x768", "1280x720", "1920x1080"]
    selected_resolution = StringVar(value=resolutions[0])  # Default resolution

    # Change resolution function
    def change_resolution():
        width, height = map(int, selected_resolution.get().split('x'))
        root.geometry(f"{width}x{height}")
        output_text.insert(tk.END, f"Resolution changed to {width}x{height}\n")
        output_text.see(tk.END)

    # Options for aspect ratio
    aspect_ratios = ["16:9", "4:3", "1:1"]
    selected_aspect_ratio = StringVar(value="16:9")  # Set default aspect ratio to "16:9"

    # Change aspect ratio function
    def change_aspect_ratio():
        aspect_ratio = selected_aspect_ratio.get()
        width_ratio, height_ratio = map(int, aspect_ratio.split(":"))
        current_width = root.winfo_width()
        new_height = int(current_width * height_ratio / width_ratio)
        root.geometry(f"{current_width}x{new_height}")
        output_text.insert(tk.END, f"Aspect ratio changed to {aspect_ratio}\n")
        output_text.see(tk.END)

    # Create buttons and dropdowns for settings options arranged horizontally
    tk.Button(settings_frame, text="Change Background Color", command=change_background_color).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(settings_frame, text="Change Terminal Color", command=change_terminal_color).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(settings_frame, text="Change Button Color", command=change_button_color).pack(side=tk.LEFT, padx=5, pady=5)

    # Resolution dropdown
    tk.Label(settings_frame, text="Resolution:").pack(side=tk.LEFT, padx=5, pady=5)
    resolution_menu = tk.OptionMenu(settings_frame, selected_resolution, *resolutions, command=lambda _: change_resolution())
    resolution_menu.pack(side=tk.LEFT, padx=5, pady=5)

    # Aspect ratio dropdown
    tk.Label(settings_frame, text="Aspect Ratio:").pack(side=tk.LEFT, padx=5, pady=5)
    aspect_ratio_menu = tk.OptionMenu(settings_frame, selected_aspect_ratio, *aspect_ratios, command=lambda _: change_aspect_ratio())
    aspect_ratio_menu.pack(side=tk.LEFT, padx=5, pady=5)

    # Update the settings window size to fit the content
    settings_window.update_idletasks()  # Update the window size calculations
    settings_window.geometry(settings_window.winfo_width() + 20, settings_window.winfo_height())  # Add padding

# Create the main application window
root = tk.Tk()
root.title("TGGF - GAME RUNNER")

# Default window size
root.geometry("800x600")

# Create a frame for the buttons at the top and center-align them
button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

# Create a button to run the game
run_button = tk.Button(button_frame, text="Run Game", command=run_game)
run_button.pack(side=tk.LEFT, padx=10)

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
