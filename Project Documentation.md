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

### Kindness Harbor - Data Integration & Reporting Functions
**Functions Implemented:** 
- `integrate_data_sources(sources, schema_map=None)` — Combines various case data files (CSV, JSON, XML) into one dataset, or optionally harmonizes different field names based on a given schema map. 
- `standardize_case_fields(df)` — Cleans and normalizes key fields such as date, location names, and age formats to a standard format prior to analysis.
- `summarize_case_trends(df, by='date')` — Bins the number of cases by a specified field (default: date) and generates a light summary table for quick trend analysis.
- `plot_case_trend_line(trend_df, out_path=None)` — Generates a basic line plot of case counts by time and saves it to file, if provided, for reporting purposes.
- `export_dataset(df, path, format='csv')` — Exports a preprocessed dataset into a user-provided file path in CSV or JSON format for dissemination or subsequent analysis.

  **Files Modified:**  
- `src/pipeline_functions.py` — Main functions implemented here. 
- `docs/function_reference.md` — Added documentation for each function
