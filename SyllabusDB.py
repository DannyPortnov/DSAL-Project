import Course
import SpecialityCourse
import SpecialityCoursesDB

class SyllabusDB:
    "Syllabus Data base Object Implementation"

    def __init__(self, file):
        self._file_name = file
        self._mandatory_courses = dict()     # key: course number, value: course object
        # self._final_project_courses = dict()  # holds the type of final project that are available
        self._computers = SpecialityCoursesDB("Computers")
        self._signals = SpecialityCoursesDB("Signals")
        self._devices = SpecialityCoursesDB("Devices")

        self._total_points = 160
        self._mandatory_points = {"industry": 129, "research": 124, "project": 122}
        self._major_points = {"industry": 20, "research": 20, "project": 20}
        self._minor_points = {"industry": 0, "research": 10, "project": 10}
        self._external_points = {"industry": 11, "research": 6, "project": 8}
        self._major_must_courses = {"industry": 4, "research": 4, "project": 4}
        self._minor_must_courses = {"industry": 0, "research": 3, "project": 3}
        self._general_points = 6
        self._sport_points = 1

    
    # open the csv file and read only the first line- header
    def _open_db(self):
        f = open(self._file, "r", encoding="utf-8")
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
    def get_required_points(self, final_project):
        return self._mandatory_points[final_project], self._major_points[final_project], \
                self._minor_points[final_project], self._external_points[final_project]
    
    def get_required_speciality_must(self, final_project):
        return self._minor_must_courses[final_project], self._major_must_courses[final_project]

    # TODO: update DB creation to ignore the lines with the symbol: #
    def create_db(self):
        f, line = self._open_db()
        while line:
            line = f.readline().strip().split(',')    # read course data to a list
            # number, points, name, is_must, computers, signals, devices, pre_courses_list, parallel_course = extract_line(d)
            # course = Course(number, name, points, is_must, computers, signals, devices, pre_courses_list, parallel_course)
            if line[4] == "חובה":
                course = Course(int(line[1]), line[2], float(line[3]), line[4], get_pre_course_obj(line[8:12]), self.get_course_by_number(line[12]))
                self._mandatory_courses[course.get_points()] = course
            else:
                # TODO: catch with regex the type of course in the speciality Computers: catch if belongs to HW or SW
                course = SpecialityCourse(int(line[1]), line[2], float(line[3]), line[4], line[5], line[6], line[7], get_pre_course_obj(line[8:12]), self.get_course_by_number(line[12]))
                self._computers.add_course(course)
                self._signals.add_course(course)
                self._devices.add_course(course)



    def get_course_by_number(self, number):
        if number in self._mandatory_courses.keys():
            return self._mandatory_courses[number]
        else:
            print("Does not exist")
        
        course = self._computers.get_course(number)
        if course is not None:
            return course
        
        course = self._signals.get_course(number)
        if course is not None:
            return course
        
        course = self._devices.get_course(number)
        if course is not None:
            return course




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
def get_pre_course_obj(pre_courses_list):
    pass
