import pygame
import os
import sys
import random


BALL_SPEED = 25
ACCELERATION = 6
DAMAGE = 20
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
        self.rect.y = HEIGHT - self.image.get_height()
        self.health = 100
        self.balls = 3

    def update(self, *args, **kwargs):
        pass


class UpWall(pygame.sprite.Sprite):
    image_upwall = load_image("up_wall.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = UpWall.image_upwall
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - self.image.get_width()
        self.rect.y = 0


class LeftWall(pygame.sprite.Sprite):
    image_leftwall = load_image("left_wall.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = LeftWall.image_leftwall
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - self.image.get_width() - UpWall.image_upwall.get_width()
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
        self.rect.x = Character.image_character.get_width() - 2
        self.rect.y = HEIGHT - BottomWall.image_pool.get_height()


class Ball(pygame.sprite.Sprite):
    image_ball = load_image("moved_ball.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.frames = []
        self.cut_sheet(Ball.image_ball, 3)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(WIDTH // 2, HEIGHT // 2)
        self.clock = pygame.time.Clock()
        self.time = 0
        self.vy_way = 1
        self.vx_way = 1
        self.vx = BALL_SPEED
        self.vy = BALL_SPEED
        self.step = 1
        self.animation_iter = 0

    def cut_sheet(self, sheet, columns):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height())
        for i in range(columns):
            frame_location = (self.rect.w * i, 0)
            self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self, *args, **kwargs):
        if self.animation_iter == 5:
            self.cur_frame = (self.cur_frame + self.step) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.animation_iter = 0
        self.animation_iter += 1

        tick = self.clock.tick()
        self.time += tick
        self.rect.x += int(self.vx * self.vx_way * tick / 60)
        self.rect.y += int(self.vy * self.vy_way * tick / 60)

        if "group_dict" in kwargs:
            # kwargs["group_dict"]["wall_sprites"].sprites()
            # [<UpWall Sprite(in 2 groups)>,
            # <LeftWall Sprite(in 2 groups)>,
            # <RightWall Sprite(in 2 groups)>,
            # <BottomWall Sprite(in 2 groups)>]
            if s := pygame.sprite.spritecollideany(self, kwargs["group_dict"]["wall_sprites"]):
                self.step = -self.step
                if s is kwargs["group_dict"]["wall_sprites"].sprites()[3] and self.vy_way > 0:
                    self.vy_way = -self.vy_way
                if s is kwargs["group_dict"]["wall_sprites"].sprites()[2] and self.vx_way > 0:
                    self.vx_way = -self.vx_way
                if s is kwargs["group_dict"]["wall_sprites"].sprites()[1] and self.vx_way < 0:
                    self.vx_way = -self.vx_way
                if s is kwargs["group_dict"]["wall_sprites"].sprites()[0] and self.vy_way < 0:
                    self.vy_way = -self.vy_way

            # kwargs["group_dict"]["hand_sprites"].sprites()
            # [<Platform Sprite(in 2 groups)>,
            # <Hand Sprite(in 2 groups)>]
            if s := pygame.sprite.spritecollideany(self, kwargs["group_dict"]["hand_sprites"]):
                self.step = -self.step
                if s is kwargs["group_dict"]["hand_sprites"].sprites()[0] and self.vy_way > 0:
                    self.vy_way = -self.vy_way
                    self.vx += ACCELERATION
                    self.vy += ACCELERATION
                if s is kwargs["group_dict"]["hand_sprites"].sprites()[1] and self.vy_way > 0:
                    self.vy_way = -self.vy_way
                    self.vx -= ACCELERATION
                    self.vy -= ACCELERATION
                    kwargs["group_dict"]["char_sprite"].sprites()[0].health -= DAMAGE


class Platform(pygame.sprite.Sprite):
    image_platform = load_image("platform.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Platform.image_platform
        self.rect = self.image.get_rect()
        self.rect.x = Character.image_character.get_width() + Hand.image_flex_hand_part.get_width()
        self.rect.y = HEIGHT - (Character.image_character.get_height() - 101)

    def update(self, *args, **kwargs):
        if "pos" in kwargs:
            pos = kwargs["pos"]
            left_edge = Character.image_character.get_width() + LeftWall.image_leftwall.get_width()
            right_edge = WIDTH - RightWall.image_rightwall.get_width() - Platform.image_platform.get_width()
            if left_edge <= pos[0] <= right_edge:
                self.rect.x = pos[0]


class Hand(pygame.sprite.Sprite):
    image_flex_hand_part = load_image("hand_part.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Hand.image_flex_hand_part
        self.rect = self.image.get_rect()
        self.rect.x = Character.image_character.get_width()
        self.rect.y = HEIGHT - (Character.image_character.get_height() - 128)

    def update(self, *args, **kwargs):

        if "pos" in kwargs:
            pos = kwargs["pos"]
            left_edge = Character.image_character.get_width() + LeftWall.image_leftwall.get_width()
            right_edge = WIDTH - RightWall.image_rightwall.get_width() - Platform.image_platform.get_width()
            if left_edge <= pos[0] <= right_edge:
                self.image = pygame.transform.scale(self.image, (pos[0] - Character.image_character.get_width(),
                                                                 self.image.get_height()))
                self.rect = pygame.Rect(self.rect.x, self.rect.y,
                                        self.rect.x + self.image.get_width(), self.rect.y + self.image.get_height())


def render_text(screen, group_dict):
    char_sprite = group_dict["char_sprite"]
    ball_sprite = group_dict["ball_sprite"]
    if char_sprite.sprites()[0].health > 0:
        text_out1 = f"Здоровье: {char_sprite.sprites()[0].health}%"
    else:
        text_out1 = f"Здоровье: {0}%"
    text_out2 = f"Скорость: {ball_sprite.sprites()[0].vx}"
    text_out3 = f"Время: {round(ball_sprite.sprites()[0].time / 1000, 1)} ceк"
    font = pygame.font.Font(None, 35)
    text = font.render(text_out1, True, (255, 0, 0))
    screen.blit(text, (10, HEIGHT - Character.image_character.get_height() - 30))
    text = font.render(text_out2, True, (0, 0, 0))
    screen.blit(text, (10, HEIGHT - Character.image_character.get_height() - 60))
    text = font.render(text_out3, True, (0, 255, 0))
    screen.blit(text, (10, HEIGHT - Character.image_character.get_height() - 90))


def main():
    pygame.init()
    size = WIDTH, HEIGHT
    main_screen = pygame.display.set_mode(size)
    running = True

    all_sprites = pygame.sprite.Group()
    hand_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()
    ball_sprite = pygame.sprite.GroupSingle()
    char_sprite = pygame.sprite.GroupSingle()

    group_dict = {"all_sprites": all_sprites,
                  "hand_sprites": hand_sprites,
                  "wall_sprites": wall_sprites,
                  "ball_sprite": ball_sprite,
                  "char_sprite": char_sprite}

    Platform(all_sprites, hand_sprites)
    Ball(all_sprites, ball_sprite)
    Character(all_sprites, char_sprite)
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
        all_sprites.update(group_dict=group_dict)
        main_screen.fill((255, 255, 255))
        render_text(main_screen, group_dict)
        all_sprites.draw(main_screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()


