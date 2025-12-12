import pygame
import sys
import math
import random
from settings import *
from maze import generate_maze
from ui import load_fonts, draw_game_ui, draw_transition_screen, draw_gameover_screen, draw_minimap

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
    MAP, VISITED_MAP, items = generate_maze(floor)
    
    # ステータス変化用の変数
    speed_multiplier = 1.0
    speed_effect_end_time = 0
    reveal_map = False
    
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
            
            if current_ticks < speed_effect_end_time:
                speed_multiplier = 1.0
                
            current_move_speed = (MOVE_SPEED_BASE + (floor * 0.01)) * speed_multiplier
            
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
            
            for item in items[:]:
                # プレイヤーとの距離を計算
                dist = math.sqrt((player_x - item["x"])**2 + (player_y - item["y"])**2)
                
                if dist < 0.5: # 半径0.5マス以内なら取得
                    itype = item["type"]
                    print(f"Got item: {itype}") # デバッグ表示
                    
                    # --- 効果発動 ---
                    if itype == ITEM_HOURGLASS:
                        current_time_limit += 15 # 15秒延長
                        
                    elif itype == ITEM_MAP:
                        # 全ての visited_map を 1 にする
                        for y in range(len(VISITED_MAP)):
                            for x in range(len(VISITED_MAP[0])):
                                VISITED_MAP[y][x] = 1
                                
                    elif itype == ITEM_WARP_START:
                        player_x = START_POS_X
                        player_y = START_POS_Y
                        
                    elif itype == ITEM_WARP_RANDOM:
                        # 床マスのリストを取得してランダムワープ
                        # (簡易的に実装。壁の中に出ないように注意)
                        while True:
                            rx = random.randint(1, len(MAP[0])-2)
                            ry = random.randint(1, len(MAP)-2)
                            if MAP[ry][rx] == 0:
                                player_x = rx + 0.5
                                player_y = ry + 0.5
                                break
                                
                    elif itype == ITEM_SPEED_UP:
                        speed_multiplier = 2.0 # 2倍速
                        speed_effect_end_time = current_ticks + 5000 # 5秒間
                        
                    elif itype == ITEM_SPEED_DOWN:
                        speed_multiplier = 0.5 # 半分
                        speed_effect_end_time = current_ticks + 5000 # 5秒間

                    # 取得したらリストから消す
                    items.remove(item)
                
            # --- 時間管理 ---
            elapsed_time = (current_ticks - start_time) / 1000.0
            remaining_time = current_time_limit - elapsed_time
            
            # タイムオーバー処理
            if remaining_time <= 0:
                game_state = GAME_STSAE_GAMEOVER
                
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
                MAP, VISITED_MAP, items= generate_maze(floor)
                current_time_limit = BASE_TIME_LIMIT + (floor - 1) * TIME_PER_FLOOR
                
                player_x, player_y = START_POS_X, START_POS_Y
                player_angle = 0
                
                game_state = GAME_STATE_TRANSITION
                start_time = pygame.time.get_ticks()

            # --- 描画処理 ---
            pygame.draw.rect(screen, (50, 50, 50), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT / 2))
            pygame.draw.rect(screen, (100, 100, 100), (0, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT / 2))

            # zバッファ
            z_buffer = [0] * NUM_RAYS
            
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
                
                z_buffer[ray] = distance_to_wall
                
                # 壁描画用の補正
                corrected_dist = distance_to_wall * math.cos(player_angle - ray_angle)
                
                wall_height = SCREEN_HEIGHT / corrected_dist if corrected_dist > 0 else SCREEN_HEIGHT
                wall_top = (SCREEN_HEIGHT / 2) - (wall_height / 2)

                intensity = 255 / (1 + corrected_dist * 0.3)

                if is_stair:
                    wall_color = (intensity * 0.2, intensity * 0.8, intensity * 0.2)
                else:
                    MAX_BRIGHTNESS = 144
                    intensity = MAX_BRIGHTNESS / (1 + corrected_dist * 0.3)
                    wall_color = (
                        max(0, min(255, int(intensity * 0.77))), 
                        max(0, min(255, int(intensity * 0.88))), 
                        max(0, min(255, int(intensity * 1.0)))
                    )    
                    
                pygame.draw.line(screen, wall_color, (ray, wall_top), (ray, wall_top + wall_height), 1)
                
            # 2. スプライト描画 (アイテム)
            # プレイヤーから遠い順に並べ替え (Painter's Algorithm)
            sprite_list = []
            for item in items:
                dist = math.sqrt((player_x - item["x"])**2 + (player_y - item["y"])**2)
                sprite_list.append((dist, item))
            sprite_list.sort(key=lambda x: x[0], reverse=True)

            # アイテムごとの色定義
            ITEM_COLORS = {
                ITEM_HOURGLASS: (255, 215, 0),   # 金
                ITEM_MAP:       (0, 255, 255),   # 水色
                ITEM_WARP_START:(128, 0, 128),   # 紫
                ITEM_WARP_RANDOM:(255, 0, 255),  # ピンク
                ITEM_SPEED_UP:  (0, 255, 0),     # 緑
                ITEM_SPEED_DOWN:(50, 50, 50),    # グレー
            }

            for dist, item in sprite_list:
                # アイテムの相対位置
                sprite_x = item["x"] - player_x
                sprite_y = item["y"] - player_y
                
                plane_len = math.tan(FOV / 2)
                # カメラ平面の逆変換 (ビルボード計算)
                # FOV=60度の場合、Projection Planeは約0.66
                # プレイヤーの向きベクトル (dirX, dirY)
                dir_x = math.cos(player_angle)
                dir_y = math.sin(player_angle)
                # カメラ平面ベクトル (planeX, planeY) - 垂直なベクトル
                plane_x = -dir_y * plane_len # 0.66 ≒ tan(FOV/2)
                plane_y = dir_x * plane_len

                # 行列式計算
                det = plane_x * dir_y - dir_x * plane_y
                if det == 0: continue # ゼロ除算回避
                
                inv_det = 1.0 / det   
                
                # カメラ空間での座標変換
                transform_x = inv_det * (dir_y * sprite_x - dir_x * sprite_y)
                transform_y = inv_det * (-plane_y * sprite_x + plane_x * sprite_y) # これが奥行き(深度)

                if transform_y > 0.1: # プレイヤーの前にある場合のみ描画
                    # 画面上のX座標中心
                    sprite_screen_x = int((SCREEN_WIDTH / 2) * (1 + transform_x / transform_y))
                    
                    # 画面上の高さ・幅計算
                    sprite_height = abs(int(SCREEN_HEIGHT / transform_y))
                    sprite_width = sprite_height # 正方形とする

                    # パフォーマンスのため、画面内にあるかチェック
                    if -sprite_width < sprite_screen_x < SCREEN_WIDTH + sprite_width:
                        color = ITEM_COLORS.get(item["type"], (255, 255, 255))
                        circle_center = (sprite_screen_x, SCREEN_HEIGHT // 2)
                        circle_radius = sprite_height // 4 # 少し小さく調整
                        
                        # 本来は1ラインずつZバッファ判定すべきだが、簡易的に「中心点のZバッファ」で判定する
                        # (アイテムの中心が壁の手前なら描画)
                        check_ray = max(0, min(NUM_RAYS - 1, sprite_screen_x))
                        
                        if transform_y < z_buffer[check_ray]:
                            # 単純な円を描画
                            pygame.draw.circle(screen, color, circle_center, circle_radius)
                            # 枠線
                            pygame.draw.circle(screen, (0,0,0), circle_center, circle_radius, 2)
                               
            draw_minimap(screen, player_x, player_y, player_angle, MAP, VISITED_MAP, items)
            draw_game_ui(screen, fonts, floor, remaining_time, score)
            
        # -------------------------------
        # 3. ゲームオーバー (GAMEOVER)  
        # -------------------------------
        elif game_state == GAME_STSAE_GAMEOVER:
            draw_gameover_screen(screen, fonts, score, floor)
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                # ゲームリセット
                floor = 1
                score = 0
                plus_score = 0
                MAP, VISITED_MAP, items = generate_maze(floor)
                current_time_limit = BASE_TIME_LIMIT
                player_x = START_POS_X
                player_y = START_POS_Y
                player_angle = 0
                start_time = pygame.time.get_ticks()
                game_state = GAME_STATE_TRANSITION    
        
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()