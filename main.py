import logging
import os
from dotenv import load_dotenv
from services.ChildPubService import ChildPubService


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)


def main():
    """Main entry point for the GAM Child Publisher Monitor."""
    # Load environment variables
    load_dotenv()
    
    logging.info("Starting GAM Child Publisher Monitor")
    
    try:
        # Fetch and process child publisher account statuses
        result = ChildPubService.fetch_account_status()
        logging.info(f"Monitoring completed with result: {result}")
        
    except Exception as e:
        logging.critical(f"Critical error in main execution: {e}")
        raise


if __name__ == "__main__":
    main()
