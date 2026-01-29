import csv
import os
import logging
import random
import config
import sys
import string

logger = logging.getLogger(__name__)

class DataLoader:
    _data = []

    @classmethod
    def load_data(cls):
        """Loads valid test data from CSV."""
        if cls._data:
            return cls._data
            
        file_path = config.DATA_FILE_PATH
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Normalize headers
                        phone = row.get('telephoneNumber') or row.get('phoneNumber')
                        scenario = row.get('scenario', 'default')
                        
                        if phone:
                            cls._data.append({
                                "telephoneNumber": phone.strip(),
                                "scenario": scenario.strip().lower()
                            })
                logger.info(f"Loaded {len(cls._data)} records from {file_path}")
            except Exception as e:
                logger.error(f"Failed to load data file: {e}")
                sys.exit(1)
        else:
            logger.warning(f"Data file {file_path} not found. Using fallback mock data.")
            cls._data = [
                {"telephoneNumber": "07700900001", "scenario": "future"},
                {"telephoneNumber": "07700900002", "scenario": "present"},
                {"telephoneNumber": "07700900003", "scenario": "past"},
            ]
            
        return cls._data

    @classmethod
    def get_valid_record(cls):
        """Returns a random record where scenario is NOT 'invalid'."""
        if not cls._data:
            cls.load_data()
        
        valid_records = [r for r in cls._data if r['scenario'] != 'invalid']
        if valid_records:
            return random.choice(valid_records)
        return random.choice(cls._data) # Fallback if no valid records exist

    @classmethod
    def generate_invalid_payload(cls):
        """Generates a random invalid payload for negative testing."""
        failure_type = random.choice(["plus44", "non_numeric", "too_short", "empty"])
        
        if failure_type == "plus44":
            return {"telephoneNumber": "+447700900001"}, "started_with_plus44"
        elif failure_type == "non_numeric":
            return {"telephoneNumber": "077abc90001"}, "non_numeric"
        elif failure_type == "too_short":
            return {"telephoneNumber": "077"}, "too_short"
        elif failure_type == "empty":
            return {"telephoneNumber": ""}, "empty"
        
        return {"telephoneNumber": "invalid"}, "unknown"
