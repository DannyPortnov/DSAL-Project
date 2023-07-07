def assign_courses(internship_type, specialities, credit_points, courses):
    # define the credit point requirements for each speciality based on the internship type
    if internship_type == 'industry':
        speciality_requirements = {'computers': 20, 'signals': 10, 'devices': 0}
    elif internship_type == 'project':
        speciality_requirements = {'computers': 15, 'signals': 0, 'devices': 5}
    else:
        speciality_requirements = {'computers': 0, 'signals': 0, 'devices': 0}

    # initialize the assignment of courses to specialities
    assignment = {speciality: [] for speciality in specialities}

    n = len(courses)
    m = credit_points + 1
    dp = [[[False for k in range(m)] for j in range(m)] for i in range(n+1)]
    dp[0][0][0] = True

    for i in range(1, n+1):
        for j in range(m):
            for k in range(m):
                if courses[i-1]['speciality'] == specialities[0] or courses[i-1]['speciality'] == 'shared':
                    if j >= courses[i-1]['credit_points']:
                        dp[i][j][k] |= dp[i-1][j-courses[i-1]['credit_points']][k]
                if courses[i-1]['speciality'] == specialities[1] or courses[i-1]['speciality'] == 'shared':
                    if k >= courses[i-1]['credit_points']:
                        dp[i][j][k] |= dp[i-1][j][k-courses[i-1]['credit_points']]
                dp[i][j][k] |= dp[i-1][j][k]

    if not dp[n][speciality_requirements[specialities[0]]][speciality_requirements[specialities[1]]]:
        return None

    i = n
    j = speciality_requirements[specialities[0]]
    k = speciality_requirements[specialities[1]]
    while i > 0:
        if courses[i-1]['speciality'] == specialities[0] or courses[i-1]['speciality'] == 'shared':
            if j >= courses[i-1]['credit_points'] and dp[i-1][j-courses[i-1]['credit_points']][k]:
                assignment[specialities[0]].append(courses[i-1])
                j -= courses[i-1]['credit_points']
                i -= 1
                continue
        if courses[i-1]['speciality'] == specialities[1] or courses[i-1]['speciality'] == 'shared':
            if k >= courses[i-1]['credit_points'] and dp[i-1][j][k-courses[i-1]['credit_points']]:
                assignment[specialities[1]].append(courses[i-1])
                k -= courses[i-1]['credit_points']
                i -= 1
                continue
        i -= 1

    return assignment

# example usage
courses = [{'name': 'Course A', 'credit_points': 5, 'speciality': 'shared'},
           {'name': 'Course B', 'credit_points': 5, 'speciality': 'shared'},
           {'name': 'Course C', 'credit_points': 5, 'speciality': 'shared'},
           {'name': 'Course D', 'credit_points': 4, 'speciality': 'shared'},
           {'name': 'Course D', 'credit_points': 3, 'speciality': 'shared'},
           {'name': 'Course D', 'credit_points': 3, 'speciality': 'shared'},
           {'name': 'Course D', 'credit_points': 2, 'speciality': 'shared'},
           {'name': 'Course D', 'credit_points': 3, 'speciality': 'shared'}]
assignment = assign_courses('industry', ['computers', 'signals'], 30, courses)
print(assignment)
#  O(n * m^2) time, where n is the number of courses and m is the maximum number of credit points.
