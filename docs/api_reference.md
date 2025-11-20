# API Reference 

Classes designed by Julian Tubel

This part of the project includes two classes that manage COVID-19 case data.  
They are designed to make it easy to store, clean, and summarize information about reported cases.

- **`CaseRecord`** represents one case entry.
- **`CaseDataset`** manages a group of case records and provides dataset-wide operations.

---

## Overview of the API

1. Create individual `CaseRecord` objects for each row of data.  
   Each record checks that the date, location, age, and case count are valid.

2. Add the records to a `CaseDataset`.  
   The dataset lets you clean up missing values, standardize formats, and filter by location or age.

3. Use summary methods to get quick statistics such as totals and averages.

---

## Public Interfaces

### Class: `CaseRecord`

Represents one validated COVID-19 case.

**Properties**

| Name | Type | Description |
|------|------|-------------|
| `date` | `str` | Report date in `YYYY-MM-DD` format. |
| `location` | `str` | Region or area name (title-cased). |
| `age` | `int` | Age between 0 and 120. Missing ages handled later during cleaning. |
| `cases` | `int` | Non-negative number of cases. |

**Methods**

| Method | Description |
|--------|--------------|
| `to_dict()` | Returns the record as a dictionary. |
| `__str__()` | Returns a readable string for printing. |
| `__repr__()` | Returns a developer-friendly string. |

---

### Class: `CaseDataset`

Holds many `CaseRecord` objects and provides methods for cleaning, filtering, and summarizing.

**Core**

| Method | Description |
|--------|--------------|
| `add_record(record)` | Adds a validated `CaseRecord`. |
| `remove_record(index)` | Removes a record by index. |
| `__len__()` | Returns the number of records. |
| `__iter__()` | Allows looping over all records. |

**Cleaning**

| Method | Description |
|--------|--------------|
| `normalize_fields()` | Makes sure all location names use title case. |
| `impute_missing()` | Replaces missing or invalid ages with 0 and removes records with 0 cases. |

**Filtering**

| Method | Description |
|--------|--------------|
| `filter_by_location(location)` | Returns all records from a given location. |
| `filter_by_age_range(min_age, max_age)` | Returns records within the given age range. |

**Aggregation and Summary**

| Method | Description |
|--------|--------------|
| `count_unique_locations()` | Counts how many unique locations are in the dataset. |
| `mean_cases()` | Calculates the average number of cases per record. |
| `summarize()` | Returns a dictionary with totals and averages. |

**Utility**

| Method | Description |
|--------|--------------|
| `to_dicts()` | Returns all records as dictionaries. |
| `__str__()` | Returns a short summary of the dataset. |

---
