import time


class Log:
    def __init__(self, message, message_type, success, adder='main'):
        self.__time = time.time()
        self.__message = message
        self.__success = success
        self.__message_type = message_type
        self.__adder = adder

    @property
    def text(self):
        return f"({self.__adder})" \
               f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.__time))}]" \
               f"{self.__message_type}: {self.__message}"

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text

    def __eq__(self, other):
        return other == self.__success


if __name__ == '__main__':
    a = Log('测试', 'message.text', False)
    if a != False:
        print(a)
