"""
alert_report.py
Reporting Module for Health Data Pipeline.
Refactored to work with CaseRecord objects and PipelineManager.
"""

from typing import List, Dict
import datetime

class AlertReport:
    """
    Generates alerts for high-case days based on CaseRecord objects.
    """

    def __init__(self, records: list, threshold: int = 50):
        """
        Initialize with a list of CaseRecord objects.
        
        Args:
            records (list[CaseRecord]): Data from the pipeline.
            threshold (int): Case count that triggers an alert.
        """
        # Removed strict type check for list[dict] to allow CaseRecord objects
        if not isinstance(records, list):
            raise TypeError("Records must be a list.")
        if threshold < 0: 
            raise ValueError("Threshold must be non-negative.")

        self._records = records
        self._threshold = threshold

    def generate_alerts(self) -> List[str]:
        """
        Scan records and return alert messages for days exceeding threshold.
        """
        alerts = []
        for r in self._records:
            cases = r.cases if hasattr(r, 'cases') else r.get('cases', 0)
            date = r.date if hasattr(r, 'date') else r.get('date', 'Unknown')
            loc = r.location if hasattr(r, 'location') else r.get('location', 'Unknown')

            if cases > self._threshold:
                alerts.append(f"ALERT: {loc} had {cases} cases on {date} (Threshold: {self._threshold})")
        
        return alerts

    def save_report(self, filename: str = "alert_summary.txt"):
        """
        Write all alerts to a text file.
        """
        alerts = self.generate_alerts()
        with open(filename, "w") as f:
            f.write(f"--- OUTBREAK ALERT REPORT ---\n")
            f.write(f"Generated: {datetime.datetime.now()}\n")
            f.write(f"Threshold: {self._threshold} cases\n\n")
            
            if not alerts:
                f.write("No high-risk days detected.\n")
            else:
                for alert in alerts:
                    f.write(alert + "\n")
        
        print(f"Report saved to {filename} with {len(alerts)} alerts.")

    def __str__(self):
        return f"AlertReport(threshold={self._threshold}, records={len(self._records)})"
