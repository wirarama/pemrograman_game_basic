import pygame
import math
import heapq
from enum import Enum

# ==========================================
# 1. DEFINISI STATE & ALGORITMA A*
# ==========================================
class NPCState(Enum):
    PATROL = 1
    CHASE = 2
    ATTACK = 3

def heuristic(a, b):
    # Menggunakan jarak Manhattan untuk Grid 4-arah atau 8-arah
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path_astar(start, goal, obstacles):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        # Cek tetangga (Kiri, Kanan, Atas, Bawah, dan Diagonal)
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]:
            next_node = (current[0] + dx, current[1] + dy)
            
            # Batas layar (Grid 25x19 untuk resolusi 800x600 dengan tile 32px)
            if not (0 <= next_node[0] < 25 and 0 <= next_node[1] < 19):
                continue
            
            if next_node in obstacles:
                continue
                
            # Biaya gerak: 1 untuk lurus, 1.414 untuk diagonal
            move_cost = 1.414 if dx != 0 and dy != 0 else 1
            new_cost = cost_so_far[current] + move_cost
            
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(next_node, goal)
                heapq.heappush(frontier, (priority, next_node))
                came_from[next_node] = current

    # Rangkai ulang jalur (retrace)
    path = []
    if goal in came_from:
        curr = goal
        while curr != start:
            path.append(curr)
            curr = came_from[curr]
        path.reverse()
    return path

# ==========================================
# 2. KELAS NPC DENGAN FSM DAN PATHFINDING
# ==========================================
class EnemyNPC:
    def __init__(self, x, y, waypoints):
        self.rect = pygame.Rect(x, y, 32, 32)
        # Posisi float agar pergerakan mulus
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.speed = 120 # Piksel per detik
        
        self.state = NPCState.PATROL
        
        self.chase_radius = 250
        self.attack_radius = 45
        self.waypoints = waypoints
        self.current_wp_index = 0
        
        self.path = [] 
        self.path_timer = 0 
        
    def update(self, player_rect, obstacles, dt):
        center_x, center_y = self.rect.center
        p_center_x, p_center_y = player_rect.center
        dist_to_player = math.hypot(p_center_x - center_x, p_center_y - center_y)
        
        # --- LOGIKA TRANSISI FSM ---
        if self.state == NPCState.PATROL:
            if dist_to_player <= self.chase_radius:
                self.state = NPCState.CHASE
                self.path = [] 
                
        elif self.state == NPCState.CHASE:
            if dist_to_player <= self.attack_radius:
                self.state = NPCState.ATTACK
            elif dist_to_player > self.chase_radius:
                self.state = NPCState.PATROL
                self.path = [] 
                
        elif self.state == NPCState.ATTACK:
            if dist_to_player > self.attack_radius:
                self.state = NPCState.CHASE

        # --- EKSEKUSI STATE ---
        self.execute_state(player_rect.center, obstacles, dt)

    def execute_state(self, player_pos, obstacles, dt):
        self.path_timer -= dt
        
        if self.state == NPCState.PATROL:
            target = self.waypoints[self.current_wp_index]
            self.move_towards(target, obstacles, dt)
            
            if math.hypot(target[0] - self.rect.centerx, target[1] - self.rect.centery) < 10:
                self.current_wp_index = (self.current_wp_index + 1) % len(self.waypoints)
                self.path = [] 
                
        elif self.state == NPCState.CHASE:
            if self.path_timer <= 0:
                self.path = [] 
                self.path_timer = 0.5 # Refresh A* tiap 0.5 detik saat ngejar
                
            self.move_towards(player_pos, obstacles, dt)
            
        elif self.state == NPCState.ATTACK:
            self.path = [] # Diam di tempat saat menyerang
            # Logika menyerang bisa ditaruh di sini
            
    def move_towards(self, target_pos, obstacles, dt):
        if len(self.path) == 0:
            start_node = (self.rect.centerx // 32, self.rect.centery // 32)
            target_node = (int(target_pos[0] // 32), int(target_pos[1] // 32))
            self.path = find_path_astar(start_node, target_node, obstacles)

        if self.path and len(self.path) > 0:
            next_node = self.path[0]
            target_x = (next_node[0] * 32) + 16 
            target_y = (next_node[1] * 32) + 16
            
            # --- TRANSLASI MATEMATIKA PERGERAKAN ---
            dx = target_x - self.pos_x
            dy = target_y - self.pos_y
            dist = math.hypot(dx, dy)
            
            if dist > 1.0:
                dir_x = dx / dist
                dir_y = dy / dist
                
                step = min(self.speed * dt, dist)
                self.pos_x += dir_x * step
                self.pos_y += dir_y * step
                
                self.rect.centerx = round(self.pos_x)
                self.rect.centery = round(self.pos_y)
            
            # Pop node jika sudah sangat dekat
            if dist < 5:
                self.path.pop(0)

# ==========================================
# 3. GAME LOOP UTAMA
# ==========================================
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Demo NPC AI - A* & FSM")
    clock = pygame.time.Clock()

    # Setup Objek
    player = pygame.Rect(100, 100, 32, 32)
    player_speed = 200
    
    # Rute Patroli (Titik X, Y Piksel)
    waypoints = [(700, 100), (700, 500), (100, 500)]
    npc = EnemyNPC(400, 100, waypoints)

    # Setup Dinding/Obstacles (Grid Koordinat)
    obstacles = set()
    for i in range(10, 15): obstacles.add((i, 8))   # Dinding tengah horizontal
    for i in range(5, 12): obstacles.add((8, i))    # Dinding tengah vertikal
    for i in range(10, 18): obstacles.add((18, i))  # Dinding kanan vertikal

    running = True
    while running:
        dt = clock.tick(60) / 1000.0 # Delta time dalam detik

        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.top > 0: player.y -= player_speed * dt
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player.bottom < 600: player.y += player_speed * dt
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.left > 0: player.x -= player_speed * dt
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.right < 800: player.x += player_speed * dt

        # 2. Update Logika
        npc.update(player, obstacles, dt)

        # 3. Rendering Visual
        screen.fill((30, 30, 30)) # Latar gelap

        # Gambar Dinding (Obstacles)
        for obs in obstacles:
            pygame.draw.rect(screen, (100, 100, 100), (obs[0]*32, obs[1]*32, 32, 32))

        # Gambar Waypoints (Patroli)
        for wp in waypoints:
            pygame.draw.circle(screen, (255, 255, 255), wp, 5)

        # Gambar Jalur A* NPC (Garis Putih Tipis)
        if len(npc.path) > 0:
            path_pixels = [(npc.rect.centerx, npc.rect.centery)] + [(n[0]*32+16, n[1]*32+16) for n in npc.path]
            pygame.draw.lines(screen, (200, 200, 200), False, path_pixels, 2)

        # Gambar Player (Biru)
        pygame.draw.rect(screen, (0, 150, 255), player)

        # Gambar Area Jangkauan NPC (Visual Debug)
        pygame.draw.circle(screen, (255, 255, 0), npc.rect.center, npc.chase_radius, 1) # Kuning: Chase
        pygame.draw.circle(screen, (255, 0, 0), npc.rect.center, npc.attack_radius, 1)  # Merah: Attack

        # Gambar NPC berdasarkan State-nya
        npc_color = (0, 255, 0) # Hijau = Patrol
        if npc.state == NPCState.CHASE:
            npc_color = (255, 200, 0) # Kuning = Chase
        elif npc.state == NPCState.ATTACK:
            npc_color = (255, 0, 0) # Merah = Attack
            
        pygame.draw.rect(screen, npc_color, npc.rect)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()