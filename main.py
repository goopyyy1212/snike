import pygame
from random import randint

pygame.init()

WIDTH_WINDOW = 500
HEIGHT_WINDOW = 500
window = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))

BLUE = (0, 0, 255)
ORANGE = (255, 155, 69)

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
          

eat = Eat(100, 100, 35, 35, "eat.png")
game = True
while game:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    
    window.blit(bg, (0, 0))
    eat.draw()


    pygame.display.update()

