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


class AbstractObject(ABC):
    def __init__(self, icon, position):
        self.sprite = icon
        self.position = position

    def draw(self, display):
        padding = display.game_engine.padding
        display.blit(self.sprite, ((self.position[0]-padding[0]) * display.game_engine.sprite_size,
                                   (self.position[1]-padding[1]) * display.game_engine.sprite_size))


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2


class Ally(Interactive, AbstractObject):

    def __init__(self, icon, action, position):
        self.action = action
        super().__init__(icon, position)

    def interact(self, engine, hero):
        self.action(engine, hero)


class Enemy(Interactive, Creature):

    def __init__(self, icon, stats, xp, position):
        self.xp = xp
        super().__init__(icon, stats, position)

    def interact(self, engine, hero):
        hero.hp = hero.hp - self.stats['strength'] - self.stats['endurance']
        if hero.hp > 0:
            hero.exp += self.xp
            for level in hero.level_up():
                engine.notify('Level UP!!!')
            engine.notify('Enemy defeated')
        else:
            engine.notify('You are dead')
            engine.restart_level()




class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp


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


class Berserk(Effect):
    effects = {
        "strength": 20,
        "endurance": 5,
        "intelligence": -5,
        "luck": -2
    }

    def apply_effect(self):
        for buff, value in self.effects.items():
            self.stats[buff] += value


class Blessing(Effect):
    effects = {
        "strength": 10,
        "endurance": 5,
        "intelligence": -2,
        "luck": 2
    }

    def apply_effect(self):
        for buff, value in self.effects.items():
            self.stats[buff] += value


class Weakness(Effect):
    effects = {
        "strength": -5,
        "endurance": -5,
        "intelligence": -2,
        "luck": -1
    }

    def apply_effect(self):
        for buff, value in self.effects.items():
            self.stats[buff] += value


class Poison(Effect):
    effects = {
        "strength": -2,
        "endurance": -10,
        "intelligence": 0,
        "luck": -5
    }

    def apply_effect(self):
        for buff, value in self.effects.items():
            self.stats[buff] += value

