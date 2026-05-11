numbers = [1, 2, 3, 4, 5]

for num in numbers:
    print(num)

n = 100
count = 0

for i in range(n):
    for j in range(n):
        count += 1

print('연산: ', count)