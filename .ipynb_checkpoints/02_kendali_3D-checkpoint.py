import pygame
import math
import sys

# ==========================================
# 1. INISIALISASI GAME ENGINE
# ==========================================
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demonstrasi 3D Engine Sederhana (Telah Diperbaiki)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18, bold=True)

# ==========================================
# 2. FONDASI SISTEM KOORDINAT 3D (LOCAL SPACE)
# ==========================================
# Titik-titik (Vertices) kubus dari -1 sampai 1
vertices = [
    [-1, -1, -1], [ 1, -1, -1], [ 1,  1, -1], [-1,  1, -1], # Sisi Depan
    [-1, -1,  1], [ 1, -1,  1], [ 1,  1,  1], [-1,  1,  1]  # Sisi Belakang
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0), # Kotak Depan
    (4, 5), (5, 6), (6, 7), (7, 4), # Kotak Belakang
    (0, 4), (1, 5), (2, 6), (3, 7)  # Garis penghubung
]

# ==========================================
# 3. VARIABEL TRANSFORMASI 3D
# ==========================================
angle_x = 0.0 
angle_y = 0.0 
angle_z = 0.0 

# [PERBAIKAN DI SINI] - Skala diubah jadi 1.0 agar tidak raksasa
scale = 1.0         
pos_z = 3.0          
fov = 400.0  # FOV dibesarkan sedikit agar kubus tampak pas di layar        

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- INPUT ---
    keys = pygame.key.get_pressed()
    
    # Rotasi
    if keys[pygame.K_w]: angle_x -= 2.0 * dt
    if keys[pygame.K_s]: angle_x += 2.0 * dt
    if keys[pygame.K_a]: angle_y -= 2.0 * dt
    if keys[pygame.K_d]: angle_y += 2.0 * dt
    if keys[pygame.K_q]: angle_z -= 2.0 * dt
    if keys[pygame.K_e]: angle_z += 2.0 * dt
        
    # Translasi & Skala
    if keys[pygame.K_UP]: pos_z -= 2.0 * dt    
    if keys[pygame.K_DOWN]: pos_z += 2.0 * dt  
    if keys[pygame.K_RIGHT]: scale += 1.0 * dt # Kecepatan skala disesuaikan
    if keys[pygame.K_LEFT]: scale -= 1.0 * dt  

    # Mencegah layar terbalik karena nilai Z minus atau skala minus
    if pos_z < 0.1: pos_z = 0.1
    if scale < 0.1: scale = 0.1

    # --- UPDATE MATEMATIKA ---
    projected_points = []

    for v in vertices:
        x, y, z = v[0], v[1], v[2]

        # Rotasi Y
        rot_y_x = x * math.cos(angle_y) - z * math.sin(angle_y)
        rot_y_z = x * math.sin(angle_y) + z * math.cos(angle_y)
        x, z = rot_y_x, rot_y_z

        # Rotasi X
        rot_x_y = y * math.cos(angle_x) - z * math.sin(angle_x)
        rot_x_z = y * math.sin(angle_x) + z * math.cos(angle_x)
        y, z = rot_x_y, rot_x_z
        
        # Rotasi Z
        rot_z_x = x * math.cos(angle_z) - y * math.sin(angle_z)
        rot_z_y = x * math.sin(angle_z) + y * math.cos(angle_z)
        x, y = rot_z_x, rot_z_y

        z += pos_z 

        # Proyeksi Perspektif
        f = fov / z if z != 0 else 0
            
        screen_x = (x * f * scale) + (WIDTH / 2)
        screen_y = (y * f * scale) + (HEIGHT / 2)

        projected_points.append([screen_x, screen_y])

    # --- RENDER ---
    screen.fill((15, 20, 25)) # Background abu-abu sangat gelap

    # Gambar Garis (Wireframe) dengan warna Cyan terang
    for edge in edges:
        p1 = projected_points[edge[0]]
        p2 = projected_points[edge[1]]
        pygame.draw.line(screen, (0, 255, 255), (p1[0], p1[1]), (p2[0], p2[1]), 3)
        
        # Gambar Titik Sudut dengan warna Kuning
        pygame.draw.circle(screen, (255, 255, 0), (int(p1[0]), int(p1[1])), 6)

    # UI Information Text
    texts = [
        f"Rotasi X (Pitch) : {angle_x:.2f} | Tombol W / S",
        f"Rotasi Y (Yaw)   : {angle_y:.2f} | Tombol A / D",
        f"Rotasi Z (Roll)  : {angle_z:.2f} | Tombol Q / E",
        f"Jarak Z (Depth)  : {pos_z:.2f} | Panah Atas / Bawah",
        f"Skala (Zoom)     : {scale:.2f} | Panah Kiri / Kanan"
    ]
    
    for i, t in enumerate(texts):
        text_surf = font.render(t, True, (255, 255, 255))
        screen.blit(text_surf, (15, 15 + (i * 25)))

    pygame.display.flip()

pygame.quit()
sys.exit()