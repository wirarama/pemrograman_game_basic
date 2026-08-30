import pygame
import math
import random
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Physics: Circle Collision & Momentum")
clock = pygame.time.Clock()

class Ball:
    def __init__(self, x, y, radius, mass, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-200, 200)
        self.vy = random.uniform(-200, 200)
        self.radius = radius
        self.mass = mass
        self.color = color

    def update(self, dt):
        # Translasi / Pergerakan
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Collision Detection dengan Tembok (Batas Layar)
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -1
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx *= -1
            
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= -1
        elif self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

def check_collision(b1, b2):
    # Rumus Jarak Euclidean (Pythagoras)
    dx = b2.x - b1.x
    dy = b2.y - b1.y
    distance = math.sqrt(dx**2 + dy**2)

    # Deteksi Tabrakan: Jika jarak < jumlah radius kedua bola
    if distance < b1.radius + b2.radius:
        # 1. RESOLUSI PENETRASI (Mencegah bola saling menempel)
        overlap = 0.5 * (distance - b1.radius - b2.radius)
        
        # Hindari pembagian dengan nol
        if distance == 0: distance = 0.0001 
        
        nx = dx / distance # Normal X
        ny = dy / distance # Normal Y
        
        # Geser bola agar tidak bertumpuk
        b1.x -= nx * overlap
        b1.y -= ny * overlap
        b2.x += nx * overlap
        b2.y += ny * overlap

        # 2. RESOLUSI PANTULAN (Elastic Collision)
        # Menghitung kecepatan relatif
        kx = b1.vx - b2.vx
        ky = b1.vy - b2.vy
        
        # Dot product dari kecepatan dengan vektor normal
        p = 2.0 * (nx * kx + ny * ky) / (b1.mass + b2.mass)
        
        # Terapkan perubahan kecepatan berdasarkan massa
        b1.vx -= p * b2.mass * nx
        b1.vy -= p * b2.mass * ny
        b2.vx += p * b1.mass * nx
        b2.vy += p * b1.mass * ny

# Membuat beberapa bola
balls = []
colors = [(231, 76, 60), (46, 204, 113), (52, 152, 219), (241, 196, 15), (155, 89, 182)]
for _ in range(10):
    r = random.randint(20, 50)
    m = r # Massa sebanding dengan ukuran
    b = Ball(random.randint(100, 700), random.randint(100, 500), r, m, random.choice(colors))
    balls.append(b)

running = True
while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update fisika
    for ball in balls:
        ball.update(dt)

    # Cek tabrakan antar bola
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            check_collision(balls[i], balls[j])

    # Render
    screen.fill((30, 30, 40))
    for ball in balls:
        ball.draw(screen)
        
    pygame.display.flip()

pygame.quit()
sys.exit()