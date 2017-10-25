def my_wrapper(func):
    func(MyScreen())

class MyScreen:
    def __init__(self):
        pass

    def clear(self):
        pass

    def refresh(self):
        pass

    def addstr(self, *args):
        print(*args)

    def getkey(self):
        return input("key: ")

