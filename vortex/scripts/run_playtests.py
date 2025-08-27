#!/usr/bin/env python3
"""Script to run automated playtests and generate reports."""

import asyncio
import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

from ..tests.automation.playtest_harness import PlaytestHarness

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f'playtest_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)
logger = logging.getLogger(__name__)

async def main():
    """Run playtests and generate reports."""
    parser = argparse.ArgumentParser(description="Run automated playtests for Vortex")
    parser.add_argument(
        "--report-dir",
        type=str,
        default="playtest_reports",
        help="Directory to store playtest reports"
    )
    parser.add_argument(
        "--scenarios",
        type=str,
        nargs="*",
        help="Specific scenarios to run (default: all scenarios)"
    )
    args = parser.parse_args()
    
    # Create report directory
    report_dir = Path(args.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Initialize playtest harness
        logger.info("Initializing playtest harness...")
        harness = PlaytestHarness()
        
        # Get scenarios
        all_scenarios = harness.create_standard_scenarios()
        if args.scenarios:
            scenarios = [
                s for s in all_scenarios
                if s.name in args.scenarios
            ]
            if not scenarios:
                logger.error(f"No matching scenarios found. Available scenarios: {[s.name for s in all_scenarios]}")
                return 1
        else:
            scenarios = all_scenarios
        
        # Run scenarios
        logger.info(f"Running {len(scenarios)} scenarios...")
        results = await harness.run_all_scenarios()
        
        # Generate report
        report = harness.generate_report()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = report_dir / f"playtest_report_{timestamp}.md"
        
        with open(report_path, "w") as f:
            f.write(report)
        
        logger.info(f"Report generated: {report_path}")
        
        # Log summary
        successful = sum(1 for r in results if r.success)
        logger.info(f"Playtesting complete: {successful}/{len(results)} scenarios passed")
        
        if len(results) > successful:
            logger.warning("Some scenarios failed. Check the report for details.")
            return 1
        
        return 0
        
    except Exception as e:
        logger.error(f"Error during playtesting: {str(e)}", exc_info=True)
        return 1
    
    finally:
        # Cleanup
        try:
            await harness.cleanup()
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}", exc_info=True)

if __name__ == "__main__":
    sys.exit(asyncio.run(main())) 