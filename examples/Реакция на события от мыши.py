import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.color = (255, 255, 255)
        self.red_rects = []
        self.blue_rects = []
        self.black_rects = []

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.left, self.left + self.width * self.cell_size, self.cell_size):
            for j in range(self.left, self.left + self.height * self.cell_size, self.cell_size):
                pygame.draw.rect(screen, self.color, (i, j, self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        x_click = mouse_pos[0]
        y_click = mouse_pos[1]
        if x_click > self.width * self.cell_size + self.left or \
                y_click > self.height * self.cell_size + self.top or \
                x_click <= self.left or y_click <= self.top:
            return None
        cell_x = x_click - ((x_click - self.left) % self.cell_size)
        cell_y = y_click - ((y_click - self.top) % self.cell_size)
        return cell_x, cell_y

    def render_color_rects(self):
        for i in self.red_rects:
            pygame.draw.rect(screen, (255, 0, 0), (i[0] + 1, i[1] + 1, self.cell_size - 2, self.cell_size - 2))
        for i in self.blue_rects:
            pygame.draw.rect(screen, (0, 0, 255), (i[0] + 1, i[1] + 1, self.cell_size - 2, self.cell_size - 2))
        for i in self.black_rects:
            pygame.draw.rect(screen, (0, 0, 0), (i[0] + 1, i[1] + 1, self.cell_size - 2, self.cell_size - 2))

    def on_click(self, mouse_pos):
        if mouse_pos not in self.red_rects and mouse_pos not in self.blue_rects:
            if mouse_pos in self.black_rects:
                self.red_rects.append(self.black_rects.pop(self.black_rects.index(mouse_pos)))
            else:
                self.red_rects.append(mouse_pos)
        elif mouse_pos in self.red_rects and mouse_pos not in self.blue_rects:
            self.blue_rects.append(self.red_rects.pop(self.red_rects.index(mouse_pos)))
        elif mouse_pos not in self.red_rects and mouse_pos in self.blue_rects:
            self.black_rects.append(self.blue_rects.pop(self.blue_rects.index(mouse_pos)))
        self.render_color_rects()

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
board = Board(2, 2)
board.set_view(20, 20, 20)
running = True
screen.fill((0, 0, 0))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    board.render(screen)
    pygame.display.flip()
