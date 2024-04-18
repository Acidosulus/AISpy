class ParentClass:
    val = 1
    def vr(self):
        print(self.val)

class ChildClass(ParentClass):
    val = 2
    pass

obj = ChildClass()

class_ref = obj.__class__

class_name = class_ref.__name__

print("Имя класса объекта:", class_name)

obj.vr()

print('========================')


class EC():
    def vr(self):
        return 1

foo = eval('EC()')
print(type(foo))
print(foo.vr())


print('========================')

def foo(length:int) -> list:
    result = []
    for i in (range(length+1) if length>=0 else range(length,0+1)):
        if i % 2 == 0:
            result.append(i)
    return result

print(*foo(-10))


def foo2(length:int) -> list:
    return (i for i in (range(length+1) if length>=0 else range(length,0+1)) if i % 2 == 0)

print(*foo2(-10))