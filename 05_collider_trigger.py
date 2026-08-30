import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Demo Collider Solid vs Trigger")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20, bold=True)

# ==========================================
# KOMPONEN GAME (AABB COLLIDERS)
# ==========================================
# 1. PLAYER (Karakteristik Rigidbody & Kinematic)
player_rect = pygame.Rect(100, 250, 50, 50) # Kotak 50x50
player_speed = 300.0

# 2. SOLID COLLIDER (Tembok statis, menolak player)
wall_rect = pygame.Rect(400, 150, 50, 300) 

# 3. TRIGGER COLLIDER (Zona area, tembus tapi memicu event)
trigger_rect = pygame.Rect(600, 200, 100, 200)

# Variabel State
in_trigger_zone = False
score = 0

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- A. INPUT & KINEMATIC UPDATE ---
    keys = pygame.key.get_pressed()
    
    # Simpan posisi lama sebelum bergerak untuk 'Resolusi Tabrakan'
    old_x, old_y = player_rect.x, player_rect.y

    if keys[pygame.K_LEFT]:  player_rect.x -= int(player_speed * dt)
    if keys[pygame.K_RIGHT]: player_rect.x += int(player_speed * dt)
    if keys[pygame.K_UP]:    player_rect.y -= int(player_speed * dt)
    if keys[pygame.K_DOWN]:  player_rect.y += int(player_speed * dt)

    # --- B. COLLISION DETECTION (SOLID) ---
    # Jika menabrak tembok (Solid), kembalikan posisi ke awal (Resolusi Penetrasi)
    if player_rect.colliderect(wall_rect):
        player_rect.x = old_x
        player_rect.y = old_y
        # Di engine asli (seperti Unity), ini memicu OnCollisionEnter

    # --- C. TRIGGER DETECTION (GHOST/EVENT) ---
    # Jika masuk area trigger, posisi TIDAK dikembalikan (Tembus), tapi state berubah
    was_in_zone = in_trigger_zone
    in_trigger_zone = player_rect.colliderect(trigger_rect)
    
    # Logika OnTriggerEnter (Baru masuk zona)
    if in_trigger_zone and not was_in_zone:
        score += 10
        print("Memicu OnTriggerEnter: Score bertambah!")
    
    # Logika OnTriggerExit (Keluar dari zona)
    if not in_trigger_zone and was_in_zone:
        print("Memicu OnTriggerExit!")

    # --- D. RENDER ---
    screen.fill((40, 44, 52)) # Background gelap

    # Gambar Trigger Zone (Warna Transparan/Hijau Gelap)
    trigger_color = (46, 204, 113) if in_trigger_zone else (20, 100, 50)
    pygame.draw.rect(screen, trigger_color, trigger_rect)
    
    # Gambar Tembok (Solid - Merah)
    pygame.draw.rect(screen, (231, 76, 60), wall_rect)

    # Gambar Player (Biru)
    pygame.draw.rect(screen, (52, 152, 219), player_rect)

    # UI Teks
    texts = [
        f"Score (Trigger): {score}",
        "Biru: Player (Gunakan Panah)",
        "Merah: Solid Collider (Tidak tembus)",
        "Hijau: Trigger Zone (Tembus + Event)"
    ]
    for i, t in enumerate(texts):
        screen.blit(font.render(t, True, (255, 255, 255)), (10, 10 + (i*25)))

    pygame.display.flip()

pygame.quit()
sys.exit()