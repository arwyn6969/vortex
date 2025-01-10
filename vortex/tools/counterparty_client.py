"""Counterparty API Client

This module provides a client for interacting with the Counterparty Core API,
handling token data, issuances, and ownership information.
"""

import logging
from typing import Dict, List, Optional, Any, Union
import requests
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TokenInfo:
    """Data class for token information."""
    asset: str
    asset_longname: Optional[str]
    description: str
    issuer: Optional[str]
    divisible: bool
    locked: bool
    supply: int
    asset_id: Optional[int] = None

@dataclass
class IssuanceEvent:
    """Data class for token issuance events."""
    tx_hash: str
    block_index: int
    block_time: int
    source: str
    quantity: int
    divisible: bool
    lock: bool
    description: str
    status: str
    asset_longname: Optional[str] = None
    reset: bool = False
    callable: bool = False
    call_date: int = 0
    call_price: float = 0.0

@dataclass
class SendEvent:
    """Data class for token send events."""
    tx_hash: str
    block_index: int
    block_time: int
    source: str
    destination: str
    asset: str
    quantity: int
    memo: Optional[str] = None
    status: str = "valid"

@dataclass
class DispenserInfo:
    """Data class for dispenser information."""
    tx_hash: str
    block_index: int
    source: str
    asset: str
    give_quantity: int
    escrow_quantity: int
    status: str
    give_remaining: int
    block_time: int
    dispense_count: int = 0
    satoshirate: float = 0.0
    oracle_address: Optional[str] = None

@dataclass
class DividendEvent:
    """Data class for dividend events."""
    tx_hash: str
    block_index: int
    block_time: int
    source: str
    asset: str
    dividend_asset: str
    quantity_per_unit: int
    status: str
    dividend_asset_info: Dict[str, Any]

@dataclass
class EnhancedSendEvent:
    """Data class for enhanced send events with memo support."""
    tx_hash: str
    block_index: int
    block_time: int
    source: str
    destination: str
    asset: str
    quantity: int
    memo: Optional[str] = None
    memo_is_hex: bool = False
    status: str = "valid"

@dataclass
class Order:
    """Data class for order information."""
    tx_hash: str
    block_index: int
    source: str
    give_asset: str
    give_quantity: int
    give_remaining: int
    get_asset: str
    get_quantity: int
    get_remaining: int
    expiration: int
    expire_index: int
    fee_required: int
    fee_provided: int
    fee_remaining: int
    status: str
    block_time: int

@dataclass
class OrderMatch:
    """Data class for order match information."""
    id: str
    tx0_hash: str
    tx0_address: str
    tx0_block_index: int
    tx0_expiration: int
    tx1_hash: str
    tx1_address: str
    tx1_block_index: int
    tx1_expiration: int
    forward_asset: str
    forward_quantity: int
    backward_asset: str
    backward_quantity: int
    status: str
    block_time: int

@dataclass
class AssetTransfer:
    """Data class for asset transfer information."""
    tx_hash: str
    block_index: int
    source: str
    destination: str
    asset: str
    quantity: int
    status: str
    block_time: int

@dataclass
class BroadcastEvent:
    """Data class for broadcast events."""
    tx_hash: str
    block_index: int
    source: str
    timestamp: int
    value: float
    fee_fraction_int: int
    text: str
    status: str
    block_time: int

@dataclass
class BTCPay:
    """Data class for BTC payment information."""
    tx_hash: str
    block_index: int
    source: str
    destination: str
    btc_amount: int
    order_match_id: str
    status: str
    block_time: int

class CounterpartyAPIError(Exception):
    """Custom exception for Counterparty API errors."""
    pass

class CounterpartyClient:
    """Client for interacting with the Counterparty Core API."""
    
    def __init__(self, api_url: str, verify_ssl: bool = True):
        """Initialize the Counterparty client.
        
        Args:
            api_url: Base URL for the Counterparty API
            verify_ssl: Whether to verify SSL certificates
        """
        self.api_url = api_url.rstrip('/')
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
    
    def _make_request(
        self, endpoint: str, method: str = 'GET', params: Optional[Dict] = None
    ) -> Dict:
        """Make a request to the Counterparty API.
        
        Args:
            endpoint: API endpoint to call
            method: HTTP method to use
            params: Query parameters
            
        Returns:
            API response as dictionary
            
        Raises:
            CounterpartyAPIError: If the API request fails
        """
        try:
            url = f"{self.api_url}/{endpoint.lstrip('/')}"
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            
            # Check if API is ready
            if response.headers.get('X-COUNTERPARTY-READY', 'false').lower() != 'true':
                logger.warning("Counterparty API is not fully synced")
            
            data = response.json()
            if 'error' in data:
                raise CounterpartyAPIError(f"API Error: {data['error']}")
                
            return data.get('result', {})
            
        except requests.exceptions.RequestException as e:
            raise CounterpartyAPIError(f"Request failed: {str(e)}")
        except ValueError as e:
            raise CounterpartyAPIError(f"Invalid JSON response: {str(e)}")
    
    def get_token_info(self, token_name: str) -> TokenInfo:
        """Get information about a specific token.
        
        Args:
            token_name: Name of the token
            
        Returns:
            TokenInfo object containing token details
        """
        try:
            data = self._make_request(f"v2/assets/{token_name}")
            return TokenInfo(
                asset=data['asset'],
                asset_longname=data.get('asset_longname'),
                description=data.get('description', ''),
                issuer=data.get('issuer'),
                divisible=data.get('divisible', False),
                locked=data.get('locked', False),
                supply=data.get('supply', 0),
                asset_id=data.get('asset_id')
            )
        except Exception as e:
            logger.error(f"Error fetching token info for {token_name}: {e}")
            raise
    
    def get_token_holders(
        self, token_name: str, min_balance: int = 0
    ) -> Dict[str, int]:
        """Get current holders of a token.
        
        Args:
            token_name: Name of the token
            min_balance: Minimum balance to include
            
        Returns:
            Dictionary of addresses and their balances
        """
        try:
            data = self._make_request(
                f"v2/assets/{token_name}/holders",
                params={'min_balance': min_balance}
            )
            return {
                holder['address']: holder['balance']
                for holder in data
                if holder['balance'] > min_balance
            }
        except Exception as e:
            logger.error(f"Error fetching holders for {token_name}: {e}")
            raise
    
    def get_issuances(
        self, token_name: str, start_block: Optional[int] = None
    ) -> List[IssuanceEvent]:
        """Get issuance events for a token.
        
        Args:
            token_name: Name of the token
            start_block: Optional starting block number
            
        Returns:
            List of IssuanceEvent objects
        """
        try:
            params = {'asset': token_name}
            if start_block is not None:
                params['start_block'] = start_block
                
            data = self._make_request("v2/events/ISSUANCE", params=params)
            
            issuances = []
            for event in data.get('result', []):
                params = event['params']
                issuances.append(IssuanceEvent(
                    tx_hash=event['tx_hash'],
                    block_index=event['block_index'],
                    block_time=event['block_time'],
                    source=params['issuer'],
                    quantity=params['quantity'],
                    divisible=params['divisible'],
                    lock=params.get('lock', False),
                    description=params.get('description', ''),
                    status=params['status'],
                    asset_longname=params.get('asset_longname'),
                    reset=params.get('reset', False),
                    callable=params.get('callable', False),
                    call_date=params.get('call_date', 0),
                    call_price=params.get('call_price', 0.0)
                ))
            
            return issuances
            
        except Exception as e:
            logger.error(f"Error fetching issuances for {token_name}: {e}")
            raise
    
    def get_sends(
        self, token_name: str, start_block: Optional[int] = None
    ) -> List[SendEvent]:
        """Get send events for a token.
        
        Args:
            token_name: Name of the token
            start_block: Optional starting block number
            
        Returns:
            List of SendEvent objects
        """
        try:
            params = {'asset': token_name}
            if start_block is not None:
                params['start_block'] = start_block
                
            data = self._make_request("v2/events/SEND", params=params)
            
            sends = []
            for event in data.get('result', []):
                params = event['params']
                sends.append(SendEvent(
                    tx_hash=event['tx_hash'],
                    block_index=event['block_index'],
                    block_time=event['block_time'],
                    source=params['source'],
                    destination=params['destination'],
                    asset=params['asset'],
                    quantity=params['quantity'],
                    memo=params.get('memo'),
                    status=params['status']
                ))
            
            return sends
            
        except Exception as e:
            logger.error(f"Error fetching sends for {token_name}: {e}")
            raise

    def get_dispensers(
        self, 
        token_name: Optional[str] = None,
        status_in: Optional[List[str]] = None
    ) -> List[DispenserInfo]:
        """Get dispenser information for a token.
        
        Args:
            token_name: Optional name of the token to filter by
            status_in: Optional list of statuses to filter by
            
        Returns:
            List of DispenserInfo objects
        """
        try:
            params = {}
            if token_name:
                params['asset'] = token_name
            if status_in:
                params['status_in'] = status_in
                
            data = self._make_request("v2/dispensers", params=params)
            
            dispensers = []
            for dispenser in data:
                dispensers.append(DispenserInfo(
                    tx_hash=dispenser['tx_hash'],
                    block_index=dispenser['block_index'],
                    source=dispenser['source'],
                    asset=dispenser['asset'],
                    give_quantity=dispenser['give_quantity'],
                    escrow_quantity=dispenser['escrow_quantity'],
                    status=dispenser['status'],
                    give_remaining=dispenser['give_remaining'],
                    block_time=dispenser['block_time'],
                    dispense_count=dispenser.get('dispense_count', 0),
                    satoshirate=dispenser.get('satoshirate', 0.0),
                    oracle_address=dispenser.get('oracle_address')
                ))
            
            return dispensers
            
        except Exception as e:
            logger.error(f"Error fetching dispensers for {token_name}: {e}")
            raise

    def get_dividends(
        self, token_name: str, start_block: Optional[int] = None
    ) -> List[DividendEvent]:
        """Get dividend events for a token.
        
        Args:
            token_name: Name of the token
            start_block: Optional starting block number
            
        Returns:
            List of DividendEvent objects
        """
        try:
            params = {'asset': token_name}
            if start_block is not None:
                params['start_block'] = start_block
                
            data = self._make_request("v2/events/DIVIDEND", params=params)
            
            dividends = []
            for event in data.get('result', []):
                params = event['params']
                dividends.append(DividendEvent(
                    tx_hash=event['tx_hash'],
                    block_index=event['block_index'],
                    block_time=event['block_time'],
                    source=params['source'],
                    asset=params['asset'],
                    dividend_asset=params['dividend_asset'],
                    quantity_per_unit=params['quantity_per_unit'],
                    status=params['status'],
                    dividend_asset_info=params['dividend_asset_info']
                ))
            
            return dividends
            
        except Exception as e:
            logger.error(f"Error fetching dividends for {token_name}: {e}")
            raise

    def get_enhanced_sends(
        self, token_name: str, start_block: Optional[int] = None
    ) -> List[EnhancedSendEvent]:
        """Get enhanced send events for a token (includes memo support).
        
        Args:
            token_name: Name of the token
            start_block: Optional starting block number
            
        Returns:
            List of EnhancedSendEvent objects
        """
        try:
            params = {'asset': token_name}
            if start_block is not None:
                params['start_block'] = start_block
                
            data = self._make_request("v2/events/ENHANCED_SEND", params=params)
            
            sends = []
            for event in data.get('result', []):
                params = event['params']
                sends.append(EnhancedSendEvent(
                    tx_hash=event['tx_hash'],
                    block_index=event['block_index'],
                    block_time=event['block_time'],
                    source=params['source'],
                    destination=params['destination'],
                    asset=params['asset'],
                    quantity=params['quantity'],
                    memo=params.get('memo'),
                    memo_is_hex=params.get('memo_is_hex', False),
                    status=params['status']
                ))
            
            return sends
            
        except Exception as e:
            logger.error(f"Error fetching enhanced sends for {token_name}: {e}")
            raise

    def get_token_history(
        self, 
        token_name: str, 
        start_block: Optional[int] = None,
        event_types: Optional[List[str]] = None
    ) -> Dict[str, List[Any]]:
        """Get comprehensive token history including multiple event types.
        
        Args:
            token_name: Name of the token
            start_block: Optional starting block number
            event_types: Optional list of event types to include
                        (ISSUANCE, SEND, ENHANCED_SEND, DIVIDEND, etc.)
            
        Returns:
            Dictionary of event lists by type
        """
        if event_types is None:
            event_types = ['ISSUANCE', 'SEND', 'ENHANCED_SEND', 'DIVIDEND']
            
        history: Dict[str, List[Any]] = {}
        
        try:
            for event_type in event_types:
                if event_type == 'ISSUANCE':
                    history['issuances'] = self.get_issuances(token_name, start_block)
                elif event_type == 'SEND':
                    history['sends'] = self.get_sends(token_name, start_block)
                elif event_type == 'ENHANCED_SEND':
                    history['enhanced_sends'] = self.get_enhanced_sends(token_name, start_block)
                elif event_type == 'DIVIDEND':
                    history['dividends'] = self.get_dividends(token_name, start_block)
            
            return history
            
        except Exception as e:
            logger.error(f"Error fetching token history for {token_name}: {e}")
            raise

    def get_token_metrics(self, token_name: str) -> Dict[str, Union[int, float, str]]:
        """Get comprehensive token metrics.
        
        Args:
            token_name: Name of the token
            
        Returns:
            Dictionary containing various token metrics
        """
        try:
            # Get basic token info
            token = self.get_token_info(token_name)
            
            # Get holder information
            holders = self.get_token_holders(token_name)
            
            # Get dispensers
            dispensers = self.get_dispensers(token_name)
            active_dispensers = [d for d in dispensers if d.status == 'valid']
            
            # Calculate metrics
            metrics = {
                'total_supply': token.supply,
                'holder_count': len(holders),
                'active_dispenser_count': len(active_dispensers),
                'total_dispensed': sum(d.give_quantity - d.give_remaining for d in active_dispensers),
                'is_locked': token.locked,
                'is_divisible': token.divisible,
                'unique_holders': len(set(holders.keys())),
                'average_balance': token.supply / len(holders) if holders else 0,
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating token metrics for {token_name}: {e}")
            raise

    def get_orders(
        self,
        give_asset: Optional[str] = None,
        get_asset: Optional[str] = None,
        status_in: Optional[List[str]] = None,
        source: Optional[str] = None
    ) -> List[Order]:
        """Get orders matching specified criteria.
        
        Args:
            give_asset: Asset being sold
            get_asset: Asset being bought
            status_in: List of order statuses to include
            source: Address that created the order
            
        Returns:
            List of Order objects
        """
        try:
            params = {}
            if give_asset:
                params['give_asset'] = give_asset
            if get_asset:
                params['get_asset'] = get_asset
            if status_in:
                params['status_in'] = status_in
            if source:
                params['source'] = source
                
            data = self._make_request("v2/orders", params=params)
            
            orders = []
            for order in data:
                orders.append(Order(
                    tx_hash=order['tx_hash'],
                    block_index=order['block_index'],
                    source=order['source'],
                    give_asset=order['give_asset'],
                    give_quantity=order['give_quantity'],
                    give_remaining=order['give_remaining'],
                    get_asset=order['get_asset'],
                    get_quantity=order['get_quantity'],
                    get_remaining=order['get_remaining'],
                    expiration=order['expiration'],
                    expire_index=order['expire_index'],
                    fee_required=order['fee_required'],
                    fee_provided=order['fee_provided'],
                    fee_remaining=order['fee_remaining'],
                    status=order['status'],
                    block_time=order['block_time']
                ))
            
            return orders
            
        except Exception as e:
            logger.error(f"Error fetching orders: {e}")
            raise

    def get_order_matches(
        self,
        tx_hash: Optional[str] = None,
        status_in: Optional[List[str]] = None
    ) -> List[OrderMatch]:
        """Get order matches.
        
        Args:
            tx_hash: Optional transaction hash to filter by
            status_in: Optional list of statuses to include
            
        Returns:
            List of OrderMatch objects
        """
        try:
            params = {}
            if tx_hash:
                params['tx_hash'] = tx_hash
            if status_in:
                params['status_in'] = status_in
                
            data = self._make_request("v2/order_matches", params=params)
            
            matches = []
            for match in data:
                matches.append(OrderMatch(
                    id=match['id'],
                    tx0_hash=match['tx0_hash'],
                    tx0_address=match['tx0_address'],
                    tx0_block_index=match['tx0_block_index'],
                    tx0_expiration=match['tx0_expiration'],
                    tx1_hash=match['tx1_hash'],
                    tx1_address=match['tx1_address'],
                    tx1_block_index=match['tx1_block_index'],
                    tx1_expiration=match['tx1_expiration'],
                    forward_asset=match['forward_asset'],
                    forward_quantity=match['forward_quantity'],
                    backward_asset=match['backward_asset'],
                    backward_quantity=match['backward_quantity'],
                    status=match['status'],
                    block_time=match['block_time']
                ))
            
            return matches
            
        except Exception as e:
            logger.error(f"Error fetching order matches: {e}")
            raise

    def get_asset_transfers(
        self,
        asset: Optional[str] = None,
        source: Optional[str] = None,
        destination: Optional[str] = None,
        start_block: Optional[int] = None
    ) -> List[AssetTransfer]:
        """Get asset transfer events.
        
        Args:
            asset: Optional asset name to filter by
            source: Optional source address
            destination: Optional destination address
            start_block: Optional starting block number
            
        Returns:
            List of AssetTransfer objects
        """
        try:
            params = {}
            if asset:
                params['asset'] = asset
            if source:
                params['source'] = source
            if destination:
                params['destination'] = destination
            if start_block:
                params['start_block'] = start_block
                
            data = self._make_request("v2/events/ASSET_TRANSFER", params=params)
            
            transfers = []
            for event in data.get('result', []):
                params = event['params']
                transfers.append(AssetTransfer(
                    tx_hash=event['tx_hash'],
                    block_index=event['block_index'],
                    source=params['source'],
                    destination=params['destination'],
                    asset=params['asset'],
                    quantity=params['quantity'],
                    status=params['status'],
                    block_time=event['block_time']
                ))
            
            return transfers
            
        except Exception as e:
            logger.error(f"Error fetching asset transfers: {e}")
            raise

    def get_broadcasts(
        self,
        source: Optional[str] = None,
        start_block: Optional[int] = None,
        text_search: Optional[str] = None
    ) -> List[BroadcastEvent]:
        """Get broadcast events.
        
        Args:
            source: Optional source address
            start_block: Optional starting block number
            text_search: Optional text to search for in broadcast messages
            
        Returns:
            List of BroadcastEvent objects
        """
        try:
            params = {}
            if source:
                params['source'] = source
            if start_block:
                params['start_block'] = start_block
            if text_search:
                params['text_search'] = text_search
                
            data = self._make_request("v2/events/BROADCAST", params=params)
            
            broadcasts = []
            for event in data.get('result', []):
                params = event['params']
                broadcasts.append(BroadcastEvent(
                    tx_hash=event['tx_hash'],
                    block_index=event['block_index'],
                    source=params['source'],
                    timestamp=params['timestamp'],
                    value=params['value'],
                    fee_fraction_int=params['fee_fraction_int'],
                    text=params['text'],
                    status=params['status'],
                    block_time=event['block_time']
                ))
            
            return broadcasts
            
        except Exception as e:
            logger.error(f"Error fetching broadcasts: {e}")
            raise

    def get_btcpays(
        self,
        source: Optional[str] = None,
        destination: Optional[str] = None,
        order_match_id: Optional[str] = None
    ) -> List[BTCPay]:
        """Get BTC payment events.
        
        Args:
            source: Optional source address
            destination: Optional destination address
            order_match_id: Optional order match ID
            
        Returns:
            List of BTCPay objects
        """
        try:
            params = {}
            if source:
                params['source'] = source
            if destination:
                params['destination'] = destination
            if order_match_id:
                params['order_match_id'] = order_match_id
                
            data = self._make_request("v2/events/BTCPAY", params=params)
            
            btcpays = []
            for event in data.get('result', []):
                params = event['params']
                btcpays.append(BTCPay(
                    tx_hash=event['tx_hash'],
                    block_index=event['block_index'],
                    source=params['source'],
                    destination=params['destination'],
                    btc_amount=params['btc_amount'],
                    order_match_id=params['order_match_id'],
                    status=params['status'],
                    block_time=event['block_time']
                ))
            
            return btcpays
            
        except Exception as e:
            logger.error(f"Error fetching BTC payments: {e}")
            raise

    def get_market_history(
        self,
        asset1: str,
        asset2: str,
        start_block: Optional[int] = None,
        end_block: Optional[int] = None
    ) -> Dict[str, List[Any]]:
        """Get comprehensive market history between two assets.
        
        Args:
            asset1: First asset
            asset2: Second asset
            start_block: Optional starting block
            end_block: Optional ending block
            
        Returns:
            Dictionary containing orders, matches, and other market events
        """
        try:
            # Get all relevant orders
            orders = self.get_orders(
                give_asset=asset1,
                get_asset=asset2
            ) + self.get_orders(
                give_asset=asset2,
                get_asset=asset1
            )
            
            # Get order matches
            matches = []
            for order in orders:
                matches.extend(self.get_order_matches(tx_hash=order.tx_hash))
            
            # Get BTC payments
            btcpays = []
            for match in matches:
                btcpays.extend(self.get_btcpays(order_match_id=match.id))
            
            return {
                'orders': orders,
                'matches': matches,
                'btcpays': btcpays
            }
            
        except Exception as e:
            logger.error(
                f"Error fetching market history for {asset1}/{asset2}: {e}"
            )
            raise

def main():
    """Example usage of CounterpartyClient."""
    client = CounterpartyClient("http://localhost:4000/api")
    
    try:
        token_name = "MYASSETA"
        
        # Get market history
        market = client.get_market_history(token_name, "XCP")
        print(f"\nMarket History:")
        print(f"Orders: {len(market['orders'])}")
        print(f"Matches: {len(market['matches'])}")
        print(f"BTC Payments: {len(market['btcpays'])}")
        
        # Get recent orders
        orders = client.get_orders(give_asset=token_name)
        print(f"\nRecent Orders:")
        for order in orders[:3]:
            print(f"TX: {order.tx_hash}")
            print(f"Give: {order.give_quantity} {order.give_asset}")
            print(f"Get: {order.get_quantity} {order.get_asset}")
        
        # Get broadcasts
        broadcasts = client.get_broadcasts(text_search=token_name)
        print(f"\nBroadcasts:")
        for broadcast in broadcasts[:3]:
            print(f"TX: {broadcast.tx_hash}")
            print(f"Text: {broadcast.text}")
            
    except CounterpartyAPIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 