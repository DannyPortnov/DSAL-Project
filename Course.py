from __future__ import annotations  # for self reference
from Constants import *
from Constants import format_parallel_course_error


class Course:
    "Course Object Implementation"

    # TODO: need to create str method to class course in order to print: number, points, name

    # def __init__(self, number, points, name, is_must, computers, signals, devices, pre_courses_list, parallel_course):
    def __init__(self, number: int, name: str, points: float, is_must: str,
                 pre_courses_list: list[Course] | None, parallel_course: Course | None):
        self._name = name
        self._number = number
        self._points = points
        # is the course's condition must or choice
        self._set_condition(is_must)  # Sets self._is_must
        # hold the pre-courses that must be taken before this course
        self._pre_courses: dict[Course, None] = {}
        self._set_pre_courses(pre_courses_list)
        # self._specialties = self._set_specialties(computers, signals, devices)  # the specialties in which this course is available
        self._parallel_course = parallel_course
        self._semester_num: int = None  # the semester in which this course was taken
        # in order to check if a student took a course or not- default value is false
        self._was_taken = False

    def get_semester_num(self):
        return self._semester_num

    def get_name(self):
        return self._name

    def set_semester_num(self, semester_num: int):
        self._semester_num = semester_num

    def get_parallel_course(self):
        return self._parallel_course
    # set a pre_course, key = pre_course's Course object

    def _set_pre_courses(self, pre_courses_list: list[Course] | None):
        if pre_courses_list is not None and len(pre_courses_list):
            for course in pre_courses_list:
                self._pre_courses[course] = None

    # set the condition of the course: must or choise

    def _set_condition(self, is_must: str):
        if is_must == REQUIRED_COURSE_INDICATOR:
            self._is_must = True
        self._is_must = False

    def mark_as_taken(self):
        """Mark the course as taken"""
        self._was_taken = True

    # returns the condition of a course: must or choise
    def is_mandatory(self):
        return self._is_must

    def was_taken(self):
        """Returns True if the student took the course, False otherwise"""
        return self._was_taken

    # returns course's points
    def get_points(self):
        return self._points

    # returns course's number
    def get_number(self):
        return self._number

    def is_finished_properly(self) -> tuple[bool, str | None]:
        """Checks if all the pre courses and the parrallel course were taken, 
        this allows to determine if a course was finished properly"""
        if len(self._pre_courses):
            for course in self._pre_courses:
                if course.was_taken() is False:
                    return False, format_pre_course_error(self, course)
        # Check if the parallel course was taken in the same semester
        if self._parallel_course is not None:
            if self._parallel_course.was_taken() is False \
                    or self._parallel_course.get_semester_num() != self._semester_num:
                return False, format_parallel_course_error(self, self._parallel_course)
        return True

    # validate a course by checking it's points, name and number
    def validate_course(self, number: int, points: float, name: str):
        if number == self._number and points == self._points and name == self._name:
            return True
        return False

    def __str__(self):
        return f"Course: {self._number}, {self._name}, {self._points} points"


# function that converts a condition's value to an actual word
def number_to_condition(num: int):
    if num == 1:
        return SpecialityCourseType.REQUIRED
    elif num == 2:
        return SpecialityCourseType.OPTIONAL
    else:
        return None
