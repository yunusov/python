from decimal import Decimal

a = Decimal('5')
b = Decimal('3.1415')
c = a + b
c-= Decimal('1')

z = 'Hello'
z*=10


# Для списка чисел вывести сумму чисел до первого отрицательного (не включая его).
# arr = [3, 5, 7, -2, 6]
# s = 0
# for n in arr:
#     if n < 0:
#         break
#     s += n
# print(s)


import itertools
arr = [3, 5, 7, -2, 6]
print(sum([n for n in itertools.takewhile(lambda x: x >= 0, arr)]))
