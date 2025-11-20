# -------------------------------
#       Data Loader Class
#  Loads CSV, JSON, or XML files
# -------------------------------

import csv
import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Any

class DataLoader:
    """Load raw COVID case data from files."""

    def __init__(self, sources: List[str]):
        """Initialize with a list of file paths."""
        if not isinstance(sources, list) or not all(isinstance(s, str) for s in sources):
            raise TypeError("Sources must be a list of file paths.")
        self._sources = sources
        self._data: List[Dict[str, Any]] = []

    @property
    def data(self) -> List[Dict[str, Any]]:
        """Return loaded data."""
        return self._data

    def load_data(self) -> None:
        """Load all files into a combined dataset."""
        combined = []
        for path in self._sources:
            if path.endswith(".csv"):
                combined.extend(self._load_csv(path))
            elif path.endswith(".json"):
                combined.extend(self._load_json(path))
            elif path.endswith(".xml"):
                combined.extend(self._load_xml(path))
            else:
                raise ValueError(f"Unsupported file type for {path}")
        self._data = combined

    # ------------------- Private Loading Methods -------------------
    def _load_csv(self, path: str) -> List[Dict[str, Any]]:
        with open(path, newline='') as f:
            reader = csv.DictReader(f)
            return [dict(row) for row in reader]

    def _load_json(self, path: str) -> List[Dict[str, Any]]:
        with open(path) as f:
            return json.load(f)

    def _load_xml(self, path: str) -> List[Dict[str, Any]]:
        tree = ET.parse(path)
        root = tree.getroot()
        records = []
        for child in root:
            record = {elem.tag: elem.text for elem in child}
            records.append(record)
        return records

    def __str__(self):
        return f"DataLoader with {len(self._sources)} sources, {len(self._data)} records loaded"

    def __repr__(self):
        return f"DataLoader(sources={self._sources})"

