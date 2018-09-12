import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:

    def __init__(self, v, speed=None):
        self.v = v
        self.speed = speed

    def __add__(self, y):
        return Vec2d((self.v[0] + y.v[0], self.v[1] + y.v[1]))

    def __sub__(self, y):
        return Vec2d((self.v[0] - y.v[0], self.v[1] - y.v[1]))

    def __mul__(self, k):
        if isinstance(k, Vec2d):
            v = self.v[0] * k.v, self.v[1] * k.v
        else:
            v = self.v[0] * k, self.v[1] * k
        return Vec2d(v)

    def __len__(self):
        return round(math.sqrt(self.v[0]**2 + self.v[1]**2))

    def int_pair(self):
        return int(self.v[0]), int(self.v[1])


class Polyline:
    def __init__(self, points=None):
        if points is not None:
            self.points = points
        else:
            self.points = []

    def __add__(self, other: Vec2d):
        self.points.append(other)

    def __len__(self):
        return len(self.points)

    def __str__(self):
        return str(self.points)

    def set_points(self):
        for p in range(len(self.points)):
            now_speed = self.points[p].speed
            self.points[p] = self.points[p] + Vec2d(self.points[p].speed)
            self.points[p].speed = now_speed
            if self.points[p].v[0] > SCREEN_DIM[0] or self.points[p].v[0] < 0:
                self.points[p].speed = (- self.points[p].speed[0], self.points[p].speed[1])
            if self.points[p].v[1] > SCREEN_DIM[1] or self.points[p].v[1] < 0:
                self.points[p].speed = (self.points[p].speed[0], -self.points[p].speed[1])

    def del_point(self):
        self.points = self.points[0:len(self.points) - 1]

    def drow_points(self, style='points', width=3, color=(255, 255, 255)):
        if style == 'line':
            for p_n in range(-1, len(self) - 1):
                pygame.draw.line(gameDisplay, color, (int(self.points[p_n].v[0]), int(self.points[p_n].v[1])),
                                 (int(self.points[p_n + 1].v[0]), int(self.points[p_n + 1].v[1])), width)

        elif style == 'points':
            for p in self.points:
                pygame.draw.circle(gameDisplay, color, (int(p.v[0]), int(p.v[1])), width)

    def more_speed(self):
        for p in range(len(self.points)):
            self.points[p].speed = (self.points[p].speed[0] * 2, self.points[p].speed[1] * 2)

    def less_speed(self):
        for p in range(len(self.points)):
            self.points[p].speed = (self.points[p].speed[0] / 2, self.points[p].speed[1] / 2)

    def add_multi(self):
        for i in range(3):
            v_add_multi = Vec2d((random.random() * SCREEN_DIM[0], random.random() * SCREEN_DIM[0]),
                          (random.random() * 2, random.random() * 2))
            self.points.append(v_add_multi)

    def del_multi(self):
        try:
            self.points = self.points[0:len(self.points) - 3]
        except:
            return


class Knot(Polyline):
    def __init__(self, points=None):
        super().__init__(points)

    def get_knot(self):
        if len(self) < 3:
            return []
        res = []
        for i in range(-2, len(self) -2):
            ptn = []
            ptn.append((self.points[i] + self.points[i+1]) * 0.5)
            ptn.append(self.points[i+1])
            ptn.append((self.points[i+1] + self.points[i+2]) * 0.5)

            res.extend(Knot.get_points(ptn, len(self)))
        return res

    @staticmethod
    def get_points(base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(Knot.get_point(base_points, i * alpha))
        return res

    @staticmethod
    def get_point(points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha) + (Knot.get_point(points, alpha, deg - 1) * (1 - alpha))


# Отрисовка справки
def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["W", "More speed"])
    data.append(["s", "Less speed"])
    data.append(["Q", "Add multi points"])
    data.append(["A", "Remove multi points"])
    data.append(["", ""])
    data.append([str(len(polyline.points)), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# Основная программа
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")
    polyline = Polyline()

    working = True
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    polyline = Polyline()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    v_add = Vec2d((random.random() * SCREEN_DIM[0], random.random() * SCREEN_DIM[0]),
                                  (random.random() * 2, random.random() * 2))
                    polyline.__add__(v_add)
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    polyline.del_point()
                if event.key == pygame.K_w:
                    polyline.more_speed()
                if event.key == pygame.K_s:
                    polyline.less_speed()
                if event.key == pygame.K_q:
                    polyline.add_multi()
                if event.key == pygame.K_a:
                    polyline.del_multi()

            if event.type == pygame.MOUSEBUTTONDOWN:
                v1 = Vec2d(event.pos, (random.random() * 2, random.random() * 2))
                polyline.__add__(v1)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        polyline.drow_points()
        knots = Knot(polyline.points)
        Knot(knots.get_knot()).drow_points("line", 3, color)
        if not pause:
            polyline.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
