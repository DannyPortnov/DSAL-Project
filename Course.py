# class Course:
#     "Course Object Implementation"

#     def __init__(self):
#         self._name = None
#         self._number = None
#         self._points = None
#         self._is_must = None        # is the course's condition must or choice
#         self._pre_courses = dict()  # hold the pre-courses that must be taken before this course
#         self._specialties = dict()  # holds the specialties in which this course is available
#         self._is_done = False       # in order to check if a student took a course or not- default value is false


#     def set_name(self, name):
#         self._name = name
    
#     def set_number(self, number):
#         self._number = number
    
#     def set_points(self, points):
#         self._points = points

#     # set the specialties condition: key = name ; value = must, choice or none
#     def set_specialties(self, computers, signals, devices):
#         if self._is_must:
#             raise TypeError('This Course Is Must, Not A Specialty')
#         self._specialties["computers"] = number_to_condition(computers)
#         self._specialties["signals"] = number_to_condition(signals)
#         self._specialties["devices"] = number_to_condition(devices)
        
#     # set a pre_course, key = pre_course's Course object
#     def set_pre_courses(self, pre_courses_list):
#         if len(pre_courses_list):
#             for course in pre_courses_list:
#                 self._pre_courses[course] = None
    
#     # set the condition of the course: must or choise
#     def set_condition(self, is_must):
#         if is_must:
#             self._is_must = True
#         self._is_must = False

#     # mark if a student took this course
#     def mark_as_done(self):
#         self._is_done = True 

#     # returns the condition of a course: must or choise
#     def check_if_must(self):
#         return self._is_must

#     # returns course's status, if it was taken or not
#     def get_status(self):
#         return self._is_done
    
#     # validate if the pre courses are finished
#     def validate_pre_courses(self):
#         if len(self._pre_courses):
#             for course in self._pre_courses.keys():
#                 if course.get_status() is False:
#                     return False
#         return True
        
# # function that converts a condition's value to an actual word
# def number_to_condition(num):
#     if num == 1:
#         return "Must"
#     elif num == 2:
#         return "Choice"
#     else:
#         return None
    

class Course:
    "Course Object Implementation"

    # def __init__(self, number, points, name, is_must, computers, signals, devices, pre_courses_list, parallel_course):
    def __init__(self, number, points, name, is_must, pre_courses_list, parallel_course):
        self._name = name
        self._number = number
        self._points = points
        self._is_must = self._set_condition(is_must)     # is the course's condition must or choice
        self._pre_courses = self._set_pre_courses(pre_courses_list)     # hold the pre-courses that must be taken before this course
        # self._specialties = self._set_specialties(computers, signals, devices)  # the specialties in which this course is available
        self._parallel_course = parallel_course
        self._is_done = False       # in order to check if a student took a course or not- default value is false


    # # set the specialties condition: key = name ; value = must, choice or none
    # def _set_specialties(self, computers, signals, devices):
    #     specialties = dict()
    #     # if self._is_must is False:
    #     specialties["computers"] = number_to_condition(computers)
    #     specialties["signals"] = number_to_condition(signals)
    #     specialties["devices"] = number_to_condition(devices)
    #     return specialties
    #     # else:
    #     #     specialties["computers"] = None
    #     #     specialties["signals"] = None
    #     #     specialties["devices"] = None
    #     # raise TypeError('This Course Is Must, Not A Specialty')
    
    # set a pre_course, key = pre_course's Course object
    def _set_pre_courses(self, pre_courses_list):
        if len(pre_courses_list):
            for course in pre_courses_list:
                self._pre_courses[course] = None
    
    # set the condition of the course: must or choise
    def _set_condition(self, is_must):
        if is_must:
            self._is_must = True
        self._is_must = False

    # mark if a student took this course
    def mark_as_done(self):
        self._is_done = True 

    # returns the condition of a course: must or choise
    def check_if_must(self):
        return self._is_must

    # returns course's status, if it was taken or not
    def get_status(self):
        return self._is_done
 
    # returns course's points
    def get_points(self):
        return self._points
   
    # returns course's number
    def get_number(self):
        return self._number
    
    # validate if the pre courses are finished
    def validate_pre_courses(self):
        if len(self._pre_courses):
            for course in self._pre_courses.keys():
                if course.get_status() is False:
                    return False
        return True
        
    # validate a course by checking it's points, name and number
    def validate_course(self, number, points, name):
        if number is self._number and points is self._points and name is self._name:
            return True
        
        return False
    






# function that converts a condition's value to an actual word
def number_to_condition(num):
    if num == 1:
        return "Must"
    elif num == 2:
        return "Choice"
    else:
        return None