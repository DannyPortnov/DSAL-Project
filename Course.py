from Constants import *


class Course:
    """ Class for courses """

    def __init__(self, number, name, points, is_must, pre_courses, parallel_course):
        self._name = name.strip()
        self._number = number
        self._points = points
        # is the course's mandoatory or choise
        self._is_must = True if is_must == REQUIRED_COURSE_INDICATOR else False
        # hold the pre-courses that must be taken before this course
        self._pre_courses = dict.fromkeys(pre_courses, None)
        self._parallel_course = (parallel_course, None)
        self._was_taken = False

    def get_name(self):
        return self._name

    def set_parallel_course(self, course):
        self._parallel_course = (self._parallel_course[0], course)

    def get_parallel_course(self):
        return self._parallel_course

    def get_pre_courses(self):
        return self._pre_courses

    def set_was_taken(self, was_taken):
        self._was_taken = was_taken

    # returns the condition of a course: must or choise
    def is_mandatory(self):
        return self._is_must

    def get_was_taken(self):
        """Returns True if the student took the course, False otherwise"""
        return self._was_taken

    # returns course's points
    def get_points(self):
        return self._points

    # returns course's number
    def get_number(self):
        return self._number

    def _format_missing_course_error(self, missing_course, missing_course_type):
        return (f"You haven't done {self.get_name()}'s ({self.get_number()}) {missing_course_type},"
                f" {missing_course.get_name()} ({missing_course.get_number()})\n")

    def is_finished_properly(self):
        """Checks if all the pre courses were taken, 
        this allows to determine if a course was finished properly"""
        is_finished = True
        message = ""
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
    def validate_course(self, points, name):
        """ Checks if the course's data matches the syllabus.

        Args:
            points (`float`): Course's credit points. 
            name (`str`): Course's name. 

        Returns:
            `str`: Message with the data that doesn't match the syllabus.
        """
        if points == self._points and name == self._name:
            return ""
        points_mismatch = f"Points of course {self._number} don't match syllabus, expected {self._points} but got {points}\n"
        name_mismatch = f"Name of course {self._number} doesn't match syllabus, expected {self._name} but got {name}\n"
        result = points_mismatch if points != self._points else ""
        result += name_mismatch if name != self._name else ""
        return result

    def __str__(self):
        return f"{self._number}     {self._points}      {self._name}"

    def __repr__(self):
        return f"{self._name}"
