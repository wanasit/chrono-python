from chrono_python.types import Moment


import datetime

def find_year_closest_to_ref(ref: Moment, month: int, day: int) -> int:
    """Find the year closest to the reference moment for the given month and day."""
    ref_dt = ref.datetime()
    
    # Try current, next, and last year to find the closest match
    try:
        current_year_dt = ref_dt.replace(year=ref_dt.year, month=month, day=day)
    except ValueError:
        if month == 2 and day == 29:
            current_year_dt = ref_dt.replace(year=ref_dt.year, month=2, day=28) + datetime.timedelta(days=1)
        else:
            current_year_dt = ref_dt.replace(year=ref_dt.year, month=month, day=day)
            
    try:
        next_year_dt = current_year_dt.replace(year=ref_dt.year + 1)
    except ValueError:
        next_year_dt = current_year_dt.replace(year=ref_dt.year + 1, month=2, day=28) + datetime.timedelta(days=1)
        
    try:
        last_year_dt = current_year_dt.replace(year=ref_dt.year - 1)
    except ValueError:
        last_year_dt = current_year_dt.replace(year=ref_dt.year - 1, month=2, day=28) + datetime.timedelta(days=1)
        
    diff_current = abs((current_year_dt - ref_dt).total_seconds())
    diff_next = abs((next_year_dt - ref_dt).total_seconds())
    diff_last = abs((last_year_dt - ref_dt).total_seconds())
    
    if diff_next < diff_current and diff_next < diff_last:
        return ref_dt.year + 1
    elif diff_last < diff_current and diff_last < diff_next:
        return ref_dt.year - 1
    else:
        return ref_dt.year


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
