"""
forecasting_analyzer.py
Project 3: Concrete Implementation of an Analyzer.
Inherits from AbstractAnalyzer (defined by Kindness).
"""

from abc import ABC, abstractmethod
from statistics import mean

class AbstractAnalyzer(ABC):
    @abstractmethod
    def analyze(self, records: list):
        pass

class ForecastingAnalyzer(AbstractAnalyzer):
  

    def __init__(self, days_ahead=7):
        self.days_ahead = days_ahead

    def analyze(self, records: list):
        """
        Process records and predict future cases.
        
        Args:
            records (list[CaseRecord]): List of case objects.
            
        Returns:
            dict: Prediction results.
        """
        # Extract numerical case data from records
 
        case_counts = [r.cases for r in records if isinstance(r.cases, (int, float))]
        
        if len(case_counts) < 2:
            return {"error": "Insufficient data for prediction"}

        changes = [case_counts[i] - case_counts[i-1] for i in range(1, len(case_counts))]
        avg_change = mean(changes) if changes else 0

        predictions = []
        last_val = case_counts[-1]
        for _ in range(self.days_ahead):
            next_val = max(0, int(last_val + avg_change))
            predictions.append(next_val)
            last_val = next_val

        return {
            "historical_count": len(case_counts),
            "average_daily_change": round(avg_change, 2),
            "future_predictions": predictions
        }
