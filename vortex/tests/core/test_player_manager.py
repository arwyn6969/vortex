"""
Tests for the PlayerManager class.
"""
import pytest
from unittest.mock import MagicMock, patch
import json
from pathlib import Path
import tempfile
import shutil
from datetime import datetime, timedelta

from vortex.src.core.player_manager import PlayerManager
from vortex.src.core.player import Player
from vortex.src.core.user_profiling.profile_matrix import ProfileMatrix, ProfileDimension
from vortex.src.core.user_profiling.questionnaire import VoightKampffQuestionnaire, Question


class TestPlayerManager:
    """Test suite for the PlayerManager class."""
    
    @pytest.fixture
    def mock_ui(self):
        """Create a mock UI object."""
        ui = MagicMock()
        ui.get_input.return_value = "Test Player"
        ui.display_text = MagicMock()
        return ui
        
    @pytest.fixture
    def mock_profile_matrix(self):
        """Create a mock ProfileMatrix object."""
        profile_matrix = MagicMock(spec=ProfileMatrix)
        profile_matrix.create_profile.return_value = True
        profile_matrix.has_profile.return_value = True
        return profile_matrix
        
    @pytest.fixture
    def player_manager(self, mock_ui, mock_profile_matrix):
        """Create a PlayerManager instance with mock dependencies."""
        return PlayerManager(mock_ui, mock_profile_matrix)
        
    @pytest.fixture
    def temp_save_dir(self):
        """Create a temporary directory for save files."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            save_path = Path(tmp_dir) / "saves"
            save_path.mkdir(exist_ok=True)
            yield save_path
            
    def test_create_player(self, player_manager, mock_ui, mock_profile_matrix):
        """Test player creation functionality."""
        # Test with valid name
        mock_ui.get_input.return_value = "Test Player"
        
        with patch("vortex.src.core.config.config.get", return_value="Central Hub"):
            player = player_manager.create_player()
            
        assert player is not None
        assert player.name == "Test Player"
        assert player.current_pond == "Central Hub"
        mock_profile_matrix.create_profile.assert_called_once_with("Test Player")
        
        # Test with empty name
        mock_ui.get_input.return_value = ""
        assert player_manager.create_player() is None
        
        # Test with provided name
        player = player_manager.create_player("Provided Name")
        assert player is not None
        assert player.name == "Provided Name"
        
        # Test with exception
        mock_profile_matrix.create_profile.side_effect = ValueError("Test error")
        assert player_manager.create_player("Error Test") is None
        mock_ui.display_text.assert_any_call("\nError: Test error")
        
    @patch("time.sleep")  # Patch sleep to speed up tests
    def test_run_questionnaire(self, mock_sleep, player_manager, mock_ui):
        """Test questionnaire functionality."""
        # Setup mock questionnaire
        question = Question(
            id="q1",
            text="Test question?",
            context="Test context",
            dimension_impacts={
                ProfileDimension.ANALYTICAL: 0.8,
                ProfileDimension.INTUITIVE: 0.2
            }
        )
        
        player_manager.questionnaire = MagicMock(spec=VoightKampffQuestionnaire)
        player_manager.questionnaire.questions = [question]
        player_manager.questionnaire.get_question.return_value = question
        player_manager.questionnaire.analyze_response.return_value = {
            ProfileDimension.ANALYTICAL: 0.8,
            ProfileDimension.INTUITIVE: 0.2
        }
        
        # Test with no player
        assert player_manager.run_questionnaire() is None
        
        # Create player and test questionnaire
        player_manager.player = Player("Test Player")
        mock_ui.get_input.return_value = "Test response"
        
        with patch("vortex.src.core.config.config.get", return_value=0.1):
            result = player_manager.run_questionnaire()
            
        assert result is not None
        assert ProfileDimension.ANALYTICAL in result
        assert ProfileDimension.INTUITIVE in result
        assert result[ProfileDimension.ANALYTICAL] == 0.8
        assert result[ProfileDimension.INTUITIVE] == 0.2
        
        # Test with empty questionnaire
        player_manager.questionnaire.questions = []
        assert player_manager.run_questionnaire() is None
        
        # Test with exception in analysis
        player_manager.questionnaire.questions = [question]
        player_manager.questionnaire.analyze_response.side_effect = Exception("Test error")
        assert player_manager.run_questionnaire() is not None  # Should continue despite errors
        
    def test_save_player(self, player_manager, temp_save_dir):
        """Test player saving functionality."""
        # Test with no player
        assert player_manager.save_player() is False
        
        # Create player
        player_manager.player = Player("Test Player")
        player_manager.player.tokens = {"wisdom": 5, "harmony": 3}
        player_manager.player.visited_locations = ["Central Hub", "Wisdom Pond"]
        
        # Test saving with mocked config
        with patch("vortex.src.core.config.config.get", return_value=str(temp_save_dir)):
            assert player_manager.save_player() is True
            
            # Verify file was created
            save_path = temp_save_dir / "test_player.json"
            assert save_path.exists()
            
            # Verify file contents
            with open(save_path, 'r') as f:
                data = json.load(f)
                assert data["name"] == "Test Player"
                assert data["tokens"]["wisdom"] == 5
                assert "visited_locations" in data
                assert "Central Hub" in data["visited_locations"]
                assert "saved_at" in data
                
        # Test saving with exception
        with patch("vortex.src.core.config.config.get", side_effect=Exception("Test error")):
            assert player_manager.save_player() is False
            
    def test_load_player(self, player_manager, temp_save_dir):
        """Test player loading functionality."""
        # Create a save file
        save_data = {
            "name": "Test Player",
            "current_pond": "Wisdom Pond",
            "inventory": ["map", "compass"],
            "tokens": {"wisdom": 10, "harmony": 5},
            "visited_locations": ["Central Hub", "Wisdom Pond"],
            "stats": {"puzzles_solved": 3}
        }
        
        save_path = temp_save_dir / "test_player.json"
        with open(save_path, 'w') as f:
            json.dump(save_data, f)
            
        # Test loading with mocked config
        with patch("vortex.src.core.config.config.get", return_value=str(temp_save_dir)):
            player = player_manager.load_player("Test Player")
            
            assert player is not None
            assert player.name == "Test Player"
            assert player.current_pond == "Wisdom Pond"
            assert player.inventory == ["map", "compass"]
            assert player.tokens["wisdom"] == 10
            assert player.visited_locations == ["Central Hub", "Wisdom Pond"]
            assert player.stats["puzzles_solved"] == 3
            
            # Test loading non-existent player
            assert player_manager.load_player("Non Existent") is None
            
        # Test loading with exception
        with patch("vortex.src.core.config.config.get", side_effect=Exception("Test error")):
            assert player_manager.load_player("Test Player") is None
            
    def test_list_saved_players(self, player_manager, temp_save_dir):
        """Test listing saved players."""
        # Create some save files
        for name in ["player_one", "player_two", "player_three"]:
            save_path = temp_save_dir / f"{name}.json"
            with open(save_path, 'w') as f:
                json.dump({"name": name}, f)
                
        # Test listing with mocked config
        with patch("vortex.src.core.config.config.get", return_value=str(temp_save_dir)):
            players = player_manager.list_saved_players()
            
            assert len(players) == 3
            assert "player_one" in players
            assert "player_two" in players
            assert "player_three" in players
            
        # Test with non-existent directory
        with patch("vortex.src.core.config.config.get", return_value="/non/existent/path"):
            assert player_manager.list_saved_players() == []
            
        # Test with exception
        with patch("vortex.src.core.config.config.get", side_effect=Exception("Test error")):
            assert player_manager.list_saved_players() == []
            
    def test_update_player_location(self, player_manager):
        """Test updating player location."""
        # Test with no player
        player_manager.update_player_location("New Location")  # Should not error
        
        # Create player
        player_manager.player = Player("Test Player")
        player_manager.player.visited_locations = ["Central Hub"]
        
        # Update location
        player_manager.update_player_location("Wisdom Pond")
        
        assert player_manager.player.current_pond == "Wisdom Pond"
        assert set(player_manager.player.visited_locations) == {"Central Hub", "Wisdom Pond"}
        
        # Update to same location
        player_manager.update_player_location("Wisdom Pond")
        assert len(player_manager.player.visited_locations) == 2  # No duplicates
        
    def test_should_autosave(self, player_manager):
        """Test autosave time checking."""
        # Test with no player
        assert player_manager.should_autosave() is False
        
        # Create player
        player_manager.player = Player("Test Player")
        
        # Test with recent save time
        with patch("vortex.src.core.config.config.get", return_value=10):  # 10 minute interval
            player_manager.last_save_time = datetime.now()
            assert player_manager.should_autosave() is False
            
            # Test with old save time
            player_manager.last_save_time = datetime.now() - timedelta(minutes=15)
            assert player_manager.should_autosave() is True 