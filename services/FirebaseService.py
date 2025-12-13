import logging
import os
import firebase_admin
from firebase_admin import credentials, db


class FirebaseService:
    _initialized = False

    @staticmethod
    def initialize():
        """Initialize Firebase Admin SDK if not already initialized."""
        if not FirebaseService._initialized:
            cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
            database_url = os.getenv('FIREBASE_DATABASE_URL')

            if not cred_path or not database_url:
                logging.error("Firebase credentials or database URL not configured")
                raise ValueError("Firebase configuration missing")

            if not os.path.exists(cred_path):
                logging.error(f"Firebase credentials file not found: {cred_path}")
                raise FileNotFoundError(f"Firebase credentials file not found: {cred_path}")

            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': database_url
            })
            FirebaseService._initialized = True
            logging.info("Firebase initialized successfully")

    @staticmethod
    def get_closed_account_config(key):
        """
        Retrieve closed account configuration from Firebase.

        Args:
            key (str): The key to retrieve from Firebase.

        Returns:
            dict: The configuration data, or None if not found.
        """
        try:
            FirebaseService.initialize()
            ref = db.reference(f'config/{key}')
            data = ref.get()
            return data
        except Exception as e:
            logging.error(f"Failed to get Firebase config for key '{key}': {e}")
            return None

    @staticmethod
    def set_closed_account_config(data, key):
        """
        Store closed account configuration to Firebase.

        Args:
            data (dict): The data to store.
            key (str): The key under which to store the data.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            FirebaseService.initialize()
            ref = db.reference(f'config/{key}')
            ref.set(data)
            logging.info(f"Firebase config updated for key '{key}'")
            return True
        except Exception as e:
            logging.error(f"Failed to set Firebase config for key '{key}': {e}")
            return False
