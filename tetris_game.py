
import pygame
import random
from enum import Enum

# Pygame 초기화
pygame.init()

# 색상 정의
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    CYAN = (0, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    ORANGE = (255, 165, 0)
    GRAY = (128, 128, 128)

# 테트로미노 정의
TETROMINOS = {
    'I': {
        'shape': [[1, 1, 1, 1]],
        'color': Colors.CYAN
    },
    'O': {
        'shape': [[1, 1], [1, 1]],
        'color': Colors.YELLOW
    },
    'T': {
        'shape': [[0, 1, 0], [1, 1, 1]],
        'color': Colors.PURPLE
    },
    'S': {
        'shape': [[0, 1, 1], [1, 1, 0]],
        'color': Colors.GREEN
    },
    'Z': {
        'shape': [[1, 1, 0], [0, 1, 1]],
        'color': Colors.RED
    },
    'J': {
        'shape': [[1, 0, 0], [1, 1, 1]],
        'color': Colors.BLUE
    },
    'L': {
        'shape': [[0, 0, 1], [1, 1, 1]],
        'color': Colors.ORANGE
    }
}

class Tetris:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.grid_width = 10
        self.grid_height = 20
        self.block_size = 25
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Tetris Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # 게임 보드 (0: 빈칸, 1: 채워진칸)
        self.board = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.board_colors = [[Colors.BLACK for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
        self.current_piece = None
        self.current_pos = [0, 0]
        self.next_piece = None
        self.spawn_new_piece()
        
        self.score = 0
        self.level = 1
        self.fall_speed = 500  # 밀리초 단위
        self.fall_time = 0
        self.running = True
        self.game_over = False
        
    def spawn_new_piece(self):
        """새로운 블록 생성"""
        if self.next_piece is None:
            piece_type = random.choice(list(TETROMINOS.keys()))
            self.next_piece = TETROMINOS[piece_type]
        
        self.current_piece = self.next_piece
        piece_type = random.choice(list(TETROMINOS.keys()))
        self.next_piece = TETROMINOS[piece_type]
        
        self.current_pos = [0, self.grid_width // 2 - 1]
        
        # 충돌 감지 (게임 오버)
        if not self.can_place():
            self.game_over = True
    
    def get_piece_shape(self):
        """현재 블록의 shape 반환"""
        return self.current_piece['shape']
    
    def get_piece_color(self):
        """현재 블록의 color 반환"""
        return self.current_piece['color']
    
    def can_place(self, offset_row=0, offset_col=0):
        """블록을 배치할 수 있는지 확인"""
        shape = self.get_piece_shape()
        row, col = self.current_pos[0] + offset_row, self.current_pos[1] + offset_col
        
        for i, shape_row in enumerate(shape):
            for j, cell in enumerate(shape_row):
                if cell:
                    new_row = row + i
                    new_col = col + j
                    
                    # 경계 확인
                    if new_row >= self.grid_height or new_col < 0 or new_col >= self.grid_width:
                        return False
                    
                    # 다른 블록과의 충돌 확인
                    if new_row >= 0 and self.board[new_row][new_col]:
                        return False
        
        return True
    
    def place_piece(self):
        """현재 블록을 보드에 배치"""
        shape = self.get_piece_shape()
        color = self.get_piece_color()
        row, col = self.current_pos
        
        for i, shape_row in enumerate(shape):
            for j, cell in enumerate(shape_row):
                if cell:
                    board_row = row + i
                    board_col = col + j
                    
                    if board_row >= 0:
                        self.board[board_row][board_col] = 1
                        self.board_colors[board_row][board_col] = color
        
        self.clear_lines()
        self.spawn_new_piece()
    
    def clear_lines(self):
        """완성된 라인 제거"""
        lines_cleared = 0
        rows_to_remove = []
        
        for i in range(self.grid_height):
            if all(self.board[i]):
                rows_to_remove.append(i)
                lines_cleared += 1
        
        # 완성된 행 제거
        for row in sorted(rows_to_remove, reverse=True):
            del self.board[row]
            del self.board_colors[row]
            self.board.insert(0, [0] * self.grid_width)
            self.board_colors.insert(0, [Colors.BLACK] * self.grid_width)
        
        # 점수 계산
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 800
        
        # 레벨 업
        self.level = 1 + self.score // 1000
        self.fall_speed = max(100, 500 - self.level * 50)
    
    def rotate_piece(self):
        """블록 회전"""
        shape = self.current_piece['shape']
        # 시계 방향 회전
        rotated = [[shape[len(shape) - 1 - j][i] for j in range(len(shape))] 
                   for i in range(len(shape[0]))]
        
        old_shape = self.current_piece['shape']
        self.current_piece['shape'] = rotated
        
        # 회전 후 충돌 확인
        if not self.can_place():
            self.current_piece['shape'] = old_shape
    
    def move_left(self):
        """블록을 왼쪽으로 이동"""
        if self.can_place(offset_col=-1):
            self.current_pos[1] -= 1
    
    def move_right(self):
        """블록을 오른쪽으로 이동"""
        if self.can_place(offset_col=1):
            self.current_pos[1] += 1
    
    def move_down(self):
        """블록을 아래로 이동"""
        if self.can_place(offset_row=1):
            self.current_pos[0] += 1
            return True
        else:
            return False
    
    def hard_drop(self):
        """블록을 끝까지 떨어뜨림"""
        while self.can_place(offset_row=1):
            self.current_pos[0] += 1
        self.place_piece()
    
    def update(self, delta_time):
        """게임 상태 업데이트"""
        if self.game_over:
            return
        
        self.fall_time += delta_time
        
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            if not self.move_down():
                self.place_piece()
    
    def handle_input(self):
        """입력 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.move_right()
                elif event.key == pygame.K_DOWN:
                    self.move_down()
                elif event.key == pygame.K_SPACE:
                    self.hard_drop()
                elif event.key == pygame.K_UP:
                    self.rotate_piece()
                elif event.key == pygame.K_r:
                    self.__init__()  # 게임 재시작
    
    def draw_grid(self):
        """게임 보드 그리기"""
        # 보드 배경
        pygame.draw.rect(self.screen, Colors.GRAY, 
                        (0, 0, self.grid_width * self.block_size, self.grid_height * self.block_size), 2)
        
        # 배치된 블록들 그리기
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if self.board[i][j]:
                    pygame.draw.rect(self.screen, self.board_colors[i][j],
                                   (j * self.block_size, i * self.block_size, 
                                    self.block_size, self.block_size))
                    pygame.draw.rect(self.screen, Colors.BLACK,
                                   (j * self.block_size, i * self.block_size, 
                                    self.block_size, self.block_size), 1)
    
    def draw_current_piece(self):
        """현재 블록 그리기"""
        shape = self.get_piece_shape()
        color = self.get_piece_color()
        row, col = self.current_pos
        
        for i, shape_row in enumerate(shape):
            for j, cell in enumerate(shape_row):
                if cell:
                    pygame.draw.rect(self.screen, color,
                                   ((col + j) * self.block_size, (row + i) * self.block_size,
                                    self.block_size, self.block_size))
                    pygame.draw.rect(self.screen, Colors.BLACK,
                                   ((col + j) * self.block_size, (row + i) * self.block_size,
                                    self.block_size, self.block_size), 1)
    
    def draw_next_piece(self):
        """다음 블록 미리보기 그리기"""
        x = self.grid_width * self.block_size + 30
        y = 50
        
        text = self.font.render('Next:', True, Colors.WHITE)
        self.screen.blit(text, (x, y))
        
        shape = self.next_piece['shape']
        color = self.next_piece['color']
        
        for i, shape_row in enumerate(shape):
            for j, cell in enumerate(shape_row):
                if cell:
                    pygame.draw.rect(self.screen, color,
                                   (x + j * 20, y + 40 + i * 20, 20, 20))
                    pygame.draw.rect(self.screen, Colors.BLACK,
                                   (x + j * 20, y + 40 + i * 20, 20, 20), 1)
    
    def draw_info(self):
        """점수 및 레벨 정보 그리기"""
        x = self.grid_width * self.block_size + 30
        y = 200
        
        score_text = self.font.render(f'Score: {self.score}', True, Colors.WHITE)
        level_text = self.font.render(f'Level: {self.level}', True, Colors.WHITE)
        
        self.screen.blit(score_text, (x, y))
        self.screen.blit(level_text, (x, y + 50))
        
        # 조작 설명
        help_texts = [
            'Controls:',
            'Left/Right: Move',
            'Down: Drop',
            'Space: Hard Drop',
            'Up: Rotate',
            'R: Restart'
        ]
        
        for i, text in enumerate(help_texts):
            help_text = self.font.render(text, True, Colors.WHITE)
            self.screen.blit(help_text, (x, y + 120 + i * 30))
    
    def draw_game_over(self):
        """게임 오버 화면 그리기"""
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill(Colors.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render('GAME OVER', True, Colors.RED)
        restart_text = self.font.render('Press R to restart', True, Colors.WHITE)
        final_score_text = self.font.render(f'Final Score: {self.score}', True, Colors.WHITE)
        
        self.screen.blit(game_over_text, 
                        (self.screen_width // 2 - game_over_text.get_width() // 2, 
                         self.screen_height // 2 - 100))
        self.screen.blit(final_score_text,
                        (self.screen_width // 2 - final_score_text.get_width() // 2,
                         self.screen_height // 2))
        self.screen.blit(restart_text,
                        (self.screen_width // 2 - restart_text.get_width() // 2,
                         self.screen_height // 2 + 100))
    
    def draw(self):
        """화면 그리기"""
        self.screen.fill(Colors.BLACK)
        self.draw_grid()
        self.draw_current_piece()
        self.draw_next_piece()
        self.draw_info()
        
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        """게임 루프"""
        while self.running:
            delta_time = self.clock.tick(60)  # 60 FPS
            
            self.handle_input()
            self.update(delta_time)
            self.draw()
        
        pygame.quit()

if __name__ == '__main__':
    game = Tetris()
    game.run()
