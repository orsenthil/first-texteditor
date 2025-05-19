import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class TextEditor:
    """A simple text editor application."""

    def __init__(self, root):
        """Initialize the text editor.
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        self.filename = None
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        # Configure root window
        self.root.title("Text Editor")
        self.root.minsize(width=400, height=400)
        self.root.maxsize(width=400, height=400)
        
        # Create text widget
        self.text = tk.Text(self.root, width=400, height=400)
        self.text.pack()
        
        # Create menu
        self.create_menu()
        
    def create_menu(self):
        """Create the application menu."""
        menubar = tk.Menu(self.root)
        
        # File menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new_file)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_command(label="Save As", command=self.save_as)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)
    
    def new_file(self):
        """Create a new file."""
        self.filename = "Untitled"
        # "1.0" means line 1, character 0 (start of text widget)
        # tk.END represents the end of the text widget
        self.text.delete("1.0", tk.END)
    
    def save_file(self):
        """Save the current file."""
        if self.filename is None or self.filename == "Untitled":
            self.save_as()
            return
            
        self._write_to_file(self.filename)
    
    def save_as(self):
        """Save the current file with a new name."""
        file = filedialog.asksaveasfile(
            mode='w',
            defaultextension=".txt",
            filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]
        )
        
        if file is None:  # User cancelled
            return
            
        self.filename = file.name
        file.close()  # Close the file returned by asksaveasfile
        
        self._write_to_file(self.filename)
    
    def _write_to_file(self, filename):
        """Write the current text to a file.
        
        Args:
            filename: The path to the file to write to
        """
        try:
            # "1.0" means line 1, character 0 (start of text widget)
            # tk.END represents the end of the text widget
            content = self.text.get("1.0", tk.END)
            with open(filename, "w", encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            messagebox.showerror(
                title="Save Error",
                message=f"Unable to save file: {str(e)}"
            )
    
    def open_file(self):
        """Open a file."""
        file = filedialog.askopenfile(
            mode='r',
            filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]
        )
        
        if file is None:  # User cancelled
            return
            
        self.filename = file.name
        
        try:
            content = file.read()
            # "1.0" means line 1, character 0 (start of text widget)
            # tk.END represents the end of the text widget
            self.text.delete("1.0", tk.END)
            # "1.0" means insert at the start of the text widget (line 1, char 0)
            self.text.insert("1.0", content)
            file.close()
        except Exception as e:
            messagebox.showerror(
                title="Open Error",
                message=f"Unable to open file: {str(e)}"
            )


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()

