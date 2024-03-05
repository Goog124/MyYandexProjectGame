import pygame

if __name__ == '__main__':
    n = input()
    try:
        n = int(n)
    except:
        print("Неправильный формат ввода")
        quit()

    pygame.init()
    size = width, height = 300, 300
    screen = pygame.display.set_mode(size)

    color = (255, 255, 255)
    dx = width // (2 * n)
    dy = height // (2 * n)
    x1 = y1 = 0
    x2 = width
    y2 = height
    for i in range(n):
        pygame.draw.ellipse(screen, color, (0, y1, width, y2), 1)
        pygame.draw.ellipse(screen, color, (x1, 0, x2, height), 1)
        y1 += dy
        y2 -= dy * 2
        x1 += dx
        x2 -= dx * 2

    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
