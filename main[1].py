import pygame
import random
import sys
from pathlib import Path

# Basic config
WIDTH, HEIGHT = 600, 700
FPS = 60

# Initialize
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Runner")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28)

# Load assets (use generated simple assets if files missing)
ASSET_DIR = Path(__file__).parent / "assets"
ASSET_DIR.mkdir(exist_ok=True)

def load_image(path, fallback_draw_fn):
    try:
        img = pygame.image.load(path).convert_alpha()
    except Exception:
        img = fallback_draw_fn()
    return img

# Fallback generators
def make_player():
    surf = pygame.Surface((56,40), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (200,200,255), [(0,40),(28,0),(56,40)])
    pygame.draw.rect(surf, (100,100,255), (8,20,40,12))
    return surf

def make_meteor():
    surf = pygame.Surface((48,48), pygame.SRCALPHA)
    pygame.draw.circle(surf, (180,90,60), (24,24), 22)
    for i in range(6):
        pygame.draw.circle(surf, (200,120,80), (8+i*6,8+i*3), 3)
    return surf

def make_bg():
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.fill((6,6,20))
    # stars
    for i in range(120):
        x = random.randrange(0, WIDTH)
        y = random.randrange(0, HEIGHT)
        r = random.choice([1,1,2])
        pygame.draw.circle(surf, (200,200,255), (x,y), r)
    return surf

player_img = load_image(str(ASSET_DIR / "player.png"), make_player)
meteor_img = load_image(str(ASSET_DIR / "meteor.png"), make_meteor)
bg_img = load_image(str(ASSET_DIR / "background.png"), make_bg)

# Player properties
player_rect = player_img.get_rect(midbottom=(WIDTH//2, HEIGHT-30))
PLAYER_SPEED = 6

# Meteor handling
meteor_group = pygame.sprite.Group()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = meteor_img
        self.rect = self.image.get_rect(topleft=(x,y))
        self.speed = speed
        self.rotate_angle = random.uniform(-3,3)
        self._orig = self.image
        self._angle = 0
    def update(self):
        self.rect.y += self.speed
        # simple rotation
        self._angle = (self._angle + self.rotate_angle) % 360
        self.image = pygame.transform.rotate(self._orig, self._angle)
        # adjust rect to keep position stable
        if self.rect.top > HEIGHT + 50:
            self.kill()

# Game variables
score = 0
spawn_timer = 0
meteor_speed = 3
running = True
game_over = False

# UI helpers
def draw_text(surf, text, x, y):
    img = font.render(text, True, (230,230,230))
    surf.blit(img, (x,y))

def reset_game():
    global score, spawn_timer, meteor_speed, game_over
    meteor_group.empty()
    score = 0
    spawn_timer = 0
    meteor_speed = 3
    player_rect.centerx = WIDTH//2
    game_over = False

# Main loop
while running:
    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()

    # Input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_rect.x += PLAYER_SPEED

    # constrain
    player_rect.x = max(0, min(WIDTH - player_rect.width, player_rect.x))

    if not game_over:
        # spawn meteors
        spawn_timer += 1
        if spawn_timer > max(12, 50 - score//200):
            x = random.randint(0, WIDTH-48)
            meteor_group.add(Meteor(x, -60, meteor_speed + random.random()*1.8))
            spawn_timer = 0

        # update meteors
        meteor_group.update()

        # collisions
        for m in meteor_group:
            if player_rect.colliderect(m.rect):
                game_over = True

        # scoring and difficulty
        score += 1
        if score % 800 == 0:
            meteor_speed += 0.6

    # draw
    screen.blit(bg_img, (0,0))
    meteor_group.draw(screen)
    screen.blit(player_img, player_rect.topleft)
    draw_text(screen, f"Score: {score}", 12, 12)

    if game_over:
        draw_text(screen, "GAME OVER - Press R to restart", WIDTH//2 - 200, HEIGHT//2 - 10)
        draw_text(screen, "Press Q or Close Window to Exit", WIDTH//2 - 200, HEIGHT//2 + 30)

    pygame.display.flip()

pygame.quit()
sys.exit()