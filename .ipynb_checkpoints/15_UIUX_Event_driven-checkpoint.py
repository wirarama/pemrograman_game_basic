import pygame
import sys

# ==========================================
# 1. EVENT MANAGER (OBSERVER HUB)
# ==========================================
class EventManager:
    """Sistem sentral untuk mendaftarkan dan memancarkan event"""
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type, listener_function):
        """Mendaftarkan fungsi UI untuk mendengarkan event tertentu"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener_function)

    def post(self, event_type, data=None):
        """Memicu event dan mengirimkan data ke semua UI yang mendengarkan"""
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener(data)

# ==========================================
# 2. GAMEPLAY DOMAIN (PUBLISHER)
# ==========================================
class Player:
    """Logika Player yang tidak tahu menahu tentang visual UI sama sekali"""
    def __init__(self, event_manager):
        self.em = event_manager
        self.max_health = 100
        
        # Subscribe ke event reset agar Player bisa mereset statusnya sendiri
        self.em.subscribe("GAME_RESET", self.reset)
        self.reset()

    def reset(self, data=None):
        self._health = self.max_health
        self._score = 0
        self.is_game_over = False
        
        # Pancarkan status awal
        self.em.post("HEALTH_CHANGED", {"current": self._health, "max": self.max_health})
        self.em.post("SCORE_CHANGED", {"score": self._score})

    def take_damage(self, amount):
        if self.is_game_over:
            return
            
        self._health = max(0, self._health - amount)
        print(f"[GAMEPLAY] Player kena damage! Sisa HP: {self._health}")
        
        # Publish Event: "HEALTH_CHANGED"
        self.em.post("HEALTH_CHANGED", {"current": self._health, "max": self.max_health})

        # Cek kondisi Kalah (HP Habis)
        if self._health <= 0:
            self.is_game_over = True
            print("[GAMEPLAY] HP Habis! Memancarkan event GAME_OVER.")
            self.em.post("GAME_OVER", {"message": "GAME OVER! HP HABIS"})

    def add_score(self, amount):
        if self.is_game_over:
            return

        self._score += amount
        print(f"[GAMEPLAY] Player dapat skor! Total: {self._score}")
        
        # Publish Event: "SCORE_CHANGED"
        self.em.post("SCORE_CHANGED", {"score": self._score})

        # Cek kondisi Menang (Skor >= 1000)
        if self._score >= 1000:
            self.is_game_over = True
            print("[GAMEPLAY] Target Skor Tercapai! Memancarkan event VICTORY.")
            self.em.post("VICTORY", {"message": "SELAMAT! ANDA MENANG!"})

# ==========================================
# 3. UI DOMAIN (SUBSCRIBER/OBSERVER)
# ==========================================
class HealthBarUI:
    def __init__(self, event_manager, x, y):
        self.x = x
        self.y = y
        self.current_hp = 100
        self.max_hp = 100
        
        event_manager.subscribe("HEALTH_CHANGED", self.on_health_updated)

    def on_health_updated(self, data):
        self.current_hp = data["current"]
        self.max_hp = data["max"]

    def draw(self, surface):
        hp_ratio = self.current_hp / self.max_hp
        pygame.draw.rect(surface, (200, 50, 50), (self.x, self.y, 200, 25)) # Background
        pygame.draw.rect(surface, (50, 200, 50), (self.x, self.y, 200 * hp_ratio, 25)) # Fill
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, 200, 25), 2) # Border

class ScoreUI:
    def __init__(self, event_manager, font, x, y):
        self.font = font
        self.x = x
        self.y = y
        self.text_surface = None
        
        event_manager.subscribe("SCORE_CHANGED", self.on_score_updated)
        self.on_score_updated({"score": 0})

    def on_score_updated(self, data):
        score_val = data["score"]
        self.text_surface = self.font.render(f"SCORE: {score_val}", True, (255, 255, 255))

    def draw(self, surface):
        if self.text_surface:
            surface.blit(self.text_surface, (self.x, self.y))

class ButtonUI:
    """Helper class untuk tombol pada menu akhir"""
    def __init__(self, x, y, width, height, text, color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = (min(color[0] + 40, 255), min(color[1] + 40, 255), min(color[2] + 40, 255))
        self.action = action
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.action:
                self.action()

    def draw(self, surface, font):
        current_col = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_col, self.rect, border_radius=8)
        
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class EndGameUI:
    """Subscriber yang memproses event GAME_OVER dan VICTORY"""
    def __init__(self, event_manager, width, height, font_title, font_button):
        self.em = event_manager
        self.width = width
        self.height = height
        self.font_title = font_title
        self.font_button = font_button
        
        self.active = False
        self.title_text = ""
        self.title_color = (255, 255, 255)

        # Mendaftarkan diri ke event
        self.em.subscribe("GAME_OVER", self.on_game_over)
        self.em.subscribe("VICTORY", self.on_victory)
        self.em.subscribe("GAME_RESET", self.on_reset)

        # Buat Tombol
        center_x = width // 2
        self.btn_restart = ButtonUI(center_x - 170, 350, 150, 50, "Ulang", (50, 150, 255), self.restart_game)
        self.btn_quit = ButtonUI(center_x + 20, 350, 150, 50, "Selesai", (200, 50, 50), self.quit_game)

    def on_game_over(self, data):
        self.active = True
        self.title_text = data["message"]
        self.title_color = (220, 50, 50) # Merah

    def on_victory(self, data):
        self.active = True
        self.title_text = data["message"]
        self.title_color = (50, 220, 50) # Hijau

    def on_reset(self, data=None):
        self.active = False # Sembunyikan overlay saat game di-reset

    def restart_game(self):
        # UI memancarkan event bahwa game ingin diulang
        self.em.post("GAME_RESET")

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def handle_event(self, event):
        if not self.active:
            return
        self.btn_restart.handle_event(event)
        self.btn_quit.handle_event(event)

    def draw(self, surface):
        if not self.active:
            return

        # Overlay semi-transparan
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(210)
        overlay.fill((20, 20, 20))
        surface.blit(overlay, (0, 0))

        # Judul Pesan
        title_surf = self.font_title.render(self.title_text, True, self.title_color)
        title_rect = title_surf.get_rect(center=(self.width // 2, 220))
        surface.blit(title_surf, title_rect)

        # Draw Tombol
        self.btn_restart.draw(surface, self.font_button)
        self.btn_quit.draw(surface, self.font_button)

# ==========================================
# 4. INISIALISASI & MAIN LOOP
# ==========================================
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Event-Driven UI (Game Over & Victory Overlay)")
clock = pygame.time.Clock()

font_title = pygame.font.Font(None, 56)
font_ui = pygame.font.Font(None, 40)
font_info = pygame.font.Font(None, 28)

# Buat Instance Hub
event_mgr = EventManager()

# Instansiasi Publisher & Subscribers
player = Player(event_mgr)
hp_bar = HealthBarUI(event_mgr, x=20, y=20)
score_text = ScoreUI(event_mgr, font=font_ui, x=580, y=20)
end_game_ui = EndGameUI(event_mgr, WIDTH, HEIGHT, font_title, font_ui)

while True:
    screen.fill((40, 40, 40))
    
    # Event Handling Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # Alirkan event mouse ke UI Overlay jika aktif
        end_game_ui.handle_event(event)
            
        if event.type == pygame.KEYDOWN:
            # Input gameplay hanya diproses bila game belum berakhir
            if not player.is_game_over:
                if event.key == pygame.K_SPACE:
                    player.take_damage(20)
                if event.key == pygame.K_RETURN:
                    player.add_score(200)

    # Draw Teks Instruksi Gameplay
    info = font_info.render("Tekan SPACE (-20 HP) | Tekan ENTER (+200 Skor)", True, (180, 180, 180))
    screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 300))

    # Draw HUD (Di-render tiap frame berdasarkan data ter-cache dari event)
    hp_bar.draw(screen)
    score_text.draw(screen)
    
    # Draw Menu Overlay (Hanya menggambar jika active=True)
    end_game_ui.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)