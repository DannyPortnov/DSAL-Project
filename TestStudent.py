from typing import List, Dict, Optional, Any

def assign_courses(internship_type: str, specialities: List[str], credit_points: int,
                    courses: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, str]]]:
    # define the credit point requirements for each speciality based on the internship type
    if internship_type == 'industry':
        speciality_requirements = {'computers': 20, 'signals': 10, 'devices': 0}
    elif internship_type == 'project':
        speciality_requirements = {'computers': 15, 'signals': 0, 'devices': 5}
    else:
        speciality_requirements = {'computers': 0, 'signals': 0, 'devices': 0}

    # initialize the assignment of courses to specialities
    assignment:Dict[str, List[Dict[str, str]]] = {speciality: [] for speciality in specialities}

    num_courses = len(courses)
    max_credit_points = credit_points + 1
    is_possible = [[False for j in range(max_credit_points)] for i in range(num_courses+1)]
    is_possible[0][0] = True

    for i in range(1, num_courses+1):
        for j in range(max_credit_points):
            if courses[i-1]['speciality'] == specialities[0] or courses[i-1]['speciality'] == 'shared':
                if j >= courses[i-1]['credit_points']:
                    is_possible[i][j] |= is_possible[i-1][j-courses[i-1]['credit_points']]
            if courses[i-1]['speciality'] == specialities[1] or courses[i-1]['speciality'] == 'shared':
                k = credit_points - j
                if k >= courses[i-1]['credit_points']:
                    is_possible[i][j] |= is_possible[i-1][j]
            is_possible[i][j] |= is_possible[i-1][j]

    if not any(is_possible[num_courses][j] for j in range(speciality_requirements[specialities[0]], max_credit_points)):
        raise ValueError('There is no possible assignment of courses to specialities')

    i = num_courses
    j = next(j for j in range(speciality_requirements[specialities[0]], max_credit_points) if is_possible[num_courses][j])
    while i > 0:
        k = credit_points - j
        if courses[i-1]['speciality'] == specialities[0] or courses[i-1]['speciality'] == 'shared':
            if j >= courses[i-1]['credit_points'] and is_possible[i-1][j-courses[i-1]['credit_points']]:
                assignment[specialities[0]].append(courses[i-1])
                j -= courses[i-1]['credit_points']
                i -= 1
                continue
        if courses[i-1]['speciality'] == specialities[1] or courses[i-1]['speciality'] == 'shared':
            if k >= courses[i-1]['credit_points'] and is_possible[i-1][j]:
                assignment[specialities[1]].append(courses[i-1])
                i -= 1
                continue
        i -= 1

    # check that the sum of credit points for each speciality equals the requirements
    # Not sure it is necessary to check this, consider removing it later
    for speciality in specialities:
        if sum(course['credit_points'] for course in assignment[speciality]) != speciality_requirements[speciality]:
            raise ValueError('The sum of credit points for each speciality should equal the requirements')

    return assignment

# is_possible[i][j] represents whether it is possible to assign the first
#  i courses such that the first speciality has j credit points.
#  The second speciality’s credit points can be inferred from
#  the total credit points and the first speciality’s credit points.

# example usage
courses = [{'credit_points': 5, 'speciality': 'shared'},
           {'credit_points': 5, 'speciality': 'shared'},
           {'credit_points': 5, 'speciality': 'shared'},
           {'credit_points': 4, 'speciality': 'shared'},
           {'credit_points': 3, 'speciality': 'shared'},
           {'credit_points': 3, 'speciality': 'shared'},
           {'credit_points': 2, 'speciality': 'shared'},
           {'credit_points': 3, 'speciality': 'shared'}]
choosen_intership = 'industry'
assignment = assign_courses(choosen_intership, ['computers', 'signals'], 30, courses)

print(assignment)

# O(n * m) time, where n is the number of courses and m is the maximum number of credit points.
