import logging
from googleads import ad_manager


def get_gam_client(network_code, service_account_path):
    """
    Create and return a Google Ad Manager client.

    Args:
        network_code (str): The GAM network code (optional, can be in YAML).
        service_account_path (str): Path to the googleads.yaml configuration file.

    Returns:
        GoogleAdsClient: Configured GAM client.

    Raises:
        Exception: If client creation fails.
    """
    try:
        # Create client using the YAML configuration file
        client = ad_manager.AdManagerClient.LoadFromStorage(service_account_path)
        
        # Override network code if provided as parameter
        if network_code:
            client.network_code = network_code
        
        logging.info(f"GAM client created successfully for network code: {client.network_code}")
        return client
    except Exception as e:
        logging.error(f"Failed to create GAM client: {e}")
        raise

