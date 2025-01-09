import pytest
from src.core.player import Player

def test_player_creation():
    player = Player("TestUser")
    assert player.name == "TestUser"
    assert len(player.inventory) == 0
    assert len(player.completed_challenges) == 0

def test_inventory_management():
    player = Player("TestUser")
    player.add_to_inventory("TestItem")
    assert player.has_item("TestItem")
    assert player.remove_from_inventory("TestItem")
    assert not player.has_item("TestItem") 