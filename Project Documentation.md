### Julian Tubel — Data Validation & Aggregation Functions

**Functions Implemented:**  
- `validate_case_entry()` — Checks that all required fields exist and contain valid values.  
- `format_date()` — Standardizes inconsistent date formats into `YYYY-MM-DD`.  
- `clean_case_data()` — Cleans a list of case records by fixing dates and removing invalid entries.  
- `aggregate_cases_by_date()` — Aggregates total case counts per date for summary charts.

**Files Modified:**  
- `src/data_utils.py` — All functions implemented here.  
- `docs/function_reference.md` — Added documentation for each function
