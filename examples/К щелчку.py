import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('К щелчку')
    size = width, height = 501, 501
    screen = pygame.display.set_mode(size)
    running = True
    v = 130
    vx = 0
    vy = 0
    f_x = x = start_x = width // 2
    f_y = y = start_y = height // 2
    color = (255, 0, 0)
    clock = pygame.time.Clock()
    fps = 60
    pygame.draw.circle(screen, color, (start_x, start_y), 20)
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                f_x, f_y = event.pos
                vx = v * ((f_x - x) / abs(f_x - x))
                vy = v * ((f_y - y) / abs(f_y - y))
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, color, (int(x), int(y)), 20)
        clock.tick(fps)
        pygame.display.flip()
        if vx <= 0 and vy <= 0:
            if x >= f_x:
                x += vx / fps
            if y >= f_y:
                y += vy / fps
        elif vx >= 0 and vy <= 0:
            if x <= f_x:
                x += vx / fps
            if y >= f_y:
                y += vy / fps
        elif vx >= 0 and vy >= 0:
            if x <= f_x:
                x += vx / fps
            if y <= f_y:
                y += vy / fps
        elif vx <= 0 and vy >= 0:
            if x >= f_x:
                x += vx / fps
            if y <= f_y:
                y += vy / fps
    pygame.quit()
