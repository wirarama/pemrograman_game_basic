import pygame
import sys

# ==========================================
# 1. INISIALISASI GAME ENGINE (PYGAME)
# ==========================================
pygame.init()

# Pengaturan Layar (GUI)
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demonstrasi Arsitektur Game & Transformasi 2D")

# Mengatur Font untuk UI (Antarmuka Grafis Text)
font = pygame.font.SysFont("Arial", 20, bold=True)
small_font = pygame.font.SysFont("Arial", 16)

# Mengatur FPS dan Clock (Siklus Waktu)
clock = pygame.time.Clock()
TARGET_FPS = 60

# ==========================================
# 2. PEMBUATAN ASET (SPRITE)
# ==========================================
# Kita membuat "Sprite" sederhana menggunakan Surface Pygame (Kotak dengan penunjuk arah)
# Penunjuk arah (segitiga) penting agar rotasi terlihat jelas.
SPRITE_SIZE = 100
original_sprite = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
original_sprite.fill((41, 128, 185)) # Warna kotak: Biru
# Menggambar segitiga kuning sebagai "kepala" atau penunjuk arah depan
pygame.draw.polygon(original_sprite, (241, 196, 15), [(50, 10), (90, 90), (10, 90)])

# ==========================================
# 3. VARIABEL STATE (FONDASI KOORDINAT)
# ==========================================
# Posisi Awal (Translasi) - diletakkan di tengah layar
pos_x = float(WIDTH // 2)
pos_y = float(HEIGHT // 2)

# Rotasi dan Skala
angle = 0.0      # Derajat rotasi (0 - 360)
scale = 1.0      # Skala 1.0 = ukuran asli

# Kecepatan Transformasi
move_speed = 300.0   # Piksel per detik
rot_speed = 150.0    # Derajat per detik
scale_speed = 1.0    # Pembesaran per detik

# ==========================================
# 4. GAME LOOP (SIKLUS HIDUP UTAMA)
# ==========================================
running = True
while running:
    # --- A. MENGHITUNG DELTA TIME (dt) ---
    # Memastikan game berjalan di kecepatan yang sama di komputer mana pun
    dt = clock.tick(TARGET_FPS) / 1000.0 

    # --- B. FASE INPUT ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Mengambil status semua tombol keyboard saat ini
    keys = pygame.key.get_pressed()

    # --- C. FASE UPDATE (MANIPULASI TRANSFORMASI 2D) ---
    
    # 1. Translasi (Posisi) - Menggunakan tombol Panah atau WASD
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        pos_x -= move_speed * dt
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        pos_x += move_speed * dt
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        pos_y -= move_speed * dt
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        pos_y += move_speed * dt

    # 2. Rotasi - Menggunakan Q (Kiri) dan E (Kanan)
    if keys[pygame.K_q]:
        angle += rot_speed * dt
    if keys[pygame.K_e]:
        angle -= rot_speed * dt

    # 3. Skala - Menggunakan Z (Membesar) dan C (Mengecil)
    if keys[pygame.K_z]:
        scale += scale_speed * dt
    if keys[pygame.K_c]:
        scale -= scale_speed * dt
        
    # Batasi agar skala tidak menjadi negatif atau terlalu besar
    scale = max(0.2, min(scale, 4.0)) 


    # --- D. FASE RENDER (PENGGAMBARAN) ---
    
    # 1. Bersihkan layar setiap frame (Background gelap)
    screen.fill((44, 62, 80)) # Warna Slate/Abu-abu gelap

    # 2. Eksekusi Transformasi pada Sprite
    # pygame.transform.rotozoom melakukan Rotasi dan Skala secara bersamaan
    # dengan kualitas yang baik dan mulus.
    transformed_sprite = pygame.transform.rotozoom(original_sprite, angle, scale)
    
    # Dapatkan titik tengah baru dari sprite yang sudah ditransformasi
    # Ini penting agar sprite berputar pada poros tengahnya, bukan pojoknya.
    sprite_rect = transformed_sprite.get_rect(center=(int(pos_x), int(pos_y)))

    # 3. Gambar Sprite ke Layar
    screen.blit(transformed_sprite, sprite_rect)

    # 4. Gambar Antarmuka Grafis (UI / HUD) untuk debugging & informasi
    ui_texts = [
        f"FPS: {clock.get_fps():.1f}",
        f"Posisi (X, Y) : ({pos_x:.1f}, {pos_y:.1f}) | Arah Panah/WASD",
        f"Rotasi        : {angle:.1f} derajat | Tombol Q / E",
        f"Skala         : {scale:.2f}x | Tombol Z / C"
    ]

    # Render teks UI di pojok kiri atas
    y_offset = 10
    for text in ui_texts:
        text_surface = font.render(text, True, (236, 240, 241)) # Warna putih tulang
        screen.blit(text_surface, (10, y_offset))
        y_offset += 30
        
    # Render instruksi di bawah
    instruction = "Tekan panah/WASD untuk bergerak | Q/E untuk memutar | Z/C untuk zoom"
    inst_surf = small_font.render(instruction, True, (189, 195, 199))
    screen.blit(inst_surf, (10, HEIGHT - 30))

    # 5. Flip Layar (Tampilkan frame yang sudah selesai digambar)
    pygame.display.flip()

# ==========================================
# 5. SHUTDOWN / EXIT
# ==========================================
pygame.quit()
sys.exit()