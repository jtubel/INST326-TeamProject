from abc import ABC, abstractmethod
from typing import List, Dict, Any
from statistics import mean

class AbstractAnalyzer(ABC):
    """
    Base class for all analysis modules.
    Enforces a standard interface for processing case records.
    """
    
    @abstractmethod
    def analyze(self, records: List[Any]) -> Dict[str, Any]:
        """
        Process a list of records and return summary statistics.
        Must be implemented by subclasses.
        """
        pass

class TrendAnalyzer(AbstractAnalyzer):
    """
    Concrete implementation of AbstractAnalyzer.
    Focuses on time-series trends and moving averages.
    """

    def analyze(self, records: List[Any]) -> Dict[str, Any]:
        """
        Main entry point for the pipeline to run this analyzer.
        """
        if not records:
            return {"status": "No data"}

        # Convert objects to dicts if needed, or access attributes directly
        # Handling both CaseRecord objects (your code) and raw dicts (legacy)
        clean_data = []
        for r in records:
            # Polymorphic handling: support objects or dicts
            val = r.cases if hasattr(r, 'cases') else r.get('cases', 0)
            date = r.date if hasattr(r, 'date') else r.get('date', 'Unknown')
            clean_data.append({'cases': int(val), 'date': date})

        return {
            "total_cases": sum(d['cases'] for d in clean_data),
            "moving_average": self._calculate_moving_average(clean_data),
            "average_daily": mean(d['cases'] for d in clean_data) if clean_data else 0
        }

    def _calculate_moving_average(self, data: List[Dict], window: int = 7) -> List[float]:
        """Internal helper method for moving averages."""
        sorted_cases = sorted(data, key=lambda x: x['date'])
        daily_counts = [c['cases'] for c in sorted_cases]
        
        ma = []
        for i in range(len(daily_counts)):
            start_idx = max(0, i - window + 1)
            window_values = daily_counts[start_idx:i+1]
            ma.append(round(mean(window_values), 2))
        return ma
