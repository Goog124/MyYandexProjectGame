import pygame
import os
import sys
import random


BALL_SPEED = 2
WIDTH = 1200
HEIGHT = 1000


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Character(pygame.sprite.Sprite):
    image_character = load_image("character.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Character.image_character
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT - self.image.get_size()[1]

    def update(self):
        pass


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


class BottomWall(pygame.sprite.Sprite):
    image_pool = load_image("pool.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = BottomWall.image_pool
        self.rect = self.image.get_rect()
        self.rect.x = Character.image_character.get_size()[0] - 2
        self.rect.y = HEIGHT - BottomWall.image_pool.get_size()[1]


class Ball(pygame.sprite.Sprite):
    image_platform = load_image("ball.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Ball.image_platform
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT // 2
        self.moving = False
        self.clock = pygame.time.Clock()

    def update(self):
        self.rect.x += BALL_SPEED
        self.rect.y += BALL_SPEED
        self.clock.tick(60)


class Platform(pygame.sprite.Sprite):
    image_platform = load_image("platform.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Platform.image_platform
        self.rect = self.image.get_rect()
        self.rect.x = Character.image_character.get_size()[0] + Hand.image_flex_hand_part.get_size()[0]
        self.rect.y = HEIGHT - (Character.image_character.get_size()[1] - 101)

    def update(self, move=0, pos=0):
        if pos:
            left_edge = Character.image_character.get_size()[0] + LeftWall.image_leftwall.get_size()[0]
            right_edge = WIDTH - RightWall.image_rightwall.get_size()[0] - Platform.image_platform.get_size()[0]
            if left_edge <= pos[0] <= right_edge:
                self.rect.x = pos[0]


class Hand(pygame.sprite.Sprite):
    image_flex_hand_part = load_image("hand_part.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Hand.image_flex_hand_part
        self.rect = self.image.get_rect()
        self.rect.x = Character.image_character.get_size()[0]
        self.rect.y = HEIGHT - (Character.image_character.get_size()[1] - 128)

    def update(self, *args, move=0, pos=0):

        if pos:
            left_edge = Character.image_character.get_size()[0] + LeftWall.image_leftwall.get_size()[0]
            right_edge = WIDTH - RightWall.image_rightwall.get_size()[0] - Platform.image_platform.get_size()[0]
            if left_edge <= pos[0] <= right_edge:
                self.image = pygame.transform.scale(self.image, (pos[0] - Character.image_character.get_size()[0],
                                                                 self.image.get_size()[1]))


def main():
    pygame.init()
    size = WIDTH, HEIGHT
    main_screen = pygame.display.set_mode(size)
    running = True

    all_sprites = pygame.sprite.Group()
    hand_sprites = pygame.sprite.Group()
    ball_sprite = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()
    Platform(all_sprites, hand_sprites)
    Ball(all_sprites, ball_sprite)
    Character(all_sprites)
    Hand(all_sprites, hand_sprites)
    UpWall(all_sprites, wall_sprites)
    LeftWall(all_sprites, wall_sprites)
    RightWall(all_sprites, wall_sprites)
    BottomWall(all_sprites, wall_sprites)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                hand_sprites.update(pos=event.pos)
        ball_sprite.update()
        main_screen.fill((255, 255, 255))
        all_sprites.draw(main_screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()


