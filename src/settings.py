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
BASE_TIME_LIMIT = 20   # 1階層の基本制限時間 (秒)
TIME_PER_FLOOR = 5    # 1階層上がるごとに追加される時間
CLEAR_BONUS = 500      # 階層クリアボーナス
TIME_BONUS_PER_SEC = 10 # 残り時間1秒あたりのタイムボーナス

# --- ゲーム状態 ---
GAME_STATE_TRANSITION = "transition"
GAME_STATE_PLAYING = "playing"
GAME_STSAE_GAMEOVER = "gameover"

# --- 色の定義 (よく使う色) ---
COLOR_WHITE = (255, 255, 255) # 白
COLOR_BLACK = (0, 0, 0)  # 黒
COLOR_RED   = (255, 50, 50) # 赤
COLOR_GREEN = (50, 255, 50) # 緑
COLOR_BLUE  = (0, 0, 255) # 青
COLOR_CYAN  = (0, 255, 255) # シアン
COLOR_GOLD  = (255, 215, 0) # 金色
COLOR_SHADOW= (0, 0, 0) # 影の色 黒
COLOR_FLOOR = (80, 80, 80) # 床の色 灰
COLOR_WALL  = (200, 200, 200) # 壁の色 明るい灰
COLOR_STAIRS= (0, 255, 0) # 階段の色 緑
COLOR_PLAYER= (255, 0, 0) # プレイヤーの色 赤
COLOR_BG    = (40, 40, 50) # 背景色 濃い灰青
COLOR_SCANLINE = (0, 0, 0, 50) # スキャンラインの色 (半透明黒)

# --- アイテム設定 ---
ITEM_HOURGLASS = "hourglass" # 時間延長アイテム
ITEM_MAP = "map"           # マップ表示アイテム
ITEM_WARP_START = "warp_start" # スタート地点ワープアイテム
ITEM_WARP_RANDOM = "warp_random" # ランダムワープアイテム
ITEM_SPEED_UP    = "speed_up"    # スピードアップ
ITEM_SPEED_DOWN  = "speed_down"  # スピードダウン (罠)

# アイテムの色 (ミニマップ用)
# "謎の光"っぽい、淡いシアン色
COLOR_ITEM_MYSTERY = (200, 240, 255) 
# メッセージ表示用の色
COLOR_MESSAGE_BG = (0, 0, 0, 180) # 半透明の黒