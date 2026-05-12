#1.
with open("file.txt", "r", encoding="utf-8") as file:
    data = file.read()
    print("파일 내용: ", data)

#2.
#file = open("file.txt", "r", encoding="utf-8")
#data = file.read()
#file.close()

#3.큰 파일 읽기
with open("file.txt", "r", encoding="tuf-8") as file:
    lines = file.readlines()
    print("파일 내용: ", lines)