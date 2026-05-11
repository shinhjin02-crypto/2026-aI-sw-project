print(my_list[-1])
print(my_list[-2])

print(my_list[1:3])
print(my_list[3:5]) #3포함 5안포함
print(my_list[:2]) #시작부터 2를 포함하지 않는 것까지
print(my_list[2:]) #2부터 끝까지

my_list.remove(99)
print(my_list)

#특정 인덱스 요소 삭제하기
my_list.pop(3) #3 인덱스 삭제
print(my_list)