import pygame
import os
import sys
import random


BALL_SPEED = 15
BASE_SIZE = 10
WIDTH = 1200
HEIGHT = 1000
MOVE_SPEED = 20


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
    image_platform = load_image("ball_skin.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Ball.image_platform
        self.rect = self.image.get_rect()

    def update(self):
        pass


class Platform(pygame.sprite.Sprite):
    image_platform = load_image("platform_skin1.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Platform.image_platform
        self.rect = self.image.get_rect()
        self.rect.x = Character.image_character.get_size()[0] + Hand.image_flex_hand_part.get_size()[0]
        print(self.rect.x)
        self.rect.y = HEIGHT - (Character.image_character.get_size()[1] - 101)

    def update(self, move=0):
        if move and (255 <= self.rect.x + move <= WIDTH - Platform.image_platform.get_size()[0]):
            self.rect.x += move


class Character(pygame.sprite.Sprite):
    image_character = load_image("Main_char.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Character.image_character
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT - self.image.get_size()[1]

    def update(self):
        pass


class Hand(pygame.sprite.Sprite):
    image_flex_hand_part = load_image("Hand_part.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Hand.image_flex_hand_part
        self.rect = self.image.get_rect()
        self.rect.x = Character.image_character.get_size()[0]
        self.rect.y = HEIGHT - (Character.image_character.get_size()[1] - 128)

    def update(self, *args, move=0):
        if move:
            size_x, size_y = self.image.get_size()
            if Hand.image_flex_hand_part.get_size()[0] <= size_x + move:
                self.image = pygame.transform.scale(self.image, (size_x + move, size_y))
                print(size_x)


def main():
    pygame.init()
    size = WIDTH, HEIGHT
    main_screen = pygame.display.set_mode(size)
    running = True

    all_sprites = pygame.sprite.Group()
    hand_sprite = pygame.sprite.Group()
    Platform(all_sprites, hand_sprite)
    Ball(all_sprites)
    Character(all_sprites)
    Hand(all_sprites, hand_sprite)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    hand_sprite.update(move=-MOVE_SPEED)
                elif event.key == pygame.K_RIGHT:
                    hand_sprite.update(move=MOVE_SPEED)

        main_screen.fill((255, 255, 255))
        all_sprites.draw(main_screen)
        hand_sprite.draw(main_screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()


