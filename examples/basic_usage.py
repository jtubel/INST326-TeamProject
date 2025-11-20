# Demonstration of CaseRecord and CaseDataset classes designed by Julian Tubel

from CaseRecord import CaseRecord
from CaseDataset import CaseDataset

# --- Create several CaseRecord objects ---
record1 = CaseRecord("2025-03-01", "Maryland", 28, 5)
record2 = CaseRecord("2025-03-02", "Maryland", 35, 3)
record3 = CaseRecord("2025-03-03", "Virginia", 40, 8)
record4 = CaseRecord("2025-03-04", "Virginia", 42, 0)  # will be dropped later

# --- Add records to a CaseDataset ---
dataset = CaseDataset()
dataset.add_record(record1)
dataset.add_record(record2)
dataset.add_record(record3)
dataset.add_record(record4)

print("Initial dataset:")
for record in dataset:
    print(record)

# --- Normalize and clean the dataset ---
dataset.normalize_fields()   # Title-case locations (standard formatting)
dataset.impute_missing()     # Removes zero-case records, replaces invalid ages

# --- Display summary information ---
print("\nCleaned dataset summary:")
print(dataset.summarize())

print("\nAverage cases per record:", round(dataset.mean_cases(), 2))
print("Unique locations:", dataset.count_unique_locations())

# --- Example of filtering ---
print("\nRecords from Maryland only:")
for record in dataset.filter_by_location("maryland"):
    print(record)

# --- Export records as dictionaries ---
print("\nAll records as dictionaries:")
for record_dict in dataset.to_dicts():
    print(record_dict)
