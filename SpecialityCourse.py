from typing import Optional
from Constants import *
from Course import Course
import re


class SpecialityCourse(Course):
    "Speciality Course Object Implementation"

    def __init__(self, number: int, name: str, points: float, is_must: str,
                 computers, signals, devices, pre_courses_list: list[Course] | None ) -> None:

        super().__init__(number, name, points, is_must, pre_courses_list)
        # the specialties in which this course is available
        self._specialities: dict[Speciality, SpecialityCourseType] = {}
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
    def get_speciality_course_type(self, speciality: Speciality) -> SpecialityCourseType:
        """ Returns if the course is required, optional or not in the speciality

        Args:
            speciality (`Speciality`): The speciality the course is checked for

        Returns:
            SpecialityCourseType: The course type in the speciality
        """
        return self._specialities[speciality]

    # def get_computers(self):
    #     return self._computers

    # def get_signals(self):
    #     return self._signals

    # def get_devices(self):
    #     return self._devices

    # we need to assume that each computer's course include: (חומרה) or (תוכנה) in it's name
    def check_if_hw_sw(self) -> Optional[ComputersSpecialityRequiredCourseType]:
        for course_type in ComputersSpecialityRequiredCourseType:
            if course_type.value in self._name:
                return course_type
        return None
            


# function that converts a condition's value to an actual word
def translate_condition(hebrew_condition: str) -> SpecialityCourseType:
    if hebrew_condition == REQUIRED_COURSE_INDICATOR:
        return SpecialityCourseType.REQUIRED
    elif hebrew_condition == OPTIONAL_COURSE_INDICATOR:
        return SpecialityCourseType.OPTIONAL
    return SpecialityCourseType.NA
        
