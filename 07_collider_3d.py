import pygame
import math
import random
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Physics: Z-Depth Collider & Projection")
clock = pygame.time.Clock()

class Sphere3D:
    def __init__(self, x, y, z, radius, color):
        self.x = x
        self.y = y
        self.z = z
        self.vx = random.uniform(-100, 100)
        self.vy = random.uniform(-100, 100)
        self.vz = random.uniform(-100, 100)
        self.radius = radius # Radius asli dalam 3D
        self.color = color

    def update(self, dt, bounds):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt

        # 3D BOUNDARY COLLISION (Mantul di dalam kotak 3D)
        if self.x > bounds or self.x < -bounds:
            self.vx *= -1
            self.x = bounds if self.x > bounds else -bounds
            
        if self.y > bounds or self.y < -bounds:
            self.vy *= -1
            self.y = bounds if self.y > bounds else -bounds
            
        if self.z > bounds or self.z < 0: # Z = 0 adalah kamera, Z = bounds adalah batas jauh
            self.vz *= -1
            self.z = bounds if self.z > bounds else 0

def check_collision_3d(s1, s2):
    # Rumus Jarak 3D
    dx = s2.x - s1.x
    dy = s2.y - s1.y
    dz = s2.z - s1.z
    distance = math.sqrt(dx**2 + dy**2 + dz**2)

    if distance < s1.radius + s2.radius:
        # Tukar arah kecepatan (Resolusi tabrakan 3D Sederhana)
        s1.vx, s2.vx = s2.vx, s1.vx
        s1.vy, s2.vy = s2.vy, s1.vy
        s1.vz, s2.vz = s2.vz, s1.vz
        
        # Pisahkan sedikit agar tidak menempel
        overlap = (s1.radius + s2.radius - distance) / 2
        if distance != 0:
            s1.x -= (dx/distance) * overlap
            s1.y -= (dy/distance) * overlap
            s1.z -= (dz/distance) * overlap
            s2.x += (dx/distance) * overlap
            s2.y += (dy/distance) * overlap
            s2.z += (dz/distance) * overlap

# Setup
bounds_3d = 300 # Ukuran ruangan 3D
spheres = []
colors = [(231, 76, 60), (46, 204, 113), (52, 152, 219), (241, 196, 15)]

for _ in range(8):
    s = Sphere3D(random.uniform(-100, 100), random.uniform(-100, 100), random.uniform(100, bounds_3d), 30, random.choice(colors))
    spheres.append(s)

FOV = 400.0 # Field of View

running = True
while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for s in spheres:
        s.update(dt, bounds_3d)

    for i in range(len(spheres)):
        for j in range(i + 1, len(spheres)):
            check_collision_3d(spheres[i], spheres[j])

    # Z-SORTING: Mengurutkan objek dari Z terbesar (paling jauh) ke terkecil
    # Agar bola yang jauh tidak digambar di depan bola yang dekat
    spheres.sort(key=lambda s: s.z, reverse=True)

    screen.fill((20, 20, 25))

    # Render Proyeksi 3D ke 2D
    for s in spheres:
        # Jika objek berada di belakang kamera (Z <= 0), jangan digambar
        if s.z + 100 <= 0: continue 
        
        # Proyeksi Perspektif
        z_factor = FOV / (s.z + 200) # +200 untuk menggeser kamera mundur
        screen_x = int(s.x * z_factor + WIDTH / 2)
        screen_y = int(s.y * z_factor + HEIGHT / 2)
        
        # Radius bola 2D juga mengecil jika jarak Z-nya menjauh
        screen_radius = int(s.radius * z_factor)
        
        # Simulasi shading (Semakin jauh, semakin gelap)
        darkness = max(0.2, min(1.0, 1.0 - (s.z / bounds_3d)))
        draw_color = (int(s.color[0] * darkness), int(s.color[1] * darkness), int(s.color[2] * darkness))

        pygame.draw.circle(screen, draw_color, (screen_x, screen_y), screen_radius)
        # Efek Garis agar terlihat 3D
        pygame.draw.circle(screen, (255, 255, 255), (screen_x, screen_y), screen_radius, 1)

    # UI
    font = pygame.font.SysFont("Arial", 16)
    screen.blit(font.render("3D Sphere Collision (X, Y, Z Physics)", True, (255, 255, 255)), (10, 10))
    pygame.display.flip()

pygame.quit()
sys.exit()