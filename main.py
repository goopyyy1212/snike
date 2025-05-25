import pygame

pygame.init()

WIDTH_WINDOW = 500
HEIGHT_WINDOW = 500
window = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))

BLUE = (0, 0, 255)
ORANGE = (255, 155, 69)

bg = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH_WINDOW, HEIGHT_WINDOW))

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    window.blit(bg, (0, 0))


    pygame.display.update()

