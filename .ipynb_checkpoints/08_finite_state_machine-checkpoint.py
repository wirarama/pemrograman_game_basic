import pygame
import sys

# Inisialisasi Pygame
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FSM vs Blend Tree Demonstration")
font = pygame.font.SysFont(None, 28)
small_font = pygame.font.SysFont(None, 20)

# Warna merepresentasikan "Animasi"
COLOR_IDLE = (100, 100, 100)  # Abu-abu
COLOR_WALK = (50, 200, 50)    # Hijau
COLOR_RUN = (50, 50, 250)     # Biru
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Variabel Global Karakter
current_speed = 0.0
MAX_SPEED = 10.0
ACCELERATION = 0.05

def lerp_color(c1, c2, t):
    """Fungsi linear interpolation (Lerp) untuk mencampur dua warna"""
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t)
    )

def draw_text(surface, text, pos, color=WHITE, is_small=False):
    f = small_font if is_small else font
    text_surface = f.render(text, True, color)
    surface.blit(text_surface, pos)

clock = pygame.time.Clock()

while True:
    screen.fill((30, 30, 30))
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Input Control untuk menaikkan/menurunkan kecepatan
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] or keys[pygame.K_UP]:
        current_speed = min(current_speed + ACCELERATION, MAX_SPEED)
    elif keys[pygame.K_LEFT] or keys[pygame.K_DOWN]:
        current_speed = max(current_speed - ACCELERATION, 0.0)

    # ==========================================
    # LOGIKA 1: FINITE STATE MACHINE (FSM)
    # Transisi diskrit berdasarkan threshold
    # ==========================================
    fsm_state = "IDLE"
    fsm_color = COLOR_IDLE
    
    if current_speed >= 6.0:
        fsm_state = "RUN"
        fsm_color = COLOR_RUN
    elif current_speed >= 1.0:
        fsm_state = "WALK"
        fsm_color = COLOR_WALK

    # ==========================================
    # LOGIKA 2: BLEND TREE (1D)
    # Interpolasi kontinu berdasarkan parameter
    # Titik kunci: Idle(0), Walk(5), Run(10)
    # ==========================================
    blend_color = COLOR_IDLE
    blend_text = ""
    
    if current_speed <= 5.0:
        # Blend antara Idle dan Walk
        t = current_speed / 5.0  # Normalisasi 0-5 menjadi 0.0-1.0
        blend_color = lerp_color(COLOR_IDLE, COLOR_WALK, t)
        blend_text = f"Idle: {100 - int(t*100)}% | Walk: {int(t*100)}%"
    else:
        # Blend antara Walk dan Run
        t = (current_speed - 5.0) / 5.0  # Normalisasi 5-10 menjadi 0.0-1.0
        blend_color = lerp_color(COLOR_WALK, COLOR_RUN, t)
        blend_text = f"Walk: {100 - int(t*100)}% | Run: {int(t*100)}%"

    # --- RENDER UI ---
    
    # Info Kecepatan
    draw_text(screen, f"Tekan Kiri/Kanan Panah (Speed: {current_speed:.1f} / 10.0)", (200, 20))

    # Render FSM (Kiri)
    pygame.draw.rect(screen, fsm_color, (100, 100, 200, 200))
    pygame.draw.rect(screen, WHITE, (100, 100, 200, 200), 2)
    draw_text(screen, "FSM (Diskrit)", (130, 70))
    draw_text(screen, f"State: {fsm_state}", (110, 310))
    draw_text(screen, "Ganti state seketika", (110, 340), is_small=True)

    # Render Blend Tree (Kanan)
    pygame.draw.rect(screen, blend_color, (500, 100, 200, 200))
    pygame.draw.rect(screen, WHITE, (500, 100, 200, 200), 2)
    draw_text(screen, "Blend Tree (Kontinu)", (510, 70))
    draw_text(screen, blend_text, (480, 310))
    draw_text(screen, "Mencampur 2 animasi bersamaan", (490, 340), is_small=True)

    pygame.display.flip()
    clock.tick(60)