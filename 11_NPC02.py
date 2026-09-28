import pygame
import sys
import math

class Entity:
    def __init__(self, start_x, start_y):
        # 1. Membuat Permukaan (Surface) sebagai visual Entity
        # SRCALPHA digunakan agar background rotasi transparan
        self.original_image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.original_image.fill((255, 50, 50)) # Warna Kotak Merah
        
        # Tambahkan indikator "depan" (garis hitam) agar rotasi terlihat
        # Menggambar kotak kecil di sisi KANAN (arah 0 derajat)
        pygame.draw.rect(self.original_image, (0, 0, 0), (26, 8, 6, 16)) 
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(start_x, start_y))
        
        # Simpan posisi aktual dalam float
        self.pos_x = float(start_x)
        self.pos_y = float(start_y)
        
        self.speed = 150 
        self.angle = 0
        
    def move_towards_target(self, target_x, target_y, dt):
        dx = target_x - self.pos_x
        dy = target_y - self.pos_y
        
        distance = math.hypot(dx, dy)
        
        if distance > 0.1:
            dir_x = dx / distance
            dir_y = dy / distance
            
            step_distance = min(self.speed * dt, distance)
            
            self.pos_x += dir_x * step_distance
            self.pos_y += dir_y * step_distance
            
            # 2. LOGIKA ROTASI MATEMATIKA
            # Gunakan -dy karena sumbu Y di monitor/Pygame terbalik dari kartesian
            angle_rad = math.atan2(-dy, dx)
            self.angle = math.degrees(angle_rad) # Konversi Radian ke Derajat
            
            # 3. Merotasi Gambar (selalu gunakan original_image)
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            
            # 4. Sinkronisasi Rect (Ukurannya berubah saat dirotasi, jadi harus di-center ulang)
            self.rect = self.image.get_rect(center=(round(self.pos_x), round(self.pos_y)))
            
        else:
            self.pos_x = target_x
            self.pos_y = target_y
            # Tetap pertahankan sudut rotasi terakhir saat berhenti
            self.rect = self.image.get_rect(center=(round(target_x), round(target_y)))

def main():
    pygame.init()
    
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Demo Translasi & Rotasi Vektor")
    
    clock = pygame.time.Clock()
    
    player = Entity(width // 2, height // 2)
    target_x, target_y = float(width // 2), float(height // 2)
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    target_x, target_y = event.pos

        player.move_towards_target(target_x, target_y, dt)

        screen.fill((40, 40, 40)) 
        
        pygame.draw.line(screen, (100, 100, 100), player.rect.center, (target_x, target_y), 2)
        pygame.draw.circle(screen, (0, 255, 0), (int(target_x), int(target_y)), 5)
        
        # 5. Menggambar Entity bukan lagi pakai draw.rect, melainkan blit Surface
        screen.blit(player.image, player.rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()