try:
    result = 10/0
except:
    print("알 수 없는 오류입니다.")

print("다음 코드 정상 진행")

try:
    number = int("hello")
except ValueError:
    print("해당 글자는 숫자로 변환할 수 없습니다.")
print("아몰랑 일단 에러 통과 ..")

alist = [1,2,3]
try:
    alist[3]
except IndexError:
    print("입력 범위를 초과하였습니다.")

# result = 10 / 0

# number = int("hello")

#alist = [1, 2, 3]
#alist[1]

try:
    with open("없는 파일 명.txt", "r") as file:
        data =  file.read()
except FileNotFoundError:
    print("해당 파일이 존재하지 않습니다.")
