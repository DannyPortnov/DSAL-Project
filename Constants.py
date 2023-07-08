

from Course import Course
# from enum import StrEnum  # Assuming you have Python 3.11 or higher
from enum import Enum, auto

class Interships(Enum):
    INVALID = auto(),
    INDUSTRY = auto(),
    RESEARCH = auto(),
    PROJECT = auto()

class Speciality(Enum):
    INVALID = auto(),
    COMPUTERS = auto(),
    SIGNALS = auto(),
    DEVICES = auto()

class SpecialityType(Enum):
    MAJOR = auto(),
    MINOR = auto()

class SpecialityCourseType(Enum):
    NA = auto(),
    REQUIRED = auto(),
    OPTIONAL = auto()

class ComputersSpecialityRequiredCourseType(str, Enum):
    HW = '(חומרה)',
    SW = '(תוכנה)'

REQUIRED_COURSE_INDICATOR = "חובה"

OPTIONAL_COURSE_INDICATOR = "בחירה"

SEMESTER_LINE_INDICATOR = "סמסטר"

INVALID_COURSE_DATA_ERROR = "Course's data does not match Syllabus"

COURSE_NUMBER_NOT_FOUND_ERROR = "Course number not found"

def format_pre_course_error(course:Course, pre_course:Course):
    """Returns a formatted error message for a pre course that hasn't been done"""
    return f"You haven't done {course.get_name}'s pre-course, {pre_course.get_name()}"