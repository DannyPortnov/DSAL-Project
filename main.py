import Course
from Student import Student
from SyllabusDB import SyllabusDB

# open the csv file and read only the first line- header
# header = ['Semester','Number','Points','Name','is_must','computers','signals','devices','precourse a','precourse b',...,parallel]


def open_db(file):
    f = open(file, "r", encoding="utf-8")
    header = f.readline().strip().split(',')
    return f, header

# need to get the pre_courses objects by using the pre courses list of strings


def get_pre_course_obj(pre_courses_list):
    pass

# def extract_line(line):
#     number = line[1]
#     points = line[2]
#     name = line[3]
#     is_must = line[4]
#     computers = line[5]
#     signals = line[6]
#     devices = line[7]
#     pre_courses_list = get_pre_course_obj(line[8:12])
#     parallel_course = line[12]
#     return number, points, name, is_must, computers, signals, devices, pre_courses_list, parallel_course


def generate_db(file):
    f, line = open_db(file)
    while line:
        line = f.readline().strip().split(',')    # read course data to a list
        # number, points, name, is_must, computers, signals, devices, pre_courses_list, parallel_course = extract_line(d)
        # course = Course(number, points, name, is_must, computers, signals, devices, pre_courses_list, parallel_course)
        course = Course(line[1], float(line[2]), line[3], line[4], line[5],
                        line[6], line[7], get_pre_course_obj(line[8:12]), line[12])

        # another way: if we use the other Course's implementation:
        # course = Course()
        # course.set_number(line[1])
        # course.set_points(line[2])
        # course.set_name(line[3])
        # course.set_condition(line[4])

        # course.set_specialties(line[5], line[6], line[7])
        # course.set_pre_courses(line[8:12])

    # *point*
    # If the code reaches this point, it means you have finished reading the file


def test_invalid_intership() -> None:
    student = init_student_and_db(
        "student with invalid intership.txt")
    student.generate_result_file()


def test_minor_computers() -> None:

    student = init_student_and_db("minor computers.txt")
    student.generate_result_file()


def test_2_specialities_with_1_missing_required_in_minor() -> None:

    student = init_student_and_db(
        "Student with 2 specialties but missing 1 required in minor.txt")
    student.generate_result_file()


def init_student_and_db(student_file: str) -> Student:
    syllabus = SyllabusDB("courses_fulllist.csv")
    student = Student(student_file, syllabus)
    return student


def valid_student(init_student_and_db):
    student = init_student_and_db("student1.txt")
    student.generate_result_file()


if __name__ == "__main__":
    test_2_specialities_with_1_missing_required_in_minor()
    # test_minor_computers()
    # test_invalid_intership()
    # valid_student(init_student_and_db)
