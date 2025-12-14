import unittest
import os
import csv
import json
import xml.etree.ElementTree as ET
from typing import List

# Import Everyone's Modules
from case_data_manager import CaseRecord, CSVDataset, JSONDataset
from xml_dataset import XMLDataset                  # Kindness
from analysis_modules import TrendAnalyzer          # Kindness
from forecasting_analyzer import ForecastingAnalyzer # Yonael
from pipeline_manager import PipelineManager        # Yonael
from alert_report import AlertReport                # Chioma

class TestHealthDataPipeline(unittest.TestCase):
    
    def setUp(self):
        """
        Create temporary dummy files (CSV, JSON, XML) before every test.
        This ensures we test with fresh data every time.
        """
        self.csv_file = "test_data.csv"
        self.json_file = "test_data.json"
        self.xml_file = "test_data.xml"
        
        # 1. Create Dummy CSV
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["date", "location", "cases"])
            writer.writerow(["2025-01-01", "Florida", "100"])
            writer.writerow(["2025-01-02", "Florida", "150"])

        # 2. Create Dummy JSON
        with open(self.json_file, 'w') as f:
            data = [
                {"date": "2025-02-01", "location": "New York", "cases": 200},
                {"date": "2025-02-02", "location": "New York", "cases": 250}
            ]
            json.dump(data, f)

        # 3. Create Dummy XML (Kindness's Format)
        root = ET.Element("data")
        record1 = ET.SubElement(root, "record")
        ET.SubElement(record1, "date").text = "2025-03-01"
        ET.SubElement(record1, "location").text = "Texas"
        ET.SubElement(record1, "cases").text = "300"
        
        record2 = ET.SubElement(root, "record")
        ET.SubElement(record2, "date").text = "2025-03-02"
        ET.SubElement(record2, "location").text = "Texas"
        ET.SubElement(record2, "cases").text = "350"
        
        tree = ET.ElementTree(root)
        tree.write(self.xml_file)

    def tearDown(self):
        """Remove dummy files after tests finish."""
        for f in [self.csv_file, self.json_file, self.xml_file]:
            if os.path.exists(f):
                os.remove(f)

    # ----------------------------------------------------------------
    # JULIAN'S TESTS (Base Architecture)
    # ----------------------------------------------------------------
    def test_csv_loading(self):
        """Unit Test: Verify CSVDataset loads correctly."""
        ds = CSVDataset(self.csv_file)
        ds.load_data()
        records = ds.get_all_records()
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].location, "Florida")
        self.assertEqual(records[0].cases, 100)

    def test_json_loading(self):
        """Unit Test: Verify JSONDataset loads correctly."""
        ds = JSONDataset(self.json_file)
        ds.load_data()
        records = ds.get_all_records()
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].location, "New York")

    # ----------------------------------------------------------------
    # KINDNESS'S TESTS (XML & Trends)
    # ----------------------------------------------------------------
    def test_xml_loading(self):
        """Unit Test: Verify XMLDataset loads correctly."""
        ds = XMLDataset(self.xml_file)
        ds.load_data()
        records = ds.get_all_records()
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].location, "Texas")
        self.assertEqual(records[0].cases, 300)

    def test_trend_analyzer(self):
        """Unit Test: Verify TrendAnalyzer calculates stats correctly."""
        # Create dummy records in memory
        records = [
            CaseRecord("2025-01-01", "TestLoc", 10),
            CaseRecord("2025-01-02", "TestLoc", 20),
            CaseRecord("2025-01-03", "TestLoc", 30)
        ]
        analyzer = TrendAnalyzer()
        results = analyzer.analyze(records)
        
        self.assertEqual(results['total_cases'], 60)
        self.assertEqual(results['average_daily'], 20.0)
        self.assertEqual(len(results['moving_average']), 3)

    # ----------------------------------------------------------------
    # YONAEL'S TESTS (Forecasting & Pipeline Manager)
    # ----------------------------------------------------------------
    def test_forecasting_analyzer(self):
        """Unit Test: Verify ForecastingAnalyzer predicts future values."""
        records = [
            CaseRecord("2025-01-01", "TestLoc", 10),
            CaseRecord("2025-01-02", "TestLoc", 20), # +10 increase
            CaseRecord("2025-01-03", "TestLoc", 30)  # +10 increase
        ]
        # It should predict +10 for next days: 40, 50, 60...
        analyzer = ForecastingAnalyzer(days_ahead=3)
        results = analyzer.analyze(records)
        
        predictions = results['future_predictions']
        self.assertEqual(len(predictions), 3)
        self.assertEqual(predictions[0], 40) 
        self.assertEqual(predictions[1], 50)

    def test_pipeline_integration(self):
        """
        INTEGRATION TEST: Verify PipelineManager connects Data -> Analysis.
        This tests the whole flow (Julian -> Yonael -> Kindness).
        """
        manager = PipelineManager()
        
        # 1. Add Data (Julian's Module)
        csv_ds = CSVDataset(self.csv_file)
        manager.add_dataset(csv_ds)
        
        # 2. Add Analyzer (Kindness's Module)
        trend_tool = TrendAnalyzer()
        manager.register_analyzer(trend_tool)
        
        # 3. Run Pipeline
        results = manager.run_full_analysis()
        
        # 4. Verify output
        self.assertIn("TrendAnalyzer", results)
        self.assertEqual(results["TrendAnalyzer"]["total_cases"], 250) # 100 + 150

    # ----------------------------------------------------------------
    # CHIOMA'S TESTS (Reporting)
    # ----------------------------------------------------------------
    def test_alert_generation(self):
        """Unit Test: Verify AlertReport flags high cases."""
        records = [
            CaseRecord("2025-01-01", "SafeCity", 10),
            CaseRecord("2025-01-02", "DangerCity", 100)
        ]
        # Threshold is 50, so DangerCity should trigger alert
        report = AlertReport(records, threshold=50)
        alerts = report.generate_alerts()
        
        self.assertEqual(len(alerts), 1)
        self.assertIn("DangerCity", alerts[0])
        self.assertIn("100 cases", alerts[0])

    def test_alert_report_integration(self):
        """
        SYSTEM TEST: Verify Data -> Report flow.
        """
        # Load data using Julian's loader
        ds = CSVDataset(self.csv_file) # Contains 100, 150
        ds.load_data()
        
        # Pass to Chioma's reporter with low threshold
        report = AlertReport(ds.get_all_records(), threshold=120) 
        alerts = report.generate_alerts()
        
        # Only the 150 case should trigger
        self.assertEqual(len(alerts), 1)
        self.assertIn("150 cases", alerts[0])

if __name__ == '__main__':
    unittest.main()
