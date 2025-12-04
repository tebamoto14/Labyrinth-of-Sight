import pygame
import sys
import math
from settings import *
from maze import generate_maze
from ui import load_fonts, draw_game_ui, draw_transition_screen, draw_minimap

def main():
    # --- Pygameの初期化 ---
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(SCREEN_TITLE)
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    # --- フォントの準備 ---
    fonts = load_fonts()

    # --- ゲーム変数の初期化 ---
    floor = 1
    score = 0
    plus_score = 0
    
    # プレイヤー
    player_x = START_POS_X
    player_y = START_POS_Y
    player_angle = 0

    # マップ生成
    MAP, VISITED_MAP = generate_maze(floor)
    
    # 時間管理
    current_time_limit = BASE_TIME_LIMIT
    start_time = pygame.time.get_ticks()
    
    # ゲーム状態
    game_state = GAME_STATE_TRANSITION

    # --- ゲームループ ---
    running = True
    while running:
        # --- イベント処理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        current_ticks = pygame.time.get_ticks()

        # -------------------------------
        # 1. 階層切り替え中 (TRANSITION)
        # -------------------------------
        if game_state == GAME_STATE_TRANSITION:
            draw_transition_screen(screen, fonts, floor, current_time_limit, score, start_time, plus_score)
            
            if current_ticks - start_time > 3000:
                game_state = GAME_STATE_PLAYING
                start_time = pygame.time.get_ticks()
                
        # -------------------------------
        # 2. プレイ中 (PLAYING)
        # -------------------------------
        elif game_state == GAME_STATE_PLAYING:
            # --- プレイヤーの移動 ---
            mouse_dx, _ = pygame.mouse.get_rel()
            player_angle += mouse_dx * ROTATION_SPEED

            keys = pygame.key.get_pressed()
            current_move_speed = MOVE_SPEED_BASE + (floor * 0.01)
            move_x = 0
            move_y = 0
            
            if keys[pygame.K_w]:
                move_x += math.cos(player_angle) * current_move_speed
                move_y += math.sin(player_angle) * current_move_speed
            if keys[pygame.K_s]:
                move_x -= math.cos(player_angle) * current_move_speed
                move_y -= math.sin(player_angle) * current_move_speed
            if keys[pygame.K_d]:
                move_x -= math.sin(player_angle) * current_move_speed
                move_y += math.cos(player_angle) * current_move_speed
            if keys[pygame.K_a]:
                move_x += math.sin(player_angle) * current_move_speed
                move_y -= math.cos(player_angle) * current_move_speed

            # 当たり判定
            if move_x != 0:
                check_x = int(player_x + move_x + COLLISION_OFFSET) if move_x > 0 else int(player_x + move_x - COLLISION_OFFSET)
                if MAP[int(player_y)][check_x] != 1:
                    player_x += move_x

            if move_y != 0:
                check_y = int(player_y + move_y + COLLISION_OFFSET) if move_y > 0 else int(player_y + move_y - COLLISION_OFFSET)
                if MAP[check_y][int(player_x)] != 1:
                    player_y += move_y
                            
            # --- 時間管理 ---
            elapsed_time = (current_ticks - start_time) / 1000.0
            remaining_time = current_time_limit - elapsed_time
            
            # タイムオーバー処理
            if remaining_time <= 0:
                floor = 1
                score = 0
                plus_score = 0
                MAP, VISITED_MAP = generate_maze(floor)
                current_time_limit = BASE_TIME_LIMIT
                player_x, player_y = START_POS_X, START_POS_Y
                game_state = GAME_STATE_TRANSITION
                start_time = pygame.time.get_ticks()
                
            # 訪問記録
            current_map_x, current_map_y = int(player_x), int(player_y)
            VISITED_MAP[current_map_y][current_map_x] = 1    

            # 階段到達処理
            if MAP[current_map_y][current_map_x] == 2:
                floor_bonus = int(remaining_time * TIME_BONUS_PER_SEC)
                earned_score = CLEAR_BONUS + floor_bonus
                plus_score = earned_score
                score += earned_score
                
                floor += 1
                MAP, VISITED_MAP = generate_maze(floor)
                current_time_limit = BASE_TIME_LIMIT + (floor - 1) * TIME_PER_FLOOR
                
                player_x, player_y = START_POS_X, START_POS_Y
                player_angle = 0
                
                game_state = GAME_STATE_TRANSITION
                start_time = pygame.time.get_ticks()

            # --- 描画処理 ---
            pygame.draw.rect(screen, (50, 50, 50), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT / 2))
            pygame.draw.rect(screen, (100, 100, 100), (0, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT / 2))

            # レイキャスティング
            for ray in range(NUM_RAYS):
                ray_angle = (player_angle - FOV / 2) + (ray / NUM_RAYS) * FOV
                distance_to_wall = 0
                step = 0.02
                ray_x, ray_y = player_x, player_y
                is_stair = False

                while True:
                    ray_x += math.cos(ray_angle) * step
                    ray_y += math.sin(ray_angle) * step
                    map_x, map_y = int(ray_x), int(ray_y)

                    if not (0 <= map_y < len(MAP) and 0 <= map_x < len(MAP[0])):
                        distance_to_wall = float('inf')
                        break

                    if MAP[map_y][map_x] != 0: 
                        distance_to_wall = math.sqrt((ray_x - player_x)**2 + (ray_y - player_y)**2)
                        is_stair = (MAP[map_y][map_x] == 2)
                        break
                
                distance_to_wall *= math.cos(player_angle - ray_angle)
                wall_height = SCREEN_HEIGHT / distance_to_wall if distance_to_wall > 0 else SCREEN_HEIGHT
                wall_top = (SCREEN_HEIGHT / 2) - (wall_height / 2)

                intensity = 255 / (1 + distance_to_wall * 0.3)

                if is_stair:
                    wall_color = (intensity * 0.2, intensity * 0.8, intensity * 0.2)
                else:
                    MAX_BRIGHTNESS = 144
                    intensity = MAX_BRIGHTNESS / (1 + distance_to_wall * 0.3)
                    wall_color = (
                        max(0, min(255, int(intensity * 0.77))), 
                        max(0, min(255, int(intensity * 0.88))), 
                        max(0, min(255, int(intensity * 1.0)))
                    )    
                    
                pygame.draw.line(screen, wall_color, (ray, wall_top), (ray, wall_top + wall_height), 1)
                
            draw_minimap(screen, player_x, player_y, player_angle, MAP, VISITED_MAP)
            draw_game_ui(screen, fonts, floor, remaining_time, score)
            
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()