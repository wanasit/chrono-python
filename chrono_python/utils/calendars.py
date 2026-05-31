from chrono_python.types import Moment


def find_year_closest_to_ref(ref: Moment, month: int, day: int) -> int:
    """Find the year closest to the reference moment for the given month and day."""
    return ref.datetime().year


def find_most_likely_ad_year(year_number: int) -> int:
    """Find the most likely AD year from a raw year number.

    If the year number is less than 100:
    - If it is greater than 50, it is treated as a year in the 1900s (e.g., 97 -> 1997).
    - Otherwise, it is treated as a year in the 2000s (e.g., 12 -> 2012).
    """
    if year_number < 100:
        if year_number > 50:
            year_number += 1900
        else:
            year_number += 2000
    return year_number
