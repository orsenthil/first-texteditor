import unittest
from unittest.mock import MagicMock, patch, mock_open
import tkinter as tk
from io import StringIO

from main import TextEditor


class TestTextEditor(unittest.TestCase):
    """Test cases for the TextEditor class."""

    def setUp(self):
        """Set up test environment before each test."""
        self.root = tk.Tk()
        self.editor = TextEditor(self.root)
        # Insert some sample text for testing
        # "1.0" means line 1, character 0 (start of text widget)
        self.editor.text.insert("1.0", "Sample text for testing")
        
    def tearDown(self):
        """Clean up after each test."""
        self.root.destroy()
    
    def test_init(self):
        """Test initialization of the TextEditor."""
        self.assertIsNone(self.editor.filename)
        self.assertEqual(self.editor.root, self.root)
        self.assertIsInstance(self.editor.text, tk.Text)
    
    def test_new_file(self):
        """Test creating a new file."""
        # Set up initial state
        self.editor.filename = "test.txt"
        # "1.0" means line 1, character 0 (start of text widget)
        # tk.END is the end position of the text widget
        self.editor.text.delete("1.0", tk.END)
        self.editor.text.insert("1.0", "Initial content")
        
        # Call the method under test
        self.editor.new_file()
        
        # Check the results
        self.assertEqual(self.editor.filename, "Untitled")
        # Get text from start (1.0) to end and verify it's empty
        self.assertEqual(self.editor.text.get("1.0", tk.END).strip(), "")
    
    @patch('tkinter.filedialog.asksaveasfile')
    def test_save_as_success(self, mock_asksaveasfile):
        """Test save_as functionality when file dialog returns a file."""
        # Set up the mock
        mock_file = MagicMock()
        mock_file.name = "/path/to/test.txt"
        mock_asksaveasfile.return_value = mock_file
        
        # Call the method
        with patch('builtins.open', mock_open()) as mock_file_open:
            self.editor.save_as()
        
        # Assertions
        self.assertEqual(self.editor.filename, "/path/to/test.txt")
        mock_file.close.assert_called_once()
        mock_file_open.assert_called_once_with("/path/to/test.txt", "w", encoding='utf-8')
    
    @patch('tkinter.filedialog.asksaveasfile')
    def test_save_as_cancelled(self, mock_asksaveasfile):
        """Test save_as functionality when user cancels the dialog."""
        # Set up the mock to return None (dialog cancelled)
        mock_asksaveasfile.return_value = None
        original_filename = self.editor.filename
        
        # Call the method
        self.editor.save_as()
        
        # Assertions - filename should remain unchanged
        self.assertEqual(self.editor.filename, original_filename)
    
    def test_save_file_new(self):
        """Test saving a new file (should call save_as)."""
        # Setup
        self.editor.filename = "Untitled"
        self.editor.save_as = MagicMock()
        
        # Call the method
        self.editor.save_file()
        
        # Assert save_as was called
        self.editor.save_as.assert_called_once()
    
    def test_save_file_existing(self):
        """Test saving an existing file."""
        # Setup
        self.editor.filename = "/path/to/existing.txt"
        
        # Call the method
        with patch('builtins.open', mock_open()) as mock_file:
            self.editor.save_file()
        
        # Assertions
        mock_file.assert_called_once_with("/path/to/existing.txt", "w", encoding='utf-8')
        mock_file().write.assert_called_once()
    
    @patch('tkinter.messagebox.showerror')
    def test_save_file_error(self, mock_showerror):
        """Test error handling when saving fails."""
        # Setup
        self.editor.filename = "/path/to/existing.txt"
        
        # Create a mock that raises an exception when write is called
        m = mock_open()
        m.return_value.__enter__.return_value.write.side_effect = IOError("Test error")
        
        # Call the method
        with patch('builtins.open', m):
            self.editor.save_file()
        
        # Assert error dialog was shown
        mock_showerror.assert_called_once()
    
    @patch('tkinter.filedialog.askopenfile')
    def test_open_file_success(self, mock_askopenfile):
        """Test opening a file successfully."""
        # Setup mock file
        mock_file = MagicMock()
        mock_file.name = "/path/to/opened.txt"
        mock_file.read.return_value = "File content"
        mock_askopenfile.return_value = mock_file
        
        # Call the method
        self.editor.open_file()
        
        # Assertions
        self.assertEqual(self.editor.filename, "/path/to/opened.txt")
        # Get text from start (1.0) to end and check content
        self.assertEqual(self.editor.text.get("1.0", tk.END).strip(), "File content")
        mock_file.read.assert_called_once()
        mock_file.close.assert_called_once()
    
    @patch('tkinter.filedialog.askopenfile')
    def test_open_file_cancelled(self, mock_askopenfile):
        """Test behavior when user cancels file open dialog."""
        # Setup - dialog returns None
        mock_askopenfile.return_value = None
        # Get the current text content to verify it doesn't change
        original_content = self.editor.text.get("1.0", tk.END)
        
        # Call the method
        self.editor.open_file()
        
        # Assertions - content shouldn't change
        self.assertEqual(self.editor.text.get("1.0", tk.END), original_content)
    
    @patch('tkinter.filedialog.askopenfile')
    @patch('tkinter.messagebox.showerror')
    def test_open_file_error(self, mock_showerror, mock_askopenfile):
        """Test error handling when opening a file fails."""
        # Setup - file.read raises an exception
        mock_file = MagicMock()
        mock_file.name = "/path/to/error.txt"
        mock_file.read.side_effect = IOError("Test error")
        mock_askopenfile.return_value = mock_file
        
        # Call the method
        self.editor.open_file()
        
        # Assertions
        mock_showerror.assert_called_once()


if __name__ == "__main__":
    unittest.main() 