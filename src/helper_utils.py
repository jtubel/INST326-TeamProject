def is_valid_location(location: str) -> bool:
    """Validate that a location name is non-empty and alphabetic.

    Args:
        location (str): The location name to validate.

    Returns:
        bool: True if the location name is valid, False otherwise.

    Raises:
        TypeError: If location is not a string.

    Examples:
        >>> is_valid_location("New York")
        True
        >>> is_valid_location("123 Main St")
        False
        >>> is_valid_location("")
        False
    """
    if not isinstance(location, str):
        raise TypeError("Location must be a string.")

    location = location.strip()
    return bool(location) and all(ch.isalpha() or ch.isspace() for ch in location)


def normalize_age(age_value) -> int:
    """Normalize different age input formats into a single integer value.

    Args:
        age_value (str | int): The age value, which may be an integer,
            string, or range (e.g., "20-30").

    Returns:
        int: A single representative age value.
        Returns -1 if the input cannot be parsed.

    Examples:
        >>> normalize_age("25")
        25
        >>> normalize_age("20-30")
        25
        >>> normalize_age(40)
        40
    """
    if isinstance(age_value, int):
        return age_value

    if isinstance(age_value, str):
        age_value = age_value.strip()
        if "-" in age_value:
            try:
                start, end = map(int, age_value.split("-"))
                return (start + end) // 2
            except ValueError:
                return -1
        elif age_value.isdigit():
            return int(age_value)

    return -1 

def calculate_case_fatality_rate(total_cases: int, total_deaths: int) -> float:
    """
    Calculate the case fatality rate as a percentage.
    
    Args:
        total_cases (int): Total number of cases
        total_deaths (int): Total number of deaths
    
    Returns:
        float: Fatality rate as a percentage
    
    Examples:
        >>> calculate_case_fatality_rate(1000, 25)
        2.5
    """
    if not isinstance(total_cases, int) or not isinstance(total_deaths, int):
        raise TypeError("Both inputs must be integers")
    if total_cases < 0 or total_deaths < 0:
        raise ValueError("Case and death counts cannot be negative")
    if total_cases == 0:
        raise ValueError("Total cases cannot be zero")
    
    return (total_deaths / total_cases) * 100


