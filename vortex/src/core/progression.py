"""
Module for virtue progression, including VirtueMeter.
"""

class VirtueMeter:
    """Tracks the virtue progression value for zones and guides."""

    def __init__(self, initial_value: float = 0.0):
        """Initialize VirtueMeter with an optional initial value (0.0-1.0)."""
        # Internal private storage for value
        self._value: float = 0.0
        # Use setter to initialize and clamp the initial value
        self.value = initial_value

    @property
    def value(self) -> float:
        """Get the current virtue value."""
        return self._value

    @value.setter
    def value(self, new_value: float) -> None:
        """Set virtue value, clamping it between 0.0 and 1.0."""
        try:
            val = float(new_value)
        except (TypeError, ValueError):
            # Ignore invalid assignments silently
            return
        # Clamp the value within allowed range
        self._value = min(1.0, max(0.0, val)) 