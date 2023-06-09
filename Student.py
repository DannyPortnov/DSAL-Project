from io import TextIOWrapper
import regex as re


class Student:
    "Student Object Implementation"

    def __init__(self, file_name, syllabus_db):
        # def __init__(self, name, id, major, minor, general_points, sport_points):
        self._file_name = file_name
        self._syllabus_db = syllabus_db
        self._name = None
        self._id = None
        self._major = None
        self._minor = None
        self._general_points = None
        self._sport_points = None

        self._internship_type = None   # holds the type of internship that the student chose
     
        # store the minimum points in order to complete
        self._required_mandatory_points = None
        self._required_major_points = None
        self._required_minor_points = None
        self._required_external_points = None


        # calculate the amount of points the student got
        self._total_points = 0
        self._mandatory_points = 0
        self._major_points = 0
        self._minor_points = 0
        self._external_points = 0

        self._mandatory_courses = dict()  # key: course number, value: course object
        self._speciality_courses = dict()  # key: course number, value: course object
        self._invalid_courses = dict()  # key: course, value: why course is invalid

    # def _open_db(self):
    #     f = open(self._file, "r", encoding="utf-8")
    #     return f

    def set_name(self, name):
        self._name = name

    def set_id(self, id):
        self._id = id

    def set_major(self, major):
        self._major = major

    def set_minor(self, minor):
        self._minor = minor

    def set_general_points(self, general_points):
        self._general_points = general_points

    def set_sport_points(self, sport_points):
        self._sport_points = sport_points

    # TODO: maybe change the list to another data structure
    # add a course object to the stduent's dict of mandatory courses
    def add_mandatory_course(self, course):
        self._mandatory_courses[course.get_number()] = course
        course.mark_as_done()

    # add a course object to the stduent's dict of speciality courses
    def add_speciality_course(self, course):
        self._speciality_courses[course.get_number()] = course
        course.mark_as_done()
    
    # add a course object to the stduent's dict of invlid courses
    def add_invalid_course(self, course, message):
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

        while line:
            line = next(self._ignore_comments(file))
            course_number, credit, name = extract_course_data_from_line(line)
            course = self._syllabus_db.get_course_by_number(course_number)
            if course.validate_course(course_number, credit, name):
                if course.is_mandatory():
                    self.add_mandatory_course(course)
                else:
                    self.add_speciality_course(course)              
            else:
                self._invalid_courses[course] = "Course's data does not match Syllabus"


    def _ignore_comments(self, file: TextIOWrapper):
            for line in file:
                if not line.startswith("#"):
                    yield line.strip()


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
            self._internship_type = "industry"
       
        # check if project is research in the college
        elif (31052 in self._mandatory_courses.keys()) and (31053 in self._mandatory_courses.keys()):
            # check if the project type had already updated, if so- the student did not report the project courses correctly        
            # if self._internship_type is None:   
            self._internship_type = "research"
       
        # check if project is mini_project in the college
        elif (31050 in self._mandatory_courses.keys()) and (31051 in self._mandatory_courses.keys()):
            # check if the project type had already updated, if so- the student did not report the project courses correctly
            # if self._internship_type is None:
            self._internship_type = "project"
        else:
            self._internship_type = "Invalid Project Type Selection"

    

    def update_mandatory_points(self, course):
        for course in self._mandatory_courses.values():
            if course.is_finished_properly():
                        self._total_points += course.get_points()
                        self._mandatory_points += course.get_points()
            else:
                # TODO: pop out an invalid course from self._courses dict
                self.add_invalid_course(course, "Student did not finish one of the pre-courses")
            

    def update_speciality_points(self, course):
        for course in self._speciality_courses.values():

            if course.is_finished_properly():
                        self._total_points += course.get_points()
                        self._mandatory_points += course.get_points()
            else:
                # TODO: pop out an invalid course from self._courses dict
                self.add_invalid_course(course, "Student did not finish one of the pre-courses")


    def update_required_points(self):
        req_mand, req_maj, req_min, req_ext = self._syllabus_db.get_required_points(self._internship_type)
        self._required_mandatory_points = req_mand
        self._required_major_points = req_maj
        self._required_minor_points = req_min
        self._required_external_points = req_ext



    # check if the students is allowed to finish the degree 
    def run_courses_check(self):
        self.update_mandatory_points()
        self.update_internship_type()
        self.update_required_points()




        # for course in self._courses:            
        #     if course.is_mandatory():
        #         self.update_mandatory_points(course)
        #     else:   # course is a SpecialtyCourse
        #         self._project_type = self.check_project_type()
        #         if self._project_type is not "Invalid Project Type Selection":
                    





def extract_course_data_from_line(line):
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


def extract_student_data_from_line(line):
    line = line.strip()  # Remove leading/trailing whitespaces
    # Use regex to extract the field name and its value while ignoring text after '#'
    match = re.match(r'([^:]+):\s*([^#]*)', line)
    if match:
        field_value = match.group(2).strip()
    return field_value


def test_ignoring_comments():
    student = Student("student1.txt", None)
    student.read_student_data()
    pass


if __name__ == "__main__":
    test_ignoring_comments()
