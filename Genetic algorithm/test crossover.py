import random

a = [1, 2, 3, 4, 5, 6]
b = [5, 2, 4, 6, 1, 3]
c = [None]*len(a)

r = random.randint(1, len(a))
temp = []

for i in range(0, len(b)):
    if b[i] not in a[0:r]:
        temp.append(b[i])

c = a[0:r] + temp
print(r, c)



