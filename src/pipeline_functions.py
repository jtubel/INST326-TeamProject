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

def clean_case_data(case_list):
    """Clean a list of case records.

    Args:
        case_list (list): List of dictionaries, each representing a disease case.

    Returns:
        list: Cleaned list of valid cases.

    Example:
        >>> clean_case_data([
        ... {'date': '03/01/25', 'location': 'DC', 'age': 30, 'cases': '4'},
        ... {'date': '', 'location': 'MD', 'age': None, 'cases': 3}
        ... ])
        [{'date': '2025-03-01', 'location': 'DC', 'age': 30, 'cases': 4}]
    """
    cleaned = []
    for case in case_list:
        if not validate_case_entry(case):
            continue
        case["date"] = format_date(case["date"])
        if case["date"] == "INVALID":
            continue
        try:
            case["cases"] = int(case["cases"])
        except (ValueError, TypeError):
            continue
        cleaned.append(case)
    return cleaned

def aggregate_cases_by_date(cleaned_cases):
    """Aggregate total disease cases by date.

    Args:
        cleaned_cases (list): List of cleaned case dictionaries.

    Returns:
        dict: Dictionary with date strings as keys and total case counts as values.

    Example:
        >>> aggregate_cases_by_date([
        ... {'date': '2025-03-01', 'cases': 4},
        ... {'date': '2025-03-01', 'cases': 6},
        ... {'date': '2025-03-02', 'cases': 2}
        ... ])
        {'2025-03-01': 10, '2025-03-02': 2}
    """
    result = {}
    for record in cleaned_cases:
        date = record.get("date")
        count = record.get("cases", 0)
        if not isinstance(count, int):
            continue
        if date not in result:
            result[date] = 0
        result[date] += count
    return result
