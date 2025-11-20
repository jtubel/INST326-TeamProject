# -------------------------------
#       Trend Analyzer Class
#  Analyze and summarize cases
# -------------------------------

from typing import List, Dict, Any
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
