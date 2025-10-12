def validate_case_entry(case):
    """Validate a single disease case record.

    Args:
        case (dict): A dictionary representing a case record with keys 
                     like 'date', 'location', 'age', and 'cases'.

    Returns:
        bool: True if valid, False otherwise.

    Raises:
        TypeError: If input is not a dictionary.

    Example:
        >>> validate_case_entry({'date': '2025-03-01', 'location': 'DC', 'age': 30, 'cases': 4})
        True
    """
    if not isinstance(case, dict):
        raise TypeError("Case entry must be a dictionary.")

    required = ["date", "location", "age", "cases"]
    for key in required:
        if key not in case:
            return False
        if case[key] in (None, "", "NA"):
            return False
    return True

def format_date(date_str):
    """Convert a date string into standard 'YYYY-MM-DD' format.

    Args:
        date_str (str): Date string (e.g. '03/01/25', '2025-03-01').

    Returns:
        str: Reformatted date string, or 'INVALID' if not parseable.

    Example:
        >>> format_date("03/01/25")
        '2025-03-01'
    """
    if not isinstance(date_str, str):
        return "INVALID"

    parts = date_str.replace("/", "-").split("-")

    if len(parts) == 3:
        if len(parts[0]) == 4:  # already YYYY-MM-DD
            return f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
        elif len(parts[2]) == 2:  # assume YY -> 20YY
            return f"20{parts[2]}-{parts[0].zfill(2)}-{parts[1].zfill(2)}"
    return "INVALID"

def clean_case_data(cases: list[dict]) -> list[dict]:
    """Clean and standardize a list of disease case records.

    Args:
        cases (list[dict]): A list of case dictionaries containing 'date', 'location', and 'cases'.

    Returns:
        list[dict]: A cleaned list of valid, standardized case dictionaries.

    Raises:
        TypeError: If input is not a list of dictionaries.

    Examples:
        >>> clean_case_data([{"date": "03/01/25", "location": "boston", "cases": "10"}])
        [{'date': '2025-03-01', 'location': 'Boston', 'cases': 10}]
    """
    if not isinstance(cases, list):
        raise TypeError("Input must be a list of dictionaries.")

    cleaned_data = []
    for record in cases:
        if not validate_case_entry(record):
            continue

        formatted_date = format_date(record["date"])
        if formatted_date == "INVALID":
            continue

        try:
            case_count = int(record["cases"])
        except ValueError:
            continue

        cleaned_record = {
            "date": formatted_date,
            "location": record["location"].strip().title(),
            "cases": case_count
        }
        cleaned_data.append(cleaned_record)

    return cleaned_data


def generate_epidemic_summary(cases: list[dict]) -> dict:
    """Generate a statistical summary from cleaned disease case records.

    Args:
        cases (list[dict]): List of standardized case dictionaries.

    Returns:
        dict: A dictionary containing aggregate statistics such as total cases,
              cases per location, peak day, and averages.

    Raises:
        TypeError: If input is not a list of dictionaries or if records are invalid.

    Examples:
        >>> sample = [
        ...     {"date": "2025-03-01", "location": "Boston", "cases": 10},
        ...     {"date": "2025-03-02", "location": "Boston", "cases": 20},
        ...     {"date": "2025-03-01", "location": "Chicago", "cases": 15},
        ... ]
        >>> generate_epidemic_summary(sample)
        {
            'total_cases': 45,
            'unique_locations': 2,
            'cases_by_location': {'Boston': 30, 'Chicago': 15},
            'peak_day': {'date': '2025-03-02', 'cases': 20},
            'average_daily_cases': 22.5,
            'time_span': {'start': '2025-03-01', 'end': '2025-03-02'}
        }
    """
    if not isinstance(cases, list) or not all(isinstance(c, dict) for c in cases):
        raise TypeError("Input must be a list of dictionaries.")

    total_cases = 0
    cases_by_location = {}
    cases_by_date = {}
    dates = set()

    for record in cases:
        date = record.get("date")
        location = record.get("location")
        count = record.get("cases", 0)

        if not (date and location):
            continue

        total_cases += count
        dates.add(date)
        cases_by_location[location] = cases_by_location.get(location, 0) + count
        cases_by_date[date] = cases_by_date.get(date, 0) + count

    if not cases_by_date:
        return {}

    # Find peak day
    peak_date = max(cases_by_date, key=cases_by_date.get)
    peak_count = cases_by_date[peak_date]

    # Calculate average daily cases
    average_daily = total_cases / len(cases_by_date)

    summary = {
        "total_cases": total_cases,
        "unique_locations": len(cases_by_location),
        "cases_by_location": cases_by_location,
        "peak_day": {"date": peak_date, "cases": peak_count},
        "average_daily_cases": round(average_daily, 2),
        "time_span": {"start": min(dates), "end": max(dates)}
    }

    return summary

def integrate_data_sources(sources, schema_map=None):
    """Combine multiple case data files (CSV, JSON, XML) into a unified dataset.

    Args:
        sources (list[str]): List of file paths to data sources.
        schema_map (dict, optional): Mapping of source field names to canonical names.

    Returns:
        list[dict]: Combined list of case dictionaries with unified fields.

    Raises:
        FileNotFoundError: If any source file cannot be found.
        TypeError: If sources is not a list of strings.

    Example:
        >>> integrate_data_sources(["data/jan.csv", "data/feb.json"])
        [{'date': '2025-01-01', 'location': 'Boston', 'age': 25, 'cases': 5}, ...]
    """
    if not isinstance(sources, list) or not all(isinstance(s, str) for s in sources):
        raise TypeError("Sources must be a list of file paths.")

    combined = []
    for path in sources:
        # Simplified: real implementation would detect type and parse CSV/JSON/XML
        # Here we simulate loading data
        combined.extend([])  # placeholder for loaded records
    return combined


def standardize_case_fields(df):
    """Normalize key fields such as dates, locations, and age values.

    Args:
        df (list[dict]): List of case dictionaries.

    Returns:
        list[dict]: List of case dictionaries with standardized fields.

    Raises:
        TypeError: If input is not a list of dictionaries.

    Example:
        >>> standardize_case_fields([{"date": "03/01/25", "location": "boston", "age": "20-29", "cases": "10"}])
        [{'date': '2025-03-01', 'location': 'Boston', 'age': 24, 'cases': 10}]
    """
    if not isinstance(df, list) or not all(isinstance(r, dict) for r in df):
        raise TypeError("Input must be a list of dictionaries.")

    standardized = []
    for record in df:
        rec = record.copy()
        # Example normalization logic
        rec["location"] = rec.get("location", "").strip().title()
        # Age normalization: range midpoint
        age = rec.get("age")
        if isinstance(age, str) and "-" in age:
            parts = age.split("-")
            rec["age"] = int((int(parts[0]) + int(parts[1])) / 2)
        elif isinstance(age, int):
            rec["age"] = age
        else:
            rec["age"] = None
        standardized.append(rec)
    return standardized


def summarize_case_trends(df, by='date'):
    """Aggregate case counts and produce a summary by a specified field.

    Args:
        df (list[dict]): List of standardized case dictionaries.
        by (str): Field to aggregate by (default is 'date').

    Returns:
        dict: Dictionary with total cases, counts per group, and averages.

    Raises:
        TypeError: If input is not a list of dictionaries.

    Example:
        >>> summarize_case_trends([{'date': '2025-03-01', 'cases': 5}, {'date': '2025-03-01', 'cases': 10}])
        {'total_cases': 15, 'counts_by_date': {'2025-03-01': 15}, 'average': 15.0}
    """
    if not isinstance(df, list) or not all(isinstance(r, dict) for r in df):
        raise TypeError("Input must be a list of dictionaries.")

    summary = {"total_cases": 0, f"counts_by_{by}": {}, "average": 0.0}
    for record in df:
        key = record.get(by)
        count = record.get("cases", 0)
        summary["total_cases"] += count
        if key not in summary[f"counts_by_{by}"]:
            summary[f"counts_by_{by}"][key] = 0
        summary[f"counts_by_{by}"][key] += count

    groups = summary[f"counts_by_{by}"]
    summary["average"] = summary["total_cases"] / len(groups) if groups else 0
    return summary


def plot_case_trend_line(trend_df, out_path=None):
    """Plot a line chart of case counts over time.

    Args:
        trend_df (dict): Dictionary returned by summarize_case_trends.
        out_path (str, optional): File path to save the chart image.

    Returns:
        None

    Example:
        >>> plot_case_trend_line({'counts_by_date': {'2025-03-01': 15, '2025-03-02': 20}})
        # Displays a line chart
    """
    import matplotlib.pyplot as plt

    x = list(trend_df.get("counts_by_date", {}).keys())
    y = list(trend_df.get("counts_by_date", {}).values())
    plt.figure(figsize=(8,4))
    plt.plot(x, y, marker='o')
    plt.xlabel("Date")
    plt.ylabel("Cases")
    plt.title("Case Trend Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    if out_path:
        plt.savefig(out_path)
    plt.show()


def export_dataset(df, path, format='csv'):
    """Export processed dataset to CSV or JSON file.

    Args:
        df (list[dict]): List of case dictionaries.
        path (str): Destination file path.
        format (str): File format: 'csv' or 'json' (default 'csv').

    Returns:
        None

    Raises:
        ValueError: If format is not 'csv' or 'json'.

    Example:
        >>> export_dataset([{'date':'2025-03-01','cases':15}], 'outputs/cleaned.csv')
    """
    import csv, json

    if format not in ('csv', 'json'):
        raise ValueError("Format must be 'csv' or 'json'.")

    if format == 'csv':
        if not df:
            return
        keys = df[0].keys()
        with open(path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(df)
    else:  # JSON
        with open(path, 'w') as f:
            json.dump(df, f, indent=2)
            

    - Chioma Agoh: Contributor

def fill_missing_values(df, method = 'zero'):

Args: 
    df(list[dict]): List of cases
    method (str): Filling method - 'zero' or 'mean'. 

Returns: 
    list [dict]: New list with fill_missing_values

import copy

if method not in ['zero', 'mean']:
    raise ValueError("Method is unsupported. use 'zero' or 'mean'.")
df_filled = copy.deepcopy(df)

#Getting the numeric fields
numeric_fields = set()
for record in df:
    for key, value in record.items():
        if isinstance(value, (int, float)) or value is None:
            numeric_fields.add(key)

#Calculating means if needed
means = {}
if method =='mean':
    for field in numeric_fields:
        values = [r[field] for r in df if ininstance (r.get(field), (int, float))]
        means[field] = sum(values)/len(values) if values else 0

#For filling in the missing values
for record in dr_filled:
    for field in numeric_fields:
        if record.get(field) is None:
            record[field] = 0 if method == 'zero' else means.get(field,0)
            return df_filled

#Simple

def count_unique_locations(df):

    Args: 
        df(list[dict]): List of dictionaries.

    Returns: 
        Int: Number of unique location values.

    return len(set(record.get("location")for record in df if "location" in record))


#Complex

def filter_cases_by_age(df, min_age=None, max_age=None):
    """Filter case records by age range
    Args: 
        df (list[dict]): List of case dictionaries with 'age'
        min_age (int, optional): Minimum age to include.
        max_age (int, optional): Maximum age to include.

    Returns:
        list [dict]: Filtered lists of record within age range.
    """

    filtered = []
    for record in df:
        age = record.get('age')
        if isinstance(age, int):
            if (min_age is None or age >= min_age) and (max_age is None or age <= max_age):
                filtered.append(record)

    return filtered

    def generate_case_heatmap(df, output_path)='outputs/heatmap.png'):
        """Generate a heatmap of case counts by date and location.

        Args: 
            df(lisy[dict]): Lists of case dictionaires with 'date', 'location', and 'cases'.
            output_patg (str): Path to save the heatmap image.

        Returns:
            None
        """

        import pandas as peak_date
        import seaborn as standardize_case_fields
        import matplotlib.pylot as plt

        if not dr: 
            print("No data available.")
            return

#Converting to DataFrame
data = pd.DataFrame(df)
if data.empty or not {'date', 'location', 'case'}.issubset(data.columns):
    print("Missing required.")
    return

    pivot = data.privot_table(index = 'location', columns='date', values='cases', aggfunc='sum', fill_values=0)

    plt.figure(figsize=(10,6))
    sns.heatmap(pivot, annot=True, fmt='d', cmap='YLOrRD')
    plt.title("Location and Date of Cases")
    plt.xlabel("Date")
    plt.ylabel("Location")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show() 

"""
pipeline_functions.py
Yonael Zeamann - Statistical Analysis & Forecasting Functions

This module has functions for analyzing epidemic case data and making predictions.
Works with the cleaned data from the other team members' functions.
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from statistics import mean, stdev


def calculate_moving_average(case_data: List[int], window_size: int = 7) -> List[float]:
    """
    Calculate moving average of case counts to smooth out the data.
    
    Args:
        case_data (list): List of daily case counts
        window_size (int): How many days to average together (default is 7)
    
    Returns:
        list: List of averaged values (same length as input)
    
    Raises:
        ValueError: If window_size is too big or less than 1
        TypeError: If case_data isn't a list of numbers
    
    Examples:
        >>> calculate_moving_average([10, 20, 30, 40, 50], 3)
        [10.0, 15.0, 20.0, 30.0, 40.0]
    """
    if not isinstance(case_data, list):
        raise TypeError("case_data must be a list")
    if not all(isinstance(x, (int, float)) for x in case_data):
        raise TypeError("All elements in case_data must be numbers")
    if window_size < 1:
        raise ValueError("Window size must be at least 1")
    if window_size > len(case_data):
        raise ValueError("Window size cannot be larger than data length")
    
    moving_averages = []
    for i in range(len(case_data)):
        start_idx = max(0, i - window_size + 1)
        window = case_data[start_idx:i + 1]
        moving_averages.append(sum(window) / len(window))
    
    return moving_averages


def generate_outbreak_alert_report(cases_by_location: Dict[str, List[Dict]], 
                                   threshold: int = 50,
                                   days_to_analyze: int = 7) -> Dict[str, Any]:
    """
    Create an alert report showing which locations have high case counts.
    
    Args:
        cases_by_location (dict): Dictionary with location names as keys and 
                                 lists of case records as values.
        threshold (int): Alert if cases go above this number (default is 50)
        days_to_analyze (int): How many recent days to look at (default is 7)
    
    Returns:
        dict: Report with these fields,'alert_locations', 'total_alerts',
        'highest_risk','growth_rates','recommendations'.
    
    Raises:
        ValueError: If threshold is negative or days_to_analyze is less than 1
        TypeError: If cases_by_location isn't a dictionary
    
    Examples:
        >>> data = {
        ...     "City A": [{"date": "2025-01-01", "cases": 60}],
        ...     "City B": [{"date": "2025-01-01", "cases": 30}]
        ... }
        >>> report = generate_outbreak_alert_report(data, threshold=50)
        >>> report['total_alerts']
        1
    """
    if not isinstance(cases_by_location, dict):
        raise TypeError("cases_by_location must be a dictionary")
    if threshold < 0:
        raise ValueError("Threshold cannot be negative")
    if days_to_analyze < 1:
        raise ValueError("days_to_analyze must be at least 1")
    
    alert_locations = []
    growth_rates = {}
    highest_risk = None
    highest_count = 0
    
    for location, case_records in cases_by_location.items():
        if not case_records:
            continue
        
        recent_cases = case_records[-days_to_analyze:]
        total_recent = sum(record.get('cases', 0) for record in recent_cases)
        
        if total_recent >= threshold:
            alert_message = f"ALERT: {location} has {total_recent} cases (threshold: {threshold})"
            alert_locations.append({
                'location': location,
                'total_cases': total_recent,
                'alert_message': alert_message
            })
        
        if total_recent > highest_count:
            highest_count = total_recent
            highest_risk = location
        
        if len(recent_cases) >= 2:
            first_count = recent_cases[0].get('cases', 0)
            last_count = recent_cases[-1].get('cases', 0)
            if first_count > 0:
                growth_rate = ((last_count - first_count) / first_count) * 100
                growth_rates[location] = round(growth_rate, 2)
    
    recommendations = []
    if len(alert_locations) > 0:
        recommendations.append("Immediate investigation required for alert locations")
    if len(alert_locations) > 3:
        recommendations.append("Consider regional coordination for outbreak response")
    if highest_count > threshold * 2:
        recommendations.append(f"Priority response needed in {highest_risk}")
    
    return {
        'alert_locations': alert_locations,
        'total_alerts': len(alert_locations),
        'highest_risk': highest_risk,
        'highest_count': highest_count,
        'growth_rates': growth_rates,
        'recommendations': recommendations,
        'analysis_period_days': days_to_analyze
    }


def predict_future_cases(historical_cases: List[int], days_ahead: int = 7) -> List[int]:
    """
    Uses average change and predicts future cases.
    
    Args:
        historical_cases (list): List of past daily case counts
        days_ahead (int): How many days into the future to predict (default is 7)
    
    Returns:
        list: Predicted case counts for future days
    
    Raises:
        ValueError: If we don't have enough data 
        TypeError: If historical_cases isn't a list of numbers
    
    Examples:
        >>> predict_future_cases([10, 15, 20, 25, 30], 3)
        [35, 40, 45]
    """
    if not isinstance(historical_cases, list):
        raise TypeError("historical_cases must be a list")
    if len(historical_cases) < 3:
        raise ValueError("Need at least 3 historical data points for prediction")
    if days_ahead < 1:
        raise ValueError("days_ahead must be at least 1")
    if not all(isinstance(x, (int, float)) for x in historical_cases):
        raise TypeError("All elements must be numbers")
    
    daily_changes = []
    for i in range(1, len(historical_cases)):
        change = historical_cases[i] - historical_cases[i-1]
        daily_changes.append(change)
    
    avg_change = sum(daily_changes) / len(daily_changes)
    
    predictions = []
    last_value = historical_cases[-1]
    
    for day in range(days_ahead):
        next_value = last_value + avg_change
        next_value = max(0, int(round(next_value)))
        predictions.append(next_value)
        last_value = next_value
    
    return predictions
