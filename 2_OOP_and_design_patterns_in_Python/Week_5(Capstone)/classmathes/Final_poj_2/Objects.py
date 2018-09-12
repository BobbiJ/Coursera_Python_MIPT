from abc import ABC, abstractmethod
import pygame
import random


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class AbstractObject:
    pass


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2

    def _get_position(self, shift_x, shift_y, mul):
        return (self.position[0] - shift_x) * mul, (self.position[1] - shift_y) * mul

    def draw(self, canvas, shift_x, shift_y):
        canvas.blit(self.sprite, self._get_position(shift_x, shift_y, canvas.engine.sprite_size))

    def hit(self):
        return int(self.stats['strength'] + random.randint(0, self.stats['luck']))


class Enemy(Creature, Interactive):

    def __init__(self, icon, stats, exp, pos):
        super().__init__(icon, stats, pos)
        self.exp = exp

    def interact(self, engine, hero):
        self.action(engine, hero)

    def action(self, engine, hero):
        while hero.hp > 0 and self.hp > 0:
            self.hp -= hero.hit()
            hero.accept_hit(self.hit())

        if hero.hp > 0:
            hero.exp += self.exp
            hero.level_up(engine)


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self, engine):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            engine.notify("level up!")
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp

    def hit(self):
        return int(self.stats['strength'] + (self.level * 0.2) + random.randint(-1, self.stats['luck']))

    def accept_hit(self, hit):
        protect = random.randint(0, int(self.stats["endurance"] / 10 * (self.level * 0.5)))
        if protect < 0:
            protect = 0

        self.hp -= hit - protect

    def is_dead(self) -> bool:
        return self.hp <= 0


class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass


class Blessing(Effect):

    def apply_effect(self):
        stats = self.base.stats
        stats["endurance"] += 1
        stats["strength"] += 1
        stats["intelligence"] += 1
        stats["luck"] += 1
        return stats


class Fury(Effect):

    def apply_effect(self):
        stats = self.base.stats
        stats["strength"] += 5
        stats["intelligence"] -= 5
        return stats


class Berserk(Effect):

    def apply_effect(self):
        stats = self.base.stats
        stats["endurance"] += 1
        stats["strength"] += 2
        stats["intelligence"] -= 2
        return stats


class Weakness(Effect):

    def apply_effect(self):
        stats = self.base.stats
        stats["endurance"] -= 1
        stats["strength"] -= 1
        return stats
