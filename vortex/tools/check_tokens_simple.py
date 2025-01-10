#!/usr/bin/env python3
"""Simple command-line tool to check Bitcoin tokens and their multipliers."""

import sys
import json
import aiohttp
import asyncio
from decimal import Decimal
from typing import List, Dict, Set, Optional
from dataclasses import dataclass
from enum import Enum, auto

class BitcoinTokenType(Enum):
    """Types of Bitcoin-based tokens supported."""
    STAMPS = auto()
    SRC20 = auto()
    COUNTERPARTY = auto()  # Added Counterparty token type

@dataclass
class BitcoinTokenBalance:
    """Represents a token balance."""
    token_type: BitcoinTokenType
    token_id: str
    balance: Decimal
    creator: Optional[str] = None
    description: Optional[str] = None  # Added for Counterparty asset descriptions

# Special token multipliers
SPECIAL_SRC20_MULTIPLIERS: Dict[str, Decimal] = {
    "$BALD": Decimal("0.42"),
    "$VIVA": Decimal("0.21"),
    "KEVIN": Decimal("0.42"),
    "DEVIN": Decimal("0.33"),
    "WOOL": Decimal("0.33"),
    "LOG": Decimal("6.42"),
    "MANDY": Decimal("1.42"),
    "SPICE": Decimal("1.42"),
}

SPECIAL_STAMPS_MULTIPLIERS: Dict[str, Decimal] = {
    "A5433937813514022010": Decimal("0.69"),  # Special stamp multiplier
}

# Token category scores
@dataclass
class TokenCategoryScores:
    """Represents scores for different token categories."""
    pepe_count: int = 0
    boshi_count: int = 0
    dank_count: int = 0
    fake_count: int = 0

    def get_category_description(self) -> str:
        """Get a description of the holder based on their highest category count."""
        max_count = max(self.pepe_count, self.boshi_count, self.dank_count, self.fake_count)
        if max_count == 0:
            return "No special token categories found"
            
        categories = []
        if self.pepe_count == max_count:
            categories.append("PEPE")
        if self.boshi_count == max_count:
            categories.append("BOSHI")
        if self.dank_count == max_count:
            categories.append("DANK")
        if self.fake_count == max_count:
            categories.append("FAKE")
        
        # Fun status levels based on token count
        if max_count >= 1000:
            level = "GOD-TIER SUPREME OVERLORD"
        elif max_count >= 500:
            level = "LEGENDARY HOARDER"
        elif max_count >= 250:
            level = "OBSESSED WHALE"
        elif max_count >= 100:
            level = "CERTIFIED DEGEN"
        elif max_count >= 50:
            level = "MEGA CHAD"
        elif max_count >= 25:
            level = "BASED ACCUMULATOR"
        elif max_count >= 10:
            level = "MASTER"
        elif max_count >= 5:
            level = "EXPERT"
        else:
            level = "COLLECTOR"
            
        # Add funny emoji/symbol based on level
        symbol = {
            "GOD-TIER SUPREME OVERLORD": "👑",
            "LEGENDARY HOARDER": "🐉",
            "OBSESSED WHALE": "🐋",
            "CERTIFIED DEGEN": "🦍",
            "MEGA CHAD": "💪",
            "BASED ACCUMULATOR": "🗿",
            "MASTER": "⭐",
            "EXPERT": "✨",
            "COLLECTOR": "🌟"
        }[level]
        
        # Add funny suffix for extremely high counts
        if max_count >= 1000:
            suffix = f" (TOUCH GRASS: {max_count} tokens)"
        elif max_count >= 500:
            suffix = f" (SERIOUSLY?: {max_count} tokens)"
        elif max_count >= 250:
            suffix = f" (GET HELP: {max_count} tokens)"
        elif max_count >= 100:
            suffix = f" (MADLAD: {max_count} tokens)"
        else:
            suffix = f" ({max_count} tokens)"
            
        return f"{' & '.join(categories)} {level} {symbol}{suffix}"

# Creator multiplier for self-created tokens
SELF_CREATOR_MULTIPLIER = Decimal("0.33")

def calculate_token_multipliers(
    src20_tokens: Set[str],
    stamps: Set[str],
    counterparty_tokens: List[BitcoinTokenBalance],
    creator_token_count: int = 0
) -> Decimal:
    """Calculate total multiplier from owned tokens."""
    total_multiplier = Decimal("1.0")
    
    # Add SRC-20 multipliers
    for token in src20_tokens:
        if token in SPECIAL_SRC20_MULTIPLIERS:
            total_multiplier += SPECIAL_SRC20_MULTIPLIERS[token]
    
    # Add STAMPS multipliers
    for stamp in stamps:
        if stamp in SPECIAL_STAMPS_MULTIPLIERS:
            total_multiplier += SPECIAL_STAMPS_MULTIPLIERS[stamp]
    
    # Add creator token multipliers
    if creator_token_count > 0:
        total_multiplier += SELF_CREATOR_MULTIPLIER * Decimal(str(creator_token_count))
            
    return total_multiplier

def calculate_category_scores(counterparty_tokens: List[BitcoinTokenBalance]) -> TokenCategoryScores:
    """Calculate scores for different token categories."""
    scores = TokenCategoryScores()
    
    for token in counterparty_tokens:
        token_name = token.token_id.upper()
        if "PEPE" in token_name:
            scores.pepe_count += 1
        if "BOSHI" in token_name:
            scores.boshi_count += 1
        if "DANK" in token_name:
            scores.dank_count += 1
        if "FAKE" in token_name:
            scores.fake_count += 1
    
    return scores

async def get_counterparty_balances(address: str) -> List[BitcoinTokenBalance]:
    """Fetch Counterparty token balances from the API."""
    balances = []
    
    # Counterparty API endpoint
    endpoint = "http://api.counterparty.io:4000/api/"
    headers = {"content-type": "application/json"}
    
    # Get balances
    payload = {
        "method": "get_balances",
        "params": {
            "filters": [{"field": "address", "op": "==", "value": address}],
            "filterop": "AND"
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if "result" in data:
                        for balance in data["result"]:
                            # Get asset info for description
                            asset_info_payload = {
                                "method": "get_asset_info",
                                "params": {
                                    "assets": [balance["asset"]]
                                },
                                "jsonrpc": "2.0",
                                "id": 0
                            }
                            
                            description = None
                            try:
                                async with session.post(endpoint, json=asset_info_payload, headers=headers) as asset_response:
                                    if asset_response.status == 200:
                                        asset_data = await asset_response.json()
                                        if asset_data.get("result"):
                                            description = asset_data["result"][0].get("description", "")
                            except Exception as e:
                                print(f"Error fetching asset info: {str(e)}")
                            
                            balances.append(BitcoinTokenBalance(
                                token_type=BitcoinTokenType.COUNTERPARTY,
                                token_id=balance["asset"],
                                balance=Decimal(str(balance["quantity"])) / Decimal("100000000"),  # Convert satoshis to whole units
                                description=description
                            ))
    except Exception as e:
        print(f"Counterparty API error: {str(e)}")
    
    return balances

async def get_token_balances(address: str) -> List[BitcoinTokenBalance]:
    """Fetch token balances from the API."""
    balances = []
    
    # Get regular token balances
    endpoints = [
        f"https://stampchain.io/api/v2/balance/{address}",
        f"https://api.stamps.network/v2/balance/{address}",
        f"https://xchain.io/api/balances/{address}"
    ]
    
    async with aiohttp.ClientSession() as session:
        for endpoint in endpoints:
            try:
                print(f"\nTrying endpoint: {endpoint}")
                async with session.get(endpoint) as response:
                    print(f"Response status: {response.status}")
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Parse stampchain.io response
                        if "data" in data:
                            # Parse SRC-20 tokens
                            if "src20" in data["data"]:
                                for token in data["data"]["src20"]:
                                    creator = token.get("creator", "")
                                    print(f"DEBUG: SRC20 token {token['tick']} creator: {creator}")
                                    balances.append(BitcoinTokenBalance(
                                        token_type=BitcoinTokenType.SRC20,
                                        token_id=token["tick"].upper(),
                                        balance=Decimal(token["amt"]),
                                        creator=creator
                                    ))
                            
                            # Parse STAMPS
                            if "stamps" in data["data"]:
                                for token in data["data"]["stamps"]:
                                    creator = token.get("creator", "")
                                    print(f"DEBUG: STAMP {token['cpid']} creator: {creator}")
                                    balances.append(BitcoinTokenBalance(
                                        token_type=BitcoinTokenType.STAMPS,
                                        token_id=token["cpid"],
                                        balance=Decimal(str(token["balance"])),
                                        creator=creator
                                    ))
                        
                        # Successfully got data, break the loop
                        break
                    else:
                        print(f"Error response: {await response.text()}")
                        
            except Exception as e:
                print(f"Network error: {str(e)}")
                continue
    
    # Get Counterparty token balances
    counterparty_balances = await get_counterparty_balances(address)
    balances.extend(counterparty_balances)
    
    return balances

def normalize_ipfs_link(link: str) -> str:
    """Normalize IPFS links to a consistent format."""
    # Remove common prefixes
    link = link.strip().lower()
    prefixes = [
        "ipfs://",
        "ipfs:/",
        "ipfs://ipfs/",
        "https://ipfs.io/ipfs/",
        "https://gateway.ipfs.io/ipfs/",
        "https://cloudflare-ipfs.com/ipfs/",
        "https://ipfs.infura.io/ipfs/"
    ]
    
    for prefix in prefixes:
        if link.startswith(prefix):
            link = link[len(prefix):]
            break
    
    # Remove any trailing slashes
    link = link.rstrip("/")
    
    # If it's a CID, return with preferred gateway
    if link and "/" not in link:
        return f"https://ipfs.io/ipfs/{link}"
    
    return f"https://ipfs.io/ipfs/{link}"

def normalize_arweave_link(link: str) -> str:
    """Normalize Arweave links to a consistent format."""
    link = link.strip().lower()
    prefixes = [
        "ar://",
        "arweave://",
        "https://arweave.net/",
        "https://arweave.dev/"
    ]
    
    for prefix in prefixes:
        if link.startswith(prefix):
            link = link[len(prefix):]
            break
    
    return f"https://arweave.net/{link}"

def normalize_imgur_link(link: str) -> str:
    """Normalize Imgur links to a consistent format."""
    link = link.strip().lower()
    
    # Convert various Imgur formats to direct image links
    if "imgur.com/a/" in link or "imgur.com/gallery/" in link:
        # Album links - keep as is
        return link
    
    # Handle direct image links
    if not link.startswith(("http://", "https://")):
        link = f"https://imgur.com/{link}"
    
    # Convert to i.imgur.com direct links if possible
    if "imgur.com/" in link and not link.startswith("https://i.imgur.com/"):
        img_id = link.split("/")[-1].split(".")[0]
        return f"https://i.imgur.com/{img_id}.jpg"
    
    return link

def extract_json_metadata(text: str) -> Dict:
    """Extract and parse JSON metadata from text."""
    metadata = {}
    
    # Try to find JSON objects in the text
    try:
        # Look for content between curly braces
        start = text.find("{")
        if start != -1:
            # Find matching closing brace
            count = 1
            end = start + 1
            while count > 0 and end < len(text):
                if text[end] == "{":
                    count += 1
                elif text[end] == "}":
                    count -= 1
                end += 1
            
            if count == 0:
                json_str = text[start:end]
                try:
                    metadata = json.loads(json_str)
                except json.JSONDecodeError:
                    pass
    except Exception:
        pass
    
    return metadata

def parse_media_links(description: str) -> Dict[str, List[str]]:
    """Parse and categorize media links from description."""
    media = {
        "ipfs": [],
        "arweave": [],
        "imgur": [],
        "images": [],
        "videos": [],
        "audio": [],
        "other": []
    }
    
    if not description:
        return media
    
    # Extract JSON metadata first
    metadata = extract_json_metadata(description)
    
    # Process metadata if found
    if metadata:
        # Look for media links in common metadata fields
        fields_to_check = [
            "image", "animation_url", "animation", "video", "audio",
            "thumbnail", "preview", "media", "artwork", "assets",
            "external_url", "website", "links"
        ]
        
        for field in fields_to_check:
            if field in metadata:
                value = metadata[field]
                if isinstance(value, str):
                    description += f" {value}"
                elif isinstance(value, (list, dict)):
                    # Convert to string to check for links
                    description += f" {json.dumps(value)}"
    
    # Split into words and process each
    words = description.split()
    
    for word in words:
        word = word.strip("\"'(),[]{}").lower()
        
        # Skip if not a potential link
        if not any(x in word for x in ["://", ".com/", ".net/", ".io/", "ipfs/", "ar/"]):
            continue
        
        # Categorize by type
        if any(x in word for x in ["ipfs://", "ipfs/", "ipfs.io"]):
            media["ipfs"].append(normalize_ipfs_link(word))
        elif any(x in word for x in ["ar://", "arweave"]):
            media["arweave"].append(normalize_arweave_link(word))
        elif "imgur" in word:
            media["imgur"].append(normalize_imgur_link(word))
        elif any(x in word for x in [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"]):
            media["images"].append(word)
        elif any(x in word for x in [".mp4", ".webm", ".mov", ".avi"]):
            media["videos"].append(word)
        elif any(x in word for x in [".mp3", ".wav", ".ogg"]):
            media["audio"].append(word)
        elif "://" in word or any(x in word for x in [".com/", ".net/", ".io/"]):
            media["other"].append(word)
    
    # Remove duplicates while preserving order
    for key in media:
        media[key] = list(dict.fromkeys(media[key]))
    
    return media

async def get_detailed_asset_info(asset_id: str, session: aiohttp.ClientSession) -> Dict:
    """Get detailed information about a Counterparty asset."""
    endpoint = "http://api.counterparty.io:4000/api/"
    headers = {"content-type": "application/json"}
    
    # Get asset info
    asset_info_payload = {
        "method": "get_asset_info",
        "params": {
            "assets": [asset_id]
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    
    # Get issuances
    issuances_payload = {
        "method": "get_issuances",
        "params": {
            "filters": [{"field": "asset", "op": "==", "value": asset_id}],
            "filterop": "AND",
            "status": "valid"
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    
    # Get holders
    holders_payload = {
        "method": "get_holders",
        "params": {
            "assets": [asset_id]
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    
    asset_data = {
        "asset_id": asset_id,
        "description": "",
        "issuer": "",
        "supply": 0,
        "divisible": False,
        "locked": False,
        "issuances": [],
        "holders_count": 0,
        "social_links": set(),
        "media_links": {},
        "metadata": {},
        "creation_time": None
    }
    
    try:
        # Get basic asset info
        async with session.post(endpoint, json=asset_info_payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("result"):
                    info = data["result"][0]
                    description = info.get("description", "")
                    asset_data.update({
                        "description": description,
                        "issuer": info.get("issuer", ""),
                        "supply": info.get("supply", 0),
                        "divisible": info.get("divisible", False),
                        "locked": info.get("locked", False)
                    })
                    
                    # Parse media links and metadata
                    asset_data["media_links"] = parse_media_links(description)
                    asset_data["metadata"] = extract_json_metadata(description)
                    
                    # Extract social media links from description
                    desc = info.get("description", "").lower()
                    # Twitter/X links
                    twitter_handles = set()
                    for word in desc.split():
                        if word.startswith("@"):
                            twitter_handles.add(word[1:])
                        if "twitter.com/" in word:
                            handle = word.split("twitter.com/")[-1].split("/")[0].split("?")[0]
                            twitter_handles.add(handle)
                    
                    # Other social links
                    social_platforms = {
                        "discord.gg/": "Discord",
                        "t.me/": "Telegram",
                        "github.com/": "GitHub",
                        "medium.com/": "Medium",
                        "instagram.com/": "Instagram"
                    }
                    
                    for platform_url, platform_name in social_platforms.items():
                        if platform_url in desc:
                            links = [word for word in desc.split() if platform_url in word]
                            for link in links:
                                asset_data["social_links"].add((platform_name, link))
                    
                    # Add Twitter handles
                    for handle in twitter_handles:
                        asset_data["social_links"].add(("Twitter", f"@{handle}"))
        
        # Get issuance history
        async with session.post(endpoint, json=issuances_payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("result"):
                    asset_data["issuances"] = data["result"]
                    if data["result"]:
                        # Get creation time from first issuance
                        asset_data["creation_time"] = data["result"][0].get("block_time")
        
        # Get holders count
        async with session.post(endpoint, json=holders_payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("result"):
                    asset_data["holders_count"] = len(data["result"])
    
    except Exception as e:
        print(f"Error fetching detailed asset info for {asset_id}: {str(e)}")
    
    return asset_data

async def analyze_counterparty_portfolio(address: str) -> None:
    """Analyze all Counterparty assets owned or created by an address."""
    print("\n=== Detailed Counterparty Asset Analysis ===")
    
    async with aiohttp.ClientSession() as session:
        # Get balances to find owned tokens
        balances = await get_counterparty_balances(address)
        
        # Get issuances to find created tokens
        endpoint = "http://api.counterparty.io:4000/api/"
        headers = {"content-type": "application/json"}
        issuances_payload = {
            "method": "get_issuances",
            "params": {
                "filters": [{"field": "issuer", "op": "==", "value": address}],
                "filterop": "AND",
                "status": "valid"
            },
            "jsonrpc": "2.0",
            "id": 0
        }
        
        created_assets = set()
        try:
            async with session.post(endpoint, json=issuances_payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("result"):
                        for issuance in data["result"]:
                            created_assets.add(issuance["asset"])
        except Exception as e:
            print(f"Error fetching issuances: {str(e)}")
        
        # Combine owned and created assets
        all_assets = set(token.token_id for token in balances) | created_assets
        
        if not all_assets:
            print("No Counterparty assets found.")
            return
        
        # Get detailed info for each asset
        print("\nGathering detailed information...")
        assets_info = []
        for asset_id in all_assets:
            print(f"Processing {asset_id}...")
            asset_info = await get_detailed_asset_info(asset_id, session)
            assets_info.append(asset_info)
        
        # Display results
        print("\n=== Created Assets ===")
        created_count = 0
        for asset in assets_info:
            if asset["issuer"] == address:
                created_count += 1
                print(f"\n{created_count}. {asset['asset_id']}")
                print(f"   Supply: {asset['supply']:,}")
                print(f"   Holders: {asset['holders_count']:,}")
                print(f"   Issuances: {len(asset['issuances']):,}")
                
                if asset["creation_time"]:
                    from datetime import datetime
                    creation_date = datetime.fromtimestamp(asset["creation_time"]).strftime('%Y-%m-%d %H:%M:%S')
                    print(f"   Created: {creation_date}")
                
                if asset["description"]:
                    print(f"   Description: {asset['description']}")
                
                # Display media links
                if asset["media_links"]:
                    print("   Media Links:")
                    for media_type, links in asset["media_links"].items():
                        if links:
                            print(f"      {media_type.upper()}:")
                            for link in links:
                                print(f"         • {link}")
                
                # Display metadata if found
                if asset["metadata"]:
                    print("   Metadata:")
                    print(f"      {json.dumps(asset['metadata'], indent=6)}")
                
                if asset["social_links"]:
                    print("   Social Links:")
                    for platform, link in sorted(asset["social_links"]):
                        print(f"      • {platform}: {link}")
        
        print("\n=== Owned Assets ===")
        owned_count = 0
        for token in balances:
            owned_count += 1
            asset_info = next((a for a in assets_info if a["asset_id"] == token.token_id), None)
            if asset_info:
                print(f"\n{owned_count}. {token.token_id}")
                print(f"   Balance: {token.balance:,.8f}")
                print(f"   Total Supply: {asset_info['supply']:,}")
                print(f"   Holders: {asset_info['holders_count']:,}")
                if asset_info["creation_time"]:
                    from datetime import datetime
                    creation_date = datetime.fromtimestamp(asset_info["creation_time"]).strftime('%Y-%m-%d %H:%M:%S')
                    print(f"   Created: {creation_date}")
                if asset_info["description"]:
                    print(f"   Description: {asset_info['description']}")
                if asset_info["social_links"]:
                    print("   Social Links:")
                    for platform, link in sorted(asset_info["social_links"]):
                        print(f"      • {platform}: {link}")
        
        # Summary statistics
        print("\n=== Portfolio Summary ===")
        print(f"Total Created Assets: {created_count}")
        print(f"Total Owned Assets: {owned_count}")
        
        # Social media summary
        all_social_links = set()
        for asset in assets_info:
            all_social_links.update(asset["social_links"])
        
        if all_social_links:
            print("\n=== Social Media Summary ===")
            platforms = {}
            for platform, _ in all_social_links:
                platforms[platform] = platforms.get(platform, 0) + 1
            
            for platform, count in sorted(platforms.items()):
                print(f"{platform}: {count} links")
            
            print("\nAll Social Links:")
            for platform, link in sorted(all_social_links):
                print(f"• {platform}: {link}")

async def check_address(address: str, show_all: bool = False):
    """Check Bitcoin tokens for an address."""
    print(f"\nChecking address: {address}")
    print("Fetching balances...")
    
    balances = await get_token_balances(address)
    
    if not balances:
        print("\nNo tokens found for this address.")
        return
        
    # Group tokens
    src20_tokens = []
    stamps = []
    counterparty_tokens = []
    owned_src20_ticks = set()
    owned_stamps = set()
    created_tokens = set()
    
    for token in balances:
        if token.balance > 0:
            if token.creator == address:
                created_tokens.add(token.token_id)
                print(f"DEBUG: Found self-created token: {token.token_id}")
                
            if token.token_type == BitcoinTokenType.SRC20:
                src20_tokens.append(token)
                owned_src20_ticks.add(token.token_id)
            elif token.token_type == BitcoinTokenType.STAMPS:
                stamps.append(token)
                owned_stamps.add(token.token_id)
            elif token.token_type == BitcoinTokenType.COUNTERPARTY:
                counterparty_tokens.append(token)

    # Show special tokens first
    special_src20 = [t for t in src20_tokens if t.token_id in SPECIAL_SRC20_MULTIPLIERS]
    other_src20 = [t for t in src20_tokens if t.token_id not in SPECIAL_SRC20_MULTIPLIERS]
    
    special_stamps = [t for t in stamps if t.token_id in SPECIAL_STAMPS_MULTIPLIERS]
    other_stamps = [t for t in stamps if t.token_id not in SPECIAL_STAMPS_MULTIPLIERS]
    
    # Group Counterparty tokens by category
    pepe_tokens = [t for t in counterparty_tokens if "PEPE" in t.token_id.upper()]
    boshi_tokens = [t for t in counterparty_tokens if "BOSHI" in t.token_id.upper()]
    dank_tokens = [t for t in counterparty_tokens if "DANK" in t.token_id.upper()]
    fake_tokens = [t for t in counterparty_tokens if "FAKE" in t.token_id.upper()]
    other_counterparty = [t for t in counterparty_tokens 
                         if not any(keyword in t.token_id.upper() 
                                  for keyword in ["PEPE", "BOSHI", "DANK", "FAKE"])]
    
    # Display sections...
    if special_src20 or (show_all and other_src20):
        print("\n=== SRC-20 Tokens ===")
        
        if special_src20:
            print("\nSpecial Tokens (with multipliers):")
            for token in special_src20:
                multiplier = SPECIAL_SRC20_MULTIPLIERS[token.token_id]
                creator_text = " [Self Created]" if token.creator == address else ""
                print(f"★ {token.token_id}: {token.balance:,.2f} (+{multiplier}x multiplier){creator_text}")
        
        if show_all and other_src20:
            print("\nOther Tokens:")
            for token in other_src20:
                creator_text = " [Self Created]" if token.creator == address else ""
                print(f"  {token.token_id}: {token.balance:,.2f}{creator_text}")
    
    if special_stamps or (show_all and other_stamps):
        print("\n=== STAMPS ===")
        
        if special_stamps:
            print("\nSpecial Stamps (with multipliers):")
            for token in special_stamps:
                multiplier = SPECIAL_STAMPS_MULTIPLIERS[token.token_id]
                creator_text = " [Self Created]" if token.creator == address else ""
                print(f"★ {token.token_id}: {token.balance:,.2f} (+{multiplier}x multiplier){creator_text}")
        
        if show_all and other_stamps:
            print("\nOther Stamps:")
            for token in other_stamps:
                creator_text = " [Self Created]" if token.creator == address else ""
                print(f"  {token.token_id}: {token.balance:,.2f}{creator_text}")
    
    # Show Counterparty tokens by category
    if any([pepe_tokens, boshi_tokens, dank_tokens, fake_tokens]) or (show_all and other_counterparty):
        print("\n=== Counterparty Tokens ===")
        
        if pepe_tokens:
            print("\nPEPE Tokens:")
            for token in pepe_tokens:
                desc_text = f" - {token.description}" if token.description else ""
                print(f"★ {token.token_id}: {token.balance:,.8f}{desc_text}")
        
        if boshi_tokens:
            print("\nBOSHI Tokens:")
            for token in boshi_tokens:
                desc_text = f" - {token.description}" if token.description else ""
                print(f"★ {token.token_id}: {token.balance:,.8f}{desc_text}")
        
        if dank_tokens:
            print("\nDANK Tokens:")
            for token in dank_tokens:
                desc_text = f" - {token.description}" if token.description else ""
                print(f"★ {token.token_id}: {token.balance:,.8f}{desc_text}")
        
        if fake_tokens:
            print("\nFAKE Tokens:")
            for token in fake_tokens:
                desc_text = f" - {token.description}" if token.description else ""
                print(f"★ {token.token_id}: {token.balance:,.8f}{desc_text}")
        
        if show_all and other_counterparty:
            print("\nOther Tokens:")
            for token in other_counterparty:
                desc_text = f" - {token.description}" if token.description else ""
                print(f"  {token.token_id}: {token.balance:,.8f}{desc_text}")
    
    # Calculate and show category scores
    category_scores = calculate_category_scores(counterparty_tokens)
    
    print("\n=== Token Category Scores ===")
    if category_scores.pepe_count > 0:
        print(f"PEPE Score: {category_scores.pepe_count} different tokens")
    if category_scores.boshi_count > 0:
        print(f"BOSHI Score: {category_scores.boshi_count} different tokens")
    if category_scores.dank_count > 0:
        print(f"DANK Score: {category_scores.dank_count} different tokens")
    if category_scores.fake_count > 0:
        print(f"FAKE Score: {category_scores.fake_count} different tokens")
    
    print(f"\nHolder Status: {category_scores.get_category_description()}")
    
    # Calculate and show regular multiplier effect
    created_token_count = len(created_tokens)
    multiplier = calculate_token_multipliers(owned_src20_ticks, owned_stamps, [], created_token_count)
    base_rate = Decimal("0.001")
    effective_rate = base_rate * multiplier
    
    print("\n=== Base Multiplier Summary ===")
    active_multipliers = []
    
    # List active SRC-20 multipliers
    for token_id in owned_src20_ticks:
        if token_id in SPECIAL_SRC20_MULTIPLIERS:
            active_multipliers.append(f"{token_id} (+{SPECIAL_SRC20_MULTIPLIERS[token_id]}x)")
    
    # List active STAMPS multipliers
    for token_id in owned_stamps:
        if token_id in SPECIAL_STAMPS_MULTIPLIERS:
            active_multipliers.append(f"{token_id} (+{SPECIAL_STAMPS_MULTIPLIERS[token_id]}x)")
    
    if active_multipliers:
        print("\nActive Token Multipliers:")
        for m in active_multipliers:
            print(f"• {m}")
    
    if created_token_count > 0:
        creator_bonus = SELF_CREATOR_MULTIPLIER * Decimal(str(created_token_count))
        print(f"\nSelf-Created Token Bonus:")
        print(f"• {created_token_count} self-created tokens (+{creator_bonus}x)")
        print("Self-created tokens:")
        for token_id in sorted(created_tokens):
            print(f"  • {token_id}")
    
    print(f"\nTotal Multiplier Effect: {multiplier}x")
    print(f"Base Token Rate: {base_rate} per keystroke")
    print(f"Effective Token Rate: {effective_rate} per keystroke")
    
    # Show potential additional multipliers
    potential_src20 = set(SPECIAL_SRC20_MULTIPLIERS.keys()) - owned_src20_ticks
    potential_stamps = set(SPECIAL_STAMPS_MULTIPLIERS.keys()) - owned_stamps
    
    if potential_src20 or potential_stamps:
        print("\n=== Available Upgrades ===")
        print("Additional multipliers available from:")
        
        if potential_src20:
            print("\nSRC-20 Tokens:")
            for tick in sorted(potential_src20):
                print(f"• {tick} (+{SPECIAL_SRC20_MULTIPLIERS[tick]}x)")
        
        if potential_stamps:
            print("\nSTAMPS:")
            for stamp_id in sorted(potential_stamps):
                print(f"• {stamp_id} (+{SPECIAL_STAMPS_MULTIPLIERS[stamp_id]}x)")
                
        print("\nNote: Additional creator token bonuses are available (+0.0042069x per unique token)")

    # Add detailed Counterparty analysis at the end
    if counterparty_tokens or created_tokens:
        await analyze_counterparty_portfolio(address)

def main():
    if len(sys.argv) < 2:
        print("Usage: check_tokens_simple.py <bitcoin_address> [--all]")
        sys.exit(1)
    
    address = sys.argv[1]
    show_all = "--all" in sys.argv
    
    asyncio.run(check_address(address, show_all))

if __name__ == "__main__":
    main() 