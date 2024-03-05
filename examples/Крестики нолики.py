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
        self.current_state = 1

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.left, self.left + self.width * self.cell_size, self.cell_size):
            for j in range(self.left, self.left + self.height * self.cell_size, self.cell_size):
                pygame.draw.rect(screen, self.color, (i, j, self.cell_size, self.cell_size), 1)
                row, col = self.get_cell((i, j))
                if self.board[row][col] == 1:
                    pygame.draw.ellipse(screen, (255, 0, 0), (i + 2, j + 2, self.cell_size - 4, self.cell_size - 4), 2)
                elif self.board[row][col] == 2:
                    pygame.draw.line(screen,
                                     (0, 0, 255),
                                     (i + 2, j + 2),
                                     (i + self.cell_size - 4, j + self.cell_size - 4),
                                     2)
                    pygame.draw.line(screen,
                                     (0, 0, 255),
                                     (i + self.cell_size - 4, j + 2),
                                     (i + 2, j + self.cell_size - 4),
                                     2)

    def change_state(self):
        if self.current_state == 1:
            self.current_state = 2
        else:
            self.current_state = 1

    def get_cell(self, mouse_pos):
        x_click = mouse_pos[0]
        y_click = mouse_pos[1]
        if (x_click > self.width * self.cell_size + self.left) or \
                (y_click > self.height * self.cell_size + self.top):
            return None
        cell_col = (x_click - self.left) // self.cell_size
        cell_row = (y_click - self.top) // self.cell_size
        return cell_row, cell_col

    def on_click(self, cell):
        row = cell[0]
        col = cell[1]
        if self.board[row][col] == 0:
            self.board[row][col] = self.current_state
            self.change_state()

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
board = Board(3, 3)
board.set_view(0, 0, 150)
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
