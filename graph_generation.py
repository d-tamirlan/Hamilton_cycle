import random as r

a = int(input("Input nodes count: "))

b = [None] * a
for i in range(a):
    for j in range(a):
        b[j] = str(r.randint(0, 100))
    b[i] = "*"
    print(" ".join(b))