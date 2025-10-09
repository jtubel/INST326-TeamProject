### Julian Tubel — Data Validation & Aggregation Functions

**Functions Implemented:**  
- `validate_case_entry()` — Checks that all required fields exist and contain valid values.  
- `format_date()` — Standardizes inconsistent date formats into `YYYY-MM-DD`.  
- `clean_case_data()` — Cleans a list of case records by fixing dates and removing invalid entries.  
- `generate_epidemic_summary()` — Generates a statistical summary from cleaned disease case records
- `is_valid_location()` — Validates a location string for correctness.
- `normalize_age()` — Normalizes age formats (number or range) into a single integer.
**Files Modified:**  
- `src/pipeline_functions.py` — Main functions implemented here.
- `src/helper_utils.py` — Helper functions implemented here.  
- `docs/function_reference.md` — Added documentation for each function
