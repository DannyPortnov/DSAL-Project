from io import TextIOWrapper
from typing import Generator, Optional
import re
from Course import Course
from SyllabusDB import SyllabusDB
from Constants import *
from unittest.mock import MagicMock
from SpecialityCourse import SpecialityCourse


class Student:
    "Student Object Implementation"

    def __init__(self, file_name: str, syllabus_db: SyllabusDB):
        # def __init__(self, name, id, major, minor, general_points, sport_points):
        self._file_name = file_name
        self._syllabus_db = syllabus_db
        self._name: str = None
        self._id: int = None
        self._major: Speciality = Speciality.INVALID
        self._minor: Speciality = Speciality.INVALID
        self._general_points: int = None
        self._sport_points: int = None

        # holds the type of internship that the student chose
        self._internship_type: Interships = Interships.INVALID

        # store the minimum points in order to finish the degree
        self._required_mandatory_points: int = None
        self._required_major_points: int = None
        self._required_minor_points: int = None
        self._required_external_points: int = None

        # TODO: maybe to change the way we store this data
        # store the minimum number of required courses the student need to take in major and minor specialities
        self._required_major_required_courses = None
        self._required_minor_required_courses = None

        # calculate the amount of points the student got
        self._total_points: int = 0
        self._mandatory_points: int = 0
        self._major_points: int = 0
        self._minor_points: int = 0
        self._external_points: int = 0

        # count how many required speciality courses the student took
        self._major_required_count: int | dict[ComputersSpecialityRequiredCourseType, int] = 0
        self._minor_required_count: int | dict[ComputersSpecialityRequiredCourseType, int] = 0

        # key: course number, value: course object
        self._mandatory_courses: dict[int, Course] = {}
        # key: course number, value: course object
        self._speciality_courses: dict[int, SpecialityCourse] = {}

        # Holds all the courses that were counted in the major or minor already
        self._shared_courses: list[SpecialityCourse] = []

        self._major_speciality_courses: dict[SpecialityCourseType, list[SpecialityCourse]] = {
            SpecialityCourseType.REQUIRED: [],
            SpecialityCourseType.OPTIONAL: [],
            SpecialityCourseType.NA: []
        }

        self._minor_speciality_courses: dict[SpecialityCourseType, list[SpecialityCourse]] = {
            SpecialityCourseType.REQUIRED: [],
            SpecialityCourseType.OPTIONAL: [],
            SpecialityCourseType.NA: []
        }

        # self._external_courses: list[SpecialityCourse] = []

        # key: course, value: why course is invalid
        self._invalid_courses: dict[SpecialityCourse, str] = {}

    def set_name(self, name):
        self._name = name

    def set_id(self, id: str):
        self._id = id

    # TODO: convert string to speciality
    def set_major(self, major: str) -> None:
        self._major = major
        if self._major == Speciality.COMPUTERS:
            self._major_required_count = {
                ComputersSpecialityRequiredCourseType.SW: 0, ComputersSpecialityRequiredCourseType.HW: 0}

    def set_minor(self, minor: str) -> None:
        self._minor = minor
        if self._minor == Speciality.COMPUTERS:
            self._minor_required_count = {
                ComputersSpecialityRequiredCourseType.SW: 0, ComputersSpecialityRequiredCourseType.HW: 0}

    def set_general_points(self, general_points: str) -> None:
        self._general_points = int(general_points)

    def set_sport_points(self, sport_points: str) -> None:
        self._sport_points = int(sport_points)

    def v(self, course: SpecialityCourse | Course) -> None:
        """ Add a course to the student's taken courses.

        Args:
            course (`SpecialityCourse` | `Course`): Course to add
        """
        if type(course) is SpecialityCourse:
            self._speciality_courses[course.get_number()] = course
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
        self._invalid_courses[(course_number := course.get_number())] = message
        if course.is_mandatory():
            self._mandatory_courses.pop(course_number)
        else:
            self._speciality_courses.pop(course_number)

    def _check_finished_courses(self) -> None:
        """Ensure that all taken courses were finished properly.
        """
        all_courses: dict[int, Course | SpecialityCourse] = {
            **self._mandatory_courses, **self._speciality_courses}
        for course in all_courses.values():
            is_finished, reason_if_not = course.is_finished_properly()
            if not is_finished and reason_if_not is not None:
                self.remove_from_courses(course, reason_if_not)

    def read_student_data(self):
        with open(self._file_name, "r", encoding="utf-8") as file:
            # TODO: Put all of this in __init__ ?
            line = next(self._ignore_comments(file))
            self.set_name(extract_student_data_from_line(line))
            line = next(self._ignore_comments(file))
            self.set_id(extract_student_data_from_line(line))
            line = next(self._ignore_comments(file))
            self.set_major(extract_student_data_from_line(line))
            line = next(self._ignore_comments(file))
            self.set_minor(extract_student_data_from_line(line))
            line = next(self._ignore_comments(file))
            self.set_general_points(extract_student_data_from_line(line))
            line = next(self._ignore_comments(file))
            self.set_sport_points(extract_student_data_from_line(line))

            # When Generator depletes, next() returns None
            while (line := next(self._ignore_comments(file))) != None:
                course_number, credit, name = extract_course_data_from_line(line)
                course = self._syllabus_db.get_course_by_number(course_number)
                if course.validate_course(course_number, credit, name):
                    self._add_course(course)
                else:
                    self._invalid_courses[course] = INVALID_COURSE_DATA_ERROR

    def _ignore_comments(self, file: TextIOWrapper) -> Generator[str, None, None]:
        for line in file:
            if not line.startswith("#"):
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
        if (31054 in self._mandatory_courses.keys()) and (31055 in self._mandatory_courses.keys()):
            # if self._internship_type is None:
            self._internship_type = Interships.INDUSTRY

        # check if project is research in the college
        elif (31052 in self._mandatory_courses.keys()) and (31053 in self._mandatory_courses.keys()):
            # check if the project type had already updated, if so- the student did not report the project courses correctly
            # if self._internship_type is None:
            self._internship_type = Interships.RESEARCH

        # check if project is mini_project in the college
        elif (31050 in self._mandatory_courses.keys()) and (31051 in self._mandatory_courses.keys()):
            # check if the project type had already updated, if so- the student did not report the project courses correctly
            # if self._internship_type is None:
            self._internship_type = Interships.PROJECT
        else:
            self._internship_type = Interships.INVALID  # TODO: maybe raise an exception

    def update_mandatory_points(self, course: Course):
        for course in self._mandatory_courses.values():
            self._total_points += course.get_points()
            self._mandatory_points += course.get_points()

    # TODO: maybe do this when we read the student file
    # first we need to sort the major and minor courses by the speciality course's condition
    def sort_speciality_courses(self) -> None:
        for course in self._speciality_courses.values():
            self._major_speciality_courses[course.get_speciality_course_type(
                self._major)].append(course)
            self._minor_speciality_courses[course.get_speciality_course_type(
                self._minor)].append(course)

    def get_intersecting_courses(self, course_type_in_minor: SpecialityCourseType,
                                 course_type_in_major: SpecialityCourseType) -> set[SpecialityCourse]:
        """
            Returns the common speciality courses between major and minor based on the specified types.

            Args:
                minor_type (`SpecialityCourseType`): The speciality course type for the minor speciality.
                major_type (`SpecialityCourseType`): The speciality course type for the major speciality.

            Returns:
                `set[SpecialityCourse]`: The intersection of speciality courses based on the specified types.
        """
        minor_courses = self._minor_speciality_courses[course_type_in_minor]
        major_courses = self._major_speciality_courses[course_type_in_major]
        return set(minor_courses).intersection(major_courses)

    # method for updating the student's point in speciality

    def update_speciality_points(self):
        # update required courses in major and minor
        self.update_only_in_major_and_required_courses(
            self.get_intersecting_courses(course_type_in_major=SpecialityCourseType.REQUIRED,
                                          course_type_in_minor=SpecialityCourseType.NA))  # required in major

        if self._internship_type == Interships.RESEARCH or self._internship_type == Interships.PROJECT:
            self.update_only_in_minor_and_required_courses(
                self.get_intersecting_courses(course_type_in_major=SpecialityCourseType.REQUIRED,
                                              course_type_in_minor=SpecialityCourseType.NA))  # required in minor
            self.update_major_required_minor_optional_courses(
                self.get_intersecting_courses(course_type_in_major=SpecialityCourseType.REQUIRED,
                                              course_type_in_minor=SpecialityCourseType.OPTIONAL))   # required in major
            self.update_minor_required_major_optional_courses(
                self.get_intersecting_courses(course_type_in_major=SpecialityCourseType.OPTIONAL,
                                              course_type_in_minor=SpecialityCourseType.REQUIRED))   # required in minor
            self.update_major_required_minor_required_courses(
                self.get_intersecting_courses(course_type_in_major=SpecialityCourseType.REQUIRED,
                                              course_type_in_minor=SpecialityCourseType.REQUIRED))     # required in major or minor

        # update external points
        self.update_external_points()

        # update Choice courses in major only and minor only
        self.update_major_optional_courses_only(
            self.get_intersecting_courses(course_type_in_major=SpecialityCourseType.OPTIONAL,
                                          course_type_in_minor=SpecialityCourseType.NA))  # required in major
        if self._internship_type == Interships.RESEARCH or self._internship_type == Interships.PROJECT:
            self.update_minor_optional_courses_only(
                self.get_intersecting_courses(course_type_in_major=SpecialityCourseType.NA,
                                              course_type_in_minor=SpecialityCourseType.OPTIONAL))  # required in minor

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
    def update_only_in_major_and_required_courses(self, only_in_major_and_required: set[SpecialityCourse]) -> None:
        """ Update the pointsof the courses that are required in the major but not available in the minor.
            This method filters the speciality courses that are required only in the major speciality
            and not available in the minor speciality. It updates the count of major required courses
            taken by the student and increments the major points accordingly. If the major points exceed
            the required major points, the excess points are added to the external points.
        """

        for course in only_in_major_and_required:
            #     check if the course is MUST in Hardware or Software
            #     update a counter for amount of HW/SW courses that was taken
            # we can check if the course belongs to HW or SW
            if self._major_points < self._required_major_points:
                if self._major == Speciality.COMPUTERS:
                    # we need to assume that each computers' course name's indicate if it's HW or SW
                    if (is_hw_sw := course.check_if_hw_sw()) is not None:
                        self._major_required_count[is_hw_sw] += 1
                    # else:
                    #     self._major_required_count += 1
                    # # self.update_major_minor_computers_required_points(course, self._major_required_count)
                else:
                    self._major_required_count += 1
                self._major_points += course.get_points()
            # this course is available only in this speciality, if we exceed the number of points
            # for this major, we will put the course in external_points
            else:
                self._external_points += course.get_points()

    # update the points of minor's Must courses by using the courses that are available in the minor only

    def update_only_in_minor_and_required_courses(self, only_in_minor_and_required: set[SpecialityCourse]) -> None:
        for course in only_in_minor_and_required:
            if self._minor_points < self._required_minor_points:
                if self._minor == Speciality.COMPUTERS:
                    # we need to assume that each computers' course name's indicate if it's HW or SW
                    is_hw_sw = course.check_if_hw_sw()
                    if is_hw_sw is not None:
                        self._minor_required_count[is_hw_sw] += 1
                    # else:
                    #     self._minor_required_count += 1
                    # self.update_major_minor_computers_required_points(course, self._minor_required_count)
                else:
                    self._minor_required_count += 1
                self._minor_points += course.get_points()
            # this course is available only in this speciality, if we exceed the number of points
            # for this minor, we will put the course in external_points
            else:
                self._external_points += course.get_points()

    # update the major points if it doesn't have enough required courses

    def update_major_required_minor_optional_courses(self, required_in_major_and_optional_in_minor: set[SpecialityCourse]) -> None:
        for course in required_in_major_and_optional_in_minor:
            # major doesn't have enough required courses, and student didn't exceed amount of major points
            if self._major == Speciality.COMPUTERS:
                is_hw_sw = course.check_if_hw_sw()

                # we need to assume that each computers' course name's indicate if it's HW or SW

                if is_hw_sw is not None:
                    # TODO: change the number to constant, computers need at least 2 HW and 2 SW courses if it's major
                    if self._major_required_count[is_hw_sw] < 2 and self._major_points < self._required_major_points:
                        self._major_required_count[is_hw_sw] += 1
                        self._major_points += course.get_points()
                        return
                    # major have enough required courses, we will decide later where to put this course by checking it's credit points
            else:
                if self._major_required_count < self._required_major_required_courses and self._major_points < self._required_major_points:
                    self._major_required_count += 1
                    self._major_points += course.get_points()
                    return
                # major have enough required courses, we will decide later where to put this course by checking it's credit points
            self._shared_courses.append(course)

    # update the minor points if it doesn't have enough required courses

    def update_minor_required_major_optional_courses(self, required_in_minor_and_optional_in_major: set[SpecialityCourse]) -> None:
        for course in required_in_minor_and_optional_in_major:
            # minor doesn't have enough required courses, and student didn't exceed amount of minor points
            if self._minor == Speciality.COMPUTERS:
                is_hw_sw = course.check_if_hw_sw()
                if is_hw_sw is not None:
                    # TODO: change the number to constant, computers need at least 1 HW and 1 SW courses if it's minor
                    # TODO: NEED TO CHECK ALSO IF REACHED TO 3 MUST COURSES IN MINOR
                    if self._minor_required_count[is_hw_sw] < 1 and self._minor_points < self._required_minor_points:
                        self._minor_required_count[is_hw_sw] += 1
                        self._minor_points += course.get_points()
                        return
                    # major have enough required courses, we will decide later where to put this course by checking it's credit points
            else:
                if self._minor_required_count < self._required_minor_required_courses and self._minor_points < self._required_minor_points:
                    self._minor_required_count += 1
                    self._minor_points += course.get_points()
                    return
            # minor have enough required courses, we will decide later where to put this course by checking it's credit points
            self._shared_courses.append(course)

    # update major and minor points by checking if they have enough required courses.

    def update_major_required_minor_required_courses(self, major_required_minor_required_courses: set[SpecialityCourse]) -> None:
        for course in major_required_minor_required_courses:
            # TODO: need to have another condition if it's computers speciality.
            if self._major == Speciality.COMPUTERS:
                is_hw_sw = course.check_if_hw_sw()
                # we need to assume that each computers' course name's indicate if it's HW or SW
                if is_hw_sw is not None:
                    # TODO: change the number to constant, computers need at least 1 HW and 1 SW courses if it's minor
                    # major doesn't have enough required courses, minor does have
                    if self._major_required_count[is_hw_sw] < 2 and self._minor_points >= self._required_minor_points:
                        self._major_required_count[is_hw_sw] += 1
                        self._major_points += course.get_points()
                    # minor doesn't have enough required courses, major does have
                    elif self._major_required_count[is_hw_sw] >= 2 and self._minor_points < self._required_minor_points:
                        self._minor_required_count += 1
                        self._minor_points += course.get_points()
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
                    if self._major_required_count < self._required_major_required_courses and self._minor_required_count[is_hw_sw] >= 1:
                        self._major_required_count += 1
                        self._major_points += course.get_points()
                    # minor doesn't have enough required courses, major does have
                    elif self._major_required_count >= self._required_major_required_courses and self._minor_required_count[is_hw_sw] < 1:
                        self._minor_required_count[is_hw_sw] += 1
                        self._minor_points += course.get_points()
                    # major and minor have enough required courses, we will decide later
                    # where to put this course by checking it's credit points
                    else:
                        self._shared_courses.append(course)

            else:
                # major doesn't have enough required courses, minor does have
                if self._major_required_count < self._required_major_required_courses and self._minor_required_count >= self._required_minor_required_courses:
                    self._major_required_count += 1
                    self._major_points += course.get_points()
                # minor doesn't have enough required courses, major does have
                elif self._major_required_count >= self._required_major_required_courses and self._minor_required_count < self._required_minor_required_courses:
                    self._minor_required_count += 1
                    self._minor_points += course.get_points()
                # minor and major doesn't have enough required courses, by default we will update the required course in the major
                elif self._major_required_count < self._required_major_required_courses and self._minor_required_count < self._required_minor_required_courses:
                    self._minor_required_count += 1
                    self._minor_points += course.get_points()
                # major and minor have enough required courses, we will decide later
                # where to put this course by checking it's credit points
                else:
                    self._shared_courses.append(course)

    # update the points of major's Choice courses by using the courses that are available in the major only

    def update_major_optional_courses_only(self, only_in_major_and_optional_courses: set[SpecialityCourse]) -> None:
        for course in only_in_major_and_optional_courses:
            if self._major_points < self._required_major_points:
                self._major_points += course.get_points()
            # this course is available only in this speciality, if we exceed the number of points
            # for this major, we will put the course in external_points
            else:
                self._external_points += course.get_points()

    # update the points of minor's Choice courses by using the courses that are available in the minor only
    def update_minor_optional_courses_only(self, only_in_minor_and_optional_courses: set[SpecialityCourse]) -> None:
        for course in only_in_minor_and_optional_courses:
            if self._minor_points < self._required_minor_points:
                self._minor_points += course.get_points()
            # this course is available only in this speciality, if we exceed the number of points
            # for this minor, we will put the course in external_points
            else:
                self._external_points += course.get_points()

    # update the points of external speciality by using the courses that are not available in major and minor

    def update_external_points(self) -> None:
        for course in set(self._major_speciality_courses[SpecialityCourseType.NA]) | set(self._minor_speciality_courses[SpecialityCourseType.NA]):
            self._external_points += course.get_points()
            self._total_points += course.get_points()

    # here we update points of major, minor and external specialities by using the rest of the courses that have left.

    def update_major_minor_shared_courses_points(self) -> None:
        for course in self._shared_courses:
            # TODO: check where to put a course in consideration of its points.
            course_points = course.get_points()
            # if (self._required_major_points - (self._major_points + course_points)) > (self._required_minor_points - (self._minor_points + course_points)):
            # self._major_points += course_points

            if self._major_points + course_points < self._required_major_points:
                self._major_points += course_points
            elif self._minor_points + course_points < self._required_minor_points:
                self._minor_points += course_points
            elif self._external_points + course_points < self._required_external_points:
                self._external_points += course_points

    def update_required_data(self) -> None:
        req_mand, req_maj, req_min, req_ext = self._syllabus_db.get_required_points(
            self._internship_type)
        req_min_required, req_maj_required = self._syllabus_db.get_required_speciality_required(
            self._internship_type)
        self._required_mandatory_points = req_mand
        self._required_major_points = req_maj
        self._required_minor_points = req_min
        self._required_external_points = req_ext
        self._required_major_required_courses = req_maj_required
        self._required_minor_required_courses = req_min_required

    # check if student has enough mandatory points
    # TODO: maybe change the parameters that this method returns

    def validate_mandatory_points(self) -> bool:
        if self._required_mandatory_points <= self._mandatory_points:
            return True
        return False

    # check if student has enough external points
    # TODO: maybe change the parameters that this method returns
    def validate_external_points(self) -> bool:
        if self._required_external_points <= self._external_points:
            return True
        return False

    # check if student has enough major points
    # TODO: maybe change the parameters that this method returns
    def validate_major_points(self) -> bool:
        if self._required_major_points <= self._major_points:
            # TODO: need to check if completed the minimum required courses points in major
            return True
        return False

    # check if student has enough minor points
    # TODO: maybe change the parameters that this method returns
    def validate_minor_points(self) -> bool:
        if self._required_minor_points <= self._minor_points:
            # TODO: need to check if completed the minimum required courses points in minor
            return True
        return False

    # check if the students is allowed to finish the degree

    def run_courses_check(self) -> bool:
        self._check_finished_courses()
        self.update_mandatory_points()
        self.update_internship_type()
        self.update_required_data()
        self.sort_speciality_courses()
        self.update_speciality_points()

        # TODO: need to check if the amount of points matches the requirements
        # if self._required_mandatory_points < self._mandatory_points:

        # if self._required_major_points < self._major_points:

        # if self._required_minor_points < self._minor_points:

        # if self._required_external_points < self._external_points:
        #         # count how many required speciality courses the student took
        #         self._major_required_count = 0
        #         self._minor_required_count = 0

        #         # store the minimum number of required courses the student need to take in major and minor specialities
        #         self._required_major_required_courses = None
        #         self._required_minor_required_courses = None


def extract_course_data_from_line(line: str):
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
    return course_number, credit, name


def extract_student_data_from_line(line: str):
    line = line.strip()  # Remove leading/trailing whitespaces
    # Use regex to extract the field name and its value while ignoring text after '#'
    match = re.match(r'([^:]+):\s*([^#]*)', line)
    if match:
        field_value = match.group(2).strip()
    return field_value


def test_reading_student():
    # syllabusDB = SyllabusDB("courses_fulllist.csv")
    syllabusDB = MagicMock()
    student = Student("student1.txt", syllabusDB)
    student.read_student_data()

    pass


if __name__ == "__main__":
    test_reading_student()
