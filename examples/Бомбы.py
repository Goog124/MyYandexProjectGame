import pygame
import os
import sys
import random


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Bomb(pygame.sprite.Sprite):
    image_bomb = load_image("bomb.png")
    image_boom = load_image("boom.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Bomb.image_bomb
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(34, width - (Bomb.image_boom.get_size()[0] - 34))
        self.rect.y = random.randrange(27, height - (Bomb.image_boom.get_size()[1] - 27))

    def update(self, mouse_pos):
        x = mouse_pos[0]
        y = mouse_pos[1]

        if self.rect.x < x < self.image.get_size()[0] + self.rect.x and \
                self.rect.y < y < self.image.get_size()[1] + self.rect.y and \
                self.image is Bomb.image_bomb:
            self.rect.x -= 34
            self.rect.y -= 27
            self.image = Bomb.image_boom


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    running = True

    all_sprites = pygame.sprite.Group()
    bomb_image = load_image("bomb.png")
    for i in range(20):
        Bomb(all_sprites)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event.pos)

        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

