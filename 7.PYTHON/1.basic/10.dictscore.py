students = {
    "민수" : 84,
    "지은" : 23,
    "서준" : 77,
    "하린" : 91,
    "도윤" : 65,
    "예린" : 48,
    "지후" : 12,
    "수아" : 99,
    "현우" : 53,
    "유진" : 71 
 }

print(students)

def get_a_student(students):
    a_students = []
    for name, scroe in students.items():
        if score >= 90:
            a_students.append(name)
    return a_students
