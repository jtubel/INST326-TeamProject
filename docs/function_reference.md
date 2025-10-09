### Julian Tubel — Data Validation & Aggregation Functions

**Functions Implemented:**  
- `validate_case_entry()` — Checks that all required fields exist and contain valid values.  
- `format_date()` — Standardizes inconsistent date formats into `YYYY-MM-DD`.  
- `clean_case_data()` — Cleans a list of case records by fixing dates and removing invalid entries.  
- `generate_epidemic_summary()` — Generates a statistical summary from cleaned disease case records.  
- `is_valid_location()` — Validates a location string for correctness.  
- `normalize_age()` — Normalizes age formats (number or range) into a single integer.

### How to Use These Functions

The following workflow demonstrates how the data validation and aggregation functions can be used together in a disease data processing pipeline.

```python
from src.helper_utils import is_valid_location, normalize_age
from src.pipeline_functions import (
    validate_case_entry,
    format_date,
    clean_case_data,
    generate_epidemic_summary
)

# Example raw input data
raw_cases = [
    {"date": "03/01/25", "location": "New York", "age": "20-30", "cases": 5},
    {"date": "2025-02-15", "location": "123 Main St", "age": "unknown", "cases": 3},
    {"date": "02/28/25", "location": "Boston", "age": 40, "cases": 2}
]

# Step 1: Validate each case entry
valid_cases = [c for c in raw_cases if validate_case_entry(c)]

# Step 2: Clean data (standardize dates, normalize ages, remove invalid)
cleaned_cases = clean_case_data(valid_cases)

# Step 3: Generate summary statistics
summary = generate_epidemic_summary(cleaned_cases)

print("Cleaned Cases:")
for c in cleaned_cases:
    print(c)

print("\nEpidemic Summary:")
print(summary)
