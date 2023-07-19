

from __future__ import annotations  # for self reference
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Course import Course

from enum import Enum, auto


class Internships(Enum):
    INDUSTRY = auto(),
    RESEARCH = auto(),
    PROJECT = auto()


class Speciality(Enum):
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


INTERNSHIP_COURSES = {
    (31054, 31055): Internships.INDUSTRY,
    (31052, 31053): Internships.RESEARCH,
    (31050, 31051): Internships.PROJECT
}

REQUIRED_COURSE_INDICATOR = "חובה"

OPTIONAL_COURSE_INDICATOR = "בחירה"

SEMESTER_LINE_INDICATOR = "סמסטר"

INVALID_COURSE_DATA_ERROR = "Course's data does not match Syllabus"

COURSE_NUMBER_NOT_FOUND_ERROR = "Course number not found"

MISSING_SPORT_POINTS_ERROR = "You haven't taken the correct amount of sport points"

MISSING_GENERAL_POINTS_ERROR = "You haven't taken the correct amount of general points"

MINOR_NA_INDICATOR = "NA"

# Parenthesis are used to split the long string into multiple lines
INVALID_INTERNSHIP_ERROR = ("Invalid internship! You haven't taken both of the "
                            "final project courses (couldn't determine amount of required credits)")
