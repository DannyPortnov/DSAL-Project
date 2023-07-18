from __future__ import annotations
from typing import Optional  # for self reference
from Constants import *


class Course:
    """ Class for courses """

    def __init__(self, number: int, name: str, points: float, is_must: str,
                 pre_courses: list[int], parallel_course: Optional[int]):
        self._name: str = name.strip()
        self._number: int = number
        self._points: float = points
        # is the course's mandoatory or choise
        self._is_must = True if is_must == REQUIRED_COURSE_INDICATOR else False
        # hold the pre-courses that must be taken before this course
        self._pre_courses: dict[int, Course] = dict.fromkeys(pre_courses, None)
        self._parallel_course: tuple[Optional[int],
                                     Optional[Course]] = (parallel_course, None)
        self._was_taken = False

    def get_name(self) -> str:
        return self._name

    def set_parallel_course(self, course: Course) -> None:
        self._parallel_course = (self._parallel_course[0], course)

    def get_parallel_course(self) -> tuple[Optional[int], Optional[Course]]:
        return self._parallel_course

    def get_pre_courses(self) -> dict[int, Course]:
        return self._pre_courses

    def set_was_taken(self, was_taken: bool) -> None:
        self._was_taken = was_taken

    # returns the condition of a course: must or choise
    def is_mandatory(self) -> bool:
        return self._is_must

    def get_was_taken(self) -> bool:
        """Returns True if the student took the course, False otherwise"""
        return self._was_taken

    # returns course's points
    def get_points(self) -> float:
        return self._points

    # returns course's number
    def get_number(self) -> int:
        return self._number

    def _format_missing_course_error(self, missing_course: Course, missing_course_type: str) -> str:
        return (f"You haven't done {self.get_name()}'s ({self.get_number()}) {missing_course_type},"
                f" {missing_course.get_name()} ({missing_course.get_number()})\n")

    def is_finished_properly(self) -> tuple[bool, str]:
        """Checks if all the pre courses were taken, 
        this allows to determine if a course was finished properly"""
        # courses = [course for C in self._pre_courses if not course.was_taken()]
        is_finished: bool = True
        message: str = ""
        for pre_course in self._pre_courses.values():
            if not pre_course.get_was_taken():
                is_finished = False
                message += self._format_missing_course_error(pre_course, "pre course")
        parallel_course = self.get_parallel_course()[1]
        if parallel_course is not None and not parallel_course.get_was_taken():
            is_finished = False
            message += self._format_missing_course_error(
                parallel_course, "parallel course")
        # If disqualified, will change course to not taken
        self.set_was_taken(is_finished)
        return is_finished, message

    # validate a course by checking it's points, name and number
    def validate_course(self, number: int, points: float, name: str) -> tuple[bool, str]:
        """ Checks if the course's data is valid, if not returns a message with the data that doesn't match the syllabus.

        Args:
            number (`int`): Course's code. Has to be the same as in the syllabus.
            points (`float`): Course's credit points. Doesn't have to be the same as in the syllabus.
            name (`str`): Course's name. Doesn't have to be the same as in the syllabus.

        Returns:
            `tuple[bool, str]`: boolean value is `True` only if the course's code is valid, else `False`.
            If the course's code is invalid, the second value is a message with the data that doesn't match the syllabus.
        """
        if number != self._number:
            return False, INVALID_COURSE_DATA_ERROR
        if number == self._number and points == self._points and name == self._name:
            return True, ""
        points_mismatch = f"Points of course {number} don't match syllabus, expected {self._points} but got {points}\n"
        name_mismatch = f"Name of course {number} doesn't match syllabus, expected {self._name} but got {name}\n"
        result = points_mismatch if points != self._points else ""
        result += name_mismatch if name != self._name else ""
        return True, result

    def __str__(self) -> str:
        return f"{self._number}     {self._points}      {self._name}"

    def __repr__(self) -> str:
        return f"{self._name}"
