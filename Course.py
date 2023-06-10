from __future__ import annotations  # for self reference


class Course:
    "Course Object Implementation"

    # TODO: need to create str method to class course in order to print: number, points, name

    # def __init__(self, number, points, name, is_must, computers, signals, devices, pre_courses_list, parallel_course):
    def __init__(self, number: int, name: str, points: float, is_must: str, pre_courses_list: list[Course], parallel_course: Course):
        self._name = name
        self._number = number
        self._points = points
        # is the course's condition must or choice
        self._set_condition(is_must)  # Sets self._is_must
        # hold the pre-courses that must be taken before this course
        self._pre_courses = self._set_pre_courses(pre_courses_list)
        # self._specialties = self._set_specialties(computers, signals, devices)  # the specialties in which this course is available
        self._parallel_course = parallel_course
        # in order to check if a student took a course or not- default value is false
        self._is_done = False

    # set a pre_course, key = pre_course's Course object

    def _set_pre_courses(self, pre_courses_list: list[Course]):
        pre_courses = dict()
        if len(pre_courses_list):
            for course in pre_courses_list:
                pre_courses[course] = None
        return pre_courses

    # set the condition of the course: must or choise
    def _set_condition(self, is_must: str):
        if is_must == "חובה":
            self._is_must = True
        self._is_must = False

    # mark if a student took this course
    def mark_as_done(self):
        self._is_done = True

    # returns the condition of a course: must or choise
    def is_mandatory(self):
        return self._is_must

    # returns course's status, if it was taken or not
    def is_done(self):
        return self._is_done

    # returns course's points
    def get_points(self):
        return self._points

    # returns course's number
    def get_number(self):
        return self._number

    # check if the pre courses are finished, this allows to determine if a course was finished properly
    def is_finished_properly(self):
        if len(self._pre_courses):
            for course in self._pre_courses.keys():
                if course.is_done() is False:
                    return False
        return True

    # validate a course by checking it's points, name and number
    def validate_course(self, number: int, points: float, name: str):
        if number == self._number and points == self._points and name == self._name:
            return True
        return False


# function that converts a condition's value to an actual word
def number_to_condition(num: int):
    if num == 1:
        return "Must"
    elif num == 2:
        return "Choice"
    else:
        return None
