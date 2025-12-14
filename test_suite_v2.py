import unittest
import os
import pickle
from case_data_manager import CSVDataset, CaseRecord
from analysis_modules import TrendAnalyzer
from pipeline_manager import PipelineManager
from alert_report import AlertReport 

class TestCapstoneIntegration(unittest.TestCase):

    def setUp(self):
        """Create dummy data for testing."""
        self.test_csv = "test_capstone.csv"
        self.state_file = "test_state.pkl"
        
        with open(self.test_csv, "w") as f:
            f.write("date,location,cases\n")
            f.write("2025-01-01,TestCity,100\n")
            f.write("2025-01-02,TestCity,150\n")

    def tearDown(self):
        """Cleanup files."""
        for f in [self.test_csv, self.state_file]:
            if os.path.exists(f):
                os.remove(f)

    # --- UNIT TESTS (Individual Components) ---
    def test_record_validation(self):
        """Unit: Ensure CaseRecord stores data correctly."""
        r = CaseRecord("2025-01-01", "City", 50)
        self.assertEqual(r.cases, 50)
        self.assertEqual(r.location, "City")

    # --- INTEGRATION TESTS (Components working together) ---
    def test_manager_adds_dataset(self):
        """Integration: Manager correctly ingests a CSVDataset."""
        manager = PipelineManager()
        ds = CSVDataset(self.test_csv)
        manager.add_dataset(ds)
        # Assuming manager has a list of datasets
        self.assertEqual(len(manager._datasets), 1)

    def test_manager_runs_analysis(self):
        """Integration: Manager feeds Data into Analyzer."""
        manager = PipelineManager()
        manager.add_dataset(CSVDataset(self.test_csv))
        manager.register_analyzer(TrendAnalyzer())
        
        results = manager.run_full_analysis()
        # Verify TrendAnalyzer produced output
        self.assertIn("TrendAnalyzer", results)
        self.assertEqual(results["TrendAnalyzer"]["total_cases"], 250)

    # --- SYSTEM TESTS (End-to-End Workflow + Persistence) ---
    def test_persistence_workflow(self):
        """System: Load Data -> Save State -> Reload State -> Verify Data."""
        # 1. Start Session A
        manager_a = PipelineManager()
        manager_a.add_dataset(CSVDataset(self.test_csv))
        manager_a.save_state(self.state_file)
        
        # 2. End Session (Simulated)
        del manager_a
        
        # 3. Start Session B (Load State)
        manager_b = PipelineManager.load_state(self.state_file)
        
        # 4. Verify data persisted
        self.assertIsNotNone(manager_b)
        self.assertEqual(len(manager_b._datasets), 1)
        records = manager_b._datasets[0].get_all_records()
        self.assertEqual(records[0].cases, 100)

if __name__ == "__main__":
    unittest.main()
