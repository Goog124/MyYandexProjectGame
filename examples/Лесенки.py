import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.vy = 50
        self.clock = pygame.time.Clock()

    def update(self, mouse_pos=None, move_x=None, move_y=None):
        if mouse_pos:
            self.rect.x, self.rect.y = mouse_pos
        if move_x:
            self.rect.x += move_x
        if move_y and pygame.sprite.spritecollideany(self, platform_sprites_v):
            self.rect.y += move_y
        if pygame.sprite.spritecollideany(self, platform_sprites_h) or \
                pygame.sprite.spritecollideany(self, platform_sprites_v):
            self.vy = 0
        else:
            self.vy = 50
        self.rect.y += self.vy / 60
        self.clock.tick(60)


class PlatformHorizontal(pygame.sprite.Sprite):
    def __init__(self, *group, pos):
        super().__init__(*group)
        self.image = pygame.Surface((50, 10))
        self.image.fill((150, 150, 150))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


class PlatformVertical(pygame.sprite.Sprite):
    def __init__(self, *group, pos):
        super().__init__(*group)
        self.image = pygame.Surface((10, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    running = True

    platform_sprites_h = pygame.sprite.Group()
    platform_sprites_v = pygame.sprite.Group()
    char_sprite = pygame.sprite.Group()
    Character(char_sprite)
    char_flag = False

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    char_flag = True
                    char_sprite.update(mouse_pos=event.pos)
                elif event.button == 1 and not pygame.key.get_mods() & pygame.KMOD_LCTRL:
                    PlatformHorizontal(platform_sprites_h, pos=event.pos)
                elif event.button == 1 and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                    PlatformVertical(platform_sprites_v, pos=event.pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    char_sprite.update(move_x=-10)
                elif event.key == pygame.K_RIGHT:
                    char_sprite.update(move_x=10)
                elif event.key == pygame.K_UP:
                    char_sprite.update(move_y=-10)
                elif event.key == pygame.K_DOWN:
                    char_sprite.update(move_y=10)

        char_sprite.update()
        if char_flag:
            char_sprite.draw(screen)
        platform_sprites_h.draw(screen)
        platform_sprites_v.draw(screen)
        pygame.display.flip()
    pygame.quit()

