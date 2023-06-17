from Constants import *
from Course import Course
import re


class SpecialityCourse(Course):
    "Speciality Course Object Implementation"

    def __init__(self, number, name, points, is_must, computers, signals, devices, pre_courses_list, parallel_course) -> None:

        super().__init__(self, number, name, points, is_must, pre_courses_list, parallel_course)
        # the specialties in which this course is available
        self._specialities: dict[Speciality, SpecialityCourseType] = {}
        self._set_specialities(computers, signals, devices)
        # self._computers = number_to_condition(computers)
        # self._signals = number_to_condition(signals)
        # self._devices = number_to_condition(devices)

    # set the specialties condition: key = name ; value = must, choice or none
    def _set_specialities(self, computers, signals, devices):
        # TODO: maybe move inside __init__
        self._specialities[Speciality.COMPUTERS] = translate_condition(computers)
        self._specialities[Speciality.SIGNALS] = translate_condition(signals)
        self._specialities[Speciality.DEVICES] = translate_condition(devices)

    # returns if a course is Must, Choise or Not in the speciality
    def get_condition_by_speciality(self, speciality):
        return self._specialities[speciality]

    # def get_computers(self):
    #     return self._computers

    # def get_signals(self):
    #     return self._signals

    # def get_devices(self):
    #     return self._devices

    # we need to assume that each computer's course include: (חומרה) or (תוכנה) in it's name
    def check_if_hw_sw(self):
        pattern = fr'\(({ComputersSpecialityRequiredCourseType.HW}|{ComputersSpecialityRequiredCourseType.SW})\)'
        matches = re.findall(pattern, self._name)
        if matches:
            matched_words = ", ".join(matches)
            return matched_words
        else:
            return None


# function that converts a condition's value to an actual word
def translate_condition(hebrew_condition):
    if hebrew_condition == REQUIRED_COURSE_INDICATOR:
        return SpecialityCourseType.MUST
    elif hebrew_condition == CHOISE_COURSE_INDICATOR:
        return SpecialityCourseType.CHOISE
    else:
        return SpecialityCourseType.INVALID
