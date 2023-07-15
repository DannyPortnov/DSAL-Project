

from __future__ import annotations  # for self reference
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Course import Course

# from enum import StrEnum  # Assuming you have Python 3.11 or higher
from enum import Enum, auto


class Interships(Enum):
    INDUSTRY = auto(),
    RESEARCH = auto(),
    PROJECT = auto()


class Speciality(Enum):
    # INVALID = auto(),
    COMPUTERS = auto(),
    SIGNALS = auto(),
    DEVICES = auto()


class CourseType(Enum):
    MANDATORY = auto(),
    MAJOR = auto(),
    MINOR = auto(),
    EXTERNAL = auto()


class SpecialityCourseType(Enum):
    NA = auto(),
    REQUIRED = auto(),
    OPTIONAL = auto()


class ComputersCourseType(str, Enum):
    HW = '(חומרה)',
    SW = '(תוכנה)',
    TOTAL = auto()


REQUIRED_COURSE_INDICATOR = "חובה"

OPTIONAL_COURSE_INDICATOR = "בחירה"

SEMESTER_LINE_INDICATOR = "סמסטר"

INVALID_COURSE_DATA_ERROR = "Course's data does not match Syllabus"

COURSE_NUMBER_NOT_FOUND_ERROR = "Course number not found"

MISSING_SPORT_POINTS_ERROR = "You haven't taken the correct amount of sport points"

MISSING_GENERAL_POINTS_ERROR = "You haven't taken the correct amount of general points"

INVALID_INTERSHIP_ERROR = "Invalid intership! You haven't taken both of the \
    intership courses (couldn't determine amount of required credits)"
