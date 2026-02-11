
def test_decor_simple():

    def super_decorator(n: int | None):
        def decorator(func):
            def wrapper(*args, **kwargs):
                print("Decorator - START")
                print(n)
                result = func(*args, **kwargs)
                print("Decorator - END")
                return result

            return wrapper
        return decorator



    @super_decorator(111)
    def my_func_1(name):
        print(f"my_func-1 {name}")

    @super_decorator
    def my_func_2(name):
        print(f"my_func-2 {name}")

    @super_decorator(333)
    def my_func_3(name):
        print(f"my_func-3 {name}")


    my_func_1(name="my_func_1")
    print()
    my_func_2(name="my_func_2")
    print()
    my_func_3(name="my_func_3")