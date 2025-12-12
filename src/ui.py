import pygame
import os
import math
from settings import * # settings.pyの定数を使う

# --- フォントのロード ---
def load_fonts():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # assets/fonts/ がある前提のパス指定。環境に合わせて調整してください
        font_path = os.path.join(base_dir, "..","assets","fonts","PressStart2P-Regular.ttf")       
        return {
            "floor": pygame.font.Font(font_path, 20),
            "score": pygame.font.Font(font_path, 20),
            "time":  pygame.font.Font(font_path, 40),
            "transition": pygame.font.Font(font_path, 50)
        }
    except Exception as e:
        print(f"フォントのロードに失敗 (デフォルトフォントを使用): {e}")
        return {
            "floor": pygame.font.Font(None, 20),
            "score": pygame.font.Font(None, 26),
            "time":  pygame.font.Font(None, 40),
            "transition": pygame.font.Font(None, 50)
        }

# --- 影付き文字描画ヘルパー ---
def draw_text_shadow(screen, text, font, color, x, y, align="left"):
    shadow_surf = font.render(text, True, COLOR_SHADOW)
    main_surf = font.render(text, True, color)
    shadow_rect = shadow_surf.get_rect()
    main_rect = main_surf.get_rect()
    
    offset = 4 if align in ["center", "right"] else 3

    if align == "center":
        main_rect.center = (x, y)
        shadow_rect.center = (x + offset, y + offset)
    elif align == "right":
        main_rect.topright = (x, y)
        shadow_rect.topright = (x + offset, y + offset)
    else: # left
        main_rect.topleft = (x, y)
        shadow_rect.topleft = (x + offset, y + offset)

    screen.blit(shadow_surf, shadow_rect)
    screen.blit(main_surf, main_rect)

# --- ゲームUI描画 ---
def draw_game_ui(screen, fonts, floor, remaining_time, score):
    # 1. 左上: FLOOR
    draw_text_shadow(screen, f"FLOOR {floor}", fonts["floor"], COLOR_CYAN, 30, 30, align="left")

    # 2. 中央: TIME
    time_color = COLOR_RED if remaining_time <= 10 else COLOR_WHITE
    draw_text_shadow(screen, f"{int(remaining_time)}", fonts["time"], time_color, SCREEN_WIDTH // 2, 40, align="center")

    # 3. 右上: SCORE
    draw_text_shadow(screen, f"SCORE:{score:06}", fonts["score"], COLOR_GOLD, SCREEN_WIDTH - 20, 30, align="right")

# --- トランジション画面描画 ---
def draw_transition_screen(screen, fonts, floor, time_limit, score, start_ticks, last_plus_score):
    screen.fill(COLOR_BG)

    # スキャンライン
    scanline_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for y in range(0, SCREEN_HEIGHT, 2):
        pygame.draw.line(scanline_surface, COLOR_SCANLINE, (0, y), (SCREEN_WIDTH, y), 1)
    screen.blit(scanline_surface, (0, 0))

    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    # 各要素描画
    draw_text_shadow(screen, f"SCORE:{score:06}", fonts["score"], COLOR_GOLD, SCREEN_WIDTH - 20, 20, align="right")
    draw_text_shadow(screen, f"FLOOR {floor}", fonts["transition"], COLOR_CYAN, center_x, center_y - 60, align="center")
    
    if last_plus_score > 0:
        draw_text_shadow(screen, f"BONUS +{last_plus_score}", fonts["score"], COLOR_GREEN, center_x, center_y - 130, align="center")
    
    draw_text_shadow(screen, f"TIME LIMIT: {int(time_limit)}s", fonts["time"], COLOR_WHITE, center_x, center_y + 20, align="center")

    # 点滅メッセージ
    current_ticks = pygame.time.get_ticks()
    if (current_ticks // 500) % 2 == 0:
        draw_text_shadow(screen, "GET READY!", fonts["time"], COLOR_RED, center_x, SCREEN_HEIGHT - 80, align="center")

# --- ゲームオーバー画面描画 ---
def draw_gameover_screen(screen, fonts, score, floor):
    screen.fill((30, 0 ,0))

    # スキャンライン
    scanline_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for y in range(0, SCREEN_HEIGHT, 2):
        pygame.draw.line(scanline_surface, COLOR_SCANLINE, (0, y), (SCREEN_WIDTH, y), 1)
    screen.blit(scanline_surface, (0, 0))

    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    # 各要素描画
    draw_text_shadow(screen, "GAME OVER", fonts["transition"], COLOR_RED, center_x, center_y - 80, align="center")
    
    draw_text_shadow(screen, f"FINAL SCORE: {score:06}", fonts["score"], COLOR_GOLD, center_x, center_y + 10, align="center")
    draw_text_shadow(screen, f"REACHED FLOOR: {floor}", fonts["floor"], COLOR_CYAN, center_x, center_y + 50, align="center")

    # 点滅メッセージ
    current_ticks = pygame.time.get_ticks()
    if (current_ticks // 500) % 2 == 0:
        draw_text_shadow(screen, "PRESS SPACE TO RETRY", fonts["floor"], COLOR_WHITE, center_x, SCREEN_HEIGHT - 100, align="center")

# --- ミニマップ描画 ---
def draw_minimap(screen, px, py, p_angle, game_map, visited_map, items):
    CELL_SIZE = 7
    map_pixel_height = len(game_map) * CELL_SIZE
    
    MAP_POS_X = 10
    MAP_POS_Y = SCREEN_HEIGHT - map_pixel_height - 10

    map_height = len(game_map)
    map_width = len(game_map[0])

    for y in range(map_height):
        for x in range(map_width):
            if visited_map[y][x] == 1:
                tile_type = game_map[y][x]
                rect = (MAP_POS_X + x * CELL_SIZE, MAP_POS_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                color = None
                if tile_type == 0: color = COLOR_FLOOR
                elif tile_type == 1: color = COLOR_WALL
                elif tile_type == 2: color = COLOR_STAIRS
                
                if color:
                    pygame.draw.rect(screen, color, rect)
    
    # アイテムの描画
    for item in items:
        ix, iy = int(item["x"]), int(item["y"])
        
        if visited_map[iy][ix] == 1:
            item_map_x = MAP_POS_X + ix * CELL_SIZE  + CELL_SIZE // 2
            item_map_y = MAP_POS_Y + iy * CELL_SIZE  + CELL_SIZE // 2
            
            # アイテムの色
            if item["type"] in ITEM_MAP:
                item_color = COLOR_ITEM_MAP
            elif item["type"] in [ITEM_SPEED_DOWN]:
                item_color = COLOR_ITEM_BAD
            else:
                item_color = COLOR_ITEM_GOOD

            pygame.draw.circle(screen, item_color, (item_map_x, item_map_y), CELL_SIZE // 2 - 1)
        
    player_map_x = MAP_POS_X + px * CELL_SIZE
    player_map_y = MAP_POS_Y + py * CELL_SIZE
    pygame.draw.circle(screen, COLOR_PLAYER, (player_map_x, player_map_y), CELL_SIZE // 2)

    dir_end_x = player_map_x + math.cos(p_angle) * (CELL_SIZE * 1) 
    dir_end_y = player_map_y + math.sin(p_angle) * (CELL_SIZE * 1)
    pygame.draw.line(screen, COLOR_PLAYER, (player_map_x, player_map_y), (dir_end_x, dir_end_y), 2)