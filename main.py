import Course
from Student import Student
from SyllabusDB import SyllabusDB

# open the csv file and read only the first line- header
# header = ['Semester','Number','Points','Name','is_must','computers','signals','devices','precourse a','precourse b',...,parallel]


def init_student_and_db(student_file: str) -> Student:
    syllabus = SyllabusDB("courses_fulllist.csv")
    student = Student(student_file, syllabus)
    return student


def run_program(file_name: str):
    student = init_student_and_db(file_name)
    student.generate_result_file()


if __name__ == "__main__":
    run_program("student1.txt")  # valid student
    run_program("invalid major.txt")
    run_program("Student with 2 specialties but missing 1 required in minor.txt")
    run_program("minor computers.txt")
    run_program("student with invalid internship.txt")
    run_program("missing lots of parrallel and pre.txt")
