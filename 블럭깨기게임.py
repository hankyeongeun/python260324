import pygame
import random
import sys

# pygame 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("블럭깨기 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# 시계 및 프레임 속도
clock = pygame.time.Clock()
FPS = 60

# 폰트
font_large = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)


class Paddle:
    """패들 클래스"""
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 6
    
    def move(self, keys):
        """키보드 입력으로 패들 이동"""
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
    
    def draw(self, surface):
        """패들 그리기"""
        pygame.draw.rect(surface, CYAN, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)


class Ball:
    """공 클래스"""
    def __init__(self, x, y, radius):
        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)
        self.radius = radius
        self.speed_x = 5
        self.speed_y = -5
        self.active = True
    
    def update(self, paddle, bricks):
        """공의 위치 업데이트 및 충돌 처리"""
        if not self.active:
            return 0
        
        # 공 이동
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # 화면 경계 충돌 (좌우)
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1
        
        # 화면 경계 충돌 (상단)
        if self.rect.top <= 0:
            self.speed_y *= -1
        
        # 화면 하단 (공실패)
        if self.rect.top >= SCREEN_HEIGHT:
            self.active = False
            return 0
        
        # 패들 충돌
        if self.rect.colliderect(paddle.rect):
            if self.speed_y > 0:  # 공이 아래로 내려오는 경우만
                self.speed_y *= -1
                # 패들의 위치에 따라 공의 방향 조정
                contact_x = (self.rect.centerx - paddle.rect.left) / paddle.rect.width
                self.speed_x = (contact_x - 0.5) * 10
        
        # 블럭 충돌
        for brick in bricks[:]:
            if self.rect.colliderect(brick.rect):
                # 충돌 위치에 따라 공 정지 및 블럭 제거
                bricks.remove(brick)
                self.active = False
                return 1

        return 0
    
    def draw(self, surface):
        """공 그리기"""
        pygame.draw.circle(surface, YELLOW, self.rect.center, self.radius)


class Brick:
    """블럭 클래스"""
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    
    def draw(self, surface):
        """블럭 그리기"""
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 1)


def create_bricks():
    """블럭 생성"""
    bricks = []
    colors = [
        (255, 102, 102), # 진한 핑크
        (255, 153, 51),  # 주황
        (255, 255, 102), # 연노랑
        (102, 255, 102), # 연녹
        (102, 204, 255), # 하늘
        (153, 102, 255), # 보라
        (255, 102, 204), # 자주
        (102, 255, 204)  # 청록
    ]
    brick_width = 75
    brick_height = 20
    brick_margin = 5
    
    # 6행 8열로 블럭 생성 (상단 더 화려하게)
    for row in range(6):
        for col in range(8):
            x = col * (brick_width + brick_margin) + 25
            y = row * (brick_height + brick_margin) + 50
            color = colors[row % len(colors)]
            bricks.append(Brick(x, y, brick_width, brick_height, color))
    
    return bricks


def draw_score(surface, score, lives):
    """점수와 생명 표시"""
    score_text = font_small.render(f"점수: {score}", True, WHITE)
    lives_text = font_small.render(f"생명: {lives}", True, WHITE)
    surface.blit(score_text, (10, 10))
    surface.blit(lives_text, (SCREEN_WIDTH - 200, 10))


def draw_game_over(surface, text, color):
    """게임 오버 화면"""
    game_over_text = font_large.render(text, True, color)
    instruction_text = font_small.render("스페이스를 눌러 다시 시작하세요", True, WHITE)
    
    # 텍스트를 중앙에 배치
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    
    # 배경 어둡게
    dark_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    dark_surface.set_alpha(150)
    dark_surface.fill(BLACK)
    surface.blit(dark_surface, (0, 0))
    
    surface.blit(game_over_text, text_rect)
    surface.blit(instruction_text, instruction_rect)


def main():
    """메인 게임 루프"""
    running = True
    score = 0
    lives = 3
    game_over = False
    won = False
    
    # 게임 객체 생성
    paddle = Paddle((SCREEN_WIDTH - 300) // 2, SCREEN_HEIGHT - 40, 300, 15)
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 7)
    bricks = create_bricks()
    
    while running:
        clock.tick(FPS)
        
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over or won:
                        # 게임 재시작
                        score = 0
                        lives = 3
                        game_over = False
                        won = False
                        paddle = Paddle((SCREEN_WIDTH - 300) // 2, SCREEN_HEIGHT - 40, 300, 15)
                        ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 7)
                        bricks = create_bricks()
        
        if not game_over and not won:
            # 게임 진행
            keys = pygame.key.get_pressed()
            paddle.move(keys)
            destroyed = ball.update(paddle, bricks)
            score += destroyed * 10
            
            # 공이 화면 하단에 떨어지거나 블럭 충돌 시 (사라진 경우)
            if not ball.active:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    # 공 재시작
                    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 7)
            
            # 블럭 모두 제거했을 때
            if len(bricks) == 0:
                won = True
                score += 1000
        
        # 화면 그리기
        screen.fill(BLACK)
        
        # 게임 요소 그리기
        paddle.draw(screen)
        ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)
        
        # 점수 및 생명 표시
        draw_score(screen, score, lives)
        
        # 게임 오버 또는 승리 화면
        if game_over:
            draw_game_over(screen, "게임 오버!", RED)
        elif won:
            draw_game_over(screen, "승리!", GREEN)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

