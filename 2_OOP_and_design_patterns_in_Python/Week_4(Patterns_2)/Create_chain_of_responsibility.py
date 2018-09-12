"""Вам дан объект класса SomeObject, содержащего три поля: integer_field, float_field и string_field:



Необходимо реализовать:

EventGet(<type>) создаёт событие получения данных соответствующего типа
EventSet(<value>) создаёт событие изменения поля типа type(<value>)
Необходимо реализовать классы NullHandler, IntHandler, FloatHandler, StrHandler так, чтобы можно было создать цепочку:



Chain.handle(obj, EventGet(int)) — вернуть значение obj.integer_field
Chain.handle(obj, EventGet(str)) — вернуть значение obj.string_field
Chain.handle(obj, EventGet(float)) — вернуть значение obj.float_field
Chain.handle(obj, EventSet(1)) — установить значение obj.integer_field =1
Chain.handle(obj, EventSet(1.1)) — установить значение obj.float_field = 1.1
Chain.handle(obj, EventSet("str")) — установить значение obj.string_field = "str"
"""


"""
class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = "boo!"
"""


class EventGet:
    def __init__(self, type_):
        self.type = type_


class EventSet:
    def __init__(self, value):
        self.value = value


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, object_, event):
        if self.__successor is not None:
            return self.__successor.handle(object_, event)


class IntHandler (NullHandler):
    def handle(self, object_, event):
        if isinstance(event, EventGet):
            if event.type == int:
                return object_.integer_field
            else:
                return super().handle(object_, event)
        elif isinstance(event, EventSet):
            if type(event.value) == int:
                object_.integer_field = event.value
            else:
                super().handle(object_, event)


class FloatHandler (NullHandler):
    def handle(self, object_, event):
        if isinstance(event, EventGet):
            if event.type == float:
                return object_.float_field
            else:
                return super().handle(object_, event)
        elif isinstance(event, EventSet):
            if type(event.value) == float:
                object_.float_field = event.value
            else:
                super().handle(object_, event)


class StrHandler (NullHandler):
    def handle(self, object_, event):
        if isinstance(event, EventGet):
            if event.type == str:
                return object_.string_field
            else:
                return super().handle(object_, event)
        elif isinstance(event, EventSet):
            if type(event.value) == str:
                object_.string_field = event.value
            else:
                super().handle(object_, event)


"""
obj = SomeObject()
chain = IntHandler(FloatHandler(StrHandler(NullHandler())))
chain.handle(obj, EventSet(1.1))
print(chain.handle(obj, EventGet(float)))
"""

