
# Given the names and grades for each student in a Physics class of N students, store them in a nested list and print the name(s) of any student(s) having the second lowest grade.
# Note: If there are multiple students with the same grade, order their names alphabetically and print each name on a new line.

if __name__ == '__main__':
    students = {}
    for _ in range(int(input())):
        name = input()
        score = float(input())
        if str(score) in students.keys():
            students[str(score)].append(name)
        else:
            students[str(score)] = [name]

    keys = sorted(list(map(float, students.keys())))
    if len(keys) >= 1:
        students[str(keys[1])] = sorted(students[str(keys[1])])
        for student in students[str(keys[1])]:
            print(student)
