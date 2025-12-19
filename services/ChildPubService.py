import logging
import os
import json
from datetime import datetime
from googleads.errors import GoogleAdsServerFault, GoogleAdsValueError
from utils.helpers import get_gam_client


class ChildPubService:
    @staticmethod
    def fetch_account_status(
        network_code=None,
        service_account=None,
        statuses=None,
        page_size=500,
    ):
        """
        Fetch all child publishers for any GAM network and save to JSON.

        Args:
            network_code (str): The network code for the GAM account.
            service_account (str): Path to the service account YAML.
            statuses (list): Not used, kept for backward compatibility.
            page_size (int): Number of records to fetch per request.

        Returns:
            dict: Result with network_code, total_count, fetched_at, child_publishers.
        """
        # Load from environment variables or config if not provided
        network_code = network_code or os.getenv('GAM_NETWORK_CODE')
        service_account = service_account or os.getenv('GAM_SERVICE_ACCOUNT')
        
        if not network_code or not service_account:
            logging.error("Network code or service account not provided")
            return "Missing configuration"

        offset = 0
        more_pages = True
        data = {"headers": [], "data": []}

        HEADER_MAP = {
            "id": "ID",
            "name": "Name",
            "readinessstatus": "Readiness Status",
            "approvalstatus": "Approval Status",
            "childnetworkcode": "Child Network Code",
            "email": "Email",
            "delegationtype": "Delegation Type",
            "invitationstatus": "Invitation Status",
            
        }

        try:
            client = get_gam_client(network_code, service_account)
            pql_service = client.GetService(
                "PublisherQueryLanguageService", version="v202411"
            )

            while more_pages:
                # Fetch ALL child publishers without status filter
                pql_query = f"""
                    SELECT Id, Name, ReadinessStatus, ApprovalStatus,
                    ChildNetworkCode, Email, InvitationStatus, DelegationType
                    FROM child_publisher where DelegationType = 'IN_CHILD'
                    ORDER BY Name ASC
                    LIMIT {page_size} OFFSET {offset}
                """

                try:
                    response = pql_service.select({"query": pql_query})

                    if not response or "columnTypes" not in response:
                        logging.error("Invalid response received from the server.")
                        return "Invalid response from server"

                    if offset == 0:
                        data["headers"] = [
                            HEADER_MAP.get(column["labelName"], column["labelName"])
                            for column in response["columnTypes"]
                        ]

                    if "rows" in response and len(response["rows"]) > 0:
                        data["data"].extend(response["rows"])
                        offset += page_size
                    else:
                        more_pages = False
                except (GoogleAdsServerFault, GoogleAdsValueError) as e:
                    logging.error(f"Failed with error: {e}")
                    raise

        except Exception as e:
            logging.critical(f"An unexpected error occurred: {e}")
            raise

        if data["data"]:
            # Convert to JSON format
            child_publishers = []
            for row in data["data"]:
                publisher = {}
                for i, column in enumerate(data["headers"]):
                    publisher[column] = row["values"][i]["value"]
                child_publishers.append(publisher)
            
            # Create result
            result = {
                "network_code": network_code,
                "total_count": len(child_publishers),
                "fetched_at": datetime.now().isoformat(),
                "child_publishers": child_publishers
            }
            
            # # Save to JSON with network code in filename
            # output_file = f"child_publishers_{network_code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            # with open(output_file, 'w', encoding='utf-8') as f:
            #     json.dump(result, f, indent=2, ensure_ascii=False)
            
            # logging.info(f"Found {len(child_publishers)} child publishers for network {network_code}")
            # logging.info(f"Results saved to {output_file}")
            return result
        else:
            logging.info(f"No child publishers found for network {network_code}")
            return {"network_code": network_code, "total_count": 0, "child_publishers": []}
        


    @staticmethod
    def fetch_manager_account_status(
        network_code=None,
        service_account=None,
        page_size=500,
    ):
        """
        Fetch manager account information for a GAM network.

        Args:
            network_code (str): The network code for the GAM account.
            service_account (str): Path to the service account YAML.
            page_size (int): Number of records to fetch per request.

        Returns:
            dict: Result with network_code, total_count, fetched_at, manager_accounts.
        """
        # Load from environment variables or config if not provided
        network_code = network_code or os.getenv('GAM_NETWORK_CODE')
        service_account = service_account or os.getenv('GAM_SERVICE_ACCOUNT')
        
        if not network_code or not service_account:
            logging.error("Network code or service account not provided")
            return "Missing configuration"

        offset = 0
        more_pages = True
        data = {"headers": [], "data": []}

        HEADER_MAP = {
            "id": "ID",
            "name": "Name",
            "readinessstatus": "Readiness Status",
            "approvalstatus": "Approval Status",
            "parentchildstatus": "Parent Child Status",
            "childnetworkcode": "Child Network Code",
            "email": "Email",
        }

        try:
            client = get_gam_client(network_code, service_account)
            pql_service = client.GetService(
                "PublisherQueryLanguageService", version="v202411"
            )

            while more_pages:
                # Fetch child publishers with MANAGED status
                pql_query = f"""
                    SELECT Id, Name, ReadinessStatus, ApprovalStatus,
                    ParentChildStatus, ChildNetworkCode, Email
                    FROM child_publisher
                    WHERE ParentChildStatus = 'MANAGED'
                    ORDER BY Name ASC
                """

                try:
                    response = pql_service.select({"query": pql_query})

                    if not response or "columnTypes" not in response:
                        logging.error("Invalid response received from the server.")
                        return "Invalid response from server"

                    if offset == 0:
                        data["headers"] = [
                            HEADER_MAP.get(column["labelName"], column["labelName"])
                            for column in response["columnTypes"]
                        ]

                    if "rows" in response and len(response["rows"]) > 0:
                        data["data"].extend(response["rows"])
                        offset += page_size
                    else:
                        more_pages = False
                except (GoogleAdsServerFault, GoogleAdsValueError) as e:
                    logging.error(f"Failed with error: {e}")
                    raise

        except Exception as e:
            logging.critical(f"An unexpected error occurred: {e}")
            raise

        if data["data"]:
            # Convert to JSON format
            manager_accounts = []
            for row in data["data"]:
                account = {}
                for i, column in enumerate(data["headers"]):
                    account[column] = row["values"][i]["value"]
                manager_accounts.append(account)
            
            # Create result
            result = {
                "network_code": network_code,
                "total_count": len(manager_accounts),
                "fetched_at": datetime.now().isoformat(),
                "manager_accounts": manager_accounts
            }
            
            logging.info(f"Found {len(manager_accounts)} managed accounts for network {network_code}")
            return result
        else:
            logging.info(f"No managed accounts found for network {network_code}")
            return {"network_code": network_code, "total_count": 0, "manager_accounts": []}
