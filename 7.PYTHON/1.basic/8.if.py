print('--- if 구문 ---')

score = 70
if score >= 80:
    #print('성적은 A+ 입니다.')
    grade = 'A'
elif score >=70:
    #print('성적은 B 입니다.')
    grade = 'B'
elif score >= 60:
    #print('성적은 C 입니다.')
    grade = 'C'
else:
    #print('성적은 D 입니다.')
    grade = 'D'

print (f'이 학생의 점수는 {score}이고, 학점은 {grade} 입니다.')

month = 7
if month in [12, 1, 2]:
    #print('겨울 입니다.')
    season = '겨울'
elif month in [3, 4, 5]:
    #print('봄입니다.')
    season = '봄'
elif month in [6, 7, 8]:
    season = '여름'
elif month in [9, 10, 11]:
    season = '가을'
else:
    season = '알 수 없는'

print(f'{month}월은 {season} 입니다.')

height = 175
weight = 70
bmi = weight / ((height / 10) ** 2)

if bmi < 18.5:
    category = '저체중'
elif bmi < 25:
    category = '정상'
elif bmi < 30:
    category = '과체중'
else:
    category = '비만'

print(f'ooo님의 키는 {height} 이고, 몸무게는 {weight} 이고, BMI 지수는 {bmi}이며, 결론은 {category} 입니다.')

username = 'user'
password = '1234'

if username and password:
    if username == 'admin' and password == '1234':
        print('관리자로 로그인 되었습니다.')
    elif username == 'user' and password == '1234':
        print('잘못된 ID 또는 비밀번호 입니다.')
    else:
        print('유저네밈과 비밀번호를 입력하세요.')