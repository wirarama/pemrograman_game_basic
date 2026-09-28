import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FSM vs Blend Tree (Idle, Walk, Run, Jump)")
font = pygame.font.SysFont(None, 28)
small_font = pygame.font.SysFont(None, 20)

# Warna sebagai representasi Animasi
C_IDLE = (100, 100, 100)  # Abu-abu
C_WALK = (50, 200, 50)    # Hijau
C_RUN  = (50, 50, 250)    # Biru
C_JUMP = (250, 200, 50)   # Kuning (Lompat)
WHITE  = (255, 255, 255)

# Fisika Karakter (Kapsul pergerakan - berlaku sama untuk keduanya)
speed = 0.0
MAX_SPEED = 10.0
ACCEL = 0.1

y_pos = 0.0
y_vel = 0.0
is_grounded = True
GRAVITY = 0.6
JUMP_POWER = -12.0

# Parameter khusus Blend Tree untuk transisi halus
jump_blend_weight = 0.0 
CROSSFADE_SPEED = 0.08  # Kecepatan transisi animasi (bukan fisik)

def lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t)) # Clamp 0-1
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t)
    )

def draw_text(surface, text, pos, color=WHITE, is_small=False):
    f = small_font if is_small else font
    surface.blit(f.render(text, True, color), pos)

clock = pygame.time.Clock()

while True:
    screen.fill((30, 30, 30))
    
    # 1. EVENT & INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and is_grounded:
                y_vel = JUMP_POWER
                is_grounded = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]: speed = min(speed + ACCEL, MAX_SPEED)
    elif keys[pygame.K_LEFT]: speed = max(speed - ACCEL, 0.0)

    # 2. UPDATE FISIKA (Berlaku untuk posisi kotak di layar)
    if not is_grounded:
        y_vel += GRAVITY
        y_pos += y_vel
        if y_pos >= 0:  # Menyentuh tanah
            y_pos = 0
            y_vel = 0
            is_grounded = True

    # ==========================================
    # LOGIKA KIRI: FINITE STATE MACHINE (FSM)
    # Aturan: Hanya 1 state yang aktif. Lompat membatalkan semua.
    # ==========================================
    fsm_state = "IDLE"
    fsm_color = C_IDLE
    
    if not is_grounded:
        fsm_state = "JUMP"
        fsm_color = C_JUMP
    elif speed >= 6.0:
        fsm_state = "RUN"
        fsm_color = C_RUN
    elif speed >= 1.0:
        fsm_state = "WALK"
        fsm_color = C_WALK

    # ==========================================
    # LOGIKA KANAN: BLEND TREE & CROSSFADE
    # Aturan: Hitung locomotion dasar, lalu blend dengan Lompat
    # ==========================================
    
    # A. Hitung Locomotion 1D (Kecepatan)
    if speed <= 5.0:
        loco_t = speed / 5.0
        loco_color = lerp_color(C_IDLE, C_WALK, loco_t)
        loco_text = f"Locomotion: Idle-Walk"
    else:
        loco_t = (speed - 5.0) / 5.0
        loco_color = lerp_color(C_WALK, C_RUN, loco_t)
        loco_text = f"Locomotion: Walk-Run"

    # B. Hitung Transisi Crossfade Udara (Airborne Blend)
    # Alih-alih langsung patah (snap) seperti FSM, animasi melompat memudar masuk/keluar
    if not is_grounded:
        jump_blend_weight = min(1.0, jump_blend_weight + CROSSFADE_SPEED)
    else:
        jump_blend_weight = max(0.0, jump_blend_weight - CROSSFADE_SPEED)

    # C. Hasil Akhir Blend Tree
    blend_color = lerp_color(loco_color, C_JUMP, jump_blend_weight)
    
    # --- 3. RENDER UI ---
    draw_text(screen, f"Kiri/Kanan: Jalan/Lari | SPASI: Lompat", (250, 20))
    draw_text(screen, f"Speed: {speed:.1f} | Grounded: {is_grounded}", (320, 50), is_small=True)

    # Gambar Tanah
    pygame.draw.line(screen, WHITE, (50, 350), (850, 350), 2)

    # Render FSM (Kiri)
    fsm_rect = pygame.Rect(150, 200 + y_pos, 150, 150)
    pygame.draw.rect(screen, fsm_color, fsm_rect)
    pygame.draw.rect(screen, WHITE, fsm_rect, 2)
    
    draw_text(screen, "FSM (Diskrit)", (165, 160))
    draw_text(screen, f"State Aktif: {fsm_state}", (150, 370))
    draw_text(screen, "(Transisi Snap / Patah)", (150, 400), is_small=True)

    # Render Blend Tree (Kanan)
    blend_rect = pygame.Rect(550, 200 + y_pos, 150, 150)
    pygame.draw.rect(screen, blend_color, blend_rect)
    pygame.draw.rect(screen, WHITE, blend_rect, 2)
    
    draw_text(screen, "Blend Tree (Kontinu)", (550, 160))
    draw_text(screen, loco_text, (530, 370))
    draw_text(screen, f"Jump Blend: {int(jump_blend_weight*100)}%", (530, 395), is_small=True)
    draw_text(screen, "(Transisi Halus / Crossfade)", (530, 420), is_small=True)

    pygame.display.flip()
    clock.tick(60)