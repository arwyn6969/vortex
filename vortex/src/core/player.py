"""
Player state management.
"""

class Player:
    def __init__(self, name):
        self.name = name
        self.current_pond = None
        self.inventory = []
        self.completed_challenges = set()
        self.unlocked_streams = set()
        
    def add_to_inventory(self, item):
        self.inventory.append(item)
        
    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def has_item(self, item):
        return item in self.inventory
    
    def complete_challenge(self, challenge_id):
        self.completed_challenges.add(challenge_id)
        
    def unlock_stream(self, stream_id):
        self.unlocked_streams.add(stream_id)
        
    def can_access_stream(self, stream_id):
        return stream_id in self.unlocked_streams 