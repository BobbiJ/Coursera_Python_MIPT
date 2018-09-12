class Value:
    def __init__(self):
        self.value = None

    def __set__(self, instance, value):
        self.value = value - instance.commission * value
        return self.value

    def __get__(self, instance, owner):
        return int(self.value)


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission

