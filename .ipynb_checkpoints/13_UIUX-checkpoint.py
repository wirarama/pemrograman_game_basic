import pygame
import sys

# 1. INISIALISASI & KONFIGURASI DASAR
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Contoh UI/UX Game: Menu & HUD")
clock = pygame.time.Clock()

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
DARK_GRAY = (50, 50, 50)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 150, 255)

# Font
font_title = pygame.font.Font(None, 72)
font_menu = pygame.font.Font(None, 48)
font_hud = pygame.font.Font(None, 36)

# State Game
STATE_MENU = 0
STATE_PLAYING = 1
STATE_PAUSE = 2
current_state = STATE_MENU

# Variabel Dummy Gameplay
player_health = 100
max_health = 100
player_score = 0

# 2. FUNGSI HELPER UNTUK UI (Micro-interactions)
def draw_button(text, font, text_col, x, y, width, height, normal_col, hover_col, action):
    global current_state, player_health, player_score
    
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    button_rect = pygame.Rect(x, y, width, height)
    
    # State Feedback: Hover effect
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_col, button_rect)
        if click[0] == 1 and action is not None:
            pygame.time.delay(200) # Debounce sederhana
            action()
    else:
        pygame.draw.rect(screen, normal_col, button_rect)
        
    # Gambar teks di tengah tombol
    text_surf = font.render(text, True, text_col)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

# 3. FUNGSI AKSI TOMBOL
def start_game():
    global current_state, player_health, player_score
    current_state = STATE_PLAYING
    player_health = 100
    player_score = 0

def resume_game():
    global current_state
    current_state = STATE_PLAYING

def quit_game():
    pygame.quit()
    sys.exit()

def go_to_menu():
    global current_state
    current_state = STATE_MENU

# 4. FUNGSI RENDERING
def draw_main_menu():
    screen.fill(DARK_GRAY)
    title = font_title.render("SUPER GAME", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    draw_button("Play", font_menu, WHITE, WIDTH//2 - 100, 250, 200, 60, GRAY, BLUE, start_game)
    draw_button("Quit", font_menu, WHITE, WIDTH//2 - 100, 350, 200, 60, GRAY, RED, quit_game)

def draw_hud():
    # Health Bar (Non-Diegetic UI diletakkan di sudut kiri atas)
    hp_bar_width = 200
    hp_bar_height = 25
    hp_ratio = player_health / max_health
    
    # Background Health Bar (Merah/Kosong)
    pygame.draw.rect(screen, RED, (20, 20, hp_bar_width, hp_bar_height))
    # Foreground Health Bar (Hijau/Isi)
    pygame.draw.rect(screen, GREEN, (20, 20, hp_bar_width * hp_ratio, hp_bar_height))
    # Border
    pygame.draw.rect(screen, WHITE, (20, 20, hp_bar_width, hp_bar_height), 2)
    
    # Teks Skor (Kanan Atas)
    score_text = font_hud.render(f"Score: {player_score}", True, WHITE)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 20, 20))

def draw_gameplay():
    # Simulasi layar permainan (warna biru langit)
    screen.fill((100, 200, 250))
    
    # Instruksi di tengah layar (Spatial/Diegetic dummy)
    inst_text = font_hud.render("Tekan 'SPACE' untuk Kurangi HP | Tekan 'ESC' untuk Pause", True, BLACK)
    screen.blit(inst_text, (WIDTH//2 - inst_text.get_width()//2, HEIGHT//2))
    
    # Gambar HUD selalu paling atas
    draw_hud()

def draw_pause_menu():
    # Menggambar gameplay di latar belakang
    draw_gameplay()
    
    # Overlay Semi-Transparan
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150) # Transparansi
    overlay.fill(BLACK)
    screen.blit(overlay, (0,0))
    
    # Menu Pause
    title = font_title.render("PAUSED", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
    
    draw_button("Resume", font_menu, WHITE, WIDTH//2 - 100, 250, 200, 60, GRAY, BLUE, resume_game)
    draw_button("Main Menu", font_menu, WHITE, WIDTH//2 - 100, 350, 200, 60, GRAY, RED, go_to_menu)

# 5. MAIN LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        
        # Input Gameplay
        if event.type == pygame.KEYDOWN:
            if current_state == STATE_PLAYING:
                if event.key == pygame.K_ESCAPE:
                    current_state = STATE_PAUSE
                if event.key == pygame.K_SPACE:
                    player_health = max(0, player_health - 10)
                    player_score += 50
            elif current_state == STATE_PAUSE:
                if event.key == pygame.K_ESCAPE:
                    current_state = STATE_PLAYING

    # Logic Rendering Berdasarkan State
    if current_state == STATE_MENU:
        draw_main_menu()
    elif current_state == STATE_PLAYING:
        draw_gameplay()
    elif current_state == STATE_PAUSE:
        draw_pause_menu()

    pygame.display.flip()
    clock.tick(60)