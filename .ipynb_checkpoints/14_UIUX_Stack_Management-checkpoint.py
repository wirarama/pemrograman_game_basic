import pygame
import sys

# ==========================================
# 1. KONFIGURASI DASAR & WARNA
# ==========================================
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UI Stack Management")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
DARK_GRAY = (40, 40, 40)
BLUE = (50, 150, 255)
RED = (200, 50, 50)

font_title = pygame.font.Font(None, 64)
font_button = pygame.font.Font(None, 40)

# ==========================================
# 2. KOMPONEN UI DASAR (BUTTON & PANEL)
# ==========================================
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action  # Fungsi callback saat tombol diklik
        self.is_hovered = False

    def draw(self, surface):
        # UX: Visual feedback saat hover
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=8)
        
        text_surf = font_button.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.action:
                self.action() # Panggil fungsi aksi

class Panel:
    """Representasi satu layar menu yang berisi judul dan tombol"""
    def __init__(self, title):
        self.title = title
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def draw(self, surface):
        surface.fill(DARK_GRAY)
        
        # Gambar Judul Panel
        title_surf = font_title.render(self.title, True, WHITE)
        title_rect = title_surf.get_rect(center=(WIDTH//2, 100))
        surface.blit(title_surf, title_rect)
        
        # Gambar semua tombol
        for btn in self.buttons:
            btn.draw(surface)

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

# ==========================================
# 3. UI MANAGER (STACK CONTROLLER)
# ==========================================
class UIManager:
    def __init__(self):
        self.stack = [] # Struktur data Stack (LIFO)

    def push(self, panel):
        """Menambahkan menu baru ke tumpukan teratas"""
        self.stack.append(panel)

    def pop(self):
        """Menghapus menu teratas dan kembali ke menu di bawahnya"""
        if len(self.stack) > 1:
            self.stack.pop()

    def get_current_panel(self):
        """Mengambil menu yang sedang aktif (paling atas)"""
        if self.stack:
            return self.stack[-1]
        return None

    def draw(self, surface):
        current = self.get_current_panel()
        if current:
            current.draw(surface)

    def handle_event(self, event):
        current = self.get_current_panel()
        if current:
            current.handle_event(event)

# ==========================================
# 4. INSTANSIASI MENU & WIRING (PENGKABELAN)
# ==========================================
ui_manager = UIManager()

# Buat Panel (Layar Menu)
main_menu = Panel("MAIN MENU")
settings_menu = Panel("SETTINGS")
audio_menu = Panel("AUDIO SETTINGS")

# Aksi Tombol menggunakan Lambda untuk mengakses ui_manager
# Main Menu Buttons
main_menu.add_button(Button(WIDTH//2 - 125, 200, 250, 50, "Play Game", GRAY, BLUE, lambda: print("Game Started!")))
main_menu.add_button(Button(WIDTH//2 - 125, 270, 250, 50, "Settings", GRAY, BLUE, lambda: ui_manager.push(settings_menu)))
main_menu.add_button(Button(WIDTH//2 - 125, 340, 250, 50, "Quit", GRAY, RED, lambda: sys.exit()))

# Settings Menu Buttons
settings_menu.add_button(Button(WIDTH//2 - 125, 200, 250, 50, "Audio", GRAY, BLUE, lambda: ui_manager.push(audio_menu)))
settings_menu.add_button(Button(WIDTH//2 - 125, 270, 250, 50, "Graphics", GRAY, BLUE, lambda: print("Graphics Menu")))
settings_menu.add_button(Button(WIDTH//2 - 125, 340, 250, 50, "Back", GRAY, RED, lambda: ui_manager.pop()))

# Audio Menu Buttons
audio_menu.add_button(Button(WIDTH//2 - 125, 200, 250, 50, "Volume +", GRAY, BLUE, lambda: print("Volume Naik")))
audio_menu.add_button(Button(WIDTH//2 - 125, 270, 250, 50, "Volume -", GRAY, BLUE, lambda: print("Volume Turun")))
audio_menu.add_button(Button(WIDTH//2 - 125, 340, 250, 50, "Back", GRAY, RED, lambda: ui_manager.pop()))

# Push Main Menu sebagai menu dasar (Base)
ui_manager.push(main_menu)

# ==========================================
# 5. MAIN LOOP GAME
# ==========================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # Distribusikan event ke UI Manager
        ui_manager.handle_event(event)

    # Render UI
    ui_manager.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)