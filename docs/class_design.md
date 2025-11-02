---

# Class and Method Design

Classes designed by Julian Tubel

This section describes the detailed design of the two classes I created for managing case data.  
Each class includes validation, cleaning, and summarization methods that connect back to our Project 1 functions.

---

## Class: `CaseRecord`

### Purpose
Represents a single COVID-19 case and ensures all fields are valid when created.

### Constructor
`__init__(date: str, location: str, age: int, cases: int)`

### Attributes (through properties)

| Name | Type | Description |
|------|------|-------------|
| `date` | `str` | Checked and stored in `YYYY-MM-DD` format. |
| `location` | `str` | Cleaned and title-cased. |
| `age` | `int` | Must be between 0 and 120. |
| `cases` | `int` | Must be ≥ 0. |

### Public Methods
- `to_dict()` — Returns a dictionary with all fields.  
- `__str__()` — Human-readable text version.  
- `__repr__()` — Debug-friendly version.

### Internal Helpers
- `_parse_date(date_str)` — Validates date format.  
- `_normalize_location(loc)` — Cleans up the location string.  
- `_validate_age(age)` — Checks that age is realistic.  
- `_validate_case_count(cases)` — Checks that cases are non-negative.

---

## Class: `CaseDataset`

### Purpose
Stores many `CaseRecord` objects and provides basic tools to clean and summarize the data.

### Constructor
`__init__()`

### Core Methods
- `add_record(record)` — Adds a `CaseRecord` to the list.  
- `remove_record(index)` — Deletes a record at the given index.  
- `__len__()` — Returns the number of records.  
- `__iter__()` — Allows looping through records.

### Cleaning
- `normalize_fields()` — Ensures all locations use title case.  
- `impute_missing()` — Fixes missing ages and removes records with 0 cases.

### Filtering
- `filter_by_location(location)` — Returns matching records for one location.  
- `filter_by_age_range(min_age, max_age)` — Returns records within an age range.

### Aggregation and Summary
- `count_unique_locations()` — Counts distinct locations.  
- `mean_cases()` — Computes the average number of cases.  
- `summarize()` — Returns totals and averages in a small dictionary.

### Utility
- `to_dicts()` — Exports all records as dictionaries.  
- `__str__()` — Shows a short dataset summary.

---
