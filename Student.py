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
        self._courses = list()  # list of the courses the student took, useful for priniting
        self._invalid_courses = dict()  # key: course, value: why course is invalid
    
    # def __init__(self, name, id):
    # # def __init__(self, name, id, major, minor, general_points, sport_points):
    #     self._name = name
    #     self._id = id
    #     self._major = major
    #     self._minor = minor
    #     self._general_points = general_points
    #     self._sport_points = sport_points
    #     self._courses = list()  # list of the courses the student took, useful for priniting

    def _open_db(self):
        f = open(self._file, "r", encoding="utf-8")
        return f

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
    # add a course object to the stduent's list of courses
    def add_course(self, course):
        self._courses.append(course)
        course.mark_as_done()


    def read_student_data(self):
        f = self._open_db()
        first_comment = f.readline()
        line = f.readline()
        self.set_name(extract_student_data_from_line(line))
        line = f.readline()
        self.set_id(extract_student_data_from_line(line))
        line = f.readline()
        self.set_major(extract_student_data_from_line(line))
        line = f.readline()
        self.set_minor(extract_student_data_from_line(line))
        line = f.readline()
        self.set_general_points(extract_student_data_from_line(line))
        line = f.readline()
        self.set_sport_points(extract_student_data_from_line(line))

        while line:
            line = f.readline()
            course_number, credit, name = extract_course_data_from_line(line)
            course = self._syllabus_db.get_course_by_number(course_number)
            if course.validate_course(course_number, credit, name):
                self.add_course(course)
            else:
                self._invalid_courses[course] = "Course's data does not match Syllabus"




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



def ignore_comments(line):
    pass