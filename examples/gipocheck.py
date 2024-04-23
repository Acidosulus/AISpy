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

print('========================')

def outer_function(x):
    def inner_function(y):
        return x + y
    return inner_function

closure = outer_function(5)
print(closure(3))  # Выведет 8


print('========================')
def mul(a):
        def helper(b):
            return a * b
        return helper

print(mul(5)(2))

print('========================')

my_dict = {'a': 1, 'b': 2, 'c': 3}

for key in my_dict.keys():
    print(my_dict[key])


print('========================')
print('========================')


def cached(func):
    cache = {}
    def wrapper(*args, **kwargs):
        key=(*args,frozenset(kwargs.items()))
        print('KEY:',key)
        if key in cache:
            return f'cached: {cache[key]}'
        result = func(*args, **kwargs)
        cache[key] = result
        return result
    return wrapper

@cached
def add(a,b:int)->int:
    return a + b


print(add(1,6))
print(add(1,b=2))
print(add(1,6))
print(add(1,b=2))

import time
def time_meter(func):
    start_time = time.time()
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'Function: {func.__name__} Parameters: {(*args, kwargs)}  Execution time: {time.time()-start_time}')
        return result
    return wrapper

@time_meter
def slow_func(count):
    for i in range(count):
        k=i
        j=k
        k=j
    return k


print(slow_func(count = 10000000))