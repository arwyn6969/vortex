import unittest
from unittest.mock import Mock, patch
from vortex.src.core.ui.interface import VortexInterface, UIMode
from vortex.src.core.user_profiling.profile_matrix import ProfileMatrix

class TestVortexInterface(unittest.TestCase):
    """Test suite for the VortexInterface class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.profile_matrix = ProfileMatrix()
        
    def test_gui_mode_initialization(self):
        """Test interface initialization in GUI mode."""
        interface = VortexInterface(mode=UIMode.GUI, profile_matrix=self.profile_matrix)
        self.assertEqual(interface.mode, UIMode.GUI)
        self.assertIsNotNone(interface._ui)
        
    def test_terminal_mode_initialization(self):
        """Test interface initialization in terminal mode."""
        interface = VortexInterface(mode=UIMode.TERMINAL, profile_matrix=self.profile_matrix)
        self.assertEqual(interface.mode, UIMode.TERMINAL)
        self.assertIsNotNone(interface._ui)
    
    @patch('vortex.src.core.ui.gui.VortexGUI')
    def test_gui_message_display(self, mock_gui):
        """Test message display in GUI mode."""
        interface = VortexInterface(mode=UIMode.GUI, profile_matrix=self.profile_matrix)
        test_message = "Test message"
        interface.display_message(test_message)
        mock_gui.return_value.display_message.assert_called_once_with(test_message, "system")
    
    @patch('vortex.src.core.ui.terminal.TerminalUI')
    def test_terminal_message_display(self, mock_terminal):
        """Test message display in terminal mode."""
        interface = VortexInterface(mode=UIMode.TERMINAL, profile_matrix=self.profile_matrix)
        test_message = "Test message"
        interface.display_message(test_message)
        mock_terminal.return_value.display_text.assert_called_once_with(test_message)
    
    @patch('vortex.src.core.ui.gui.VortexGUI')
    def test_gui_quick_responses(self, mock_gui):
        """Test quick response updates in GUI mode."""
        interface = VortexInterface(mode=UIMode.GUI, profile_matrix=self.profile_matrix)
        responses = ["Option A", "Option B"]
        interface.update_quick_responses(responses)
        mock_gui.return_value.update_quick_responses.assert_called_once_with(responses)
    
    @patch('vortex.src.core.ui.gui.VortexGUI')
    def test_gui_stats_update(self, mock_gui):
        """Test stats update in GUI mode."""
        interface = VortexInterface(mode=UIMode.GUI, profile_matrix=self.profile_matrix)
        stats = {"Level": "5", "Experience": "100"}
        interface.update_stats(stats)
        mock_gui.return_value._update_stats.assert_called_once_with(stats)
    
    @patch('vortex.src.core.ui.terminal.TerminalUI')
    def test_terminal_clear_screen(self, mock_terminal):
        """Test clear screen in terminal mode."""
        interface = VortexInterface(mode=UIMode.TERMINAL, profile_matrix=self.profile_matrix)
        interface.clear_screen()
        mock_terminal.return_value.clear_screen.assert_called_once()
    
    @patch('vortex.src.core.ui.gui.VortexGUI')
    def test_gui_start_stop(self, mock_gui):
        """Test GUI start and stop methods."""
        interface = VortexInterface(mode=UIMode.GUI, profile_matrix=self.profile_matrix)
        
        interface.start()
        mock_gui.return_value.start.assert_called_once()
        
        interface.stop()
        mock_gui.return_value.stop.assert_called_once()
    
    def test_show_intro(self):
        """Test showing introduction in both modes."""
        # Test GUI mode
        with patch('vortex.src.core.ui.gui.VortexGUI') as mock_gui:
            interface = VortexInterface(mode=UIMode.GUI, profile_matrix=self.profile_matrix)
            interface.show_intro()
            mock_gui.return_value.display_message.assert_called()
        
        # Test Terminal mode
        with patch('vortex.src.core.ui.terminal.TerminalUI') as mock_terminal:
            interface = VortexInterface(mode=UIMode.TERMINAL, profile_matrix=self.profile_matrix)
            interface.show_intro()
            mock_terminal.return_value.show_intro.assert_called_once()

if __name__ == '__main__':
    unittest.main() 