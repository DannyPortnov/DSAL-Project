from io import TextIOWrapper
from typing import Generator, Optional
import re
from Course import Course
from SyllabusDB import SyllabusDB
from Constants import *
from unittest.mock import MagicMock
from SpecialityCourse import SpecialityCourse
from itertools import cycle


class Student:
    "Student Object Implementation"

    def __init__(self, file_name: str, syllabus_db: SyllabusDB):
        # def __init__(self, name, id, major, minor, general_points, sport_points):
        self._file_name = file_name
        self._syllabus_db = syllabus_db
        self._name: str = None
        self._id: int = None
        self._major: Optional[Speciality] = None
        self._minor: Optional[Speciality] = None
        self._general_points: int = None
        self._sport_points: int = None

        # holds the type of internship that the student chose
        self._internship_type: Optional[Interships] = None

        # store the minimum points in order to finish the degree
        self._required_credits: dict[CourseType, float] = {
            type: 0 for type in CourseType}
        # self._required_mandatory_points: int = None
        # self._required_major_points: int = None
        # self._required_minor_points: int = None
        # self._required_external_points: int = None

        # TODO: maybe to change the way we store this data
        # store the required number of must courses the student need to take in major and minor specialities
        self._spc_must_courses_req: dict[CourseType, int |
                                         dict[ComputersCourseType, int]] = {
            CourseType.MAJOR: 0,
            CourseType.MINOR: 0
        }

        # calculate the amount of points the student got
        self._credits_taken: dict[CourseType, float] = {type: 0 for type in CourseType}

        # count how many must speciality courses the student took
        self._spc_must_courses_taken: dict[CourseType, int |
                                           dict[ComputersCourseType, int]] = {
            CourseType.MAJOR: 0,
            CourseType.MINOR: 0
        }

        # key: course number, value: course object
        self._mandatory_courses: dict[int, Course] = {}
        # key: course number, value: course object
        self._speciality_courses: dict[CourseType, list[SpecialityCourse] | dict[SpecialityCourseType, list[SpecialityCourse]]] = {
            CourseType.MAJOR: {
                type: [] for type in SpecialityCourseType
            },
            CourseType.MINOR: {
                type: [] for type in SpecialityCourseType
            },
            CourseType.EXTERNAL: []
        }

        # Holds all the courses that were counted in the major or minor already
        self._shared_courses: list[SpecialityCourse] = []

        # self._external_courses: list[SpecialityCourse] = []

        # key: course, value: why course is invalid
        self._invalid_courses: dict[Course | int, str] = {}
        # TODO: print somewhen the invalid courses
        self.read_student_data()

    def set_name(self, name):
        self._name = name

    def set_id(self, id: str):
        self._id = id

    def set_major(self, major: str) -> None:
        # TODO: Find out if we need to check if the major is valid
        self._major = Speciality[major.upper()]
        if self._major == Speciality.COMPUTERS:
            self._spc_must_courses_taken[CourseType.MAJOR] = {
                ComputersCourseType.SW: 0, ComputersCourseType.HW: 0, ComputersCourseType.TOTAL: 0}
            self._spc_must_courses_req[CourseType.MAJOR] = {
                ComputersCourseType.SW: 0, ComputersCourseType.HW: 0, ComputersCourseType.TOTAL: 0}

    def set_minor(self, minor: str) -> None:
        # TODO: Find out if we need to check if the minor is valid
        self._minor = Speciality[minor.upper()]
        if self._minor == Speciality.COMPUTERS:
            self._spc_must_courses_taken[CourseType.MINOR] = {
                ComputersCourseType.SW: 0, ComputersCourseType.HW: 0, ComputersCourseType.TOTAL: 0}
            self._spc_must_courses_req[CourseType.MINOR] = {
                ComputersCourseType.SW: 0, ComputersCourseType.HW: 0, ComputersCourseType.TOTAL: 0}

    def set_general_points(self, general_points: str) -> None:
        self._general_points = int(general_points)

    def set_sport_points(self, sport_points: str) -> None:
        self._sport_points = int(sport_points)

    def add_course(self, course: SpecialityCourse | Course) -> None:
        """ Add a course to the student's taken courses.

        Args:
            course (`SpecialityCourse` | `Course`): Course to add
        """
        if type(course) is SpecialityCourse:
            course_type_in_major = course.get_speciality_course_type(self._major)
            course_type_in_minor = course.get_speciality_course_type(self._minor)
            self._speciality_courses[CourseType.MAJOR][course_type_in_major].append(
                course)
            self._speciality_courses[CourseType.MINOR][course_type_in_minor].append(
                course)
            if course_type_in_major == SpecialityCourseType.NA and course_type_in_minor == SpecialityCourseType.NA:
                self._speciality_courses[CourseType.EXTERNAL].append(course)
        else:
            self._mandatory_courses[course.get_number()] = course
        course.mark_as_taken()

    # add a course object to the stduent's dict of invlid courses

    def remove_from_courses(self, course: Course, message: str):
        """Remove a course from the student's taken courses.

        Args:
            course (Course): course to remove
            message (str): reason for removing the course
        """
        self._invalid_courses[course] = message
        if type(course) is SpecialityCourse:
            for speciality_type in self._speciality_courses:
                for speciality in Speciality:
                    course_type_in_speciality = course.get_speciality_course_type(
                        speciality)
                    if isinstance(self._speciality_courses[speciality_type], dict) \
                            and (course in self._speciality_courses[speciality_type][course_type_in_speciality]):
                        self._speciality_courses[speciality_type][course_type_in_speciality].remove(
                            course)
                    elif course in self._speciality_courses[speciality_type]:
                        self._speciality_courses[speciality_type].remove(course)

        else:  # is mandatory course
            self._mandatory_courses.pop(course.get_number())

    def _check_all_courses_were_finished_properly(self) -> None:
        """Ensure that all taken courses were finished properly.
        """
        all_courses: dict[int, Course | SpecialityCourse] = {**self._mandatory_courses}
        for _, inner_item in self._speciality_courses.items():
            if isinstance(inner_item, dict):
                for _, speciality_courses in inner_item.items():
                    for course in speciality_courses:
                        all_courses[course.get_number()] = course
            else:
                for course in inner_item:
                    all_courses[course.get_number()] = course
        for course in all_courses.values():
            is_finished, reason_if_not = course.is_finished_properly()
            if not is_finished and reason_if_not is not None:
                self.remove_from_courses(course, reason_if_not)

    def read_student_data(self):
        with open(self._file_name, "r", encoding="utf-8") as file:
            # TODO: Put all of this in __init__ ?
            line = next(self._ignore_comments_and_empty_lines(file))
            self.set_name(extract_student_data_from_line(line))
            line = next(self._ignore_comments_and_empty_lines(file))
            self.set_id(extract_student_data_from_line(line))
            line = next(self._ignore_comments_and_empty_lines(file))
            self.set_major(extract_student_data_from_line(line))
            line = next(self._ignore_comments_and_empty_lines(file))
            self.set_minor(extract_student_data_from_line(line))
            line = next(self._ignore_comments_and_empty_lines(file))
            self.set_general_points(extract_student_data_from_line(line))
            line = next(self._ignore_comments_and_empty_lines(file))
            self.set_sport_points(extract_student_data_from_line(line))

            # When Generator depletes, next() returns None
            while (line := next(self._ignore_comments_and_empty_lines(file), None)) != None:
                course_number, credit, name = extract_course_data_from_line(line)
                # TODO: make prettier
                try:
                    course = self._syllabus_db.get_course_by_number(course_number)
                except ValueError:
                    self._invalid_courses[course_number] = INVALID_COURSE_DATA_ERROR
                    continue
                if course.validate_course(course_number, credit, name):
                    self.add_course(course)
                else:
                    self._invalid_courses[course] = INVALID_COURSE_DATA_ERROR

    def _ignore_comments_and_empty_lines(self, file: TextIOWrapper) -> Generator[str, None, None]:
        for line in file:
            if not line.startswith("#") and line != '\n':
                yield line.strip()

    # def _resume_ignore_comments(self, file: Generator[str, None, None]):
    #     for line in file:
    #         if line.startswith("#") and contants.SEMESTER_LINE_INDICATOR in line:
    #             yield True
    #         elif not line.startswith("#"):
    #             yield line.strip()

  # TODO: maybe return a message and write it to the file: wether student is missing points or exceeding the limit

    def check_sport_points(self):
        if self._sport_points == self._syllabus_db.get_sport_points():
            return True
        return False

    # updates the type of internship that the student chose
    def update_internship_type(self):
        # check if project is internship in the idustry
        if (31054 in self._mandatory_courses) and (31055 in self._mandatory_courses):
            # if self._internship_type is None:
            self._internship_type = Interships.INDUSTRY

        # check if project is research in the college
        elif (31052 in self._mandatory_courses) and (31053 in self._mandatory_courses):
            # check if the project type had already updated, if so- the student did not report the project courses correctly
            # if self._internship_type is None:
            self._internship_type = Interships.RESEARCH

        # check if project is mini_project in the college
        elif (31050 in self._mandatory_courses) and (31051 in self._mandatory_courses):
            # check if the project type had already updated, if so- the student did not report the project courses correctly
            # if self._internship_type is None:
            self._internship_type = Interships.PROJECT
        else:
            return INVALID_INTERSHIP_ERROR
        self.update_required_data()
        if self._internship_type == Interships.INDUSTRY:
            del self._required_credits[CourseType.MINOR]
            # Remove minor speciality from the student's credit count
            del self._credits_taken[CourseType.MINOR]
            # Move all minor courses to major
            for course_type in self._speciality_courses[CourseType.MINOR]:
                if course_type in self._speciality_courses[CourseType.MAJOR]:
                    self._speciality_courses[CourseType.MAJOR][course_type] += self._speciality_courses[CourseType.MINOR][course_type]
                else:
                    self._speciality_courses[CourseType.MAJOR][course_type] = self._speciality_courses[CourseType.MINOR][course_type]
            del self._speciality_courses[CourseType.MINOR]

    def update_mandatory_points(self):
        # for course in self._mandatory_courses.values():
        #     self._credit_taken[CourseType.MANDATORY] += course.get_points()
        self._credits_taken[CourseType.MANDATORY] = sum(
            course.get_points() for course in self._mandatory_courses.values()) + self._sport_points + self._general_points

    def get_intersecting_courses(self, minor_course_type: SpecialityCourseType,
                                 major_course_type: SpecialityCourseType) -> set[SpecialityCourse]:
        """
            Returns the common speciality courses between major and minor based on the specified types.

            Args:
                minor_type (`SpecialityCourseType`): The speciality course type for the minor speciality.
                major_type (`SpecialityCourseType`): The speciality course type for the major speciality.

            Returns:
                `set[SpecialityCourse]`: The intersection of speciality courses based on the specified types.
        """
        major_courses = self._speciality_courses[CourseType.MAJOR][major_course_type]
        if CourseType.MINOR not in self._speciality_courses:
            return set(major_courses)
        minor_courses = self._speciality_courses[CourseType.MINOR][minor_course_type]
        return set(minor_courses).intersection(major_courses)

    # method for updating the student's point in speciality

    def update_speciality_points(self):
        # update required courses in major and minor
        self.update_only_in_major_and_must_courses(
            self.get_intersecting_courses(major_course_type=SpecialityCourseType.REQUIRED,
                                          minor_course_type=SpecialityCourseType.NA))  # required in major
        if self._internship_type == Interships.RESEARCH or self._internship_type == Interships.PROJECT:
            self.update_only_in_minor_and_must_courses(
                self.get_intersecting_courses(minor_course_type=SpecialityCourseType.REQUIRED,
                                              major_course_type=SpecialityCourseType.NA))  # required in minor
            self.update_major_must_minor_optional_courses(
                self.get_intersecting_courses(major_course_type=SpecialityCourseType.REQUIRED,
                                              minor_course_type=SpecialityCourseType.OPTIONAL))   # required in major
            self.update_minor_must_major_optional_courses(
                self.get_intersecting_courses(major_course_type=SpecialityCourseType.OPTIONAL,
                                              minor_course_type=SpecialityCourseType.REQUIRED))   # required in minor
            self.update_major_must_minor_must_courses(
                self.get_intersecting_courses(major_course_type=SpecialityCourseType.REQUIRED,
                                              minor_course_type=SpecialityCourseType.REQUIRED))     # required in major or minor

        # update external points
        self.update_external_points()

        # update Choice courses in major only and minor only
        self._update_speciality_optional_courses_only(
            self.get_intersecting_courses(major_course_type=SpecialityCourseType.OPTIONAL,
                                          minor_course_type=SpecialityCourseType.NA), CourseType.MAJOR)  # required in major
        if self._internship_type == Interships.RESEARCH or self._internship_type == Interships.PROJECT:
            self._update_speciality_optional_courses_only(
                self.get_intersecting_courses(major_course_type=SpecialityCourseType.NA,
                                              minor_course_type=SpecialityCourseType.OPTIONAL), CourseType.MINOR)  # required in minor
        self._shared_courses += self.get_intersecting_courses(major_course_type=SpecialityCourseType.OPTIONAL,
                                                              minor_course_type=SpecialityCourseType.OPTIONAL)  # Add shared optional courses to shared courses
        # at this point, we check the following requirements:
        # 1. we checked the required courses requirements in major and minor and calculated it accordingly.
        # 2. we calculated the optional courses that are available in major only and minor only accordingly.
        # 3. we calculated the courses that can fit only in external speciality
        # 3. after those steps, we are left with the courses that can fit into each speciality: major/minor/external.
        #    we will put the courses in such way that we calculated the points of each speciality and try to get to it's limit
        # update points by using the courses that have left
        self.update_major_minor_shared_courses_points()

    # method that updates the required course in computers speciality, with respect to it's kind: Hardware or Software
    # def update_major_minor_computers_required_points(self, course, required_count):
    #     is_hw_sw = course.check_if_hw_sw()
    #     if is_hw_sw is not None:
    #         required_count[is_hw_sw] += 1
    #     else:
    #         required_count += 1

    # TODO: in each update major/minor/external course method, need to add:  else: self.add_invalid_course(...)
    # this is for a situation when a course had not finished properly

    #
    def update_only_in_major_and_must_courses(
            self, only_major_must: set[SpecialityCourse]) -> None:
        """ 
            Update the points of the courses that are required in the major but not available in the minor.
            This method filters the speciality courses that are required only in the major speciality
            and not available in the minor speciality. It updates the count of major required courses
            taken by the student and increments the major points accordingly. If the major points exceed
            the required major points, the excess points are added to the external points.
        """

        for course in only_major_must:
            #     check if the course is MUST in Hardware or Software
            #     update a counter for amount of HW/SW courses that was taken
            # we can check if the course belongs to HW or SW
            if self._credits_taken[CourseType.MAJOR] < self._required_credits[CourseType.MAJOR]:
                if self._major == Speciality.COMPUTERS:
                    # we need to assume that each computers' course name's indicate if it's HW or SW
                    if (is_hw_sw := course.check_if_hw_sw()) is not None:
                        self._spc_must_courses_taken[CourseType.MAJOR][is_hw_sw] += 1
                        self._spc_must_courses_taken[CourseType.MAJOR][ComputersCourseType.TOTAL] += 1
                    # else:
                    #     self._major_required_count += 1
                    # # self.update_major_minor_computers_required_points(course, self._major_required_count)
                else:
                    self._spc_must_courses_taken[CourseType.MAJOR] += 1
                self._credits_taken[CourseType.MAJOR] += course.get_points()
            # this course is available only in this speciality, if we exceed the number of points
            # for this major, we will put the course in external_points
            else:
                self._credits_taken[CourseType.EXTERNAL] += course.get_points()

    # update the points of minor's Must courses by using the courses that are available in the minor only

    def update_only_in_minor_and_must_courses(
            self, only_minor_must: set[SpecialityCourse]) -> None:
        for course in only_minor_must:
            if self._credits_taken[CourseType.MINOR] < self._required_credits[CourseType.MINOR]:
                if self._minor == Speciality.COMPUTERS:
                    # we need to assume that each computers' course name's indicate if it's HW or SW
                    if (is_hw_sw := course.check_if_hw_sw()) is not None:
                        self._spc_must_courses_taken[CourseType.MINOR][is_hw_sw] += 1
                        self._spc_must_courses_taken[CourseType.MINOR][ComputersCourseType.TOTAL] += 1
                    # else:
                    #     self._required_count[SpecialityType.MINOR] += 1
                    # self.update_major_minor_computers_required_points(course, self._required_count[SpecialityType.MINOR])
                else:
                    self._spc_must_courses_taken[CourseType.MINOR] += 1
                self._credits_taken[CourseType.MINOR] += course.get_points()
            # this course is available only in this speciality, if we exceed the number of points
            # for this minor, we will put the course in external_points
            else:
                self._credits_taken[CourseType.EXTERNAL] += course.get_points()

    def _update_must_credit_taken(
        self, course_type: CourseType,
            speciality: Speciality, courses: set[SpecialityCourse]) -> None:
        """
        Check if the student has taken enough required courses in the major.
        """
        max_computers_additional_courses: int = 0
        for course in courses:

            if speciality == Speciality.COMPUTERS:
                if course_type == CourseType.MINOR:
                    max_computers_additional_courses = 1
                is_hw_sw = course.check_if_hw_sw()
                if is_hw_sw is not None:
                    if (self._spc_must_courses_taken[course_type][is_hw_sw] <
                            self._spc_must_courses_req[course_type][is_hw_sw] +
                        max_computers_additional_courses
                        and self._spc_must_courses_taken[course_type][ComputersCourseType.TOTAL] <
                            self._spc_must_courses_req[course_type][ComputersCourseType.TOTAL] +
                            max_computers_additional_courses
                            and self._credits_taken[course_type] < self._required_credits[course_type]):
                        self._spc_must_courses_taken[course_type][is_hw_sw] += 1
                        self._spc_must_courses_taken[course_type][ComputersCourseType.TOTAL] += 1
                        self._credits_taken[course_type] += course.get_points()
                    else:
                        # major have enough required courses, we will decide later where to put this course by checking it's credit points
                        self._shared_courses.append(course)
            else:
                if (self._spc_must_courses_taken[course_type] < self._spc_must_courses_req[course_type]
                        and self._credits_taken[course_type] < self._required_credits[course_type]):
                    self._spc_must_courses_taken[course_type] += 1
                    self._credits_taken[course_type] += course.get_points()
                else:
                    # major have enough required courses, we will decide later where to put this course by checking it's credit points
                    self._shared_courses.append(course)

    # update the major points if it doesn't have enough required courses

    def update_major_must_minor_optional_courses(
            self, major_must_minor_optional: set[SpecialityCourse]) -> None:
        # major doesn't have enough required courses, and student didn't exceed amount of major points
        self._update_must_credit_taken(
            CourseType.MAJOR, self._major, major_must_minor_optional)

    # update the minor points if it doesn't have enough required courses

    def update_minor_must_major_optional_courses(
            self, minor_must_major_optional: set[SpecialityCourse]) -> None:
        # minor doesn't have enough required courses, and student didn't exceed amount of minor points
        self._update_must_credit_taken(
            CourseType.MINOR, self._minor, minor_must_major_optional)

    # update major and minor points by checking if they have enough required courses.

    def update_major_must_minor_must_courses(
            self, major_must_minor_must_courses: set[SpecialityCourse]) -> None:
        for course in major_must_minor_must_courses:
            # TODO: need to have another condition if it's computers speciality.
            if self._major == Speciality.COMPUTERS:
                is_hw_sw = course.check_if_hw_sw()
                # we need to assume that each computers' course name's indicate if it's HW or SW
                if is_hw_sw is not None:
                    # TODO: change the number to constant, computers need at least 1 HW and 1 SW courses if it's minor
                    # major doesn't have enough required courses, minor does have
                    if (self._spc_must_courses_taken[CourseType.MAJOR][is_hw_sw] <
                        self._spc_must_courses_req[CourseType.MAJOR][is_hw_sw]
                            and self._credits_taken[CourseType.MINOR] >= self._required_credits[CourseType.MINOR]):
                        self._spc_must_courses_taken[CourseType.MAJOR][is_hw_sw] += 1
                        self._credits_taken[CourseType.MAJOR] += course.get_points()
                    # minor doesn't have enough required courses, major does have
                    elif (self._spc_must_courses_taken[CourseType.MAJOR][is_hw_sw] >=
                          self._spc_must_courses_req[CourseType.MAJOR][is_hw_sw]
                          and self._credits_taken[CourseType.MINOR] < self._required_credits[CourseType.MINOR]):
                        self._spc_must_courses_taken[CourseType.MINOR] += 1
                        self._credits_taken[CourseType.MINOR] += course.get_points()
                    # major and minor have enough required courses, we will decide later
                    # where to put this course by checking it's credit points
                    else:
                        self._shared_courses.append(course)

            elif self._minor == Speciality.COMPUTERS:
                # we need to assume that each computers' course name's indicate if it's HW or SW
                is_hw_sw = course.check_if_hw_sw()
                if is_hw_sw is not None:
                    # TODO: change the number to constant, computers need at least 1 HW and 1 SW courses if it's minor
                    # major doesn't have enough required courses, minor does have
                    # TODO: NEED TO CHECK ALSO IF REACHED TO 3 MUST COURSES IN MINOR
                    if (self._spc_must_courses_taken[CourseType.MAJOR] <
                        self._spc_must_courses_req[CourseType.MAJOR]
                            and self._spc_must_courses_taken[CourseType.MINOR][is_hw_sw] >=
                            self._spc_must_courses_req[CourseType.MINOR][is_hw_sw]):
                        self._spc_must_courses_taken[CourseType.MAJOR] += 1
                        self._credits_taken[CourseType.MAJOR] += course.get_points()
                    # minor doesn't have enough required courses, major does have
                    elif (self._spc_must_courses_taken[CourseType.MAJOR] >= self._spc_must_courses_req[CourseType.MAJOR]
                          and self._spc_must_courses_taken[CourseType.MINOR][is_hw_sw] <
                          self._spc_must_courses_req[CourseType.MINOR][is_hw_sw]):
                        self._spc_must_courses_taken[CourseType.MINOR][is_hw_sw] += 1
                        self._credits_taken[CourseType.MINOR] += course.get_points()
                    # major and minor have enough required courses, we will decide later
                    # where to put this course by checking it's credit points
                    else:
                        self._shared_courses.append(course)

            else:
                # major doesn't have enough required courses, minor does have
                if (self._spc_must_courses_taken[CourseType.MAJOR] < self._spc_must_courses_req[CourseType.MAJOR]
                        and self._spc_must_courses_taken[CourseType.MINOR] >= self._spc_must_courses_req[CourseType.MINOR]):
                    self._spc_must_courses_taken[CourseType.MAJOR] += 1
                    self._credits_taken[CourseType.MAJOR] += course.get_points()
                # minor doesn't have enough required courses, major does have
                elif (self._spc_must_courses_taken[CourseType.MAJOR] >= self._spc_must_courses_req[CourseType.MAJOR]
                      and self._spc_must_courses_taken[CourseType.MINOR] < self._spc_must_courses_req[CourseType.MINOR]):
                    self._spc_must_courses_taken[CourseType.MINOR] += 1
                    self._credits_taken[CourseType.MINOR] += course.get_points()
                # minor and major doesn't have enough required courses, by default we will update the required course in the major
                elif (self._spc_must_courses_taken[CourseType.MAJOR] < self._spc_must_courses_req[CourseType.MAJOR]
                      and self._spc_must_courses_taken[CourseType.MINOR] < self._spc_must_courses_req[CourseType.MINOR]):
                    self._spc_must_courses_taken[CourseType.MINOR] += 1
                    self._credits_taken[CourseType.MINOR] += course.get_points()
                # major and minor have enough required courses, we will decide later
                # where to put this course by checking it's credit points
                else:
                    self._shared_courses.append(course)

    def _update_speciality_optional_courses_only(
            self, only_in_speciality_and_optional_courses: set[SpecialityCourse], course_type: CourseType) -> None:
        for course in only_in_speciality_and_optional_courses:
            if self._credits_taken[course_type] < self._required_credits[course_type]:
                self._credits_taken[course_type] += course.get_points()
            # this course is available only in this speciality, if we exceed the number of points
            # for this speciality, we will put the course in external_points
            else:
                self._credits_taken[CourseType.EXTERNAL] += course.get_points()

    # update the points of external speciality by using the courses that are not available in major and minor

    def update_external_points(self) -> None:
        # TODO: make prettier later :)
        for course in self._speciality_courses[CourseType.EXTERNAL]:
            self._credits_taken[CourseType.EXTERNAL] += course.get_points()

    # here we update points of major, minor and external specialities by using the rest of the courses that have left.

    def update_major_minor_shared_courses_points(self) -> None:

        def filter_credits_taken() -> dict[CourseType, float]:
            return {
                type: self._credits_taken[type] for type in self._credits_taken if (
                    self._required_credits[type] > self._credits_taken[type])}

        if len(self._shared_courses) == 0:
            return
        course_items: list[tuple[SpecialityCourse, float]] = [(course, course.get_points())
                                                              for course in self._shared_courses]
        capacities = [diff for type in self._required_credits if (
            diff := self._required_credits[type] - self._credits_taken[type]) > 0]
        # Create buckets only of credits that aren't satisfied
        sacks: list[list[tuple[SpecialityCourse, float]]] = [[]
                                                             for _ in range(len(capacities))]
        capacities.sort()  # ascending order
        courses_that_didnt_fit: dict[SpecialityCourse,
                                     None] = {}  # ONLY DICTIONARY WORKS HERE !!!
        while len(course_items) != 0:
            current_course = course_items[-1]
            sacks_benefits: list[tuple[float, int]] = []
            for sack_index, sack in enumerate(sacks):
                benefit = round(capacities[sack_index] / current_course[1], 2)
                sacks_benefits.append((benefit, sack_index))
            sacks_benefits.sort(key=lambda x: x[0], reverse=True)
            # if best_benefit < benefit and best_sack_index not in current_course[2]:
            #     best_benefit = benefit
            #     best_sack_index = j
            for benefit, sack_index in sacks_benefits:
                if current_course[1] <= capacities[sack_index]:
                    sacks[sack_index].append(current_course)
                    course_items.remove(current_course)
                    capacities[sack_index] -= current_course[1]
                    break
            if current_course not in course_items:
                continue
            courses_that_didnt_fit[current_course[0]] = None
            course_items.remove(current_course)
            if len(course_items) == len(courses_that_didnt_fit):
                break

        filtered_credits_taken = filter_credits_taken()
        for type, sack in zip(filtered_credits_taken, sacks):
            self._credits_taken[type] += sum(item[1] for item in sack)
        filtered_credits_taken = filter_credits_taken()  # Continue checkings this

        # Check what happens if we have more than 1 type that doesn't have enough credits
        for type in cycle(filtered_credits_taken):
            if len(courses_that_didnt_fit) != 0:
                self._credits_taken[type] += courses_that_didnt_fit.popitem()[0].get_points()
            else:
                break

    def update_required_data(self) -> None:
        required_points: tuple[int, int, int, int] = self._syllabus_db.get_required_points(
            self._internship_type)
        required_courses_needed: tuple = self._syllabus_db.get_total_required_courses(
            self._internship_type, self._major, self._minor)
        for credit_type, credit in zip(self._required_credits.keys(), required_points):
            self._required_credits[credit_type] = credit
        for course_type, course_count in zip(self._spc_must_courses_req.keys(), required_courses_needed):
            if isinstance(self._spc_must_courses_req[course_type], dict):
                for course_type_and_amount in zip(ComputersCourseType.__members__.values(), course_count):
                    self._spc_must_courses_req[course_type][
                        course_type_and_amount[0]] = course_type_and_amount[1]
            else:
                self._spc_must_courses_req[course_type] = course_count[0]

    # check if student has enough mandatory points
    # TODO: maybe change the parameters that this method returns

    def validate_credit(self) -> str:
        """ Checks if the student has enough credit of each type.

        Returns:
            bool: True if the student has enough credit of each type, False otherwise.
        """
        # TODO: check this function
        # TODO: maybe exclude mandatory points from this function
        messages: str = ""
        for credit_type, credit in self._required_credits.items():
            if self._credits_taken[credit_type] < credit:
                messages += f"You need to take {credit - self._credits_taken[credit_type]} more {credit_type.name.lower()} credit\n"
        return messages if len(messages) > 0 else "You have enough credit"

    # check if the students is allowed to finish the degree

    def _get_invalid_courses(self) -> Optional[str]:
        if len(self._invalid_courses) > 0:
            messages = ""
            for message in self._invalid_courses.values():
                messages += message + "\n"
            return messages

    def _validate_must_courses(self) -> str:
        """Check if the student took all the required must courses, in minor and major."""
        message = ""
        # TODO: Fix in case computers is minor
        for course_type, required_must_courses in self._spc_must_courses_req.items():
            taken_must_courses_count = self._spc_must_courses_taken[course_type]
            if isinstance(required_must_courses, dict):  # Computers
                taken_in_computers = taken_must_courses_count[ComputersCourseType.TOTAL]
                required_must_course_count = self._spc_must_courses_req[course_type]
                if taken_in_computers < required_must_course_count[ComputersCourseType.TOTAL]:
                    message += "You need to take "
                    message += f"{required_must_course_count[ComputersCourseType.TOTAL] - taken_in_computers}"
                    message += f" more must {course_type.name.lower()} courses"
                    message += f" (you need at least {required_must_course_count[ComputersCourseType.HW]}"
                    message += f" {ComputersCourseType.HW.name.lower()}"
                    message += f" and {required_must_course_count[ComputersCourseType.SW]}"
                    message += f" {ComputersCourseType.SW.name.lower()} courses) \n"
            else:
                if taken_must_courses_count < required_must_courses:
                    message += f"You need to take {required_must_courses - taken_must_courses_count} more must {course_type.name.lower()} courses\n"
        return message if len(message) > 0 else "You have taken all the required must courses"

    def run_courses_check(self) -> str:
        self._check_all_courses_were_finished_properly()
        messages = self._get_invalid_courses()
        if messages is None:
            messages = ""
        self.update_mandatory_points()
        intership_message = self.update_internship_type()
        if intership_message is not None:
            return intership_message
        self.update_speciality_points()
        messages += self._validate_must_courses()
        return messages + self.validate_credit()
        # TODO: need to check if the amount of points matches the requirements
        # if self._required_mandatory_points < self._mandatory_points:

        # if self._needed_credit[CourseType.MAJOR] < self._credit_taken[CourseType.MAJOR]:

        # if self._needed_credit[CourseType.MINOR] < self._credit_taken[CourseType.MINOR]:

        # if self._required_external_points < self._credit_taken[CourseType.EXTERNAL]:
        #         # count how many required speciality courses the student took
        #         self._major_required_count = 0
        #         self._required_count[SpecialityType.MINOR] = 0

        #         # store the minimum number of required courses the student need to take in major and minor specialities
        #         self._needed_required_courses[CourseType.MAJOR] = None
        #         self._needed_required_courses[CourseType.MINOR] = None


def extract_course_data_from_line(line: str) -> tuple[int, float, str]:
    line = line.strip()  # Remove leading/trailing whitespaces
    # Use regex to extract the course number, credit, and name
    match = re.match(r'^(\d+)\s+([\d.]+)\s+(.+)$', line)
    if match:
        course_number = match.group(1)
        credit = match.group(2)
        name = match.group(3)
        print("Course Number:", course_number)
        print("Credit:", credit)
        print("Name:", name)
    return int(course_number), float(credit), name


def extract_student_data_from_line(line: str):
    line = line.strip()  # Remove leading/trailing whitespaces
    # Use regex to extract the field name and its value while ignoring text after '#'
    match = re.match(r'([^:]+):\s*([^#]*)', line)
    if match:
        field_value = match.group(2).strip()
    return field_value


def test_reading_student():
    syllabusDB = SyllabusDB("courses_fulllist.csv")
    # syllabusDB = MagicMock()
    student = Student("student1.txt", syllabusDB)
    student.run_courses_check()

    pass


if __name__ == "__main__":
    test_reading_student()
