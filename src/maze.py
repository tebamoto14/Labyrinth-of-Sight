import random
from settings import *

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
        stair_x = 2
        stair_y = 2
    else:
        stair_x, stair_y = random.choice(possible_stairs)
                
    new_map[stair_y][stair_x] = 2

    print(f"--- Floor {floor} generated! Size: {width}x{height} ---")
    print(f"Stairs at: ({stair_x}, {stair_y})")      
                
    # アイテムの設置
    items = []
    
    # 設置可能な床のリスト
    possible_item_spots = []
    for y in range(1, height-1):
        for x in range(1, width-1):
            if new_map[y][x] == 0 and not (x == 1 and y == 1):
                possible_item_spots.append((x, y))
                
    random.shuffle(possible_item_spots)
    
    # アイテムを置く数
    num_items = floor // 3 + 3

    # アイテムの種類の重みづけ
    item_types = [
        ITEM_HOURGLASS,
        ITEM_MAP,
        ITEM_WARP_START,
        ITEM_WARP_RANDOM,
        ITEM_SPEED_UP,
        ITEM_SPEED_DOWN
    ]
    # それぞれの確率
    weights = [20, 10, 15, 15, 20, 20]
    
    # 配置できる場所がある限り配置
    # sampleではなく、シャッフルしたリストの前から順番にとっていく方式に変更
    count = 0
    for x, y in possible_item_spots:
        if count >= num_items:
            break
            
        # 階段予定地には置かないように簡易ガード
        if x > stair_x +- 2 and y > stair_y +- 2:
            continue

        itype = random.choices(item_types, weights=weights, k=1)[0]
        
        items.append({
            "type": itype,
            "x": x + 0.5, # ★重要: +0.5 で必ずマスの「ど真ん中」に置く
            "y": y + 0.5
        })
        print(f"Item placed: {itype} at ({x}, {y})")
        count += 1
         
    return new_map, new_visited_map, items