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


class UpWall(pygame.sprite.Sprite):
    image_upwall = load_image("up_wall.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = UpWall.image_upwall
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - self.image.get_size()[0]
        self.rect.y = 0


class LeftWall(pygame.sprite.Sprite):
    image_leftwall = load_image("left_wall.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = LeftWall.image_leftwall
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - self.image.get_size()[0] - UpWall.image_upwall.get_size()[0]
        self.rect.y = 0


class RightWall(pygame.sprite.Sprite):
    image_rightwall = load_image("right_wall.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = RightWall.image_rightwall
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - self.image.get_size()[0]
        self.rect.y = 0


class Ball(pygame.sprite.Sprite):
    image_platform = load_image("ball.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Ball.image_platform
        self.rect = self.image.get_rect()

    def update(self):
        pass


class Platform(pygame.sprite.Sprite):
    image_platform = load_image("platform.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Platform.image_platform
        self.rect = self.image.get_rect()
        self.rect.x = Character.image_character.get_size()[0] + Hand.image_flex_hand_part.get_size()[0]
        self.rect.y = HEIGHT - (Character.image_character.get_size()[1] - 101)

    def update(self, move=0, pos=0):
        offset = Character.image_character.get_size()[0] + Hand.image_flex_hand_part.get_size()[0]
        if pos and (offset <= pos[0] <= WIDTH - Platform.image_platform.get_size()[0]):
            self.rect.x = pos[0]

        if move and (offset <= self.rect.x + move <= WIDTH - Platform.image_platform.get_size()[0]):
            self.rect.x += move


class Character(pygame.sprite.Sprite):
    image_character = load_image("character.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Character.image_character
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT - self.image.get_size()[1]

    def update(self):
        pass


class Hand(pygame.sprite.Sprite):
    image_flex_hand_part = load_image("hand_part.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Hand.image_flex_hand_part
        self.rect = self.image.get_rect()
        self.rect.x = Character.image_character.get_size()[0]
        self.rect.y = HEIGHT - (Character.image_character.get_size()[1] - 128)

    def update(self, *args, move=0, pos=0):

        if pos and pos[0] - Character.image_character.get_size()[0] > 0:
            if Hand.image_flex_hand_part.get_size()[0] \
                    <= pos[0] - Character.image_character.get_size()[0] <= \
                    WIDTH - Platform.image_platform.get_size()[0] - Character.image_character.get_size()[0]:
                self.image = pygame.transform.scale(self.image, (pos[0] - Character.image_character.get_size()[0],
                                                             self.image.get_size()[1]))

        if move:
            size_x, size_y = self.image.get_size()
            if Hand.image_flex_hand_part.get_size()[0] \
                    <= size_x + move <= \
                    WIDTH - Platform.image_platform.get_size()[0] - Character.image_character.get_size()[0]:
                self.image = pygame.transform.scale(self.image, (size_x + move, size_y))


def main():
    pygame.init()
    size = WIDTH, HEIGHT
    main_screen = pygame.display.set_mode(size)
    running = True

    all_sprites = pygame.sprite.Group()
    hand_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()
    Platform(all_sprites, hand_sprites)
    Ball(all_sprites)
    Character(all_sprites)
    Hand(all_sprites, hand_sprites)
    UpWall(all_sprites, wall_sprites)
    LeftWall(all_sprites, wall_sprites)
    RightWall(all_sprites, wall_sprites)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                hand_sprites.update(pos=event.pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    hand_sprites.update(move=-MOVE_SPEED)
                elif event.key == pygame.K_RIGHT:
                    hand_sprites.update(move=MOVE_SPEED)

        main_screen.fill((255, 255, 255))
        all_sprites.draw(main_screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()


