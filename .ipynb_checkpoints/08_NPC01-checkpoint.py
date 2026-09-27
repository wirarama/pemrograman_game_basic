import pygame
import math
from enum import Enum

# 1. Definisi State
class NPCState(Enum):
    PATROL = 1
    CHASE = 2
    ATTACK = 3

class EnemyNPC:
    def __init__(self, x, y, waypoints):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.speed = 3
        
        # Inisialisasi FSM
        self.state = NPCState.PATROL
        
        # Variabel Logika AI
        self.chase_radius = 250
        self.attack_radius = 40
        self.waypoints = waypoints
        self.current_wp_index = 0
        
        # Variabel Pathfinding
        self.path = [] # Menyimpan List node A*
        self.path_timer = 0 # Mencegah A* dihitung setiap frame
        
    def update(self, player_rect, grid, dt):
        # 2. Hitung Jarak ke Player (Kondisi Transisi)
        center_x, center_y = self.rect.center
        p_center_x, p_center_y = player_rect.center
        dist_to_player = math.hypot(p_center_x - center_x, p_center_y - center_y)
        
        # 3. Evaluasi Transisi State
        if self.state == NPCState.PATROL:
            if dist_to_player <= self.chase_radius:
                self.state = NPCState.CHASE
                self.path = [] # Reset jalur patroli
                
        elif self.state == NPCState.CHASE:
            if dist_to_player <= self.attack_radius:
                self.state = NPCState.ATTACK
            elif dist_to_player > self.chase_radius:
                self.state = NPCState.PATROL
                self.path = [] # Reset jalur kembali ke waypoint
                
        elif self.state == NPCState.ATTACK:
            if dist_to_player > self.attack_radius:
                self.state = NPCState.CHASE

        # 4. Eksekusi Aksi Berdasarkan State
        self.execute_state(player_rect.center, grid, dt)

    def execute_state(self, player_pos, grid, dt):
        self.path_timer -= dt
        
        if self.state == NPCState.PATROL:
            target = self.waypoints[self.current_wp_index]
            self.move_towards(target, grid)
            
            # Cek jika sudah sampai waypoint
            if math.hypot(target[0] - self.rect.centerx, target[1] - self.rect.centery) < 10:
                self.current_wp_index = (self.current_wp_index + 1) % len(self.waypoints)
                self.path = [] # Minta A* cari jalan ke waypoint baru
                
        elif self.state == NPCState.CHASE:
            # Karena player bergerak, perbarui jalur A* secara berkala (misal tiap 0.5 detik)
            if self.path_timer <= 0:
                self.path = [] 
                self.path_timer = 0.5 
                
            self.move_towards(player_pos, grid)
            
        elif self.state == NPCState.ATTACK:
            self.path = [] # Berhenti bergerak
            # Panggil fungsi menembak atau memukul di sini
            
    def move_towards(self, target_pos, grid):
        # Minta rute baru dari A* jika belum punya jalur
        if len(self.path) == 0:
            start_node = (self.rect.centerx // 32, self.rect.centery // 32)
            target_node = (int(target_pos[0] // 32), int(target_pos[1] // 32))
            
            # Asumsi find_path_astar adalah fungsi A* yang mengembalikan list koordinat grid
            self.path = find_path_astar(start_node, target_node, grid)

        # Logika pergerakan menyusuri node A* (menuju path[0])
        if self.path and len(self.path) > 0:
            next_node = self.path[0]
            target_x = (next_node[0] * 32) + 16 # Titik tengah grid
            target_y = (next_node[1] * 32) + 16
            
            # (Di sini tambahkan logika translasi x & y merubah self.rect.x dan self.rect.y)
            
            # Jika sudah mencapai node ini, hapus dari list
            if math.hypot(target_x - self.rect.centerx, target_y - self.rect.centery) < 5:
                self.path.pop(0)