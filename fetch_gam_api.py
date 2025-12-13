#!/usr/bin/env python
"""
API wrapper for fetching GAM child publishers data
Called by PHP API with network code as argument
"""
import sys
import logging
import os
from services.ChildPubService import ChildPubService
from dotenv import load_dotenv

# Configure minimal logging for API use
logging.basicConfig(
    level=logging.WARNING,
    format='%(message)s'
)

# Load environment variables
load_dotenv()

def main():
    if len(sys.argv) < 2:
        print("Error: Network code required")
        sys.exit(1)
    
    network_code = sys.argv[1]
    
    try:
        # Fetch data
        result = ChildPubService.fetch_account_status(network_code=network_code)
        
        if isinstance(result, dict):
            print(f"Success: Fetched {result.get('total_count', 0)} publishers for network {network_code}")
            sys.exit(0)
        else:
            print(f"Error: {result}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
