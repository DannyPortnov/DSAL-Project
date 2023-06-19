

from Course import Course
from enum import StrEnum  # Assuming you have Python 3.11 or higher

class Interships(StrEnum):
    INVALID = 'invalid',
    INDUSTRY = 'industry',
    RESEARCH = 'research',
    PROJECT = 'project'

class Speciality(StrEnum):
    INVALID = 'invalid',
    COMPUTERS = 'computers',
    SIGNALS = 'signals',
    DEVICES = 'devices'

class SpecialityCourseType(StrEnum):
    NA = None,
    REQUIRED = 'Must',
    OPTIONAL = 'Choice',

class ComputersSpecialityRequiredCourseType(StrEnum):
    INVALID = 'invalid',
    HW = 'חומרה',
    SW = 'תוכנה',

REQUIRED_COURSE_INDICATOR = "חובה"

OPTIONAL_COURSE_INDICATOR = "בחירה"

SEMESTER_LINE_INDICATOR = "סמסטר"

INVALID_COURSE_DATA_ERROR = "Course's data does not match Syllabus"

COURSE_NUMBER_NOT_FOUND_ERROR = "Course number not found"

def format_parallel_course_error(course:Course, parallel_course:Course):
    """Returns a formatted error message for a parallel course that hasn't been done"""
    return f"You haven't done {course.get_name()}'s parallel course, {parallel_course.get_name()}, in the same semester."

def format_pre_course_error(course:Course, pre_course:Course):
    """Returns a formatted error message for a pre course that hasn't been done"""
    return f"You haven't done {course.get_name}'s pre-course, {pre_course.get_name()}"