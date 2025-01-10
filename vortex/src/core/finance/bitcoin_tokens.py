"""Bitcoin token management system for STAMPS and SRC-20 tokens.

This module provides functionality to interact with Bitcoin-based tokens,
specifically STAMPS and SRC-20 tokens. It includes balance checking,
transaction monitoring, and integration with the game's asset system.
"""

import aiohttp
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto
from typing import Dict, List, Optional, Union
from uuid import UUID

class BitcoinTokenType(Enum):
    """Types of Bitcoin-based tokens supported."""
    STAMPS = auto()
    SRC20 = auto()

@dataclass
class BitcoinTokenBalance:
    """Represents a token balance."""
    token_type: BitcoinTokenType
    token_id: str
    balance: Decimal
    last_updated: datetime
    metadata: Dict

class BitcoinTokenService:
    """Service for managing Bitcoin-based tokens.
    
    This service handles interaction with the BTCStampsExplorer API
    and manages token balances for STAMPS and SRC-20 tokens.
    """
    
    def __init__(self, api_base_url: str = "https://stampchain.io/api/v2"):
        """Initialize the Bitcoin token service.
        
        Args:
            api_base_url: Base URL for the BTCStampsExplorer API
        """
        self.api_base_url = api_base_url
        self._session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def get_combined_balances(self, address: str) -> List[BitcoinTokenBalance]:
        """Get both STAMPS and SRC-20 balances for an address.
        
        Args:
            address: Bitcoin address to check
            
        Returns:
            List of token balances
        """
        session = await self._get_session()
        url = f"{self.api_base_url}/balance/{address}"
        
        async with session.get(url) as response:
            if response.status != 200:
                return []
            
            data = await response.json()
            balances = []
            
            # Process STAMPS
            if "stamps" in data:
                for stamp in data["stamps"]:
                    balances.append(BitcoinTokenBalance(
                        token_type=BitcoinTokenType.STAMPS,
                        token_id=stamp["tick"],
                        balance=Decimal(str(stamp["balance"])),
                        last_updated=datetime.utcnow(),
                        metadata=stamp
                    ))
            
            # Process SRC-20
            if "src20" in data:
                for token in data["src20"]:
                    balances.append(BitcoinTokenBalance(
                        token_type=BitcoinTokenType.SRC20,
                        token_id=token["tick"],
                        balance=Decimal(str(token["balance"])),
                        last_updated=datetime.utcnow(),
                        metadata=token
                    ))
            
            return balances
    
    async def get_src20_balances(self, address: str) -> List[BitcoinTokenBalance]:
        """Get SRC-20 token balances for an address.
        
        Args:
            address: Bitcoin address to check
            
        Returns:
            List of SRC-20 token balances
        """
        session = await self._get_session()
        url = f"{self.api_base_url}/src20/balance/{address}"
        
        async with session.get(url) as response:
            if response.status != 200:
                return []
            
            data = await response.json()
            return [
                BitcoinTokenBalance(
                    token_type=BitcoinTokenType.SRC20,
                    token_id=token["tick"],
                    balance=Decimal(str(token["balance"])),
                    last_updated=datetime.utcnow(),
                    metadata=token
                )
                for token in data
            ]
    
    async def close(self):
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None 