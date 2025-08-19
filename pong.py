import pygame
from random import randint, choice

WIDTH, HEIGHT = 800, 800
BAR_WIDTH = 10
BAR_HEIGHT = 80
BAR_VEL = 8
PLAYER_START = (700, 400)
BOT_START = (100, 400)
BALL_SIZE = 10
BALL_START_VEL_X = 5

class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, BAR_WIDTH, BAR_HEIGHT)
        self.rect.center = start_pos
        self.vel = BAR_VEL
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.rect.y - self.vel != 0:
                self.rect.y -= self.vel
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.rect.y + self.vel + BAR_HEIGHT != HEIGHT:
                self.rect.y += self.vel

    def draw(self):
        pygame.draw.rect(screen, "white", self.rect)

class Bot(Player):
    def __init__(self, start_pos):
        super().__init__(start_pos)
    
    def update(self, ball: "Ball"):
        if ball.rect.centery > self.rect.centery:
            self.rect.centery += self.vel
        elif ball.rect.centery < self.rect.centery:
            self.rect.centery -= self.vel

    def draw(self):
        super().draw()
    
class Ball(pygame.sprite.Sprite):
    def __init__(self, start_dir, start_vel_y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0,0, BALL_SIZE, BALL_SIZE)
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.vel_x = BALL_START_VEL_X * start_dir
        self.vel_y = start_vel_y
        self.reset = False

    def check_collisions(self, bars):
        if self.rect.centerx >= WIDTH:
            bot.score += 1
            self.reset = True
        elif self.rect.centerx <= 0:
            player.score += 1
            self.reset = True
        
        if self.rect.centery <= 0:
            self.vel_y *= -1
        elif self.rect.centery >= HEIGHT:
            self.vel_y *= -1
        
        if pygame.sprite.spritecollideany(ball, bars):
            
            self.vel_y = self.vel_y * 100 / randint(70, 110) + 0.2
            self.vel_x *= -1

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
    
    def draw(self):
        pygame.draw.circle(screen, "white", self.rect.center, 5)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

font = pygame.font.Font(size = 40)

player = Player(PLAYER_START)
bot = Bot(BOT_START)
bars = pygame.sprite.Group(player, bot)
start_dir = choice([-1, 1])
start_vel_y = randint(-5, 5)
ball = Ball(start_dir, start_vel_y)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update()
    ball.check_collisions(bars)
    ball.update()
    bot.update(ball)

    if ball.reset == True:
        ball.kill()
        if start_dir == -1:
            start_dir = 1
        elif start_dir == 1:
            start_dir = -1
        start_vel_y = randint(-5, 5)
        ball = Ball(start_dir, start_vel_y)

    screen.fill("black")
    score_player_text = font.render(str(player.score), False, "white")
    score_bot_text = font.render(str(bot.score), False, "white")
    screen.blit(score_player_text, (600, 100))
    screen.blit(score_bot_text, (200, 100))
    player.draw()
    bot.draw()
    ball.draw()
    pygame.display.flip()

    clock.tick(60)

pygame.quit()