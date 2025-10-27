# print('Hello world')

# print('Hello, ', input())

def practice_3():
    a = int(input())
    b = int(input())
    result = True
    while c := input():
        c = int(c)
        if a > c or b < c:
            result = False
            break
    print(result)

def practice_4():
    a = input()
    result = False
    for i in a:
        if (i == 'o' or i == 'a'):
            result = True
        if (i == 'i' or i == 'e'):
            result = False
            break
    print(result)

def practice_5():
    a = input()
    b = input()
    c = input()

practice_5()