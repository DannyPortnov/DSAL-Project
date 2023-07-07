from typing import List, Dict, Optional

def assign_courses(internship_type: str, specialities: List[str], credit_points: int, courses: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    # define the credit point requirements for each speciality based on the internship type
    if internship_type == 'industry':
        speciality_requirements = {'computers': 20, 'signals': 10, 'devices': 0}
    elif internship_type == 'project':
        speciality_requirements = {'computers': 15, 'signals': 0, 'devices': 5}
    else:
        speciality_requirements = {'computers': 0, 'signals': 0, 'devices': 0}

    # define the number of required courses for each speciality
    required_courses = {specialities[0]: 2, specialities[1]: 1}

    # initialize the assignment of courses to specialities
    assignment: Dict[str, List[Dict[str, str]]] = {speciality: [] for speciality in specialities}

    num_courses = len(courses)
    max_credit_points = credit_points + 1
    max_required_courses = max(required_courses.values()) + 1
    is_possible = [[[[False for l in range(max_required_courses)] for k in range(max_required_courses)] for j in range(max_credit_points)] for i in range(num_courses+1)]
    is_possible[0][0][0][0] = True

    for i in range(1, num_courses+1):
        for j in range(max_credit_points):
            for k in range(max_required_courses):
                for l in range(max_required_courses):
                    if courses[i-1]['speciality'] == specialities[0] or courses[i-1]['speciality'] == 'shared':
                        if j >= courses[i-1]['credit_points']:
                            if courses[i-1]['required_in_speciality'] == specialities[0] and k < max_required_courses - 1:
                                is_possible[i][j][k+1][l] |= is_possible[i-1][j-courses[i-1]['credit_points']][k][l]
                            else:
                                is_possible[i][j][k][l] |= is_possible[i-1][j-courses[i-1]['credit_points']][k][l]
                    if courses[i-1]['speciality'] == specialities[1] or courses[i-1]['speciality'] == 'shared':
                        m = credit_points - j
                        if m >= courses[i-1]['credit_points']:
                            if courses[i-1]['required_in_speciality'] == specialities[1] and l < max_required_courses - 1:
                                is_possible[i][j][k][l+1] |= is_possible[i-1][j][k][l]
                            else:
                                is_possible[i][j][k][l] |= is_possible[i-1][j][k][l]
                    is_possible[i][j][k][l] |= is_possible[i-1][j][k][l]

    if not any(is_possible[num_courses][j][required_courses[specialities[0]]][required_courses[specialities[1]]] for j in range(speciality_requirements[specialities[0]], max_credit_points)):
        raise ValueError("No valid assignment found")

    i = num_courses
    j = next(j for j in range(speciality_requirements[specialities[0]], max_credit_points) if is_possible[num_courses][j][required_courses[specialities[0]]][required_courses[specialities[1]]])
    k = required_courses[specialities[0]]
    l = required_courses[specialities[1]]
    while i > 0:
        m = credit_points - j
        if courses[i-1]['speciality'] == specialities[0] or courses[i-1]['speciality'] == 'shared':
            if j >= courses[i-1]['credit_points']:
                if courses[i-1]['required_in_speciality'] == specialities[0]:
                    if k > 0 and is_possible[i-1][j-courses[i-1]['credit_points']][k-1][l]:
                        assignment[specialities[0]].append(courses[i-1])
                        j -= courses[i-1]['credit_points']
                        k -= 1
                        i -= 1
                        continue
                else:
                    if is_possible[i-1][j-courses[i-1]['credit_points']][k][l]:
                        assignment[specialities[0]].append(courses[i-1])
                        j -= courses[i-1]['credit_points']
                        i -= 1
                        continue
        if courses[i-1]['speciality'] == specialities[1] or courses[i-1]['speciality'] == 'shared':
            if m >= courses[i-1]['credit_points']:
                if courses[i-1]['required_in_speciality'] == specialities[1]:
                    if l > 0 and is_possible[i-1][j][k][l-1]:
                        assignment[specialities[1]].append(courses[i-1])
                        l -= 1
                        i -= 1
                        continue
                else:
                    if is_possible[i-1][j][k][l]:
                        assignment[specialities[1]].append(courses[i-1])
                        i -= 1
                        continue
        i -= 1

    # check that the sum of credit points for each speciality equals the requirements
    for speciality in specialities:
        if sum(course['credit_points'] for course in assignment[speciality]) != speciality_requirements[speciality]:
            raise ValueError(f"The sum of credit points for {speciality} does not equal the requirement")
        
    # check that the number of required courses for each speciality has been met
    for speciality in specialities:
        num_required_courses = sum(1 for course in assignment[speciality] if course['required_in_speciality'] == speciality)
        if num_required_courses < required_courses[speciality]:
            raise ValueError('The number of required courses for each speciality has not been met')

    return assignment

# is_possible[i][j] represents whether it is possible to assign the first
#  i courses such that the first speciality has j credit points.
#  The second speciality’s credit points can be inferred from
#  the total credit points and the first speciality’s credit points.

# example usage
courses = [{ 'credit_points': 5, 'speciality': 'shared', 'required_in_speciality': 'computers'},
           { 'credit_points': 5, 'speciality': 'shared', 'required_in_speciality': 'computers'},
           { 'credit_points': 5, 'speciality': 'shared', 'required_in_speciality': 'signals'},
           { 'credit_points': 4, 'speciality': 'shared', 'required_in_speciality': None},
           { 'credit_points': 3, 'speciality': 'shared', 'required_in_speciality': None},
           { 'credit_points': 3, 'speciality': 'shared', 'required_in_speciality': None},
           { 'credit_points': 2, 'speciality': 'shared', 'required_in_speciality': None},
           { 'credit_points': 3, 'speciality': 'shared', 'required_in_speciality': None}]
assignment = assign_courses('industry', ['computers', 'signals'], 30, courses)
print(assignment)

# O(n * m^2 * r^2), where n is the number of courses, m is the maximum number of credit points, and r is the maximum number of required courses.
