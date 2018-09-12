from abc import ABC, abstractmethod


class Engine:
    pass


class ObservableEngine(Engine):

    def __init__(self):
        self.subscribers = []

    def subscribe(self, sub):
        self.subscribers.append(sub)

    def unsubscribe(self, sub):
        self.subscribers.remove(sub)

    def notify(self, message):
        for sub in self.subscribers:
            sub.update(message)


class AbstractObserver(ABC):

    @abstractmethod
    def update(self, message):
        pass


class ShortNotificationPrinter(AbstractObserver):

    def __init__(self):
        self.achievements = set()

    def update(self, message):
        self.achievements.add(message['title'])


class FullNotificationPrinter(AbstractObserver):

    def __init__(self):
        self.achievements = list()
        self.ach = set()

    def update(self, message):
        if message['title'] not in self.ach:
            self.ach.add(message['title'])
            self.achievements.append(message)


if __name__ == '__main__':
    obs = ObservableEngine()
    short = ShortNotificationPrinter()
    notif = FullNotificationPrinter()
    obs.subscribe(short)
    obs.subscribe(notif)
    obs.notify({"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"})
    obs.notify({"title": "Покоритель2", "text": "Дается при выполнении всех заданий в игре"})
    obs.notify({"title": "Покоритель2", "text": "Дается при выполнении всех заданий в игре"})

    print(short.achievements)
    print(notif.achievements)