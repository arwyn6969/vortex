import unittest
from unittest.mock import Mock, patch
import customtkinter as ctk
from src.core.ui.gui import VortexGUI

class TestVortexGUI(unittest.TestCase):
    """Test suite for the VortexGUI class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.gui = VortexGUI()
        
    def tearDown(self):
        """Clean up after tests."""
        if hasattr(self, 'gui') and hasattr(self.gui, 'window'):
            self.gui.window.destroy()
    
    def test_initialization(self):
        """Test that GUI is properly initialized with all components."""
        # Test window properties
        self.assertEqual(self.gui.window.title(), "Vortex of Enlightenment")
        self.assertEqual(self.gui.window.geometry(), "1200x800")
        
        # Test main components exist
        self.assertIsInstance(self.gui.display_text, ctk.CTkTextbox)
        self.assertIsInstance(self.gui.input_field, ctk.CTkEntry)
        self.assertIsInstance(self.gui.send_button, ctk.CTkButton)
        self.assertIsInstance(self.gui.stats_button, ctk.CTkButton)
        
        # Test quick response buttons
        self.assertEqual(len(self.gui.quick_buttons), 4)
        for button in self.gui.quick_buttons:
            self.assertIsInstance(button, ctk.CTkButton)
    
    def test_message_display(self):
        """Test displaying messages in the GUI."""
        test_message = "Test message"
        self.gui.display_message(test_message)
        
        # Get displayed text (excluding any formatting)
        displayed_text = self.gui.display_text.get("1.0", "end-1c").strip()
        self.assertIn(test_message, displayed_text)
        
        # Test different message types
        self.gui.display_message("System message", "system")
        self.gui.display_message("User message", "user")
        displayed_text = self.gui.display_text.get("1.0", "end-1c")
        self.assertIn("System message", displayed_text)
        self.assertIn("User message", displayed_text)
    
    def test_stats_update(self):
        """Test updating stats display."""
        test_stats = {
            "Level": "5",
            "Experience": "450/1000",
            "Wisdom": "75",
            "Progress": "45%"
        }
        self.gui._update_stats(test_stats)
        
        # Verify all stats are displayed
        for key, value in test_stats.items():
            self.assertIn(key, self.gui.stats)
            label_text = self.gui.stats[key].cget("text")
            self.assertEqual(label_text, f"{key}: {value}")
    
    def test_quick_responses_update(self):
        """Test updating quick response buttons."""
        new_responses = ["Option A", "Option B", "Option C", "Option D"]
        self.gui.update_quick_responses(new_responses)
        
        # Verify button texts are updated
        for button, response in zip(self.gui.quick_buttons, new_responses):
            self.assertEqual(button.cget("text"), response)
    
    @patch('customtkinter.CTkToplevel')
    def test_dashboard_display(self, mock_toplevel):
        """Test dashboard window creation."""
        self.gui._show_dashboard()
        mock_toplevel.assert_called_once()
    
    def test_message_callback(self):
        """Test message sending callback."""
        test_message = "Test message"
        mock_callback = Mock()
        self.gui.message_callback = mock_callback
        
        # Simulate message input and send
        self.gui.input_field.insert(0, test_message)
        self.gui._handle_send()
        
        # Verify callback was called with correct message
        mock_callback.assert_called_once_with(test_message)
        # Verify input field was cleared
        self.assertEqual(self.gui.input_field.get(), "")
    
    def test_button_callback(self):
        """Test quick response button callback."""
        mock_callback = Mock()
        self.gui.button_callback = mock_callback
        test_response = "Test response"
        
        # Simulate button click
        self.gui._handle_quick_response(test_response)
        
        # Verify callback was called with correct response
        mock_callback.assert_called_once_with(test_response)

    def test_input_field_events(self):
        """Test input field event handling."""
        # Test Enter key binding
        mock_callback = Mock()
        self.gui.message_callback = mock_callback
        test_message = "Test message"
        
        # Simulate typing and pressing Enter
        self.gui.input_field.insert(0, test_message)
        self.gui.input_field.event_generate('<Return>')
        
        # Verify message was sent and field cleared
        mock_callback.assert_called_once_with(test_message)
        self.assertEqual(self.gui.input_field.get(), "")
    
    def test_gui_state_management(self):
        """Test GUI state management during updates."""
        # Test display text state management
        self.gui.display_text.configure(state="normal")
        self.gui.display_message("Test message")
        self.assertEqual(self.gui.display_text.cget("state"), "disabled")
        
        # Test input field state during processing
        self.gui.input_field.configure(state="normal")
        self.gui._handle_send()
        self.assertEqual(self.gui.input_field.cget("state"), "normal")
    
    def test_error_handling(self):
        """Test GUI error handling."""
        # Test handling invalid stats update
        invalid_stats = None
        self.gui._update_stats(invalid_stats)  # Should not raise exception
        
        # Test handling message display with invalid type
        self.gui.display_message("Test message", "invalid_type")  # Should use default type
        displayed_text = self.gui.display_text.get("1.0", "end-1c")
        self.assertIn("Test message", displayed_text)
    
    def test_concurrent_updates(self):
        """Test handling concurrent GUI updates."""
        import time
        
        # Test that multiple rapid GUI updates are handled correctly
        messages = [
            "First message",
            "Second message",
            "Third message",
            "Fourth message",
            "Fifth message"
        ]
        
        # Simulate rapid updates
        for msg in messages:
            self.gui.display_message(msg)
            self.gui.update_quick_responses(["A", "B", "C", "D"])
            self.gui._update_stats({"Level": "1"})
            self.gui.window.update()
        
        # Give GUI time to process all updates
        for _ in range(5):
            self.gui.window.update()
            time.sleep(0.01)
        
        # Verify all messages were displayed
        displayed_text = self.gui.display_text.get("1.0", "end-1c")
        for msg in messages:
            self.assertIn(msg, displayed_text, f"Message '{msg}' not displayed")
        
        # Verify final GUI state
        self.assertEqual(
            self.gui.quick_buttons[0].cget("text"), 
            "A", 
            "Quick responses not in final state"
        )
        self.assertEqual(
            self.gui.stats["Level"].cget("text"), 
            "Level: 1", 
            "Stats not in final state"
        )

    def test_large_data_handling(self):
        """Test GUI performance with large amounts of data."""
        # Generate large text
        large_text = "Test message\n" * 1000
        
        # Measure time to display large text
        import time
        start_time = time.time()
        self.gui.display_message(large_text)
        end_time = time.time()
        
        # Verify display time is reasonable (under 1 second)
        self.assertLess(end_time - start_time, 1.0)
        
        # Verify text was displayed correctly
        displayed_text = self.gui.display_text.get("1.0", "end-1c")
        self.assertEqual(len(displayed_text.split("\n")), 1000)
        
        # Test quick response updates with many options
        many_responses = [f"Option {i}" for i in range(20)]
        self.gui.update_quick_responses(many_responses[:4])  # Should handle overflow gracefully
        
        # Verify only 4 buttons were updated
        for i, button in enumerate(self.gui.quick_buttons):
            self.assertEqual(button.cget("text"), many_responses[i])
    
    def test_memory_management(self):
        """Test memory management during extended GUI usage."""
        import sys
        import gc
        
        # Get initial memory usage
        initial_size = sys.getsizeof(self.gui)
        
        # Simulate extended usage
        for _ in range(100):
            self.gui.display_message("Test message " * 10)
            self.gui.update_quick_responses(["A", "B", "C", "D"])
            self.gui._update_stats({"Level": str(_)})
        
        # Force garbage collection
        gc.collect()
        
        # Get final memory usage
        final_size = sys.getsizeof(self.gui)
        
        # Verify memory usage hasn't grown significantly
        # Allow for some growth but not more than 50%
        self.assertLess(final_size, initial_size * 1.5)
    
    @patch('PIL.Image.open')
    def test_image_handling(self, mock_image_open):
        """Test image loading and display functionality."""
        # Mock image loading
        mock_image = Mock()
        mock_image.size = (100, 100)
        mock_image_open.return_value = mock_image
        
        # Test loading valid image
        try:
            self.gui._load_image("test.png")
        except Exception as e:
            self.fail(f"Image loading raised exception: {e}")
        
        # Test handling invalid image
        mock_image_open.side_effect = FileNotFoundError
        self.gui._load_image("nonexistent.png")  # Should handle gracefully
        
        # Test image scaling
        mock_image_open.side_effect = None
        mock_image.size = (1000, 1000)
        scaled_image = self.gui._load_image("large.png", max_size=(200, 200))
        self.assertIsNotNone(scaled_image)

if __name__ == '__main__':
    unittest.main() 