"""
Exceptions for core components.
"""

class NodeSetupError(Exception):
    """Exception raised for errors during the setup of learning path nodes."""
    pass

class GuidanceError(Exception):
    """Exception raised for errors during guidance generation or processing."""
    pass 