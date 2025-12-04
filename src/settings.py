import math

# --- 画面設定 ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "My Maze Game"

# --- 描画設定 ---
FOV = math.pi / 3  # 視野角 (60度)
NUM_RAYS = SCREEN_WIDTH # 飛ばす光線の数

# --- プレイヤー設定 ---
START_POS_X = 1.5
START_POS_Y = 1.5
MOVE_SPEED_BASE = 0.06
ROTATION_SPEED = 0.0008
COLLISION_OFFSET = 0.2

# --- ゲームバランス設定 ---
BASE_TIME_LIMIT = 30   # 1階層の基本制限時間 (秒)
TIME_PER_FLOOR = 15    # 1階層上がるごとに追加される時間
CLEAR_BONUS = 500      # 階層クリアボーナス
TIME_BONUS_PER_SEC = 10 # 残り時間1秒あたりのタイムボーナス

# --- ゲーム状態 ---
GAME_STATE_TRANSITION = "transition"
GAME_STATE_PLAYING = "playing"

# --- 色の定義 (よく使う色) ---
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED   = (255, 50, 50)
COLOR_GREEN = (50, 255, 50)
COLOR_BLUE  = (0, 0, 255)
COLOR_CYAN  = (0, 255, 255)
COLOR_GOLD  = (255, 215, 0)
COLOR_SHADOW= (0, 0, 0)
COLOR_FLOOR = (80, 80, 80)
COLOR_WALL  = (200, 200, 200)
COLOR_STAIRS= (0, 255, 0)
COLOR_PLAYER= (255, 0, 0)
COLOR_BG    = (40, 40, 50)
COLOR_SCANLINE = (0, 0, 0, 50)