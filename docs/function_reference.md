"""
Julian Tubel — Data Validation & Aggregation Functions

Functions Implemented:
- validate_case_entry(): Checks that all required fields exist and contain valid values.
- format_date(): Standardizes inconsistent date formats into 'YYYY-MM-DD'.
- clean_case_data(): Cleans a list of case records by fixing dates and removing invalid entries.
- generate_epidemic_summary(): Generates a statistical summary from cleaned disease case records.
- is_valid_location(): Validates a location string for correctness.
- normalize_age(): Normalizes age formats (number or range) into a single integer.

How to Use These Functions:
The following workflow demonstrates how the data validation and aggregation functions 
can be used together in a disease data processing pipeline.
"""
1. Import necessary helper and pipeline functions:
    from src.helper_utils import is_valid_location, normalize_age
    from src.pipeline_functions import (
        validate_case_entry,
        format_date,
        clean_case_data,
        generate_epidemic_summary
    )

2. Prepare your raw input data, e.g.:
    raw_cases = [
        {"date": "03/01/25", "location": "New York", "age": "20-30", "cases": 5},
        {"date": "2025-02-15", "location": "123 Main St", "age": "unknown", "cases": 3},
        {"date": "02/28/25", "location": "Boston", "age": 40, "cases": 2}
    ]

3. Validate each case entry:
    valid_cases = [c for c in raw_cases if validate_case_entry(c)]

4. Clean the data (standardize dates, normalize ages, remove invalid entries):
    cleaned_cases = clean_case_data(valid_cases)

5. Generate summary statistics:
    summary = generate_epidemic_summary(cleaned_cases)

6. Print results:
    print("Cleaned Cases:")
    for c in cleaned_cases:
        print(c)

    print("\\nEpidemic Summary:")
    print(summary)

Expected Output Example:

Cleaned Cases:
{'date': '2025-03-01', 'location': 'New York', 'age': 25, 'cases': 5}
{'date': '2025-02-28', 'location': 'Boston', 'age': 40, 'cases': 2}

Epidemic Summary:
{'total_cases': 7, 'unique_locations': 2, 'average_age': 32.5, 'date_range': ('2025-02-28', '2025-03-01')}
"""
