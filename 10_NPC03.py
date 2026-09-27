import pygame
import sys
import math

# ==========================================
# 1. KELAS ENTITY (PEMAIN)
# ==========================================
class Entity:
    def __init__(self, start_x, start_y):
        # Membuat Surface dengan background transparan
        self.original_image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.original_image.fill((255, 50, 50)) # Warna Merah
        
        # Indikator arah depan (hitam)
        pygame.draw.rect(self.original_image, (0, 0, 0), (26, 8, 6, 16)) 
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(start_x, start_y))
        
        # Posisi desimal untuk kelancaran bergerak
        self.pos_x = float(start_x)
        self.pos_y = float(start_y)
        
        self.speed = 200 
        self.angle = 0
        self.is_moving = False
        
    def move_towards_target(self, target_x, target_y, dt):
        dx = target_x - self.pos_x
        dy = target_y - self.pos_y
        distance = math.hypot(dx, dy)
        
        if distance > 1.0:
            self.is_moving = True
            dir_x = dx / distance
            dir_y = dy / distance
            
            step_distance = min(self.speed * dt, distance)
            
            self.pos_x += dir_x * step_distance
            self.pos_y += dir_y * step_distance
            
            # Rotasi
            angle_rad = math.atan2(-dy, dx)
            self.angle = math.degrees(angle_rad)
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            
            # Sinkronisasi Rect
            self.rect = self.image.get_rect(center=(round(self.pos_x), round(self.pos_y)))
        else:
            self.is_moving = False
            self.pos_x = target_x
            self.pos_y = target_y
            self.rect = self.image.get_rect(center=(round(target_x), round(target_y)))

# ==========================================
# 2. FUNGSI UTAMA (GAME LOOP)
# ==========================================
def main():
    pygame.init()
    
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mini Game: Translasi & Rotasi")
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24, bold=True)
    big_font = pygame.font.SysFont("Arial", 48, bold=True)
    
    # --- SETUP LEVEL ---
    start_pos = (100, 300)
    goal_rect = pygame.Rect(650, 250, 100, 100) # Area Hijau di Kanan
    
    # Daftar rintangan (Halangan)
    obstacles = [
        pygame.Rect(250, 150, 50, 300),
        pygame.Rect(450, 0, 50, 250),
        pygame.Rect(450, 400, 50, 200)
    ]
    
    player = Entity(start_pos[0], start_pos[1])
    target_x, target_y = float(start_pos[0]), float(start_pos[1])
    
    # --- VARIABEL SKOR ---
    base_score = 100
    click_count = 0
    penalty_points = 0
    
    # Untuk mencegah 1 halangan menguras poin setiap frame
    # kita catat halangan mana yang sedang disentuh saat ini.
    currently_hit_obstacles = set()
    
    game_won = False

    # --- GAME LOOP ---
    running = True
    while running:
        dt = clock.tick(60) / 1000.0 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_won:
                if event.button == 1:
                    target_x, target_y = event.pos
                    click_count += 1 # Tambah jumlah klik

        if not game_won:
            # 1. Update Posisi
            player.move_towards_target(target_x, target_y, dt)

            # 2. Deteksi Tabrakan dengan Halangan
            for i, obs in enumerate(obstacles):
                if player.rect.colliderect(obs):
                    if i not in currently_hit_obstacles:
                        # Baru saja masuk halangan ini, kurangi poin!
                        currently_hit_obstacles.add(i)
                        penalty_points += 15
                else:
                    if i in currently_hit_obstacles:
                        # Sudah keluar dari halangan ini
                        currently_hit_obstacles.remove(i)
            
            # 3. Deteksi Tabrakan dengan Goal
            if player.rect.colliderect(goal_rect):
                game_won = True

        # --- RENDERING (MENGGAMBAR) ---
        screen.fill((40, 40, 40)) 
        
        # Gambar Area Start (Biru)
        pygame.draw.circle(screen, (0, 100, 255), start_pos, 40, 2)
        
        # Gambar Area Goal (Hijau)
        pygame.draw.rect(screen, (0, 200, 0), goal_rect)
        goal_text = font.render("GOAL", True, (255,255,255))
        screen.blit(goal_text, (goal_rect.x + 15, goal_rect.y + 35))
        
        # Gambar Halangan (Oranye)
        for obs in obstacles:
            pygame.draw.rect(screen, (255, 140, 0), obs)
            
        # Gambar Garis Target (Hanya jika sedang jalan)
        if player.is_moving and not game_won:
            pygame.draw.line(screen, (100, 100, 100), player.rect.center, (target_x, target_y), 2)
            pygame.draw.circle(screen, (0, 255, 0), (int(target_x), int(target_y)), 5)
        
        # Gambar Pemain
        screen.blit(player.image, player.rect)

        # Hitung Skor Aktual
        current_score = base_score - (click_count * 2) - penalty_points

        # UI Info (Atas Layar)
        info_text = font.render(f"Klik: {click_count} (-2)  |  Halangan Hit: {penalty_points//15} (-15)  |  SKOR: {current_score}", True, (255,255,255))
        screen.blit(info_text, (20, 20))

        # Jika Menang, Tampilkan Layar Skor
        if game_won:
            overlay = pygame.Surface((width, height))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0,0))
            
            win_text = big_font.render("TARGET TERCAPAI!", True, (0, 255, 0))
            score_text = big_font.render(f"SKOR AKHIR ANDA: {current_score}", True, (255, 255, 0))
            
            screen.blit(win_text, (width//2 - win_text.get_width()//2, height//2 - 60))
            screen.blit(score_text, (width//2 - score_text.get_width()//2, height//2 + 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()