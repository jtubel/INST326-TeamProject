from src.cleaning import fill_missing_values
from src.transformations import count_unique_locations
from src.alert_report import AlertReport

class PipelineManager:
    def __init__(self, data):
        self.data = data
        self.alert_report = None
        self.results = {}

    def run(self, config):
        if config.get("clean"):
            self.data = fill_missing_values(self.data)

        if config.get("analyze"):
            self.alert_report = AlertReport(self.data)
            self.results["alerts"] = self.alert_report.generate_alerts()

        if config.get("summary"):
            self.results["locations"] = count_unique_locations(self.data)

        return self.results
      
      import json
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def save_state(filename, state):
    with open(DATA_DIR / filename, "w") as f:
        json.dump(state, f)

def load_state(filename):

from src.persistence import save_state, load_state

def save(self, filename):
    save_state(filename, self.results)

def load(self, filename):
    self.results = load_state(filename)
    with open(DATA_DIR / filename) as f:
        return json.load(f)
def save_state(self, filename: str = "pipeline_state.pkl"):
        """
        PROJ 4: DATA PERSISTENCE
        Saves the current state of the pipeline (loaded datasets and analyzers) to a file.
        """
        try:
            with open(filename, 'wb') as f:
                pickle.dump(self, f)
            print(f"System state successfully saved to {filename}")
        except IOError as e:
            print(f"Error saving system state: {e}")

    @staticmethod
    def load_state(filename: str = "pipeline_state.pkl"):
        """
        PROJ 4: DATA PERSISTENCE
        Loads a previously saved pipeline state from a file.
        """
        if not os.path.exists(filename):
            print(f"No saved state found at {filename}")
            return None
        
        try:
            with open(filename, 'rb') as f:
                manager = pickle.load(f)
            print(f"System state loaded from {filename}")
            return manager
        except (IOError, pickle.PickleError) as e:
            print(f"Error loading system state: {e}")
            return None
import unittest
from src.pipeline_manager import PipelineManager

class TestIntegration(unittest.TestCase):
    def test_pipeline_runs(self):
        data = [{"cases": 100, "location": "MD"}]
        pipeline = PipelineManager(data)

        results = pipeline.run({
            "clean": True,
            "analyze": True,
            "summary": True
        })

        self.assertIn("alerts", results)

import unittest
from src.pipeline_manager import PipelineManager

class TestSystem(unittest.TestCase):
    def test_save_and_load(self):
        data = [{"cases": 200, "location": "NY"}]
        pipeline = PipelineManager(data)
        pipeline.run({"analyze": True})

        pipeline.save("state.json")
        pipeline.load("state.json")

        self.assertTrue(pipeline.results)
