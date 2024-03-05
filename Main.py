import pygame
import os
import sys
import random


SPEED = 15
BASE_SIZE = 10


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

class Level(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)


class Ball(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)


class Platform(pygame.sprite.Sprite):
    image_platform = load_image("platform_skin1.png")

    def __init__(self, *group):
        super().__init__(*group)
        super().__init__(*group)
        self.image = Platform.image_platform
        self.rect = self.image.get_rect()

    def update(self):
        pass
def main():
    pygame.init()
    size = width, height = 1200, 800
    main_screen = pygame.display.set_mode(size)
    running = True

    all_sprites = pygame.sprite.Group()
    Platform(all_sprites)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        main_screen.fill((0, 0, 0))
        all_sprites.draw(main_screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()


