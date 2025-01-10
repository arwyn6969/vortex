"""
CLI script to run the image generator application.
"""

import argparse
import logging
from pathlib import Path

from .app import create_app
from .model import StyleGANModel
from .storage import IPFSStorage

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Image Generator AI Application")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to run the server on"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port to run the server on"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run in debug mode"
    )
    
    args = parser.parse_args()
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Create required directories
        Path("uploads").mkdir(exist_ok=True)
        Path("generated").mkdir(exist_ok=True)
        
        # Initialize components
        model = StyleGANModel()
        storage = IPFSStorage()
        
        # Create and run the application
        app = create_app(model, storage)
        logger.info(f"Starting server on {args.host}:{args.port}")
        app.run(host=args.host, port=args.port, debug=args.debug)
    
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise

if __name__ == "__main__":
    main() 