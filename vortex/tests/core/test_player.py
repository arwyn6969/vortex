import pytest
from hypothesis import given, strategies as st
from vortex.src.core.player import Player

@pytest.fixture
def default_player():
    """Create a default player for testing."""
    return Player(
        player_id="test_player_1",
        username="test_user",
        level=1
    )

class TestPlayer:
    def test_player_creation(self, default_player):
        """Test basic player creation and attributes."""
        assert default_player.player_id == "test_player_1"
        assert default_player.username == "test_user"
        assert default_player.level == 1

    @given(st.integers(min_value=1, max_value=100))
    def test_player_level_property(self, level):
        """Property-based test for player leveling system."""
        player = Player(
            player_id="test_player_2",
            username="test_user_2",
            level=level
        )
        assert player.level == level
        assert player.level >= 1
        assert isinstance(player.level, int)

    @pytest.mark.benchmark(group="player-operations")
    def test_player_state_update_benchmark(self, benchmark, default_player):
        """Benchmark player state updates."""
        def update_operation():
            default_player.update_state({"experience": 100})
            return True
        
        result = benchmark(update_operation)
        assert result is True

    @pytest.mark.integration
    def test_player_inventory_integration(self, default_player):
        """Test integration between player and inventory systems."""
        # Add items to inventory
        default_player.add_to_inventory("test_item", 1)
        assert "test_item" in default_player.inventory
        assert default_player.inventory["test_item"] == 1

    @pytest.mark.slow
    def test_player_progression(self, default_player):
        """Test long-running player progression mechanics."""
        initial_level = default_player.level
        
        # Simulate extended gameplay
        for _ in range(100):
            default_player.gain_experience(100)
        
        assert default_player.level > initial_level

    def test_player_validation(self):
        """Test player data validation."""
        with pytest.raises(ValueError):
            Player(player_id="", username="test", level=0)
        
        with pytest.raises(ValueError):
            Player(player_id="test", username="", level=1)
        
        with pytest.raises(ValueError):
            Player(player_id="test", username="test", level=-1)

    @pytest.mark.property
    @given(
        st.text(min_size=1, max_size=20),
        st.text(min_size=1, max_size=20),
        st.integers(min_value=1, max_value=100)
    )
    def test_player_property_invariants(self, player_id, username, level):
        """Property-based test for player invariants."""
        player = Player(
            player_id=player_id,
            username=username,
            level=level
        )
        
        assert len(player.player_id) > 0
        assert len(player.username) > 0
        assert player.level >= 1
        assert player.inventory == {} 