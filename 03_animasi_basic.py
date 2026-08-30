import pygame
import sys

# ==========================================
# 1. INISIALISASI GAME ENGINE
# ==========================================
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demonstrasi FSM Animasi Sprite")
clock = pygame.time.Clock()
TARGET_FPS = 60

# ==========================================
# 2. HELPER: MEMBUAT DUMMY SPRITE SHEET
# ==========================================
# Fungsi ini murni agar kode bisa jalan tanpa Anda harus download gambar dulu.
# Di game asli, Anda menggunakan pygame.image.load("spritesheet.png")
def create_dummy_sprites():
    idle_frames = []
    run_frames = []
    size = 100
    
    # Bikin 4 frame untuk IDLE (Warna Biru yang bernapas perlahan)
    for i in range(4):
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        color = (52, 152, 219 - (i * 20)) # Biru memudar
        pygame.draw.rect(surf, color, (10, 10 + i*2, 80, 80)) # Kotak naik turun
        idle_frames.append(surf)

    # Bikin 6 frame untuk RUN (Warna Merah yang bergerak cepat)
    for i in range(6):
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        color = (231, 76, 60 - (i * 10)) # Merah
        # Kotak miring ke depan (simulasi lari)
        pygame.draw.polygon(surf, color, [(20 + i*5, 10), (90 + i*5, 10), (70 - i*5, 90), (0 - i*5, 90)])
        run_frames.append(surf)
        
    return {"IDLE": idle_frames, "RUN": run_frames}

# ==========================================
# 3. KELAS KARAKTER (FSM & ANIMATOR)
# ==========================================
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 250.0
        
        # Load Animasi
        self.animations = create_dummy_sprites()
        
        # Variabel Finite State Machine (FSM)
        self.current_state = "IDLE"
        self.facing_right = True
        
        # Variabel Internal Animator
        self.current_frame_index = 0.0
        self.animation_speed = 10.0  # Kecepatan putar frame (frames per detik)

    def set_state(self, new_state):
        # Mencegah reset animasi jika state tidak berubah
        if self.current_state != new_state:
            self.current_state = new_state
            self.current_frame_index = 0.0 # Reset animasi ke frame pertama

    def update(self, dt, keys):
        # 1. BACA INPUT & LOGIKA PERGERAKAN (Translasi)
        is_moving = False
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed * dt
            self.facing_right = False
            is_moving = True
            
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed * dt
            self.facing_right = True
            is_moving = True

        # 2. LOGIKA TRANSISI FSM (Berdasarkan pergerakan)
        if is_moving:
            self.set_state("RUN")
            self.animation_speed = 15.0 # Animasi lari lebih cepat
        else:
            self.set_state("IDLE")
            self.animation_speed = 8.0  # Animasi idle lebih lambat

        # 3. UPDATE TIMER ANIMASI (Maju ke frame berikutnya)
        self.current_frame_index += self.animation_speed * dt
        
        # Dapatkan jumlah total frame dari state saat ini
        total_frames = len(self.animations[self.current_state])
        
        # Jika frame indeks melebihi batas, loop kembali ke 0
        if self.current_frame_index >= total_frames:
            self.current_frame_index = 0.0

    def draw(self, screen):
        # 1. Ambil gambar spesifik dari array berdasarkan State dan Indeks
        frame_list = self.animations[self.current_state]
        
        # Konversi float index menjadi integer (karena index list harus bulat)
        current_image = frame_list[int(self.current_frame_index)]
        
        # 2. Jika menghadap kiri, Flip (Skala -1 pada X) gambarnya
        if not self.facing_right:
            current_image = pygame.transform.flip(current_image, True, False)

        # 3. Render gambar ke layar (di titik tengah posisi x, y)
        rect = current_image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(current_image, rect)
        
        # Debugging Teks: Menampilkan State di atas kepala pemain
        font = pygame.font.SysFont("Arial", 16, bold=True)
        text_color = (46, 204, 113) if self.current_state == "RUN" else (236, 240, 241)
        state_text = font.render(f"State: {self.current_state}", True, text_color)
        screen.blit(state_text, (self.x - 40, self.y - 70))

# ==========================================
# 4. INISIALISASI GAME LOOP
# ==========================================
player = Player(WIDTH // 2, HEIGHT // 2)

running = True
while running:
    # A. HITUNG DELTA TIME
    dt = clock.tick(TARGET_FPS) / 1000.0

    # B. BACA EVENT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()

    # C. UPDATE LOGIKA
    player.update(dt, keys)

    # D. RENDER
    screen.fill((44, 62, 80)) # Background Dark Slate
    
    # Gambar Lantai
    pygame.draw.rect(screen, (52, 73, 94), (0, HEIGHT//2 + 50, WIDTH, HEIGHT//2))
    
    # Gambar Player
    player.draw(screen)
    
    # UI Instruksi
    font = pygame.font.SysFont("Arial", 18)
    inst = font.render("Tahan A / D atau Panah Kiri / Kanan untuk melihat Transisi Animasi", True, (200, 200, 200))
    screen.blit(inst, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()