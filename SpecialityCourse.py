import Course

class SpecialityCourse(Course):
    "Course Object Implementation"

    def __init__(self, number, points, name, is_must, computers, signals, devices, pre_courses_list, parallel_course):
        
        super().__init__(self, number, points, name, is_must, pre_courses_list, parallel_course)
        self._specialities = self._set_specialities(computers, signals, devices)  # the specialties in which this course is available
        # self._computers = number_to_condition(computers)
        # self._signals = number_to_condition(signals)
        # self._devices = number_to_condition(devices)

    # set the specialties condition: key = name ; value = must, choice or none
    def _set_specialities(self, computers, signals, devices):
        specialties = dict()
        specialties["computers"] = number_to_condition(computers)
        specialties["signals"] = number_to_condition(signals)
        specialties["devices"] = number_to_condition(devices)
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

# function that converts a condition's value to an actual word
def number_to_condition(num):
    if num == 1:
        return "Must"
    elif num == 2:
        return "Choice"
    else:
        return None