from CaseRecord import CaseRecord

class CaseDataset:
    """
    Collection of CaseRecord objects with cleaning, filtering, and aggregation
    (derived from Project 1 functions).
    """

    def __init__(self):
        self._records: list[CaseRecord] = []

    # ---------- core ----------
    def add_record(self, record: CaseRecord) -> None:
        """Add a validated CaseRecord to the dataset."""
        if not isinstance(record, CaseRecord):
            raise TypeError("Only CaseRecord instances can be added.")
        self._records.append(record)

    def remove_record(self, index: int) -> None:
        """Remove a record by index."""
        if index < 0 or index >= len(self._records):
            raise IndexError("Index out of range.")
        del self._records[index]

    def __len__(self) -> int:
        return len(self._records)

    def __iter__(self):
        return iter(self._records)

    # ---------- data cleaning (Project 1 parity noted) ----------
    def impute_missing(self) -> None:
        """
        Normalize missing/invalid ages to 0 and remove records with 0 cases.
        (P1: fill_missing_values, clean_case_data)
        """
        cleaned: list[CaseRecord] = []
        for rec in self._records:
            if rec.cases > 0:
                if rec.age is None or rec.age < 0:
                    rec.age = 0
                cleaned.append(rec)
        self._records = cleaned

    def normalize_fields(self) -> None:
        """
        Normalize fields across all records (P1: standardize_case_fields).
        """
        for rec in self._records:
            rec.location = rec.location.title()

    # ---------- query & aggregation ----------
    def filter_by_location(self, location: str) -> list[CaseRecord]:
        """Records from a specific location (P1: filter_cases_by_location)."""
        return [r for r in self._records if r.location.lower() == location.lower()]

    def filter_by_age_range(self, min_age: int, max_age: int) -> list[CaseRecord]:
        """Records within [min_age, max_age] (P1: filter_cases_by_age)."""
        return [r for r in self._records if min_age <= r.age <= max_age]

    def count_unique_locations(self) -> int:
        """Number of unique locations (P1: count_unique_locations)."""
        return len(set(r.location for r in self._records))

    def mean_cases(self) -> float:
        """Average cases per record (P1: summarize_case_trends/average)."""
        if len(self._records) == 0:
            return 0.0
        total = sum(r.cases for r in self._records)
        return total / len(self._records)

    def summarize(self) -> dict:
        """
        Summary totals/averages (P1: generate_epidemic_summary).
        """
        total_cases = sum(r.cases for r in self._records)
        avg_cases = self.mean_cases()
        unique_locs = self.count_unique_locations()
        return {
            "total_records": len(self._records),
            "unique_locations": unique_locs,
            "total_cases": total_cases,
            "average_cases": round(avg_cases, 2)
        }

    # ---------- utility ----------
    def to_dicts(self) -> list[dict]:
        """All records as dictionaries."""
        return [r.to_dict() for r in self._records]

    def __str__(self) -> str:
        return f"CaseDataset({len(self)} records, {self.count_unique_locations()} locations)"
