from abc import ABC, abstractmethod
import csv
import json
import os

class CaseRecord:
    """
    Represents a single health data record.
    """
    def __init__(self, date, location, cases):
        self.date = date
        self.location = location
        self.cases = cases

    def __repr__(self):
        return f"Record(date='{self.date}', loc='{self.location}', cases={self.cases})"

class AbstractDataset(ABC):
    """
    Abstract Base Class defining the interface for all health datasets.
    """
    
    def __init__(self, source_path):
        self.source_path = source_path
        # COMPOSITION: The dataset HAS-A list of CaseRecord objects
        self._data = [] 
        
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Data file not found: {source_path}")

    @abstractmethod
    def load_data(self):
        """
        Abstract method to load data. Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def validate_format(self):
        """
        Abstract method to check if file format is valid.
        """
        pass

    def get_all_records(self):
        """Returns the list of records."""
        return self._data

class CSVDataset(AbstractDataset):
    """
    Specialized dataset handler for CSV files.
    """
    
    def __init__(self, source_path):
        super().__init__(source_path)

    def load_data(self):
        try:
            # Simplified open() without explicit encoding
            with open(self.source_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    record = CaseRecord(
                        row.get('date', 'Unknown'),
                        row.get('location', 'Unknown'),
                        int(row.get('cases', 0))
                    )
                    self._data.append(record)
            print(f"Successfully loaded {len(self._data)} records from CSV.")
        except ValueError as e:
            print(f"Error parsing CSV data: {e}")

    def validate_format(self):
        return self.source_path.lower().endswith('.csv')

class JSONDataset(AbstractDataset):
    """
    Specialized dataset handler for JSON files.
    """
    
    def __init__(self, source_path):
        super().__init__(source_path)

    def load_data(self):
        try:
            with open(self.source_path, 'r') as f:
                data = json.load(f)
                for entry in data:
                    record = CaseRecord(
                        entry.get('date'),
                        entry.get('location'),
                        int(entry.get('cases'))
                    )
                    self._data.append(record)
            print(f"Successfully loaded {len(self._data)} records from JSON.")
        except json.JSONDecodeError:
            print("Failed to decode JSON file.")

    def validate_format(self):
        return self.source_path.lower().endswith('.json')
