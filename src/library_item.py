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


# -------------------------------
#       Trend Analyzer Class
#  Analyze and summarize cases
# -------------------------------

from statistics import mean

class TrendAnalyzer:
    """Analyze trends in COVID case data."""

    def __init__(self, case_data: List[Dict[str, Any]]):
        """Initialize with standardized case data."""
        if not isinstance(case_data, list) or not all(isinstance(c, dict) for c in case_data):
            raise TypeError("case_data must be a list of dictionaries")
        self._cases = case_data

    @property
    def cases(self) -> List[Dict[str, Any]]:
        """Return case data."""
        return self._cases

    # ------------------- Analysis Methods -------------------
    def summarize_by_field(self, field: str = 'date') -> Dict[str, Any]:
        """Aggregate cases by a field (date or location)."""
        summary = {"total_cases": 0, f"counts_by_{field}": {}, "average": 0.0}
        for record in self._cases:
            key = record.get(field)
            count = int(record.get("cases", 0))
            summary["total_cases"] += count
            if key not in summary[f"counts_by_{field}"]:
                summary[f"counts_by_{field}"][key] = 0
            summary[f"counts_by_{field}"][key] += count
        groups = summary[f"counts_by_{field}"]
        summary["average"] = round(summary["total_cases"] / len(groups), 2) if groups else 0
        return summary

    def filter_by_age(self, min_age: int = None, max_age: int = None) -> List[Dict[str, Any]]:
        """Filter cases by age range."""
        filtered = []
        for record in self._cases:
            age = record.get("age")
            if isinstance(age, int):
                if (min_age is None or age >= min_age) and (max_age is None or age <= max_age):
                    filtered.append(record)
        return filtered

    def calculate_moving_average(self, window: int = 7) -> List[float]:
        """Compute moving average of cases over time."""
        sorted_cases = sorted(self._cases, key=lambda x: x.get("date"))
        daily_counts = [int(c.get("cases", 0)) for c in sorted_cases]
        ma = []
        for i in range(len(daily_counts)):
            start_idx = max(0, i - window + 1)
            window_values = daily_counts[start_idx:i+1]
            ma.append(sum(window_values) / len(window_values))
        return ma

    def __str__(self):
        return f"TrendAnalyzer with {len(self._cases)} case records"

    def __repr__(self):
        return f"TrendAnalyzer(cases={len(self._cases)} records)"


# -------------------------------
#        Example Usage
# -------------------------------

if __name__ == "__main__":
    loader = DataLoader(["data/cases_jan.csv", "data/cases_feb.json"])
    loader.load_data()
    print(loader)

    analyzer = TrendAnalyzer(loader.data)
    print(analyzer.summarize_by_field("location"))
    print(analyzer.calculate_moving_average(3))
    print(analyzer.filter_by_age(min_age=20, max_age=40))
