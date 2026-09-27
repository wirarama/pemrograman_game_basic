import pygame
import math

class Entity:
    def __init__(self, start_x, start_y):
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.rect.center = (start_x, start_y)
        
        # 1. Simpan posisi aktual dalam float untuk presisi desimal
        self.pos_x = float(start_x)
        self.pos_y = float(start_y)
        
        # Kecepatan dalam satuan piksel per detik
        self.speed = 150 
        
    def move_towards_target(self, target_x, target_y, dt):
        # 2. Cari selisih jarak x dan y (Vektor Arah)
        dx = target_x - self.pos_x
        dy = target_y - self.pos_y
        
        # 3. Hitung jarak total (Hipotenusa) dengan Teorema Pythagoras
        distance = math.hypot(dx, dy)
        
        # Mencegah error pembagian dengan nol jika objek sudah tepat di target
        if distance > 0.1:
            # 4. Normalisasi arah (mengubah jarak aktual menjadi rasio antara -1.0 hingga 1.0)
            dir_x = dx / distance
            dir_y = dy / distance
            
            # 5. Hitung jarak tempuh frame ini
            # Gunakan min() untuk mencegah NPC meleset (overshoot) dan bergetar melewati target
            step_distance = min(self.speed * dt, distance)
            
            # 6. Translasi posisi float
            self.pos_x += dir_x * step_distance
            self.pos_y += dir_y * step_distance
            
            # 7. Sinkronisasi posisi ke Rect (pembulatan otomatis)
            self.rect.centerx = round(self.pos_x)
            self.rect.centery = round(self.pos_y)
            
        else:
            # Objek sudah mencapai tujuan
            self.pos_x = target_x
            self.pos_y = target_y
            self.rect.center = (round(target_x), round(target_y))