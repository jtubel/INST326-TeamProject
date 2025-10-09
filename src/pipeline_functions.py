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
