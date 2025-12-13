import os
import json
import tempfile
import logging
from googleads import ad_manager


def get_gam_client(network_code, service_account_path):
    """
    Create and return a Google Ad Manager client.
    Supports both local file and environment variable configurations.

    Args:
        network_code (str): The GAM network code (optional, can be in YAML).
        service_account_path (str): Path to the googleads.yaml configuration file.

    Returns:
        GoogleAdsClient: Configured GAM client.

    Raises:
        Exception: If client creation fails.
    """
    try:
        # Check if running on cloud (environment-based credentials)
        if os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON'):
            logging.info("Using environment variable for service account credentials")
            
            # Get service account JSON from environment
            service_account_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
            
            # Create temporary service account file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                temp_file.write(service_account_json)
                temp_service_account_path = temp_file.name
            
            # Create temporary googleads.yaml
            yaml_content = f"""ad_manager:
  application_name: GAM Child Publisher Monitor
  network_code: '{network_code}'
  path_to_private_key_file: {temp_service_account_path}
"""
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_yaml:
                temp_yaml.write(yaml_content)
                temp_yaml_path = temp_yaml.name
            
            # Load client from temporary YAML
            client = ad_manager.AdManagerClient.LoadFromStorage(temp_yaml_path)
            
            # Clean up temporary files
            try:
                os.unlink(temp_service_account_path)
                os.unlink(temp_yaml_path)
            except:
                pass
                
            logging.info(f"GAM client created from environment for network: {network_code}")
        else:
            # Use local file path (for development)
            logging.info("Using local file for service account credentials")
            client = ad_manager.AdManagerClient.LoadFromStorage(service_account_path)
            
            # Override network code if provided as parameter
            if network_code:
                client.network_code = network_code
            
            logging.info(f"GAM client created successfully for network code: {client.network_code}")
        
        return client
        
    except Exception as e:
        logging.error(f"Failed to create GAM client: {e}")
        raise

