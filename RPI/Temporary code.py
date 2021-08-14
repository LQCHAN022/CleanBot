class testclass():
    def __init__(self):
        self.attr = 10
    def add2(self):
        self.attr += 2

a = testclass()
print(a.attr)

def add2(cls):
    cls.attr += 2
    cls.add2()

add2(a)

print(a.attr)

print("Front {}".format(a.attr))