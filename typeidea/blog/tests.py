from django.test import TestCase

# Create your tests here.
a = 2**1000
a = str(a)
s = 0
for i in a:
    i = int(i)
    print(i)
    s += i

print(s)
