import pickle
import os
from typing import Dict, Any

class PipelineManager:
    """
    Central controller for the Health Data Pipeline.
    Manages Datasets, Analyzers, and Data Persistence.
    """

    def __init__(self):
        """Initialize empty registries."""
        self._datasets = [] 
        self._analyzers = []

    def add_dataset(self, dataset):
        """Register a new dataset (CSV, JSON, or XML)."""
        if not hasattr(dataset, 'load_data'):
            raise TypeError("Invalid dataset: Must implement load_data interface.")
        
        print(f"Manager: Loading data from '{dataset.source_path}'...")
        dataset.load_data()
        self._datasets.append(dataset)

    def register_analyzer(self, analyzer):
        """Add an analysis tool to the pipeline."""
        if not hasattr(analyzer, 'analyze'):
            raise TypeError("Invalid tool: Must implement analyze interface.")
        self._analyzers.append(analyzer)

    def run_full_analysis(self) -> Dict[str, Any]:
        """Run all analyzers on all loaded data."""
        all_records = []
        for ds in self._datasets:
            all_records.extend(ds.get_all_records())

        if not all_records:
            return {"error": "No data loaded"}

        results = {}
        for analyzer in self._analyzers:
            tool_name = analyzer.__class__.__name__
            print(f"Running {tool_name}...")
            results[tool_name] = analyzer.analyze(all_records)
            
        return results

    # --- PROJECT 4: DATA PERSISTENCE ---
    def save_state(self, filename: str = "pipeline_state.pkl"):
        """Save the entire pipeline (datasets + analyzers) to a file."""
        try:
            with open(filename, 'wb') as f:
                pickle.dump(self, f)
            print(f"State saved to {filename}")
        except Exception as e:
            print(f"Error saving state: {e}")

    @staticmethod
    def load_state(filename: str = "pipeline_state.pkl"):
        """Load a pipeline from a file."""
        if not os.path.exists(filename):
            print("Save file not found.")
            return None
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading state: {e}")
            return None
