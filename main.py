from Student import Student
from SyllabusDB import SyllabusDB
import os


def init_student_and_db(student_file):
    syllabus = SyllabusDB("courses_fulllist.csv")
    student = Student(student_file, syllabus)
    return student


def run_program(file_name):
    student = init_student_and_db(file_name)
    student.generate_result_file()


def is_txt_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension == '.txt'


if __name__ == "__main__":
    file_name = input("Please enter full name of student's file (with extension):\n")
    if is_txt_file(file_name):
        run_program(file_name) 
        print("Done! Check your folder for the output file")
    else:
        print("The file does not have a .txt extension. Run the program again.")