from typing import Union
from Course import Course
from Constants import *
from SpecialityCourse import SpecialityCourse


class SpecialityCoursesDB:
    "Speciality Database Object Implementation"

    def __init__(self, name: Speciality):
        self._name: Speciality = name
        # key: course number, value: course object
        self._courses: dict[int, SpecialityCourse] = {}

    def get_name(self) -> Speciality:
        return self._name

    def add_course(self, course: SpecialityCourse) -> None:
        if course.get_speciality_course_type(self._name) != SpecialityCourseType.NA:
            self._courses[course.get_number()] = course

    def get_course(self, number: int) -> Union[SpecialityCourse, None]:
        return self._courses.get(number)
