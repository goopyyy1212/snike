import pygame
from random import randint
from time import sleep

pygame.init()

WIDTH_WINDOW = 500
HEIGHT_WINDOW = 500
window = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))

BLUE = (0, 0, 255)
ORANGE = (255, 155, 69)

score = 0
SIZE = 25

bg = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH_WINDOW, HEIGHT_WINDOW))

game = True

class Eat(pygame.sprite.Sprite):
    """клас для створювання картинки та випадкового її розміщення на полі гри"""
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))
        self.hitbox = self.image.get_rect()
        self.hitbox.x = x
        self.hitbox.y = y

    def draw(self):
        """Відмалювання картинки на координатах хітбоксу"""
        window.blit(self.image, (self.hitbox.x, self.hitbox.y))

    def collide(self):
        """Обробка колізії"""
        self.hitbox.x = randint(0, WIDTH_WINDOW - self.hitbox.width)
        self.hitbox.y = randint(0, HEIGHT_WINDOW - self.hitbox.height)


class Stone(pygame.sprite.Sprite):
    """клас для створювання картинки та випадкового її розміщення на полі гри"""
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))
        self.hitbox = self.image.get_rect()
        self.hitbox.x = x
        self.hitbox.y = y

    def draw(self):
        """Відмалювання картинки на координатах хітбоксу"""
        window.blit(self.image, (self.hitbox.x, self.hitbox.y))

    def collide(self):
        """Обробка колізії"""
        self.hitbox.x = randint(0, WIDTH_WINDOW - self.hitbox.width)
        self.hitbox.y = randint(0, HEIGHT_WINDOW - self.hitbox.height)


class Snake():
    """створення елементів змійки"""
    def __init__(self, x, y, size, color=ORANGE):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.size = size
        self.lastpos = [x, y]
        self.direction = "down"
        self.step = 1

    def draw(self):
        """Відмалювання змійки"""
        pygame.draw.rect(window, self.color, self.rect)
    
    def goto(self, x, y):
        """Переміщення змійки на позицію частини попереду"""
        self.lastpos = [self.rect.x, self.rect.y]
        self.rect.x = x
        self.rect.y = y

head = Snake(25, 25, SIZE, BLUE)
snake_elements = []
snake_elements.append(head)

def lose():
    text = pygame.font.SysFont("Arial", 70).render("Ти програв", True, (0, 0, 0))
    window.blit(text, (200, 200))
    global game
    game = False


def move(x, y):
    lx, ly = x, y
    for e in snake_elements:
        e.goto(lx, ly)
        lx = e.lastpos[0]
        ly = e.lastpos[1]
    
    
eat = Eat(100, 100, 35, 35, "eat.png")

stone = Eat(100, 100, 35, 35, "stone.png")
stone.collide()


while game:
    pygame.time.delay(10)
    window.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                eat.collide()
            if event.key == pygame.K_w and head.direction != "down":
                head.direction = "up"
            if event.key == pygame.K_s and head.direction != "up":
                head.direction = "down"
            if event.key == pygame.K_a and head.direction != "right":
                head.direction = "left"
            if event.key == pygame.K_d and head.direction != "left":
                head.direction = "right"

    if head.direction == "down":
        move(head.rect.x, head.rect.y + head.step)
    elif head.direction == "up":
        move(head.rect.x, head.rect.y - head.step)
    elif head.direction == "left":
        move(head.rect.x - head.step, head.rect.y)
    elif head.direction == "right":
        move(head.rect.x + head.step, head.rect.y)

    if head.rect.colliderect(eat.hitbox):
        eat.collide()
        score += 1
        for _ in range(20):
            lx, ly = snake_elements[-1].lastpos
            snake_elements.append(Snake(lx, ly, SIZE))



    if head.rect.colliderect(stone.hitbox):
        lose()

    

    eat.draw()
    stone.draw()
    #for i in range(-1, len(snake_elements), -1):
        #snake_elements[i].draw()
        #print(i)
    
    if randint(0, 100) == 0:
        stone.collide()

    for e in snake_elements:
        if head.rect.colliderect(e.rect) and snake_elements.index(e) >= head.size * 2:
            lose()
            e.color = (255, 0, 0)
        e.draw()
    if head.rect.x >= WIDTH_WINDOW - SIZE or head.rect.x <= 0 or head.rect.y >= HEIGHT_WINDOW - SIZE or head.rect.y <= 0:
        lose()
    text = pygame.font.SysFont("Arial", 35).render(str(score), True, (255, 255, 255))
    window.blit(text, (450, 0))

    pygame.display.update()
sleep(3)
