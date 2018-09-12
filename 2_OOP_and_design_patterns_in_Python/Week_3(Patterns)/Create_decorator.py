from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []

        self.stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,

            "Strength": 15,
            "Perception": 4,
            "Endurance": 8,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 8,
            "Luck": 1
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        self.base = base

    @abstractmethod
    def get_stats(self):
        return self.base.get_stats()

    def get_positive_effects(self):
        return self.base.get_positive_effects()

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class AbstractPositive(AbstractEffect, ABC):
    def get_positive_effects(self):
        effects = self.base.get_positive_effects()
        effects.append(type(self).__name__)
        return effects


class AbstractNegative(AbstractEffect, ABC):
    def get_negative_effects(self):
        effects = self.base.get_negative_effects()
        effects.append(type(self).__name__)
        return effects


class Berserk(AbstractPositive):
    def get_stats(self):
        stats = self.base.get_stats()
        stats["HP"] += 50
        stats["Strength"] += 7
        stats["Endurance"] += 7
        stats["Agility"] += 7
        stats["Luck"] += 7
        stats["Perception"] -= 3
        stats["Charisma"] -= 3
        stats["Intelligence"] -= 3
        return stats


class Blessing(AbstractPositive):
    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] += 2
        stats["Endurance"] += 2
        stats["Agility"] += 2
        stats["Luck"] += 2
        stats["Perception"] += 2
        stats["Charisma"] += 2
        stats["Intelligence"] += 2
        return stats


class Weakness(AbstractNegative):
    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] -= 4
        stats["Endurance"] -= 4
        stats["Agility"] -= 4
        return stats


class EvilEye(AbstractNegative):
    def get_stats(self):
        stats = self.base.get_stats()
        stats["Luck"] -= 10
        return stats


class Curse(AbstractNegative):
    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] -= 2
        stats["Endurance"] -= 2
        stats["Agility"] -= 2
        stats["Luck"] -= 2
        stats["Perception"] -= 2
        stats["Charisma"] -= 2
        stats["Intelligence"] -= 2
        return stats




berserk = Berserk(Hero())
print(berserk.get_positive_effects())
blessing = Blessing(berserk)
print(blessing.get_positive_effects())
curse = Curse(blessing)
print(curse.get_negative_effects())