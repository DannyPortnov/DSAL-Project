from Course import Course
from Contants import Speciality
import Contants


class SpecialityCoursesDB:
    "Speciality Database Object Implementation"

    def __init__(self, name: Speciality):
        self._name: Speciality = name
        # key: course number, value: course object
        self._courses: dict[int, Course] = {}
        # self._must_courses = dict()      # key: course number, value: course object
        # self._choise_courses = dict()      # key: course number, value: course object

    def get_name(self):
        return self._name

    def add_course(self, course: Course):
        if course.get_speciality(self._name) is None:
            self._courses[course.get_number()] = course

        # if course.get_speciality(self._name) == "Must":
        #     self._must_courses[course.get_number()] = course
        # elif course.get_speciality(self._name) == "Choise":
        #     self._choise_courses[course.get_number()] = course

    def get_course(self, number: int):
        if number in self._courses.keys():
            return self._courses[number]

        # if number in self._must_courses.keys():
        #     return self._must_courses[number]

        # elif number in self._choise_courses.keys():
        #     return self._choise_courses[number]
        return None
