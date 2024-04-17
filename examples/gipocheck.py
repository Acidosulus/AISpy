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