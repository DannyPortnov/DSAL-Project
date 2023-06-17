from io import TextIOWrapper
from typing import Generator
import re
from Course import Course
from SyllabusDB import SyllabusDB
import Constants
from Constants import Interships
from unittest.mock import MagicMock


class Student:
    "Student Object Implementation"

    def __init__(self, file_name: str, syllabus_db: SyllabusDB):
        # def __init__(self, name, id, major, minor, general_points, sport_points):
        self._file_name = file_name
        self._syllabus_db = syllabus_db
        self._name: str = None
        self._id: int = None
        self._major: int = None
        self._minor: int = None
        self._general_points: int = None
        self._sport_points: int = None

        self._internship_type:Interships = None   # holds the type of internship that the student chose

        # store the minimum points in order to finish the degree
        self._required_mandatory_points: int = None
        self._required_major_points: int = None
        self._required_minor_points: int = None
        self._required_external_points: int = None

        # TODO: maybe to change the way we store this data
        # store the minimum number of "Must" courses the student need to take in major and minor specialities
        self._required_major_must_courses = None
        self._required_minor_must_courses = None

        # calculate the amount of points the student got
        self._total_points: int = 0
        self._mandatory_points: int = 0
        self._major_points: int = 0
        self._minor_points: int = 0
        self._external_points: int = 0

        # count how many speciality "must" courses the student took
        self._major_must_count = 0 
        self._minor_must_count = 0 



        # key: course number, value: course object
        self._mandatory_courses: dict[int, Course] = {}
        # key: course number, value: course object
        self._speciality_courses: dict[int, Course] = {}
        
        # major courses only
        self._major_must_courses_only = dict()  # key: course object, value: condition (choice, must or none)
        self._major_choice_courses_only = dict()  # key: course object, value: condition (choice, must or none)
       
        # minor courses only
        self._minor_must_courses_only = dict()  # key: course object, value: condition (choice, must or none)
        self._minor_choice_courses_only = dict()  # key: course object, value: condition (choice, must or none)
        
        # Must course in major and in minor
        self._major_must_minor_must_courses = dict()
        
        # major-must, minor-choice
        self._major_must_minor_choice_courses = dict()

        # major-choice, minor-must
        self.minor_must_major_choice_courses = dict()

        # courses that are available in both major and minor
        self._major_minor_shared_courses = dict()  # courses the are shared between major and minor
        
        self._external_courses = dict()  # key: course object, value: condition (choice, must or none)
        
        # key: course, value: why course is invalid
        self._invalid_courses: dict[Course, str] = dict()




    def set_name(self, name):
        self._name = name

    def set_id(self, id):
        self._id = id

    def set_major(self, major):
        self._major = major
        if major == "Computers":
            self._major_must_count = {"תוכנה": 0, "חומרה": 0}

    def set_minor(self, minor):
        self._minor = minor
        if minor == "Computers":
            self._minor_must_count = {"תוכנה": 0, "חומרה": 0}

    def set_general_points(self, general_points):
        self._general_points = general_points

    def set_sport_points(self, sport_points):
        self._sport_points = sport_points

    # TODO: maybe change the list to another data structure
    # add a course object to the stduent's dict of mandatory courses
    def add_mandatory_course(self, course: Course):
        self._mandatory_courses[course.get_number()] = course
        course.mark_as_taken()

    # add a course object to the stduent's dict of speciality courses
    def add_speciality_course(self, course: Course):
        # # check the condition of a course in speciality
        # condition = course.get_condition_by_speciality(self._major)
        self._speciality_courses[course.get_number()] = course
        course.mark_as_taken()

    
    # add a course object to the stduent's dict of invlid courses
    def add_invalid_course(self, course: Course, message: str):
        self._invalid_courses[course.get_number()] = message
        course_number = course.get_number()
        if course.is_mandatory():
            self._mandatory_courses.pop(course_number)
        else:
            self._speciality_courses.pop(course_number)

    def read_student_data(self):
        with open(self._file_name, "r", encoding="utf-8") as file:
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
                # current_semester_courses: list[Course] = []
                if (line.startswith("#") and Constants.SEMESTER_LINE_INDICATOR in line):  # Start of semester
                    match = re.match(r'# סמסטר (\d+)', line)  # Extract semester number
                    if match:
                        semester_num = int(match.group(1))
                    # if len(current_semester_courses) == 0:
                    #     continue
                    # for course in current_semester_courses:  # Validate parrallel courses
                    #     if course.get_parallel_course() not in current_semester_courses:
                    #         self._invalid_courses[course] = contants.format_parallel_course_error(course)

                else:  # Begin reading semester's courses
                    course_number, credit, name = extract_course_data_from_line(line)
                    course = self._syllabus_db.get_course_by_number(course_number)
                    course.set_semester_num(semester_num)
                    if course.validate_course(course_number, credit, name):
                        if course.is_mandatory():
                            self.add_mandatory_course(course)
                        else:
                            self.add_speciality_course(course)
                        # current_semester_courses.append(course)
                    else:
                        self._invalid_courses[course] = Constants.INVALID_COURSE_DATA_ERROR

    def _ignore_comments(self, file: TextIOWrapper):
        for line in file:
            if (not line.startswith("#")) or (line.startswith("#") and Constants.SEMESTER_LINE_INDICATOR in line):
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
            self._internship_type = Interships.INVALID

    def update_mandatory_points(self, course: Course):
        for course in self._mandatory_courses.values():
            is_finished, reason_if_not = course.is_finished_properly()
            if is_finished:
                self._total_points += course.get_points()
                self._mandatory_points += course.get_points()
            else:
                # TODO: pop out an invalid course from self._courses dict
                self.add_invalid_course(course, reason_if_not)
            
    # TODO: maybe do this when we read the student file
    # first we need to sort the major and minor courses by the scpeciality course's condition
    def sort_speciality_courses_by_condition(self):
        for course in self._speciality_courses:
            major_condition = course.get_condition_by_speciality(self._major)
            minor_condition = course.get_condition_by_speciality(self._minor)

            if major_condition == "Must" and minor_condition == None:
                self._major_must_courses_only[course] = major_condition 

            elif major_condition == "Choice" and minor_condition == None:
                self._major_choice_courses_only[course] = major_condition
            
            elif major_condition == None and minor_condition == "Must":
                self._minor_must_courses_only[course] = minor_condition

            elif major_condition == None and minor_condition == "Choice":
                self._minor_choice_courses_only[course] = minor_condition

            elif major_condition == "Must" and minor_condition == "Choice":
                self._major_must_minor_choice_courses[course] = None     # TODO: mabye change it's value to something else

            elif major_condition == "Choice" and minor_condition == "Must":
                self.minor_must_major_choice_courses[course] = None     # TODO: mabye change it's value to something else
            
            elif major_condition == "Must" and minor_condition == "Must":
                self._major_must_minor_must_courses[course] = None     # TODO: mabye change it's value to something else
            
            elif major_condition == "Choice" and minor_condition == "Choice":
                self._major_minor_shared_courses[course] = None     # TODO: mabye change it's value to something else         
            
            elif major_condition == None and minor_condition == None:
                self._external_courses[course] = None     # TODO: mabye change it's value to something else



    #method for updating the student's point in speciality
    def update_speciality_points(self):
        # update MUST courses in major and minor
        self.update_major_must_courses_only() #must in major

        if self._internship_type == "research" or self._internship_type == "project":
            self.update_minor_must_courses_only() #must in minor
            self.update_major_must_minor_choice_courses()   #must in major
            self.update_minor_must_major_choice_courses()   #must in minor
            self.update_major_must_minor_must_courses()     #must in major or minor
        
        # update external points
        self.update_external_points()

        # update Choice courses in major only and minor only
        self.update_major_choice_courses_only() #must in major
        if self._internship_type == "research" or self._internship_type == "project":
            self.update_minor_choice_courses_only() #must in minor

        # at this point, we check the following requirements: 
        # 1. we checked the "Must" courses requirements in major and minor and calculated it accordingly.
        # 2. we calculated the "Choice" courses that are available in major only and minor only accordingly.
        # 3. we calculated the courses that can fit only in external speciality
        # 3. after those steps, we are left with the courses that can fit into each speciality: major/minor/external.
        #    we will put the courses in such way that we calculated the points of each speciality and try to get to it's limit
        # update points by using the courses that have left
        self.update_major_minor_shared_courses_points()
    

    # method that updates the must course in computers speciality, with respect to it's kind: "חומרה" or "תוכנה"
    # def update_major_minor_computers_must_points(self, course, must_count):
    #     is_hw_sw = course.check_if_hw_sw()
    #     if is_hw_sw is not None:
    #         must_count[is_hw_sw] += 1
    #     else:
    #         must_count += 1
    

    # TODO: in each update major/minor/external course method, need to add:  else: self.add_invalid_course(...)
    # this is for a situation when a course had not finished properly

    # update the points of major's Must courses by using the courses that are available in the major only
    def update_major_must_courses_only(self):
        for course in self._major_must_courses_only:
            if course.is_finished_properly():
                #     check if the course is MUST in Hardware or Software
                #     update a counter for amount of HW/SW courses that was taken
                # we can check if the course belongs to HW or SW by checking if it's name has the word: "חומרה" or "תוכנה"                
                if self._major_points < self._required_major_points:
                    if self._major == "Computers":
                        # we need to assume that each computer's course include: (חומרה) or (תוכנה) in it's name
                        is_hw_sw = course.check_if_hw_sw()
                        if is_hw_sw is not None:
                            self._major_must_count[is_hw_sw] += 1
                        # else:
                        #     self._major_must_count += 1
                        # # self.update_major_minor_computers_must_points(course, self._major_must_count)
                    else:
                        self._major_must_count += 1
                    self._major_points += course.get_points()
                # this course is available only in this speciality, if we exceed the number of points
                # for this major, we will put the course in external_points
                else:
                    self._external_points += course.get_points()

   
    # update the points of minor's Must courses by using the courses that are available in the minor only
    def update_minor_must_courses_only(self):
        for course in self._minor_must_courses_only:
            if course.is_finished_properly():
                if self._minor_points < self._required_minor_points:
                    if self._minor == "Computers":
                        # we need to assume that each computer's course include: (חומרה) or (תוכנה) in it's name
                        is_hw_sw = course.check_if_hw_sw()
                        if is_hw_sw is not None:
                            self._minor_must_count[is_hw_sw] += 1
                        # else:
                        #     self._minor_must_count += 1
                        # self.update_major_minor_computers_must_points(course, self._minor_must_count)
                    else:
                        self._minor_must_count += 1
                    self._minor_points += course.get_points()
                # this course is available only in this speciality, if we exceed the number of points
                # for this minor, we will put the course in external_points
                else:
                    self._external_points += course.get_points()
   
   
    # update the major points if it doesn't have enough must courses
    def update_major_must_minor_choice_courses(self):
        for course in self._major_must_minor_choice_courses:
            if course.is_finished_properly():
                # major doesn't have enough must courses, and student didn't exceed amount of major points
                if self._major == "Computers":
                    is_hw_sw = course.check_if_hw_sw()

                    # we need to assume that each computer's course include: (חומרה) or (תוכנה) in it's name
                    
                    if is_hw_sw is not None:
                        #TODO: change the number to constant, computers need at least 2 HW and 2 SW courses if it's major
                        if self._major_must_count[is_hw_sw] < 2 and self._major_points < self._required_major_points:
                            self._major_must_count[is_hw_sw] += 1
                            self._major_points += course.get_points()
                        # major have enough must courses, we will decide later where to put this course by checking it's credit points
                        else:
                            self._major_minor_shared_courses[course] = None
                else:
                    if self._major_must_count < self._required_major_must_courses and self._major_points < self._required_major_points:
                        self._major_must_count += 1
                        self._major_points += course.get_points()
                    # major have enough must courses, we will decide later where to put this course by checking it's credit points
                    else:
                        self._major_minor_shared_courses[course] = None
              


    # update the minor points if it doesn't have enough must courses
    def update_minor_must_major_choice_courses(self):
        for course in self.minor_must_major_choice_courses:
            if course.is_finished_properly():
                # minor doesn't have enough must courses, and student didn't exceed amount of minor points
                if self._minor == "Computers":
                    is_hw_sw = course.check_if_hw_sw()
                    if is_hw_sw is not None:
                        #TODO: change the number to constant, computers need at least 1 HW and 1 SW courses if it's minor
                        if self._minor_must_count[is_hw_sw] < 1 and self._minor_points < self._required_minor_points:
                            self._minor_must_count[is_hw_sw] += 1
                            self._minor_points += course.get_points()
                        # major have enough must courses, we will decide later where to put this course by checking it's credit points
                        else:
                            self._major_minor_shared_courses[course] = None
                else:
                    if self._minor_must_count < self._required_minor_must_courses and self._minor_points < self._required_minor_points:
                        self._minor_must_count += 1
                        self._minor_points += course.get_points()
                    # minor have enough must courses, we will decide later where to put this course by checking it's credit points
                    else:
                        self._major_minor_shared_courses[course] = None


    # update major and minor points by checking if they have enough must courses.
    def update_major_must_minor_must_courses(self):
        for course in self._major_must_minor_must_courses:
            if course.is_finished_properly():
                # TODO: need to have another condition if it's computers speciality.
                if self._major == "Computers":
                    is_hw_sw = course.check_if_hw_sw()
                    # we need to assume that each computer's course include: (חומרה) or (תוכנה) in it's name
                    if is_hw_sw is not None:
                        #TODO: change the number to constant, computers need at least 1 HW and 1 SW courses if it's minor
                        # major doesn't have enough must courses, minor does have
                        if self._major_must_count[is_hw_sw] < 2 and self._minor_points >= self._required_minor_points:
                            self._major_must_count[is_hw_sw] += 1
                            self._major_points += course.get_points()
                        # minor doesn't have enough must courses, major does have
                        elif self._major_must_count[is_hw_sw] >= 2 and self._minor_points < self._required_minor_points:
                            self._minor_must_count += 1
                            self._minor_points += course.get_points()
                        # major and minor have enough must courses, we will decide later 
                        # where to put this course by checking it's credit points
                        else:
                            self._major_minor_shared_courses[course] = None

                elif self._minor == "Computers":
                    # we need to assume that each computer's course include: (חומרה) or (תוכנה) in it's name
                    is_hw_sw = course.check_if_hw_sw()
                    if is_hw_sw is not None:
                        #TODO: change the number to constant, computers need at least 1 HW and 1 SW courses if it's minor
                        # major doesn't have enough must courses, minor does have                       
                        if self._major_must_count < self._required_major_must_courses and self._minor_must_count[is_hw_sw] >= 1:
                            self._major_must_count += 1
                            self._major_points += course.get_points()
                        # minor doesn't have enough must courses, major does have
                        elif self._major_must_count >= self._required_major_must_courses and self._minor_must_count[is_hw_sw] < 1:
                                self._minor_must_count[is_hw_sw] += 1
                                self._minor_points += course.get_points()
                        # major and minor have enough must courses, we will decide later 
                        # where to put this course by checking it's credit points
                        else:
                            self._major_minor_shared_courses[course] = None
              
                else:
                    # major doesn't have enough must courses, minor does have
                    if self._major_must_count < self._required_major_must_courses and self._minor_must_count >= self._required_minor_must_courses:
                        self._major_must_count += 1
                        self._major_points += course.get_points()
                    # minor doesn't have enough must courses, major does have
                    elif self._major_must_count >= self._required_major_must_courses and self._minor_must_count < self._required_minor_must_courses:
                        self._minor_must_count += 1
                        self._minor_points += course.get_points()
                    # minor and major doesn't have enough must courses, by default we will update the must course in the major
                    elif self._major_must_count < self._required_major_must_courses and self._minor_must_count < self._required_minor_must_courses:
                        self._minor_must_count += 1
                        self._minor_points += course.get_points()
                    # major and minor have enough must courses, we will decide later 
                    # where to put this course by checking it's credit points
                    else:
                        self._major_minor_shared_courses[course] = None
        


    # update the points of major's Choice courses by using the courses that are available in the major only
    def update_major_choice_courses_only(self):
        for course in self._major_choice_courses_only:
            if course.is_finished_properly():
                    if self._major_points < self._required_major_points:
                        self._major_points += course.get_points()
                    # this course is available only in this speciality, if we exceed the number of points
                    # for this major, we will put the course in external_points
                    else:
                        self._external_points += course.get_points()    


    # update the points of minor's Choice courses by using the courses that are available in the minor only
    def update_minor_choice_courses_only(self):
        for course in self._minor_choice_courses_only:
            if course.is_finished_properly():
                if self._minor_points < self._required_minor_points:
                    self._minor_points += course.get_points()
                # this course is available only in this speciality, if we exceed the number of points
                # for this minor, we will put the course in external_points
                else:
                    self._external_points += course.get_points()


    # update the points of external speciality by using the courses that are not available in major and minor
    def update_external_points(self):
        for course in self._external_courses:
            is_finished, reason_if_not = course.is_finished_properly()
            if is_finished:
                self._external_points += course.get_points()
                self._total_points += course.get_points()
            else:
                self.add_invalid_course(course, reason_if_not)


    # here we update points of major, minor and external specialities by using the rest of the courses that have left.
    def update_major_minor_shared_courses_points(self):
        for course in self._major_minor_shared_courses:
            if course.is_finished_properly():
                if self._major_points < self._required_major_points:
                    self._major_points += course.get_points()
                elif self._minor_points < self._required_minor_points:
                    self._minor_points += course.get_points() 
                else:
                    self._external_points += course.get_points()





    def update_required_data(self):
        req_mand, req_maj, req_min, req_ext = self._syllabus_db.get_required_points(self._internship_type)
        req_min_must, req_maj_must = self._syllabus_db.get_required_speciality_must(self._internship_type)
        self._required_mandatory_points = req_mand
        self._required_major_points = req_maj
        self._required_minor_points = req_min
        self._required_external_points = req_ext
        self._required_major_must_courses = req_maj_must
        self._required_minor_must_courses = req_min_must


    # check if student has enough mandatory points
    # TODO: maybe change the parameters that this method returns
    def validate_mandatory_points(self):
        if self._required_mandatory_points <= self._mandatory_points:
            return True
        return False
    
    # check if student has enough external points
    # TODO: maybe change the parameters that this method returns
    def validate_external_points(self):
        if self._required_external_points <= self._external_points:
            return True
        return False
    
    # check if student has enough major points
    # TODO: maybe change the parameters that this method returns
    def validate_major_points(self):
        if self._required_major_points <= self._major_points:
            # TODO: need to check if completed the minimum must courses points in major
            return True
        return False
    
    # check if student has enough minor points
    # TODO: maybe change the parameters that this method returns
    def validate_minor_points(self):
        if self._required_minor_points <= self._minor_points:
            # TODO: need to check if completed the minimum must courses points in minor
            return True
        return False


    # check if the students is allowed to finish the degree 
    def run_courses_check(self):
        self.update_mandatory_points()
        self.update_internship_type()
        self.update_required_data()
        self.sort_speciality_courses_by_condition()
        self.update_speciality_points()

        # TODO: need to check if the amount of points matches the requirements
        # if self._required_mandatory_points < self._mandatory_points:
            
        # if self._required_major_points < self._major_points:
        
        # if self._required_minor_points < self._minor_points:
        
        # if self._required_external_points < self._external_points:
        #         # count how many speciality "must" courses the student took
                    #         self._major_must_count = 0 
                    #         self._minor_must_count = 0 

        #         # store the minimum number of "Must" courses the student need to take in major and minor specialities
                    #         self._required_major_must_courses = None
                    #         self._required_minor_must_courses = None   



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
    #syllabusDB = SyllabusDB("courses_fulllist.csv")
    syllabusDB = MagicMock()
    student = Student("student1.txt", syllabusDB)
    student.read_student_data()

    pass


if __name__ == "__main__":
    test_reading_student()
