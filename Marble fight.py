import pygame
import random
import math

# --- Settings ---
WIDTH, HEIGHT = 800, 600
MARBLE_RADIUS = 15
MARBLE_COLOR = (100, 200, 255)
BG_COLOR = (30, 30, 40)
MAX_MARBLES = 100
MULTIPLY_ON_COLLISION = True

class Marble:
    def __init__(self, x, y, vx=None, vy=None):
        self.x = x
        self.y = y
        self.vx = vx if vx is not None else random.uniform(-3, 3)
        self.vy = vy if vy is not None else random.uniform(-3, 3)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        # Bounce off walls
        if self.x < MARBLE_RADIUS or self.x > WIDTH - MARBLE_RADIUS:
            self.vx *= -1
        if self.y < MARBLE_RADIUS or self.y > HEIGHT - MARBLE_RADIUS:
            self.vy *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, MARBLE_COLOR, (int(self.x), int(self.y)), MARBLE_RADIUS)

def collide(m1, m2):
    dx = m1.x - m2.x
    dy = m1.y - m2.y
    dist = math.hypot(dx, dy)
    return dist < MARBLE_RADIUS * 2

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Marble Multiply/Release Simulation")
    clock = pygame.time.Clock()

    marbles = [Marble(WIDTH // 2, HEIGHT // 2)]
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Click to "release" a marble
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if len(marbles) < MAX_MARBLES:
                    mx, my = pygame.mouse.get_pos()
                    marbles.append(Marble(mx, my))

        # Move marbles
        for m in marbles:
            m.move()

        # Check collisions and multiply
        new_marbles = []
        if MULTIPLY_ON_COLLISION:
            marble_pairs = [(i, j) for i in range(len(marbles)) for j in range(i+1, len(marbles))]
            for i, j in marble_pairs:
                m1, m2 = marbles[i], marbles[j]
                if collide(m1, m2) and len(marbles) + len(new_marbles) < MAX_MARBLES:
                    # On collision, spawn a new marble nearby
                    nx = (m1.x + m2.x) / 2 + random.randint(-10, 10)
                    ny = (m1.y + m2.y) / 2 + random.randint(-10, 10)
                    new_marbles.append(Marble(nx, ny))
        marbles.extend(new_marbles)

        # Draw
        screen.fill(BG_COLOR)
        for m in marbles:
            m.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
