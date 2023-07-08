# from Course import Course
from SpecialityCourse import SpecialityCourse
from SpecialityCoursesDB import SpecialityCoursesDB
from Constants import *
import re
# -*- coding: utf-8 -*-

class SyllabusDB:
    "Syllabus Data base Object Implementation"

    def __init__(self, file: str):
        self._file_name = file
        # key: course number, value: course object
        self._mandatory_courses_list = [] #just for debug
        self._speciality_courses_list = [] #just for debug


        self._mandatory_courses: dict[int, Course] = {}
        # self._final_project_courses = dict()  # holds the type of final project that are available
        self._computers = SpecialityCoursesDB(Speciality.COMPUTERS)
        self._signals = SpecialityCoursesDB(Speciality.SIGNALS)
        self._devices = SpecialityCoursesDB(Speciality.DEVICES)

        self._total_points = 160
        self._mandatory_points: dict[Interships, int] = {
            Interships.INDUSTRY: 129, Interships.RESEARCH: 124, Interships.PROJECT: 122}
        self._major_points: dict[Interships, int] = {
            Interships.INDUSTRY: 20, Interships.RESEARCH: 20, Interships.PROJECT: 20}
        self._minor_points: dict[Interships, int] = {
            Interships.INDUSTRY: 0, Interships.RESEARCH: 10, Interships.PROJECT: 10}
        self._external_points: dict[Interships, int] = {
            Interships.INDUSTRY: 11, Interships.RESEARCH: 6, Interships.PROJECT: 8}
        self._major_must_courses = {Interships.INDUSTRY: 4,
                                    Interships.RESEARCH: 4, Interships.PROJECT: 4}
        self._minor_must_courses = {Interships.INDUSTRY: 0,
                                    Interships.RESEARCH: 3, Interships.PROJECT: 3}
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

    def get_sport_points(self):
        return self._sport_points

    def get_speciality_by_name(self, speciality):
        if self._computers.get_name() == speciality:
            return self._computers
        elif self._signals.get_name() == speciality:
            return self._signals
        elif self._devices.get_name() == speciality:
            return self._devices

    # get the amount of points for each course type, regarding the type of project

    def get_required_points(self, final_project: Interships):
        return self._mandatory_points[final_project], self._major_points[final_project], \
            self._minor_points[final_project], self._external_points[final_project]

    def get_required_courses_in_speciality(self, final_project) -> tuple[int, int]:
        return self._minor_must_courses[final_project], self._major_must_courses[final_project]

    # TODO: update DB creation to ignore the lines with the symbol: #
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
                # number, points, name, is_must, computers, signals, devices, pre_courses_list, parallel_course = extract_line(d)
                # course = Course(number, name, points, is_must, computers, signals, devices, pre_courses_list, parallel_course)
                if line[4] == REQUIRED_COURSE_INDICATOR:
                    course = Course(number=int(line[1]), name=line[3], points=float(line[2]), is_must=line[4],
                                    pre_courses_list=self.get_pre_course_int(line[8:12]))
                    self._mandatory_courses[course.get_number()] = course
                    self._mandatory_courses_list.append(course)
                else:
                    course = SpecialityCourse(
                        number=int(line[1]), name=line[3], points=float(line[2]), is_must=line[4],
                        computers=line[5], signals=line[6], devices=line[7],
                        pre_courses_list=self.get_pre_course_int(line[8:12]))
                    self._speciality_courses_list.append(course)
                    self._computers.add_course(course)
                    self._signals.add_course(course)
                    self._devices.add_course(course)
        f.close()

    def get_course_by_number(self, number: int) -> Course | SpecialityCourse | None:
        """Returns a course object by its number. If the course is not found, raises a ValueError.
        If no number is specified in the syllabus, returns None"""
        if number is None:
            return None
        
        # if number == '':
        #     return None
        
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

    # def set_name(self, name):
    #     self._name = name

    # def set_id(self, id):
    #     self._id = id

    # def set_major(self, major):
    #     self._major = major

    # def set_minor(self, minor):
    #     self._minor = minor

    # # TODO: maybe change the list to another data structure
    # # add a course object to the stduent's list of courses
    # def add_course(self, course):
    #     self._courses.append(course)

# need to get the pre_courses objects by using the pre courses list of strings


    def print_db(self):
        for course in self._mandatory_courses_list:
            print(f"number={course.get_number()}, points={course.get_points()}, name={course.get_name()}, is_must={course._is_must}, pre_courses_list={course._pre_courses}")
        for course in self._speciality_courses_list:
            print(f"number={course.get_number()}, points={course.get_points()}, name={course.get_name()}, is_must={course._is_must}, computers={course._specialities[Speciality.COMPUTERS]}, signals={course._specialities[Speciality.SIGNALS]}, devices={course._specialities[Speciality.DEVICES]}, pre_courses_list={course._pre_courses}")





    def get_pre_course_int(self, pre_courses_list) -> Course:
        pre_courses = list()
        for course_num in pre_courses_list:
            if course_num != '':
                pre_courses.append((int(course_num)))
        return pre_courses

