print(x + y)
print(x - y)
print(x * y)
print(x / y)

#나머지
print (x % y) #x를 y로 나눈 나머지 값 : 5 나누기 3 은 몫 1 나머지 2

#제곱
print(x ** y)

print(bin(x)) #2진수 binary = 0b
print(oct(x)) #8진수 (잘 안써서 몰라도 됨)
print(nex(x)) #16진수 (많이 쓰임) = 0x

#절댓값
x = -10
print(x)
print(abs(x))

y = 4.5
print(y)
print(int(y)) #소수점의 정수 파트 구하기

z = "100"
print(z) #문자열 100
print(int(z)) #숫자 100

#비트 연산자(AND, OR, NOT, XOP, NOT)
x = 5
y = 3
print (x & y) #5 = 101, 3 = 011, 5 AND 3 = 101 & 011 = 001
print(x | y) # 5 OR 3 = 101 OR 011 = 111
print(x ^ y) #XOR 110
print(~x) #NOT

print(x << 1) #왼쪽으로 한자리 이동 0000_0101 << 1 = 0000_1010
print(x >> 1) #오른쪽으로 한자리 이동 0000_0101 >> 1 = 0000_0010


