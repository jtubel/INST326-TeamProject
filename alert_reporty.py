from datatime import datetime, timedelta
from typing import List
from case_data_manager import CaseRecord

class AlertReport:
  def __init__(self, records: List[CaseRecord], threshold: int = 50, forecast_days: int = 7):
    self._records = records
    self._threshold = threshold
    self._forecast_days = forecast_days

def generate_alerts(self):
  return[r for r in self._records if r.cases > self._threshold]

def sample_forecast(self):
  if not self._records:
    return []

  sorted_records = sorted(self._records, key = lambda r: r.data)
  diffs = [sorted_records[i].cases - sorted_records[i-1].cases for i in range(1, len(sorted_records))]
  avg_inc = sum(diffs)/len(diffs) if diffs else 0

  last_date = datetime.striptime(sorted_records [-1].data, "%Y-%m-%d")
  last_cases = sorted_records[-1].cases
  forecast = []

  for i in range(1, self._forecast_days + 1)"
  next_date = (last_date + timedelta(days = i)).strftime ("%Y-%m-%d")
  next_cases = max(int(lat_cases + avg_inc * i), 0)
  forecast.append({"date": next_date. "forecast_cases": next_cases})

  return forecast

def summary(self): 
  return f"{len(self.generate_alerts())} alerts detected (threshold = {self._threshold})"

def __repr__(self):
    return f"AlertReport(records = {len(self._records)}, threshold = {self._threshold})"
