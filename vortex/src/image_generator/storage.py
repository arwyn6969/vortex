"""
IPFS storage module using Pinata for decentralized image storage.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any

from pinatapy import PinataPy
from dotenv import load_dotenv

class IPFSStorage:
    """IPFS storage handler using Pinata."""
    
    def __init__(self):
        load_dotenv()
        
        api_key = os.getenv("PINATA_API_KEY")
        api_secret = os.getenv("PINATA_API_SECRET")
        
        if not api_key or not api_secret:
            raise ValueError(
                "Pinata API credentials not found. Please set PINATA_API_KEY and "
                "PINATA_API_SECRET environment variables."
            )
        
        self.pinata = PinataPy(api_key, api_secret)
    
    def upload_file(self, file_path: Path, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Upload a file to IPFS using Pinata.
        
        Args:
            file_path: Path to the file to upload
            metadata: Optional metadata to attach to the file
        
        Returns:
            str: IPFS hash of the uploaded file
        
        Raises:
            FileNotFoundError: If the file doesn't exist
            RuntimeError: If the upload fails
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            result = self.pinata.pin_file_to_ipfs(str(file_path), metadata or {})
            return result["IpfsHash"]
        except Exception as e:
            raise RuntimeError(f"Failed to upload file to IPFS: {e}") from e
    
    def get_file_url(self, ipfs_hash: str) -> str:
        """Get the public URL for an IPFS hash."""
        return f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}" 