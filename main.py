import pygame
from random import randint

pygame.init()

WIDTH_WINDOW = 500
HEIGHT_WINDOW = 500
window = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))

BLUE = (0, 0, 255)
ORANGE = (255, 155, 69)

SIZE = 25

bg = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH_WINDOW, HEIGHT_WINDOW))

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

def move(x, y):
    lx, ly = x, y
    for e in snake_elements:
        e.goto(lx, ly)
        lx = e.lastpos[0]
        ly = e.lastpos[1]
    
    
eat = Eat(100, 100, 35, 35, "eat.png")
game = True
while game:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                eat.collide()
            if event.key == pygame.K_w:
                head.direction = "up"
            if event.key == pygame.K_s:
                head.direction = "down"
            if event.key == pygame.K_a:
                head.direction = "left"
            if event.key == pygame.K_d:
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
        for _ in range(20):
            lx, ly = snake_elements[-1].lastpos
            snake_elements.append(Snake(lx, ly, SIZE))

    window.blit(bg, (0, 0))

    eat.draw()
    for i in range(-1, len(snake_elements), -1):
        snake_elements[i].draw()
        print(i)

    #for e in snake_elements:
        #e.draw()


    pygame.display.update()

