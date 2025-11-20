import unittest
import os
import csv
import json
from case_data_manager import CSVDataset, JSONDataset, CaseRecord, AbstractDataset

class TestCaseManager(unittest.TestCase):
    
    def setUp(self):
        """Create temporary dummy files for testing."""
        self.csv_file = "test_data.csv"
        self.json_file = "test_data.json"
        
        # Create a dummy CSV
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["date", "location", "cases"])
            writer.writerow(["2025-01-01", "Florida", "100"])
            writer.writerow(["2025-01-02", "Florida", "150"])

        # Create a dummy JSON
        with open(self.json_file, 'w') as f:
            data = [
                {"date": "2025-01-01", "location": "New York", "cases": 200},
                {"date": "2025-01-02", "location": "New York", "cases": 250}
            ]
            json.dump(data, f)

    def tearDown(self):
        """Clean up dummy files after tests."""
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)
        if os.path.exists(self.json_file):
            os.remove(self.json_file)

    def test_inheritance_and_abc(self):
        """Test that AbstractDataset cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            _ = AbstractDataset("some_path")

    def test_polymorphism_load_data(self):
        """Test that load_data behaves correctly for different types."""
        # Test CSV Polymorphism
        csv_ds = CSVDataset(self.csv_file)
        csv_ds.load_data()
        self.assertEqual(len(csv_ds.get_all_records()), 2)
        self.assertEqual(csv_ds.get_all_records()[0].location, "Florida")

        # Test JSON Polymorphism
        json_ds = JSONDataset(self.json_file)
        json_ds.load_data()
        self.assertEqual(len(json_ds.get_all_records()), 2)
        self.assertEqual(json_ds.get_all_records()[0].location, "New York")

    def test_composition(self):
        """Test that Dataset is composed of CaseRecord objects."""
        csv_ds = CSVDataset(self.csv_file)
        csv_ds.load_data()
        record = csv_ds.get_all_records()[0]
        
        # Check that the inner object is actually a CaseRecord instance
        self.assertIsInstance(record, CaseRecord)
        self.assertEqual(record.cases, 100)

if __name__ == '__main__':
    unittest.main()
