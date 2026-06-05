import pygame

from core.game import Game
from ui.renderer import Renderer
from settings import *

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("Bost Black")

clock = pygame.time.Clock()

game = Game()
renderer = Renderer(screen)

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        game.handle_event(event)

    game.update()

    renderer.draw(game)

    pygame.display.flip()

pygame.quit()