import tkinter as tk
from tkinter import filedialog, messagebox

# Initialize the main application
class NewsTickerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("News Ticker")
        self.geometry("800x200")
        self.minsize(400, 100)
        
        self.current_word_index = 0
        self.word_list = []
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
            anchor="center"
        )
        self.label.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder for speed and navigation
        self.speed = 200  # Default speed in milliseconds
        
        # Key bindings for controls
        self.bind("<Up>", self.increase_speed)
        self.bind("<Down>", self.decrease_speed)
        self.bind("<Left>", self.skip_back)
        self.bind("<Right>", self.skip_forward)

    def _setup_menu(self):
        menu = tk.Menu(self)
        
        # File menu
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_progress)
        file_menu.add_command(label="Help", command=self.show_help)
        menu.add_cascade(label="File", menu=file_menu)
        
        # Play/Pause button in the menu
        menu.add_command(label="Play/Pause", command=self.toggle_play)
        
        self.config(menu=menu)

    def open_file(self):
        filepath = filedialog.askopenfilename(
            title="Open Text File", 
            filetypes=[("Text Files", "*.txt")]
        )
        if filepath:
            with open(filepath, "r") as file:
                content = file.read()
            self.word_list = content.split()
            self.current_word_index = 0
            self.update_display()

    def save_progress(self):
        filepath = filedialog.asksaveasfilename(
            title="Save Progress", 
            filetypes=[("Text Files", "*.txt")]
        )
        if filepath:
            save_data = {
                "current_word_index": max(0, self.current_word_index - 5),
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
        help_text = tk.Text(help_window, wrap=tk.WORD)
        help_text.insert("1.0", "Help File: Add your own instructions here.\n")
        help_text.pack(fill=tk.BOTH, expand=True)
        help_text.config(state=tk.DISABLED)

    def toggle_play(self):
        self.playing = not self.playing
        if self.playing:
            self.start_ticker()
    
    def start_ticker(self):
        if self.playing and self.word_list:
            self.update_display()
            self.current_word_index += 1
            if self.current_word_index >= len(self.word_list):
                self.current_word_index = 0  # Loop back to start
            self.after(self.speed, self.start_ticker)

    def update_display(self):
        if self.word_list:
            visible_words = self.word_list[
                max(0, self.current_word_index - 2):self.current_word_index + 3
            ]
            while len(visible_words) < 5:
                visible_words.append("")
            middle_word_index = 2
            formatted_text = " ".join(
                f"[{w}]" if i == middle_word_index else w 
                for i, w in enumerate(visible_words)
            )
            self.label.config(text=formatted_text)

    def increase_speed(self, event=None):
        self.speed = max(50, self.speed - 50)

    def decrease_speed(self, event=None):
        self.speed += 50

    def skip_back(self, event=None):
        self.current_word_index = max(0, self.current_word_index - 2)
        self.update_display()

    def skip_forward(self, event=None):
        self.current_word_index = min(len(self.word_list) - 1, self.current_word_index + 2)
        self.update_display()


# Start the application
if __name__ == "__main__":
    app = NewsTickerApp()
    app.mainloop()
