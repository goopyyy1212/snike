#Модулі
import pygame
from random import randint
from time import sleep

#ініціалазація пайгейм
pygame.init()

#Змінна для контролю кадрів в секунду
clock = pygame.time.Clock()

#Розміри вікна та його створення
WIDTH_WINDOW = 600
HEIGHT_WINDOW = 600
window = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))

#Кольора
BLUE = (0, 0, 255)
ORANGE = (255, 155, 69)
GREEN = (0, 255, 0)

#Змінні рахнку респавну каменю та розміра змійки
score = 0
random_respawn = 300
SIZE = 25

#Інформація про рівні(їх кількість рахунку для переходу та картинка)
level_info = {
    7:"background.png",
    13:"backgroundGoToHill.jpg",
    18:"backgroundDesert.jpg",
    23:"backgroundWater.png",
    27:"backgroundKosmos.jpg"
}

#Перший задній фон
bg = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH_WINDOW, HEIGHT_WINDOW))

#Змінна для роботи гри
game = True

#Класс якій створює обьекти каменю та яблука
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

#Класс якії створює змійкю та керує переміщенням
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

#Створення змійки та списку її елементів
head = Snake(25, 25, SIZE, GREEN)
snake_elements = []
snake_elements.append(head)

#Функції для завершення гри програшом
def lose():
    text = pygame.font.SysFont("Arial", 70).render("Ти програв", True, (255, 0, 0))
    window.blit(text, (100, 200))
    global game
    game = False

#Функція для переміщення змійки
def move(x, y):
    lx, ly = x, y
    for e in snake_elements:
        e.goto(lx, ly)
        lx = e.lastpos[0]
        ly = e.lastpos[1]

#Функція для відмалювання заднього фону
def draw_level(bg):
    bg = pygame.transform.scale(pygame.image.load(bg), (WIDTH_WINDOW, HEIGHT_WINDOW))
    window.blit(bg, (0, 0))
    
#Створення їжі
eat = Eat(100, 100, 35, 35, "eat.png")

#Створення каменю
stone = Eat(100, 100, 35, 35, "stone.png")
stone.collide()

#Головний ігровий цикл
while game:
    #кількість кадрів в секунду
    clock.tick(60)

    #Відмалювання поточного фону та перевірка на перемогу
    for i in level_info.keys():
        if score <= i:
            draw_level(level_info[i])
            break
    else:
        text = pygame.font.SysFont("Arial", 70).render("Ти виграв", True, (0, 255, 0))
        window.blit(text, (100, 200))
        game = False

    #Обробка натискання клавіш та задопомогою цього зміна повороту змійки
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

    #Перевірка на дотик до їжі та збільшення рахунку і змійки
    if head.rect.colliderect(eat.hitbox):
        eat.collide()
        score += 1
        for _ in range(20):
            lx, ly = snake_elements[-1].lastpos
            snake_elements.append(Snake(lx, ly, SIZE))


    #перевірка на колізії голови до каменю
    if head.rect.colliderect(stone.hitbox):
        lose()

    #відмалювання їжі та початок відмалювання каменю якщо раханок більше або 3
    eat.draw()
    if score >= list(level_info.keys())[2]:
        stone.draw()

    #for i in range(-1, len(snake_elements), -1):
        #snake_elements[i].draw()
        #print(i)
    
    #Випадковий респавн каменю 
    if randint(0, random_respawn) == 0:
        stone.collide()

    #Відмалювняя всіх елементів змійки та перевірка на колізію сама с собой
    for e in snake_elements:
        if head.rect.colliderect(e.rect) and snake_elements.index(e) >= head.size * 2:
            lose()
            e.color = (255, 0, 0)
        e.draw()
    head.draw()

    #Перевірка на колізію зі стінками        
    if head.rect.x >= WIDTH_WINDOW - SIZE or head.rect.x <= 0 or head.rect.y >= HEIGHT_WINDOW - SIZE or head.rect.y <= 0:
        lose()

    #Відмалювання тексту з рахунком
    text = pygame.font.SysFont("Arial", 35).render(str(score), True, (255, 255, 255))
    window.blit(text, (550, 0))

    #Різні покращення при збільшенні рахунку
    if score >= list(level_info.keys())[4]:
        random_respawn = 50
    elif score >= list(level_info.keys())[3]:
        for e in snake_elements:
            e.step = 3
    elif score >= list(level_info.keys())[1]:
        for e in snake_elements:
            e.step = 2

    #Оновлення зображення
    pygame.display.update()
    
#затримка після відключення головного циклу
sleep(3)
