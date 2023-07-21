from Constants import *


class SpecialityCoursesDB:
    "Speciality Database Object Implementation"

    def __init__(self, name):
        self._name = name
        # key: course number, value: course object
        self._courses = {}

    def get_name(self):
        return self._name

    def add_course(self, course):
        if course.get_speciality_course_type(self._name) != SpecialityCourseType.NA:
            self._courses[course.get_number()] = course

    def get_course(self, number):
        return self._courses.get(number)
