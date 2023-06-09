class Speciality:
    "Speciality Object Implementation"

    def __init__(self, name):
        self._name = name
        self._courses = dict()      # key: course number, value: course object


    def get_name(self):
        return self._name

    def add_course(self, course):
        if course.get_speciality(self._name) is not None:
            self._courses[course.get_number()] = course
        

    def get_course(self, number):
        if number in self._courses.keys():
            return self._computers[number]
        else:
            print("Does not exist")
            return None