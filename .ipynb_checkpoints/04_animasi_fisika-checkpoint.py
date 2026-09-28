import pygame
import math
import sys

# ==========================================
# 1. INISIALISASI
# ==========================================
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demonstrasi Fisika, Momentum & Trigonometri")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)

# ==========================================
# 2. VARIABEL FISIKA & MATEMATIKA
# ==========================================
# Posisi
pos_x = float(WIDTH // 2)
pos_y = 100.0

# Kecepatan (Velocity)
vel_x = 0.0
vel_y = 0.0

# Konstanta Gaya (Forces)
GRAVITY = 1500.0       # Akselerasi gravitasi ke bawah (piksel/detik^2)
JUMP_FORCE = -700.0    # Kecepatan awal saat melompat (negatif karena Y ke atas)
MOVE_ACCEL = 1500.0    # Akselerasi saat bergerak horizontal
FRICTION = 8.0         # Tingkat redaman gesekan (semakin besar, semakin cepat berhenti)
BOUNCE_FACTOR = -0.4   # Seberapa memantul saat jatuh (0 = tidak memantul, -1 = memantul penuh)

FLOOR_Y = 500.0        # Posisi Y untuk lantai
is_grounded = False

# ==========================================
# 3. GAME LOOP
# ==========================================
running = True
while running:
    dt = clock.tick(60) / 1000.0

    # --- A. INPUT SEBAGAI TRIGGER FISIKA ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # EVENT MELOMPAT (Trigger Impuls Fisika)
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_w) and is_grounded:
                vel_y = JUMP_FORCE      # Berikan kecepatan instan ke atas
                is_grounded = False     # Objek kini berada di udara

    # EVENT BERGERAK (Memberikan gaya/akselerasi berlanjut)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        vel_x -= MOVE_ACCEL * dt
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        vel_x += MOVE_ACCEL * dt

    # --- B. UPDATE MATEMATIKA & FISIKA ---
    
    # 1. REDAMAN / FRICTION (Linear Interpolation Math)
    # Jika tidak ada tombol yang ditekan, perlambat kecepatan X secara halus menuju 0
    # Rumus: kecepatan_sekarang += (target - kecepatan_sekarang) * faktor_redaman * dt
    if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_a] or keys[pygame.K_d]):
        vel_x += (0 - vel_x) * FRICTION * dt
        
    # Batasi kecepatan maksimal horizontal agar tidak tembus pandang (Speed Cap)
    vel_x = max(-500.0, min(vel_x, 500.0))

    # 2. GRAVITASI (Kinematika)
    # Gravitasi secara konstan menarik kecepatan vertikal (Y) ke bawah
    vel_y += GRAVITY * dt

    # 3. UPDATE POSISI (Translasi Integral)
    # Posisi baru = Posisi lama + (Kecepatan * Waktu)
    pos_x += vel_x * dt
    pos_y += vel_y * dt

    # 4. COLLISION DETECTION (Lantai & Tembok)
    # Cek benturan dengan lantai
    if pos_y >= FLOOR_Y:
        pos_y = FLOOR_Y
        
        # Jika jatuh cukup keras, pantulkan (Bounce)
        if vel_y > 100.0:
            vel_y = vel_y * BOUNCE_FACTOR 
            is_grounded = False
        else:
            vel_y = 0.0 # Hentikan pantulan jika sudah kecil
            is_grounded = True

    # Cek benturan dengan tembok (Batas layar kiri & kanan) - efek memantul
    if pos_x < 25:
        pos_x = 25
        vel_x = abs(vel_x) * 0.8 # Pantul ke kanan, hilangkan 20% energi
    elif pos_x > WIDTH - 25:
        pos_x = WIDTH - 25
        vel_x = -abs(vel_x) * 0.8 # Pantul ke kiri


    # --- C. TRIGONOMETRI (Visual Tambahan) ---
    # Membuat indikator yang melayang-layang mulus menggunakan Sine Wave
    # math.sin(waktu) menghasilkan nilai bolak-balik antara -1 dan 1
    waktu_ms = pygame.time.get_ticks()
    hover_offset_y = math.sin(waktu_ms / 200.0) * 15.0 # Jarak naik turun 15 piksel


    # --- D. RENDER ---
    screen.fill((30, 30, 40)) # Background warna gelap
    
    # Gambar Lantai
    pygame.draw.rect(screen, (70, 70, 90), (0, FLOOR_Y + 25, WIDTH, HEIGHT - FLOOR_Y))

    # 1. Gambar Objek Utama (Karakter)
    # Menggunakan lingkaran berukuran radius 25
    pygame.draw.circle(screen, (46, 204, 113), (int(pos_x), int(pos_y)), 25)

    # 2. Gambar Indikator Melayang (Trigonometri)
    # Menggambar segitiga terbalik di atas kepala pemain yang naik turun
    p1 = (pos_x, pos_y - 40 + hover_offset_y)
    p2 = (pos_x - 10, pos_y - 60 + hover_offset_y)
    p3 = (pos_x + 10, pos_y - 60 + hover_offset_y)
    pygame.draw.polygon(screen, (241, 196, 15), [p1, p2, p3])

    # UI Information
    ui_texts = [
        f"Velocity X : {vel_x:.1f} px/s (Momentum & Friction)",
        f"Velocity Y : {vel_y:.1f} px/s (Gravity = {GRAVITY})",
        f"Grounded   : {is_grounded}",
        "Kontrol: A/D Bergerak, SPASI Melompat"
    ]
    
    for i, t in enumerate(ui_texts):
        text_surf = font.render(t, True, (200, 220, 220))
        screen.blit(text_surf, (15, 15 + (i * 25)))

    pygame.display.flip()

pygame.quit()
sys.exit()