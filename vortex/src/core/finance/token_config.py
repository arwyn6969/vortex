"""Configuration for token multipliers and special tokens."""

from decimal import Decimal
from typing import Dict, Set

# Special SRC-20 tokens that provide multipliers
SPECIAL_SRC20_MULTIPLIERS: Dict[str, Decimal] = {
    "BALD": Decimal("0.42"),
    "VIVIA": Decimal("0.42"),
    "KEVIN": Decimal("0.42"),
    "DEVIN": Decimal("0.42"),
    "WOOL": Decimal("0.42"),
    "LOG": Decimal("0.42"),
    "MANDY": Decimal("0.42"),
    "SPICE": Decimal("0.42"),
}

# Special STAMPS that provide multipliers
SPECIAL_STAMPS_MULTIPLIERS: Dict[str, Decimal] = {
    "A5433937813514022010": Decimal("0.69"),  # Special stamp multiplier
}

def calculate_token_multipliers(
    src20_tokens: Set[str],
    stamps: Set[str]
) -> Decimal:
    """Calculate total multiplier from owned tokens.
    
    Args:
        src20_tokens: Set of owned SRC-20 token ticks
        stamps: Set of owned stamp IDs
        
    Returns:
        Total multiplier value (1.0 base + all applicable multipliers)
    """
    total_multiplier = Decimal("1.0")
    
    # Add SRC-20 multipliers
    for token in src20_tokens:
        if token in SPECIAL_SRC20_MULTIPLIERS:
            total_multiplier += SPECIAL_SRC20_MULTIPLIERS[token]
    
    # Add STAMPS multipliers
    for stamp in stamps:
        if stamp in SPECIAL_STAMPS_MULTIPLIERS:
            total_multiplier += SPECIAL_STAMPS_MULTIPLIERS[stamp]
            
    return total_multiplier 