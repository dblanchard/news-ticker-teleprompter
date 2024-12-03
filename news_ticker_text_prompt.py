import tkinter as tk
from tkinter import filedialog, messagebox
import ast


class NewsTickerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("News Ticker")
        self.geometry("800x200")
        self.minsize(400, 100)

        self.current_char_index = 0
        self.text_content = ""
        self.file_path = ""
        self.playing = False

        # Set up menu
        self._setup_menu()

        # Create main display area
        self.display_frame = tk.Frame(self)
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.label = tk.Label(
            self.display_frame,
            text="Welcome to the News Ticker!",
            font=("Helvetica", 20),
            anchor="center",
        )
        self.label.pack(fill=tk.BOTH, expand=True)

        self.speed = 50  # Default speed in milliseconds

        # Key bindings for controls
        self.bind("<Up>", self.increase_speed)
        self.bind("<Down>", self.decrease_speed)
        self.bind("<Left>", self.skip_back)
        self.bind("<Right>", self.skip_forward)
        self.bind("<space>", self.toggle_play)

    def _setup_menu(self):
        menu = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Open Save", command=self.open_save_file)
        file_menu.add_command(label="Save", command=self.save_progress)
        file_menu.add_command(label="Help", command=self.show_help)
        menu.add_cascade(label="File", menu=file_menu)

        # Play/Pause button in the menu
        menu.add_command(label="Play/Pause", command=self.toggle_play)

        self.config(menu=menu)

    def open_file(self):
        filepath = filedialog.askopenfilename(
            title="Open Text File", filetypes=[("Text Files", "*.txt")]
        )
        if filepath:
            with open(filepath, "r") as file:
                self.text_content = file.read().replace("\n", " ")
            self.file_path = filepath
            self.current_char_index = 0
            self.update_display()

    def open_save_file(self):
        filepath = filedialog.askopenfilename(
            title="Open Save File", filetypes=[("Text Files", "*.txt")]
        )
        if filepath:
            with open(filepath, "r") as file:
                save_data = ast.literal_eval(file.read())
                self.file_path = save_data["file_path"]
                self.current_char_index = save_data["current_char_index"]
                self.speed = save_data["speed"]

            with open(self.file_path, "r") as file:
                self.text_content = file.read().replace("\n", " ")

            self.update_display()

    def save_progress(self):
        filepath = filedialog.asksaveasfilename(
            title="Save Progress", filetypes=[("Text Files", "*.txt")]
        )
        if filepath:
            save_data = {
                "file_path": self.file_path,
                "current_char_index": max(0, self.current_char_index - 50),
                "speed": self.speed,
            }
            with open(filepath, "w") as file:
                file.write(str(save_data))
            messagebox.showinfo("Saved", "Progress saved successfully!")

    def show_help(self):
        # Display a help window
        help_window = tk.Toplevel(self)
        help_window.title("Help")
        help_window.geometry("400x300")
        help_text = tk.Text(help_window, wrap=tk
