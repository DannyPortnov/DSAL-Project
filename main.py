import Course
from Student import Student
from SyllabusDB import SyllabusDB
import os


def init_student_and_db(student_file: str) -> Student:
    syllabus = SyllabusDB("courses_fulllist.csv")
    student = Student(student_file, syllabus)
    return student


def run_program(file_name: str):
    student = init_student_and_db(file_name)
    student.generate_result_file()


def is_txt_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension == '.txt'


if __name__ == "__main__":
    file_name = input("Please enter full name of student's file (with extension)\n")
    if is_txt_file(file_name):
        run_program(file_name)  # valid student
        print("Done! Check your folder for the output file")
    else:
        print("The file does not have a .txt extension. Run the program again.")

    # run_program("invalid major.txt")
    # run_program("Student with 2 specialties but missing 1 required in minor.txt")
    # run_program("minor computers.txt")
    # run_program("student with invalid internship.txt")
    # run_program("missing lots of parrallel and pre.txt")
    # run_program("missing 1 pre for speciality.txt")
    # run_program("minor is NA.txt")
