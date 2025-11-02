from datetime import datetime

class CaseRecord:
    """
    Represents a single COVID-19 case record with validation and formatting.

    Attributes (properties):
        date (str): Report date in 'YYYY-MM-DD' format.
        location (str): Region/area name, title-cased.
        age (int): Age (0–120). Missing ages normalized to 0 in cleaning.
        cases (int): Non-negative case count.
    """

    def __init__(self, date: str, location: str, age: int, cases: int):
        # private storage with validated setters
        self._date = None
        self._location = None
        self._age = None
        self._cases = None

        self.date = date
        self.location = location
        self.age = age
        self.cases = cases

    # ---------- properties ----------
    @property
    def date(self) -> str:
        return self._date

    @date.setter
    def date(self, value: str) -> None:
        self._date = self._parse_date(value)

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, value: str) -> None:
        self._location = self._normalize_location(value)

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        self._age = self._validate_age(value)

    @property
    def cases(self) -> int:
        return self._cases

    @cases.setter
    def cases(self, value: int) -> None:
        self._cases = self._validate_case_count(value)

    # ---------- internal helpers (Project 1 mappings in comments) ----------
    def _parse_date(self, date_str: str) -> str:
        """Parse and validate date string (P1: format_date)."""
        try:
            parsed = datetime.strptime(date_str.strip(), "%Y-%m-%d")
            return parsed.strftime("%Y-%m-%d")
        except Exception as exc:
            raise ValueError("Date must be formatted as YYYY-MM-DD.") from exc

    def _normalize_location(self, loc: str) -> str:
        """Normalize location string (P1: standardize_case_fields)."""
        if not isinstance(loc, str) or len(loc.strip()) == 0:
            raise ValueError("Location cannot be empty.")
        return loc.strip().title()

    def _validate_age(self, age):
        """Validate age range (P1: validate_case_entry)."""
        if age is None:
            return 0
        if not isinstance(age, int) or age < 0 or age > 120:
            raise ValueError("Age must be an integer between 0 and 120.")
        return age

    def _validate_case_count(self, cases):
        """Validate non-negative integer for cases."""
        if not isinstance(cases, int) or cases < 0:
            raise ValueError("Cases must be a non-negative integer.")
        return cases

    # ---------- export & display ----------
    def to_dict(self) -> dict:
        return {
            "date": self.date,
            "location": self.location,
            "age": self.age,
            "cases": self.cases
        }

    def __str__(self) -> str:
        return f"CaseRecord({self.date}, {self.location}, age={self.age}, cases={self.cases})"

    def __repr__(self) -> str:
        return self.__str__()
