from typing import Optional
from Constants import *
from Course import Course
import re


class SpecialityCourse(Course):
    "Speciality Course Object Implementation"

    def __init__(self, number, name, points, is_must,
                 computers, signals, devices, pre_courses) -> None:

        super().__init__(number, name, points, is_must, pre_courses, parallel_course=None)
        # the specialties in which this course is available
        self._specialities = {}
        self._set_specialities(computers, signals, devices)
        # self._computers = number_to_condition(computers)
        # self._signals = number_to_condition(signals)
        # self._devices = number_to_condition(devices)

    # set the specialties condition: key = name ; value = must, choice or none
    def _set_specialities(self, computers, signals, devices) -> None:
        # TODO: maybe move inside __init__
        self._specialities[Speciality.COMPUTERS] = translate_condition(computers)
        self._specialities[Speciality.SIGNALS] = translate_condition(signals)
        self._specialities[Speciality.DEVICES] = translate_condition(devices)

    #
    def get_speciality_course_type(self, speciality):
        """ Returns if the course is required, optional or not in the speciality

        Args:
            speciality (`Speciality`): The speciality the course is checked for

        Returns:
            SpecialityCourseType: The course type in the speciality
        """
        return self._specialities[speciality]

    # we need to assume that each computer's course include: (חומרה) or (תוכנה) in it's name
    def check_if_hw_sw(self):
        for course_type in ComputersCourseType:
            if course_type.value in self._name:
                return course_type
        return None


# function that converts a condition's value to an actual word
def translate_condition(hebrew_condition):
    if hebrew_condition == REQUIRED_COURSE_INDICATOR:
        return SpecialityCourseType.REQUIRED
    elif hebrew_condition == OPTIONAL_COURSE_INDICATOR:
        return SpecialityCourseType.OPTIONAL
    return SpecialityCourseType.NA
