from chrono_python.types import Moment


def find_year_closest_to_ref(ref: Moment, month: int, day: int) -> int:
    return ref.datetime().year
