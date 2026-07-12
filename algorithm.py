import pygame
import math
import time
from queue import PriorityQueue

WIDTH = 800

RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 153, 0)
SKY_BLUE = (0, 255, 255)
BLUE = (0, 128, 255)
DARK_BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255, 75, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

class Node:

    # WHITE = Block 
    # GREEN = Block đã được duyệt qua
    # DARK_GREEN = Block đang trong Queue
    # BLACK = Barrier
    # SKY_BLUE = Block bắt đầu
    # BLUE = Block đường đi
    # DARK_BLUE = Block kết thúc

    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == GREEN
    
    def is_open(self):
        return self.color == DARK_GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == SKY_BLUE
    
    def is_end(self):
        return self.color == DARK_BLUE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = GREEN

    def make_open(self):
        self.color = DARK_GREEN
    
    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = SKY_BLUE
    
    def make_end(self):
        self.color = DARK_BLUE
    
    def make_path(self):
        self.color = BLUE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Check bên dưới
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # Check bên trên
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # Check bên phải
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Check bên trái
            self.neighbors.append(grid[self.row][self.col - 1])


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        time.sleep(0.01)
        draw()

def h(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x2 - x1) + abs(y2 - y1)

def algorithm(draw, grid, start, end):
    count = 0

    # put(f, count, node): f là f-score 
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    # dùng để check đường đi
    # came_from là dictionary
    came_from = {}

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    # open_set_hash dùng để kiểm tra xem 1 đỉnh (node) có nằm trong open_set không 
    open_set_hash = {start}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()
                print("Why won't you close when I press X?")

        # get() sẽ xóa phần tử đầu và trả về phần tử đó
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, current, draw)

            start.make_start()
            end.make_end()
        
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
        
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()
    
    return False


def make_grid(rows, width):
    grid = []

    # gap = kích thước của mỗi hình vuông
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

def draw_grid(window, rows, width):
    gap =  width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, width))

def draw(window, grid, width, rows):
    window.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(window)
    
    draw_grid(window, rows, width)
    pygame.display.update()

def get_mouse_pos(pos, rows, width):
    gap = width // rows
    x , y = pos
    row = x // gap
    col = y // gap
    
    return row, col

def main(window, width):
    rows = 80
    grid = make_grid(rows, width)

    # start = Block bắt đầu
    # end = Block kết thúc
    start = None
    end = None

    # run = App đang chạy
    # started = Thuật toán đang chạy
    run = True
    started = False

    while run:

        # cập nhật bảng sau mỗi event
        draw(window, grid, width, rows)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if started:
                continue
            
            # chuột giữa = Tạo ô start, end
            # chuột trái = Tạo barrier
            # chuột phải = Reset lại block
            if pygame.mouse.get_pressed()[1]: # chuột giữa
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, rows, width)
                node = grid[row][col]
                
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
            
            elif pygame.mouse.get_pressed()[0]: # chuột trái
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, rows, width)
                node = grid[row][col]
                
                if node != start and node != end:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # chuột phải
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, rows, width)
                node = grid[row][col]

                if node == start:
                    start = None
                elif node == end:
                    end = None
                    
                node.reset()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    # nếu nhấn SPACE và thuật toán chưa chạy thì chạy algorithm
                    algorithm(lambda: draw(WINDOW, grid, WIDTH, rows), grid, start, end)

                elif event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(rows, width)
   
    pygame.quit()
    
pygame.init()
main(WINDOW, WIDTH)


# CÂU HỎI
#
# tại sao reconstruct_path() lại vẽ đè lên block end và start
# -> Nó ko vẽ đè lên. Trước khi đến block end thì current biến neighbors thành open (màu xanh lá) nên block end bị vẽ đè
#
# nhấn nút X ở cửa sổ không ngưng chương trình?
# -> Code viết ngu. event.type == pygame.QUIT chứ ko phải event == pygame.QUIT
#
# hàm update_neighbors không xét các trường hợp ở viền?
# -> nó có xét nhưng trường hợp đó không hợp lệ nên chỉ xét 3 hướng còn lại
#
# hàm lambda chỉ để gọi draw()?
# -> hàm algorithm chỉ nhận vào được object nên phải tạo 1 object mang hàm draw()

# Video có nhưng không dùng: def __lt__(self, other)