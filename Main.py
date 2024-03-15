import pygame
import os
import sys
import random


BALL_SPEED = 25
ACCELERATION = 8
DAMAGE = 25
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
        self.on_collide = False


class Ball(pygame.sprite.Sprite):
    image_ball = load_image("moved_ball.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.frames = []
        self.cut_sheet(Ball.image_ball, 5)
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
        self.start = False

    def cut_sheet(self, sheet, columns):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height())
        for i in range(columns):
            frame_location = (self.rect.w * i, 0)
            self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self, *args, **kwargs):
        tick = self.clock.tick()
        if kwargs["start"] and self.start:
            if self.animation_iter == 3:
                self.cur_frame = (self.cur_frame + self.step) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.animation_iter = 0
            self.animation_iter += 1

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
                        kwargs["group_dict"]["wall_sprites"].sprites()[3].on_collide = True
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
                        self.vx = max(self.vx // 2, BALL_SPEED)
                        self.vy = max(self.vy // 2, BALL_SPEED)
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
            elif left_edge > pos[0]:
                self.rect.x = left_edge
            elif right_edge < pos[0]:
                self.rect.x = right_edge


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
            res = None
            if left_edge <= pos[0] <= right_edge:
                res = pos[0]
            elif left_edge > pos[0]:
                res = left_edge
            elif right_edge < pos[0]:
                res = right_edge
            self.image = pygame.transform.scale(self.image, (res - Character.image_character.get_width(),
                                                             self.image.get_height()))
            self.rect = pygame.Rect(self.rect.x, self.rect.y,
                                    self.rect.x + self.image.get_width(), self.rect.y + self.image.get_height())


class Buttons(pygame.sprite.Sprite):
    image_buttons = load_image("Buttons.png")

    def __init__(self, *group, name):
        super().__init__(*group)
        self.name = name
        self.rect = pygame.Rect(0, 0, Buttons.image_buttons.get_width(), Buttons.image_buttons.get_height() // 3)
        frame_location = {"start": (0, self.rect.y),
                          "scores": (0, self.rect.y + (Buttons.image_buttons.get_height() // 3)),
                          "exit": (0, self.rect.y + (Buttons.image_buttons.get_height() // 3) * 2)}
        self.image = Buttons.image_buttons.subsurface(pygame.Rect(frame_location[name], self.rect.size))
        self.rect.x = 850
        self.rect.y = frame_location[name][1] + 200

    def update(self, *args, **kwargs):
        pass


def render_text(screen, group_dict, end=False):
    char_sprite = group_dict["char_sprite"]
    ball_sprite = group_dict["ball_sprite"]
    text_out0 = "Esc - выход"
    text_out1 = f"Здоровье: {max(char_sprite.sprites()[0].health, 0)}%"
    text_out2 = f"Скорость: {ball_sprite.sprites()[0].vx}"
    text_out3 = f"Время: {round(ball_sprite.sprites()[0].time / 1000, 1)} ceк"
    font = pygame.font.Font(None, 35)
    text = font.render(text_out0, True, (0, 0, 0))
    screen.blit(text, (10, 0))
    text = font.render(text_out1, True, (255, 0, 0))
    screen.blit(text, (10, HEIGHT - Character.image_character.get_height() - 30))
    text = font.render(text_out2, True, (0, 0, 0))
    screen.blit(text, (10, HEIGHT - Character.image_character.get_height() - 60))
    text = font.render(text_out3, True, (0, 255, 0))
    screen.blit(text, (10, HEIGHT - Character.image_character.get_height() - 90))

    if not group_dict["ball_sprite"].sprites()[0].start:
        text_out = "Пробел - чтобы начать"
        font = pygame.font.Font(None, 35)
        text = font.render(text_out, True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2, HEIGHT // 2 - 40))

    if end:
        text_out0 = end
        font = pygame.font.Font(None, 100)
        text = font.render(text_out0, True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2, HEIGHT // 2))




def start_game():
    all_sprites = pygame.sprite.Group()
    hand_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()
    ball_sprite = pygame.sprite.GroupSingle()
    char_sprite = pygame.sprite.GroupSingle()
    Platform(all_sprites, hand_sprites)
    Ball(all_sprites, ball_sprite)
    Character(all_sprites, char_sprite)
    Hand(all_sprites, hand_sprites)
    UpWall(all_sprites, wall_sprites)
    LeftWall(all_sprites, wall_sprites)
    RightWall(all_sprites, wall_sprites)
    BottomWall(all_sprites, wall_sprites)
    group_dict = {"all_sprites": all_sprites,
                  "hand_sprites": hand_sprites,
                  "wall_sprites": wall_sprites,
                  "ball_sprite": ball_sprite,
                  "char_sprite": char_sprite}
    return group_dict


def end_game(group_dict):
    if group_dict["char_sprite"].sprites()[0].health <= 0:
        return "health"
    elif group_dict["wall_sprites"].sprites()[3].on_collide:
        return "pool"
    rect = group_dict["ball_sprite"].sprites()[0].rect
    if not rect.colliderect((0, 0, WIDTH, HEIGHT)):
        return "leave"
    return False


def main():
    pygame.init()
    size = WIDTH, HEIGHT
    main_screen = pygame.display.set_mode(size)
    running = True
    start = False
    group_dict = start_game()
    menu_sprites = pygame.sprite.Group()
    Buttons(menu_sprites, name="start")
    Buttons(menu_sprites, name="exit")
    while running:
        if not end_game(group_dict):
            if start:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEMOTION:
                        group_dict["hand_sprites"].update(pos=event.pos)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            group_dict["ball_sprite"].sprites()[0].start = True
                        if event.key == pygame.K_ESCAPE:
                            start = False
                            group_dict["ball_sprite"].sprites()[0].start = False

                group_dict["all_sprites"].update(group_dict=group_dict, start=start)
                main_screen.fill((255, 255, 255))
                render_text(main_screen, group_dict)
                group_dict["all_sprites"].draw(main_screen)
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if menu_sprites.sprites()[1].rect.collidepoint(event.pos):
                            running = False
                        if menu_sprites.sprites()[0].rect.collidepoint(event.pos):
                            start = True
                main_screen.blit(load_image("Menu_background.png"), (0, 0))
                menu_sprites.draw(main_screen)
        else:
            end = end_game(group_dict)
            render_text(main_screen, group_dict, end)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        start = False
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()


