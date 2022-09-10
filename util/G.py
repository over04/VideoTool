class Gdata:
    def __init__(self):
        self.__data = {}
        self.__head = 0

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __getitem__(self, item):
        return self.__data[item]

    def __iter__(self):
        return self

    def __next__(self):
        if self.__head == len(self.__data):
            self.__head = 0
            raise StopIteration
        else:
            data = list(self.__data.keys())[self.__head]
            self.__head += 1
            return data

    def get(self, key, default = None):
       return self.__data.get(key,default)


g = Gdata()
