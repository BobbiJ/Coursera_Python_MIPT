from abc import ABC, abstractmethod
import pygame
import random


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class AbstractObject(ABC):

    def __init__(self):
        pass

    def draw(self, display):
        pass


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.max_hp = self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        return self.stats["endurance"] * 2 + 5

    @property
    def get_damage(self):
        x = self.stats['strength']*5 + self.stats['endurance']*2 + self.stats['intelligence']*3 + self.stats['luck']*4
        y = self.stats['strength'] + self.stats['endurance'] + self.stats['intelligence'] + self.stats['luck']
        return int(x/y)

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


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Enemy(Creature, Interactive):

    def __init__(self, icon, stats, xp, position):
        super().__init__(icon, stats, position)
        self.xp = xp

    def interact(self, engine, hero):
        hero_damage = hero.get_damage
        damage = self.get_damage
        while True:
            self.hp -= hero_damage
            engine.notify("Hero's damage - " + str(hero_damage))
            engine.notify("Enemy's HP - " + str(self.hp))
            if self.hp <= 0:
                engine.notify("Hero Killed Enemy")
                hero.exp += self.xp
                for it in hero.level_up():
                    engine.notify(it)
                return True
            else:
                engine.notify("Enemy's damage - " + str(damage))
                hero.hp -= damage
                if hero.hp <= 0:
                    engine.notify("Hero is dead")
                    engine.notify("game over")
                    engine.game_process = False
                    engine.game_over = True
                    return False

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

    def apply_effect(self):
        self.stats["strength"] += 5


class Blessing(Effect):

    def apply_effect(self):
        self.stats["endurance"] += 5


class Weakness(Effect):

    def apply_effect(self):
        self.stats['strength'] -= 1
        self.stats['endurance'] -= 1