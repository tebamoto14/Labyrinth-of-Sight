import random

# --- 迷路自動生成関数 (棒倒し法) ---
def generate_maze(floor):
    """
    階層(floor)に基づいて、新しい迷路マップを自動生成する関数
    """
    # 階層が上がるごとに迷路が大きくなる (必ず奇数にする)
    width = 3 + (floor * 2)
    height = 5 + (floor * 2) 

    # すべて壁(1)でマップを初期化
    new_map = [[1 for _ in range(width)] for _ in range(height)]
    new_visited_map = [[0 for _ in range(width)] for _ in range(height)]

    # 奇数行・奇数列のマスを床(0)にする (通路の土台)
    for y in range(1, height - 1, 2):
        for x in range(1, width - 1, 2):
            new_map[y][x] = 0

    # 棒倒し処理 (壁を壊して道を作る)
    for y in range(1, height - 1, 2):
        for x in range(1, width - 1, 2):
            # (1,1)マスはスタート地点なので、壁は倒さない
            if x == 1 and y == 1:
                continue
            
            # 倒す方向を決める
            if y == 1:
                direction = 'left' # 一番上の行は「左」にしか倒せない
            elif x == 1:
                direction = 'up' # 一番左の列は「上」にしか倒せない
            else:
                direction = random.choice(['up', 'left']) # それ以外は「上」か「左」

            # 壁を倒す (0にする)
            if direction == 'up':
                new_map[y - 1][x] = 0
            elif direction == 'left':
                new_map[y][x - 1] = 0
    
    # 階段(2)を設置する
    possible_stairs = []
    for y in range(1, height-1, 2):
        for x in range(1, width-1, 2):
            if x == 1 and y == 1: # andに修正
                continue     
            if x > width // 2 or y > height // 2:
                possible_stairs.append((x, y))    
                            
    if not possible_stairs:
        stair_x = width - 2
        stair_y = height - 2
    else:
        stair_x, stair_y = random.choice(possible_stairs)
                
    new_map[stair_y][stair_x] = 2

    print(f"--- Floor {floor} generated! Size: {width}x{height} ---")
    # print(new_map) # デバッグ用: マップの中身が見たければコメントアウトを外す
    return new_map, new_visited_map