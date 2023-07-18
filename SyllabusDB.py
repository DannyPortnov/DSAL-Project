# from Course import Course
from __future__ import annotations
from typing import Optional  # for self reference
from SpecialityCourse import SpecialityCourse
from SpecialityCoursesDB import SpecialityCoursesDB
from Constants import *
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
from Course import Course
import re
# -*- coding: utf-8 -*-


class SyllabusDB:
    "Syllabus Data base Object Implementation"

    def __init__(self, file: str):
        self._file_name: str = file
        # key: course number, value: course object
        self.all_courses: list[Course] = []
        self._mandatory_courses: dict[int, Course] = {}
        self._computers = SpecialityCoursesDB(Speciality.COMPUTERS)
        self._signals = SpecialityCoursesDB(Speciality.SIGNALS)
        self._devices = SpecialityCoursesDB(Speciality.DEVICES)

        self._total_points = 160
        self._mandatory_points: dict[Internships, int] = {
            Internships.INDUSTRY: 129, Internships.RESEARCH: 124, Internships.PROJECT: 122}
        self._major_points: dict[Internships, int] = {
            Internships.INDUSTRY: 20, Internships.RESEARCH: 20, Internships.PROJECT: 20}
        self._minor_points: dict[Internships, int] = {
            Internships.INDUSTRY: 0, Internships.RESEARCH: 10, Internships.PROJECT: 10}
        self._external_points: dict[Internships, int] = {
            Internships.INDUSTRY: 11, Internships.RESEARCH: 6, Internships.PROJECT: 8}
        self._must_courses: dict[CourseType, dict[Internships, int]] = {CourseType.MAJOR:  {Internships.INDUSTRY: 4,
                                                                                            Internships.RESEARCH: 4, Internships.PROJECT: 4},
                                                                        CourseType.MINOR:  {Internships.INDUSTRY: 0,
                                                                                            Internships.RESEARCH: 3, Internships.PROJECT: 3}}
        self._general_points = 6
        self._sport_points = 1
        self.create_db()  # automatically create the DB when the object is created

    # open the csv file and read only the first line- header

    def _open_db(self):
        f = open(self._file_name, "r", encoding="utf-8")
        header = f.readline().strip().split(',')
        return f, header

    def get_general_points(self):
        return self._general_points

    def get_total_points(self):
        return self._total_points

    def get_sport_points(self) -> int:
        return self._sport_points

    def get_speciality_by_name(self, speciality):
        if self._computers.get_name() == speciality:
            return self._computers
        elif self._signals.get_name() == speciality:
            return self._signals
        elif self._devices.get_name() == speciality:
            return self._devices

    # get the amount of points for each course type, regarding the type of project

    def get_required_points(self, final_project: Internships):
        return self._mandatory_points[final_project], self._major_points[final_project], \
            self._minor_points[final_project], self._external_points[final_project]

    def get_total_required_courses(
        self, final_project: Internships,
        major_speciality: Speciality,
            minor_speciality: Speciality):
        major_tuple = self._get_required_courses_in_speciality(
            final_project, major_speciality, CourseType.MAJOR)
        minor_tuple = self._get_required_courses_in_speciality(
            final_project, minor_speciality, CourseType.MINOR)
        return (major_tuple, minor_tuple)

    def _get_required_courses_in_speciality(
            self, final_project: Internships, speciality: Speciality, speciality_type: CourseType) -> tuple[int, int] | tuple[int]:
        required_courses_amount = self._must_courses[speciality_type][final_project]
        if speciality == Speciality.COMPUTERS:
            required_courses = (required_courses_amount//2,
                                required_courses_amount//2,
                                required_courses_amount)
        else:
            required_courses = (required_courses_amount,)
        return required_courses

    def create_db(self):
        f, line = self._open_db()
        while line:
            line = f.readline().strip().split(',')    # read course data to a list
            if len(line) == 1:
                break
            is_empty_line = "".join(line)
            match = re.search(r'#', line[1])
            if match or is_empty_line == "":
                continue
            else:
                if line[4] == REQUIRED_COURSE_INDICATOR:
                    course = Course(number=int(line[1]), name=line[3], points=float(line[2]), is_must=line[4],
                                    pre_courses=self.get_courses_codes(line[8:12]),
                                    parallel_course=self.get_course_code(line[12]))  # Assuming only 1 parallel course
                    self._mandatory_courses[course.get_number()] = course
                else:
                    course = SpecialityCourse(
                        number=int(line[1]), name=line[3], points=float(line[2]), is_must=line[4],
                        computers=line[5], signals=line[6], devices=line[7],
                        pre_courses=self.get_courses_codes(line[8:12]))  # Assuming SpecialityCourse can't have parallel courses
                    self._computers.add_course(course)
                    self._signals.add_course(course)
                    self._devices.add_course(course)
                self.all_courses.append(course)
        f.close()
        for course in self.all_courses:  # Update the pre courses to be course objects
            pre_courses = course.get_pre_courses()
            for pre_course in pre_courses:
                pre_courses[pre_course] = self.get_course_by_number(pre_course)
            parallel_course_num = course.get_parallel_course()[0]
            if parallel_course_num is not None:
                course.set_parallel_course(
                    self.get_course_by_number(parallel_course_num))

    def get_course_by_number(self, number: int) -> Course | SpecialityCourse:
        """Returns a course object by its number. If the course is not found, raises a ValueError."""

        if number in self._mandatory_courses.keys():
            return self._mandatory_courses[number]

        course = self._computers.get_course(number)
        if course is not None:
            return course

        course = self._signals.get_course(number)
        if course is not None:
            return course

        course = self._devices.get_course(number)
        if course is not None:
            return course

        raise ValueError(COURSE_NUMBER_NOT_FOUND_ERROR)

    def get_courses_codes(self, courses: list[str]) -> list[int]:
        """ Parses line of strings from the file to a list of courses codes

        Args:
            courses (`list[str]`): Line read from the file

        Returns:
            `list[int]`: Courses codes. If all the line cells are empty, returns an empty list.
        """
        courses_codes: list[int] = []
        for course_num in courses:
            if course_num != '':
                courses_codes.append((int(course_num)))
        return courses_codes

    def get_course_code(self, course: str) -> Optional[int]:
        return int(course) if course != '' else None
