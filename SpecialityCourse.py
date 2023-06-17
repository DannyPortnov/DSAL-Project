import Course
import re

class SpecialityCourse(Course):
    "Speciality Course Object Implementation"

    def __init__(self, number, name, points, is_must, computers, signals, devices, pre_courses_list, parallel_course):
        
        super().__init__(self, number, name, points, is_must, pre_courses_list, parallel_course)
        self._specialities = self._set_specialities(computers, signals, devices)  # the specialties in which this course is available
        # self._computers = number_to_condition(computers)
        # self._signals = number_to_condition(signals)
        # self._devices = number_to_condition(devices)

    # set the specialties condition: key = name ; value = must, choice or none
    def _set_specialities(self, computers, signals, devices):
        specialties = dict()
        specialties["Computers"] = translate_condition(computers)
        specialties["Signals"] = translate_condition(signals)
        specialties["Devices"] = translate_condition(devices)
        return specialties

    # returns if a course is Must, Choise or Not in the speciality
    def get_condition_by_speciality(self, speciality):
        return self._specialties[speciality]

    # def get_computers(self):
    #     return self._computers
    
    # def get_signals(self):
    #     return self._signals
    
    # def get_devices(self):
    #     return self._devices

    # we need to assume that each computer's course include: (חומרה) or (תוכנה) in it's name
    def check_if_hw_sw(self):
        pattern = r'\((חומרה|תוכנה)\)'
        matches = re.findall(pattern, self._name)
        if matches:
            matched_words = ", ".join(matches)
            return matched_words
        else:
            return None


# function that converts a condition's value to an actual word
def translate_condition(hebrew_condition):
    if hebrew_condition == "חובה":
        return "Must"
    elif hebrew_condition == "בחירה":
        return "Choice"
    else:
        return None