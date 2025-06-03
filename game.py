import pygame
import sys
import math
import random
import os

# Pygameの初期化
pygame.init()

# 画面サイズの設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gravity Dance")

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GOLD = (255, 215, 0)

# 星（重力源）の設定
star_radius = 30  # 星の半径を小さくする
GRAVITY_CONSTANT = 0.5  # 重力定数

# 惑星テクスチャの生成
def create_planet_texture(radius, base_color, detail_level=3):
    """リアルな惑星テクスチャを生成する関数"""
    # 直径の2倍のサイズでサーフェスを作成（余白を持たせる）
    size = int(radius * 2.2)
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # ベースの円を描画
    center = (size // 2, size // 2)
    pygame.draw.circle(surface, base_color, center, radius)
    
    # 惑星タイプに基づいて詳細を追加
    r, g, b = base_color
    
    # 地形の詳細を追加
    for _ in range(detail_level * 10):
        # ランダムな位置に地形の特徴を追加
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, radius * 0.9)
        x = center[0] + distance * math.cos(angle)
        y = center[1] + distance * math.sin(angle)
        
        # 特徴のサイズと色
        feature_size = random.randint(3, int(radius * 0.3))
        
        # 色のバリエーション
        color_variation = random.uniform(-30, 30)
        feature_color = (
            max(0, min(255, r + color_variation)),
            max(0, min(255, g + color_variation)),
            max(0, min(255, b + color_variation))
        )
        
        # 特徴を描画
        pygame.draw.circle(surface, feature_color, (int(x), int(y)), feature_size)
    
    # 惑星タイプに応じた特殊効果
    if base_color == RED or base_color == ORANGE:  # 火星や金星のような惑星
        # 火山や溶岩の流れを追加
        for _ in range(5):
            start_angle = random.uniform(0, 2 * math.pi)
            start_dist = random.uniform(radius * 0.5, radius * 0.9)
            start_x = center[0] + start_dist * math.cos(start_angle)
            start_y = center[1] + start_dist * math.sin(start_angle)
            
            for i in range(10):
                x = start_x + random.uniform(-radius * 0.1, radius * 0.1)
                y = start_y + random.uniform(-radius * 0.1, radius * 0.1)
                size = random.randint(2, 5)
                pygame.draw.circle(surface, YELLOW, (int(x), int(y)), size)
    
    elif base_color == BLUE:  # 地球のような惑星
        # 雲を追加
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(radius * 0.7, radius * 0.95)
            x = center[0] + distance * math.cos(angle)
            y = center[1] + distance * math.sin(angle)
            cloud_size = random.randint(5, 10)
            pygame.draw.circle(surface, WHITE, (int(x), int(y)), cloud_size)
    
    elif base_color == PURPLE or base_color == MAGENTA:  # ガス惑星
        # 縞模様を追加
        for i in range(5):
            stripe_y = center[1] - radius + (2 * radius / 6) * i
            stripe_height = radius / 4
            stripe_rect = pygame.Rect(center[0] - radius, stripe_y, radius * 2, stripe_height)
            
            # 縞の色
            stripe_color = (
                max(0, min(255, r + random.uniform(-50, 50))),
                max(0, min(255, g + random.uniform(-50, 50))),
                max(0, min(255, b + random.uniform(-50, 50)))
            )
            
            pygame.draw.ellipse(surface, stripe_color, stripe_rect)
    
    # 惑星の輪を追加（土星のような）
    if random.random() < 0.3:  # 30%の確率で輪を追加
        ring_color = (180, 180, 180, 150)  # 半透明の輪
        ring_width = radius * 0.2
        
        # 楕円形の輪を描画
        ring_rect = pygame.Rect(
            center[0] - radius * 1.5,
            center[1] - ring_width / 2,
            radius * 3,
            ring_width
        )
        pygame.draw.ellipse(surface, ring_color, ring_rect, 1)
        
        # 輪の詳細を追加
        for _ in range(20):
            ring_radius = random.uniform(radius * 1.1, radius * 1.5)
            ring_angle = random.uniform(0, 2 * math.pi)
            ring_x = center[0] + ring_radius * math.cos(ring_angle)
            ring_y = center[1] + ring_width * 0.5 * math.sin(ring_angle)
            pygame.draw.circle(surface, ring_color, (int(ring_x), int(ring_y)), 1)
    
    # 惑星の縁に光沢を追加
    for i in range(10):
        highlight_radius = radius - i
        highlight_width = 1
        highlight_color = (255, 255, 255, 10)  # 非常に透明な白
        pygame.draw.circle(surface, highlight_color, center, highlight_radius, highlight_width)
    
    return surface

# 星のリスト（位置、半径、色、テクスチャ）
stars = []

# 初期の星を追加
initial_star = {
    'pos': [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2],
    'radius': star_radius,
    'color': RED,
    'texture': None  # テクスチャは後で生成
}
initial_star['texture'] = create_planet_texture(initial_star['radius'], initial_star['color'])
stars.append(initial_star)

# 新しい星を追加する関数
def add_new_star():
    # ランダムな位置（画面の端から少し離れた場所）
    margin = 100
    
    # 宇宙船からの安全距離
    safe_distance_from_ship = 150
    
    # 有効な位置を見つけるまで繰り返す
    valid_position = False
    max_attempts = 100
    attempts = 0
    
    x, y = 0, 0
    
    while not valid_position and attempts < max_attempts:
        # ランダムな位置を生成
        x = random.randint(margin, SCREEN_WIDTH - margin)
        y = random.randint(margin, SCREEN_HEIGHT - margin)
        
        valid_position = True
        
        # 宇宙船との距離をチェック
        ship_distance = math.sqrt((x - spaceship_pos[0])**2 + (y - spaceship_pos[1])**2)
        if ship_distance < safe_distance_from_ship:
            valid_position = False
            attempts += 1
            continue
        
        # 既存の星との距離をチェック
        for star in stars:
            distance = math.sqrt((x - star['pos'][0])**2 + (y - star['pos'][1])**2)
            if distance < star['radius'] * 3:  # 星同士が近すぎる場合
                valid_position = False
                attempts += 1
                break
    
    # 最大試行回数を超えた場合は、画面の反対側に配置
    if attempts >= max_attempts:
        # 宇宙船の反対側の位置を計算
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        opposite_vector = [center_x - spaceship_pos[0], center_y - spaceship_pos[1]]
        
        # ベクトルの長さを計算
        vector_length = math.sqrt(opposite_vector[0]**2 + opposite_vector[1]**2)
        
        # 単位ベクトル化
        if vector_length > 0:
            unit_vector = [opposite_vector[0] / vector_length, opposite_vector[1] / vector_length]
        else:
            unit_vector = [1, 0]  # デフォルト方向
        
        # 宇宙船から安全距離離れた位置
        x = spaceship_pos[0] + unit_vector[0] * safe_distance_from_ship * 1.5
        y = spaceship_pos[1] + unit_vector[1] * safe_distance_from_ship * 1.5
        
        # 画面内に収める
        x = max(margin, min(SCREEN_WIDTH - margin, x))
        y = max(margin, min(SCREEN_HEIGHT - margin, y))
        
        print(f"最大試行回数を超えました。宇宙船の反対側に星を配置: ({x}, {y})")
    
    # 色をランダムに選択
    colors = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN, MAGENTA]
    color = random.choice(colors)
    
    # 半径をランダムに設定（20〜40の間）
    radius = random.randint(20, 40)
    
    # テクスチャを生成
    texture = create_planet_texture(radius, color, detail_level=random.randint(2, 5))
    
    # 新しい星を追加
    new_star = {
        'pos': [x, y],
        'radius': radius,
        'color': color,
        'texture': texture,
        'rotation': 0,
        'rotation_speed': random.uniform(-0.5, 0.5),  # 回転速度を追加
        'creation_time': pygame.time.get_ticks(),  # 作成時間を記録
        'collision_count': 0  # 衝突回数を初期化
    }
    stars.append(new_star)
    
    # 星が追加されたことを視覚的に示す
    passage_effects.append({
        'start_time': pygame.time.get_ticks(),
        'duration': 1000,  # 1秒間
        'position': [x, y],
        'particles': []
    })
    # パーティクルを生成
    for _ in range(20):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 5)
        size = random.randint(2, 6)
        color = random.choice([WHITE, YELLOW, CYAN])
        passage_effects[-1]['particles'].append({
            'pos': [x, y],
            'velocity': [speed * math.cos(angle), speed * math.sin(angle)],
            'size': size,
            'color': color,
            'life': random.uniform(0.5, 1.0)  # ライフタイム係数
        })

# 宇宙船の設定
spaceship_pos = [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2]
spaceship_velocity = [0, 1]  # 初速度
spaceship_acceleration = [0, 0]
spaceship_size = 15
thrust_power = 0.1
rotation_speed = 3
spaceship_angle = 0  # 宇宙船の向き（度数法）

# パーティクルシステム
particles = []  # 宇宙船の動きに応じたパーティクル
wave_effects = []  # 波紋エフェクト
ship_transform_effect = None  # 宇宙船の変形エフェクト

# ゲームの状態
game_over = False
score = 0
font = pygame.font.SysFont(None, 36)

# デバッグモード
debug_mode = False
invincible = False

# スコア関連
score_rate = 10  # 1秒あたり10点
last_score_update = pygame.time.get_ticks()
score_update_interval = 100  # 0.1秒ごとに更新（滑らかに見せるため）

# 星間通過の履歴を保存する変数
last_passage_stars = None

# ボーナススコア関連
score_multiplier = 1
bonus_active = False
bonus_duration = 3 * 1000  # ボーナス持続時間（3秒）
bonus_end_time = 0
last_position = spaceship_pos.copy()
bonus_cooldown = 1000  # ボーナス獲得のクールダウン（1秒）
last_bonus_time = 0

# 星間通過エフェクト
passage_effects = []

# タイマー設定
star_add_interval = 20 * 1000  # 20秒（ミリ秒）
last_star_add_time = pygame.time.get_ticks()

# 背景の星を生成
def create_starfield(num_stars):
    stars = []
    for _ in range(num_stars):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        size = random.randint(1, 3)
        brightness = random.randint(100, 255)
        color = (brightness, brightness, brightness)
        stars.append((x, y, size, color))
    return stars

# 背景の星を生成
background_stars = create_starfield(100)

# 宇宙船の描画関数
def draw_spaceship(pos, angle):
    # 基本形状（流線型の三角形）- より明確な前方向
    main_points = [
        (pos[0] + spaceship_size * 1.5 * math.cos(math.radians(angle)), 
         pos[1] - spaceship_size * 1.5 * math.sin(math.radians(angle))),  # 前方をより尖らせる
        (pos[0] + spaceship_size * 0.8 * math.cos(math.radians(angle + 145)), 
         pos[1] - spaceship_size * 0.8 * math.sin(math.radians(angle + 145))),
        (pos[0] + spaceship_size * 0.8 * math.cos(math.radians(angle + 215)), 
         pos[1] - spaceship_size * 0.8 * math.sin(math.radians(angle + 215)))
    ]
    
    # 後方の翼（より後ろに配置）
    wing_points1 = [
        main_points[1],  # 左後方から
        (pos[0] + spaceship_size * 1.2 * math.cos(math.radians(angle + 160)), 
         pos[1] - spaceship_size * 1.2 * math.sin(math.radians(angle + 160))),
        (pos[0] + spaceship_size * 0.5 * math.cos(math.radians(angle + 180)), 
         pos[1] - spaceship_size * 0.5 * math.sin(math.radians(angle + 180)))
    ]
    
    wing_points2 = [
        main_points[2],  # 右後方から
        (pos[0] + spaceship_size * 1.2 * math.cos(math.radians(angle + 200)), 
         pos[1] - spaceship_size * 1.2 * math.sin(math.radians(angle + 200))),
        (pos[0] + spaceship_size * 0.5 * math.cos(math.radians(angle + 180)), 
         pos[1] - spaceship_size * 0.5 * math.sin(math.radians(angle + 180)))
    ]
    
    # 前方を示すコックピット部分
    cockpit_points = [
        (pos[0] + spaceship_size * 0.8 * math.cos(math.radians(angle)), 
         pos[1] - spaceship_size * 0.8 * math.sin(math.radians(angle))),
        (pos[0] + spaceship_size * 0.4 * math.cos(math.radians(angle + 30)), 
         pos[1] - spaceship_size * 0.4 * math.sin(math.radians(angle + 30))),
        (pos[0] + spaceship_size * 0.4 * math.cos(math.radians(angle - 30)), 
         pos[1] - spaceship_size * 0.4 * math.sin(math.radians(angle - 30)))
    ]
    
    # 速度に応じた軌跡を描画
    velocity_magnitude = math.sqrt(spaceship_velocity[0]**2 + spaceship_velocity[1]**2)
    if velocity_magnitude > 2:
        # 速度が一定以上の場合、軌跡を描画
        trail_length = min(int(velocity_magnitude * 2), 20)  # 速度に応じた長さ（最大20）
        for i in range(1, trail_length + 1):
            alpha = 255 - (255 * i / trail_length)  # 徐々に透明に
            trail_size = spaceship_size * (1 - i / trail_length) * 0.8
            trail_pos = [
                pos[0] - spaceship_velocity[0] * 0.2 * i,
                pos[1] - spaceship_velocity[1] * 0.2 * i
            ]
            
            # 軌跡の色を決定
            if invincible:
                hue = (current_time // 50 + i * 10) % 360
                try:
                    trail_color = pygame.Color(0, 0, 0)
                    trail_color.hsva = (hue, 100, 100, 100)  # アルファ値を固定
                except:
                    # HSVAが失敗した場合はRGBで代替
                    r, g, b = hsv_to_rgb(hue/360.0, 1.0, 1.0)
                    trail_color = (r, g, b)
            elif bonus_active:
                trail_color = (255, 215, 0)  # GOLD
            else:
                trail_color = (200, 200, 255)  # Light blue
                
            # 軌跡を描画（円で表現）
            pygame.draw.circle(screen, trail_color, (int(trail_pos[0]), int(trail_pos[1])), int(trail_size))
    
    # 色の決定（無敵モード > ボーナス > 通常）
    if invincible:
        # 無敵モードの場合は虹色に点滅
        hue = (current_time // 50) % 360
        try:
            ship_color = pygame.Color(0, 0, 0)
            ship_color.hsva = (hue, 100, 100, 100)
        except:
            r, g, b = hsv_to_rgb(hue/360.0, 1.0, 1.0)
            ship_color = (r, g, b)
            
        try:
            wing_color = pygame.Color(0, 0, 0)
            wing_color.hsva = ((hue + 180) % 360, 100, 100, 100)
        except:
            r, g, b = hsv_to_rgb(((hue + 180) % 360)/360.0, 1.0, 1.0)
            wing_color = (r, g, b)
    elif bonus_active:
        ship_color = YELLOW
        wing_color = GOLD
    else:
        ship_color = WHITE
        wing_color = CYAN
    
    # 本体と翼を描画
    pygame.draw.polygon(screen, ship_color, main_points)
    pygame.draw.polygon(screen, wing_color, wing_points1)
    pygame.draw.polygon(screen, wing_color, wing_points2)
    
    # コックピット部分を描画（前方を明確に示す）
    if invincible:
        try:
            cockpit_color = pygame.Color(0, 0, 0)
            cockpit_color.hsva = ((hue + 120) % 360, 100, 100, 100)  # 補色の一つ
        except:
            r, g, b = hsv_to_rgb(((hue + 120) % 360)/360.0, 1.0, 1.0)
            cockpit_color = (r, g, b)
    elif bonus_active:
        cockpit_color = RED  # ボーナス中は赤いコックピット
    else:
        cockpit_color = RED  # 通常時も赤いコックピット（前方を明確に）
    
    pygame.draw.polygon(screen, cockpit_color, cockpit_points)
    
    # 無敵モードの場合は宇宙船の周りに保護シールドを表示
    if invincible:
        shield_radius = spaceship_size * 1.5
        try:
            shield_color = pygame.Color(0, 0, 0)
            shield_color.hsva = ((current_time // 100 + 180) % 360, 100, 100, 50)
        except:
            hue = (current_time // 100 + 180) % 360
            r, g, b = hsv_to_rgb(hue/360.0, 1.0, 0.5)  # 明度を下げて半透明っぽく
            shield_color = (r, g, b)
        pygame.draw.circle(screen, shield_color, (int(pos[0]), int(pos[1])), int(shield_radius), 2)
    
    # 推進中は炎を描画
    if keys[pygame.K_UP]:
        flame_points = [
            (pos[0] + spaceship_size * 0.7 * math.cos(math.radians(angle + 140)), 
             pos[1] - spaceship_size * 0.7 * math.sin(math.radians(angle + 140))),
            (pos[0] + spaceship_size * 0.7 * math.cos(math.radians(angle + 220)), 
             pos[1] - spaceship_size * 0.7 * math.sin(math.radians(angle + 220))),
            (pos[0] + spaceship_size * 1.5 * math.cos(math.radians(angle + 180)), 
             pos[1] - spaceship_size * 1.5 * math.sin(math.radians(angle + 180)))
        ]
        
        # 炎の色を決定
        if invincible:
            hue = (current_time // 30) % 360
            try:
                flame_color = pygame.Color(0, 0, 0)
                flame_color.hsva = (hue, 100, 100, 100)
            except:
                r, g, b = hsv_to_rgb(hue/360.0, 1.0, 1.0)
                flame_color = (r, g, b)
        elif bonus_active:
            flame_color = GOLD
        else:
            flame_color = YELLOW
            
        pygame.draw.polygon(screen, flame_color, flame_points)
        
        # 追加の粒子効果
        for _ in range(2):
            particle_angle = angle + 180 + random.uniform(-20, 20)
            particle_distance = spaceship_size * 1.8
            particle_x = pos[0] + particle_distance * math.cos(math.radians(particle_angle))
            particle_y = pos[1] - particle_distance * math.sin(math.radians(particle_angle))
            particle_size = random.uniform(1, 3)
            
            if invincible:
                hue = (current_time // 20 + random.randint(0, 360)) % 360
                try:
                    particle_color = pygame.Color(0, 0, 0)
                    particle_color.hsva = (hue, 100, 100, 100)
                except:
                    r, g, b = hsv_to_rgb(hue/360.0, 1.0, 1.0)
                    particle_color = (r, g, b)
            elif bonus_active:
                particle_color = GOLD
            else:
                particle_color = YELLOW
                
            pygame.draw.circle(screen, particle_color, (int(particle_x), int(particle_y)), int(particle_size))

# 距離を計算する関数
def calculate_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

# 星と星の間を通過したかチェックする関数
def check_passage_between_stars(prev_pos, current_pos):
    global last_passage_stars
    
    if len(stars) < 2:
        return False
    
    # 宇宙船の移動ベクトル
    ship_vector = (current_pos[0] - prev_pos[0], current_pos[1] - prev_pos[1])
    ship_distance = math.sqrt(ship_vector[0]**2 + ship_vector[1]**2)
    
    # 移動距離が小さすぎる場合はスキップ（ほぼ全ての動きを許可）
    if ship_distance < 1:
        return False
    
    # すべての星のペアについてチェック
    for i in range(len(stars)):
        for j in range(i+1, len(stars)):
            star1 = stars[i]
            star2 = stars[j]
            
            # 同じ星のペアでの連続通過を許可（連続通過制限を解除）
            # if last_passage_stars == (i, j) or last_passage_stars == (j, i):
            #     continue
            
            # 星間の距離
            star_distance = calculate_distance(star1['pos'], star2['pos'])
            
            # 星が近すぎる場合はスキップ
            if star_distance < star1['radius'] + star2['radius'] + spaceship_size * 2:
                continue
            
            # 星1と星2の位置ベクトル
            p1 = star1['pos']
            p2 = star2['pos']
            
            # 宇宙船の前回位置と現在位置
            q1 = prev_pos
            q2 = current_pos
            
            # 線分の方向ベクトル
            v1 = [p2[0] - p1[0], p2[1] - p1[1]]
            v2 = [q2[0] - q1[0], q2[1] - q1[1]]
            
            # 線分の長さ
            line_length = math.sqrt(v1[0]**2 + v1[1]**2)
            if line_length == 0:
                continue
                
            # 線分の単位ベクトル
            unit_v1 = [v1[0] / line_length, v1[1] / line_length]
            
            # 方法1: 線分の交差判定（最も正確な方法）
            # 線分の方程式: P = P1 + t(P2 - P1), 0 <= t <= 1
            # 宇宙船の軌跡の方程式: Q = Q1 + s(Q2 - Q1), 0 <= s <= 1
            
            # 交差判定のための行列式
            cross_product = v1[0] * v2[1] - v1[1] * v2[0]
            
            # 線分が平行でない場合
            if abs(cross_product) > 0.0001:
                # パラメータtとsを計算
                s = ((p1[0] - q1[0]) * v1[1] - (p1[1] - q1[1]) * v1[0]) / cross_product
                t = ((q1[0] - p1[0]) * v2[1] - (q1[1] - p1[1]) * v2[0]) / -cross_product
                
                # 交差判定: 0 <= t <= 1 かつ 0 <= s <= 1
                if 0 <= t <= 1 and 0 <= s <= 1:
                    # 交差点の座標を計算
                    intersection_x = p1[0] + t * v1[0]
                    intersection_y = p1[1] + t * v1[1]
                    
                    # 交差点が星の内部でないことを確認
                    if (calculate_distance([intersection_x, intersection_y], star1['pos']) > star1['radius'] + spaceship_size and
                        calculate_distance([intersection_x, intersection_y], star2['pos']) > star2['radius'] + spaceship_size):
                        print(f"星間通過検出! 交差点: ({intersection_x:.1f}, {intersection_y:.1f})")
                        last_passage_stars = (i, j)
                        return True
            
            # 方法2: 線分の両端を結ぶ線を横切ったかチェック
            # 前回位置と現在位置が線分の異なる側にあるかチェック
            side_prev = (q1[0] - p1[0]) * (p2[1] - p1[1]) - (q1[1] - p1[1]) * (p2[0] - p1[0])
            side_curr = (q2[0] - p1[0]) * (p2[1] - p1[1]) - (q2[1] - p1[1]) * (p2[0] - p1[0])
            
            # 符号が変わった場合（線分を横切った場合）
            if side_prev * side_curr < 0:
                # 交差点を計算
                t = side_prev / (side_prev - side_curr)
                cross_x = q1[0] + t * (q2[0] - q1[0])
                cross_y = q1[1] + t * (q2[1] - q1[1])
                
                # 交差点が線分上にあるかチェック
                v_cross = [cross_x - p1[0], cross_y - p1[1]]
                proj_cross = v_cross[0] * unit_v1[0] + v_cross[1] * unit_v1[1]
                
                if 0 <= proj_cross <= line_length:
                    # 交差点が星の内部でないことを確認
                    if (calculate_distance([cross_x, cross_y], star1['pos']) > star1['radius'] + spaceship_size and
                        calculate_distance([cross_x, cross_y], star2['pos']) > star2['radius'] + spaceship_size):
                        print(f"星間通過検出! 線分を横切りました: ({cross_x:.1f}, {cross_y:.1f})")
                        last_passage_stars = (i, j)
                        return True
            
            # 方法3: 線分への近接を検出（より緩い条件）
            # 宇宙船の現在位置から線分への最短距離を計算
            v_curr = [q2[0] - p1[0], q2[1] - p1[1]]
            proj_curr = v_curr[0] * unit_v1[0] + v_curr[1] * unit_v1[1]
            
            # 投影点が線分上にあるか確認
            if 0 <= proj_curr <= line_length:
                # 線分への垂直距離を計算
                dist_curr = abs(v_curr[0] * unit_v1[1] - v_curr[1] * unit_v1[0])
                
                # 宇宙船のサイズを考慮した距離のしきい値（より緩い条件）
                threshold = spaceship_size * 2.5
                
                if dist_curr < threshold:
                    print(f"星間通過検出! 線分への近接: 距離={dist_curr:.1f}, しきい値={threshold:.1f}")
                    last_passage_stars = (i, j)
                    return True
    
    return False

# ゲームループ
clock = pygame.time.Clock()
running = True

while running:
    current_time = pygame.time.get_ticks()
    
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r and game_over:
                # ゲームリセット
                spaceship_pos = [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2]
                spaceship_velocity = [0, 1]
                spaceship_acceleration = [0, 0]
                spaceship_angle = 0
                game_over = False
                score = 0
                score_multiplier = 1
                last_score_update = current_time
                bonus_active = False
                passage_effects = []  # エフェクトもリセット
                last_passage_stars = None  # 通過履歴をリセット
                # 星をリセット
                stars = []
                initial_star = {
                    'pos': [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2],
                    'radius': star_radius,
                    'color': RED,
                    'rotation': 0,
                    'rotation_speed': random.uniform(-0.5, 0.5),
                    'creation_time': pygame.time.get_ticks(),
                    'collision_count': 0
                }
                initial_star['texture'] = create_planet_texture(initial_star['radius'], initial_star['color'])
                stars.append(initial_star)
                last_star_add_time = current_time
                last_position = spaceship_pos.copy()
            # デバッグモード: Dキーで無敵モードの切り替え
            if event.key == pygame.K_d:
                invincible = not invincible
                if invincible:
                    print("デバッグモード: 無敵モードON")
                else:
                    print("デバッグモード: 無敵モードOFF")
    
    # 20秒ごとに新しい星を追加
    if not game_over and current_time - last_star_add_time >= star_add_interval:
        # 星が追加されることを事前に警告
        warning_text = font.render("WARNING: New planet appearing soon!", True, RED)
        screen.blit(warning_text, (SCREEN_WIDTH // 2 - 180, 10))
        
        # 残り時間が3秒以下になったら星を追加
        if current_time - last_star_add_time >= star_add_interval - 3000:
            # 点滅効果
            if (current_time // 200) % 2 == 0:  # 0.2秒ごとに点滅
                warning_text = font.render("WARNING: New planet appearing!", True, RED)
                screen.blit(warning_text, (SCREEN_WIDTH // 2 - 180, 10))
        
        # 時間が来たら星を追加
        if current_time - last_star_add_time >= star_add_interval:
            add_new_star()
            last_star_add_time = current_time
    
    # ボーナス状態の更新
    if bonus_active and current_time > bonus_end_time:
        bonus_active = False
        score_multiplier = 1
    
    if not game_over:
        # キー入力の取得
        keys = pygame.key.get_pressed()
        
        # 宇宙船の回転
        if keys[pygame.K_LEFT]:
            spaceship_angle += rotation_speed
            # 回転時のパーティクル効果
            if random.random() < 0.3:  # 30%の確率でパーティクル生成
                rotation_direction = 1
                angle_offset = random.uniform(-30, 30)
                particle_angle = spaceship_angle + 180 + angle_offset * rotation_direction
                particle_speed = random.uniform(1, 3)
                particle_size = random.uniform(1, 3)
                
                if invincible:
                    hue = (current_time // 30 + random.randint(0, 360)) % 360
                    particle_color = pygame.Color(0, 0, 0)
                    particle_color.hsva = (hue, 100, 100, 100)
                elif bonus_active:
                    particle_color = GOLD
                else:
                    particle_color = CYAN
                    
                particles.append({
                    'pos': spaceship_pos.copy(),
                    'velocity': [particle_speed * math.cos(math.radians(particle_angle)), 
                                particle_speed * math.sin(math.radians(particle_angle))],
                    'size': particle_size,
                    'color': particle_color,
                    'life': 1.0
                })
        if keys[pygame.K_RIGHT]:
            spaceship_angle -= rotation_speed
            # 回転時のパーティクル効果
            if random.random() < 0.3:  # 30%の確率でパーティクル生成
                rotation_direction = -1
                angle_offset = random.uniform(-30, 30)
                particle_angle = spaceship_angle + 180 + angle_offset * rotation_direction
                particle_speed = random.uniform(1, 3)
                particle_size = random.uniform(1, 3)
                
                if invincible:
                    hue = (current_time // 30 + random.randint(0, 360)) % 360
                    particle_color = pygame.Color(0, 0, 0)
                    particle_color.hsva = (hue, 100, 100, 100)
                elif bonus_active:
                    particle_color = GOLD
                else:
                    particle_color = CYAN
                    
                particles.append({
                    'pos': spaceship_pos.copy(),
                    'velocity': [particle_speed * math.cos(math.radians(particle_angle)), 
                                particle_speed * math.sin(math.radians(particle_angle))],
                    'size': particle_size,
                    'color': particle_color,
                    'life': 1.0
                })
            
        # 宇宙船の推進
        if keys[pygame.K_UP]:
            spaceship_acceleration[0] = thrust_power * math.cos(math.radians(spaceship_angle))
            spaceship_acceleration[1] = -thrust_power * math.sin(math.radians(spaceship_angle))
        else:
            spaceship_acceleration[0] = 0
            spaceship_acceleration[1] = 0
            
        # 重力の計算と衝突判定
        collision = False
        spaceship_acceleration[0] = 0
        spaceship_acceleration[1] = 0
        
        # 推進力の適用
        if keys[pygame.K_UP]:
            spaceship_acceleration[0] += thrust_power * math.cos(math.radians(spaceship_angle))
            spaceship_acceleration[1] += -thrust_power * math.sin(math.radians(spaceship_angle))
        
        # 各星からの重力を計算
        for star in stars:
            distance = calculate_distance(spaceship_pos, star['pos'])
            
            # 衝突判定
            if distance <= star['radius'] + spaceship_size:
                # 無敵モードの場合は衝突を無視
                if invincible:
                    # 衝突回数をカウント
                    if 'collision_count' not in star:
                        star['collision_count'] = 0
                    star['collision_count'] += 1
                    
                    print(f"無敵モード: 衝突回数 {star['collision_count']}/3")
                    
                    # 複数回衝突した場合は別の場所にワープ
                    if star['collision_count'] >= 3:
                        # 画面上のランダムな安全な位置を見つける
                        safe_pos_found = False
                        max_attempts = 20
                        attempts = 0
                        
                        while not safe_pos_found and attempts < max_attempts:
                            # 画面内のランダムな位置
                            new_x = random.randint(50, SCREEN_WIDTH - 50)
                            new_y = random.randint(50, SCREEN_HEIGHT - 50)
                            
                            # すべての星から十分離れているか確認
                            is_safe = True
                            for other_star in stars:
                                dist = calculate_distance([new_x, new_y], other_star['pos'])
                                if dist < other_star['radius'] + spaceship_size * 3:
                                    is_safe = False
                                    break
                            
                            if is_safe:
                                safe_pos_found = True
                                # 宇宙船をワープさせる
                                spaceship_pos[0] = new_x
                                spaceship_pos[1] = new_y
                                # 速度をゼロにする
                                spaceship_velocity[0] = 0
                                spaceship_velocity[1] = 0
                                # ワープエフェクトを作成
                                passage_effects.append({
                                    'start_time': current_time,
                                    'duration': 1000,
                                    'position': spaceship_pos.copy(),
                                    'particles': []
                                })
                                # パーティクルを生成
                                for _ in range(20):
                                    angle = random.uniform(0, 2 * math.pi)
                                    speed = random.uniform(1, 5)
                                    size = random.randint(2, 6)
                                    color = random.choice([WHITE, CYAN, MAGENTA])
                                    passage_effects[-1]['particles'].append({
                                        'pos': spaceship_pos.copy(),
                                        'velocity': [speed * math.cos(angle), speed * math.sin(angle)],
                                        'size': size,
                                        'color': color,
                                        'life': random.uniform(0.5, 1.0)
                                    })
                                print(f"無敵モード: 安全な場所にワープしました！")
                                
                                # 衝突カウントをリセット
                                star['collision_count'] = 0
                            
                            attempts += 1
                        
                        # 安全な場所が見つからなかった場合は画面中央付近にワープ
                        if not safe_pos_found:
                            spaceship_pos[0] = SCREEN_WIDTH // 2 + random.randint(-50, 50)
                            spaceship_pos[1] = SCREEN_HEIGHT // 2 + random.randint(-50, 50)
                            spaceship_velocity[0] = 0
                            spaceship_velocity[1] = 0
                            print(f"無敵モード: 画面中央付近にワープしました！")
                            
                            # 衝突カウントをリセット
                            star['collision_count'] = 0
                    else:
                        # 宇宙船を少し押し戻す
                        push_direction_x = spaceship_pos[0] - star['pos'][0]
                        push_direction_y = spaceship_pos[1] - star['pos'][1]
                        
                        # 正規化
                        push_magnitude = math.sqrt(push_direction_x**2 + push_direction_y**2)
                        if push_magnitude > 0:
                            push_direction_x /= push_magnitude
                            push_direction_y /= push_magnitude
                        
                        # 宇宙船を押し戻す
                        spaceship_pos[0] += push_direction_x * 10
                        spaceship_pos[1] += push_direction_y * 10
                        
                        # 速度を減衰
                        spaceship_velocity[0] *= 0.2
                        spaceship_velocity[1] *= 0.2
                        
                        print(f"無敵モード: 衝突を回避しました！ (回数: {star['collision_count']}/3)")
                # 新しく追加された星との衝突の場合は猶予を与える
                elif 'creation_time' in star and current_time - star['creation_time'] < 2000:  # 2秒間の猶予
                    # 衝突を無視して、宇宙船を少し押し戻す
                    push_direction_x = spaceship_pos[0] - star['pos'][0]
                    push_direction_y = spaceship_pos[1] - star['pos'][1]
                    
                    # 正規化
                    push_magnitude = math.sqrt(push_direction_x**2 + push_direction_y**2)
                    if push_magnitude > 0:
                        push_direction_x /= push_magnitude
                        push_direction_y /= push_magnitude
                    
                    # 宇宙船を押し戻す
                    spaceship_pos[0] += push_direction_x * 5
                    spaceship_pos[1] += push_direction_y * 5
                    
                    # 速度を減衰
                    spaceship_velocity[0] *= 0.5
                    spaceship_velocity[1] *= 0.5
                    
                    print(f"新しい星との衝突を回避しました！")
                else:
                    collision = True
                    break
                
            # 重力の方向ベクトル
            direction_x = star['pos'][0] - spaceship_pos[0]
            direction_y = star['pos'][1] - spaceship_pos[1]
            
            # 正規化
            magnitude = math.sqrt(direction_x**2 + direction_y**2)
            direction_x /= magnitude
            direction_y /= magnitude
            
            # 重力の強さ（距離の二乗に反比例）
            gravity_strength = GRAVITY_CONSTANT / (distance**2) * 1000
            
            # 重力による加速度を追加
            spaceship_acceleration[0] += direction_x * gravity_strength
            spaceship_acceleration[1] += direction_y * gravity_strength
        
        if collision:
            game_over = True
        else:
            # 速度の更新
            spaceship_velocity[0] += spaceship_acceleration[0]
            spaceship_velocity[1] += spaceship_acceleration[1]
            
            # 位置の更新
            spaceship_pos[0] += spaceship_velocity[0]
            spaceship_pos[1] += spaceship_velocity[1]
            
            # 星間通過ボーナスのチェック
            if len(stars) >= 2 and current_time - last_bonus_time > bonus_cooldown:
                # 移動距離の制限を緩和（小さな動きでも検出できるように）
                move_distance = calculate_distance(last_position, spaceship_pos)
                if move_distance > 1:  # 最小移動距離を1に設定（ほぼ全ての動きで検出）
                    passage_result = check_passage_between_stars(last_position, spaceship_pos)
                    if passage_result:
                        # スコアを2倍にする
                        old_score = score
                        score = score * 2
                        print(f"ボーナス獲得! 現在のスコア: {old_score} → {score}")
                        bonus_active = True
                        score_multiplier = 2
                        bonus_end_time = current_time + bonus_duration
                        last_bonus_time = current_time
                        
                        # 星間通過の派手な演出を作成
                        passage_effects.append({
                            'start_time': current_time,
                            'duration': 1000,  # 1秒間
                            'position': spaceship_pos.copy(),
                            'particles': []
                        })
                        # パーティクルを生成
                        for _ in range(30):
                            angle = random.uniform(0, 2 * math.pi)
                            speed = random.uniform(2, 8)
                            size = random.randint(2, 6)
                            color = random.choice([YELLOW, GOLD, ORANGE, MAGENTA, CYAN])
                            passage_effects[-1]['particles'].append({
                                'pos': spaceship_pos.copy(),
                                'velocity': [speed * math.cos(angle), speed * math.sin(angle)],
                                'size': size,
                                'color': color,
                                'life': random.uniform(0.5, 1.0)  # ライフタイム係数
                            })
                        
                        # 宇宙船の周りに円形の波紋を広げる
                        for i in range(3):  # 3つの波紋
                            wave_effects.append({
                                'start_time': current_time + i * 200,  # 少しずつ遅延
                                'position': spaceship_pos.copy(),
                                'radius': spaceship_size,
                                'max_radius': spaceship_size * 10,
                                'color': GOLD if bonus_active else CYAN,
                                'width': 2
                            })
                            speed = random.uniform(2, 8)
                            size = random.randint(2, 6)
                            color = random.choice([YELLOW, GOLD, ORANGE, MAGENTA, CYAN])
                            passage_effects[-1]['particles'].append({
                                'pos': spaceship_pos.copy(),
                                'velocity': [speed * math.cos(angle), speed * math.sin(angle)],
                                'size': size,
                                'color': color,
                                'life': random.uniform(0.5, 1.0)  # ライフタイム係数
                            })
            
            # 前回位置を更新
            last_position = spaceship_pos.copy()
            
            # スコア加算（一定間隔で更新）
            current_score_time = current_time
            if current_score_time - last_score_update >= score_update_interval:
                # 経過時間に応じたスコア加算（1秒で10点）
                elapsed_seconds = (current_score_time - last_score_update) / 1000.0
                points_to_add = elapsed_seconds * score_rate * score_multiplier
                score += points_to_add
                last_score_update = current_score_time
            
            # 画面外に出た場合は反対側から出てくる
            if spaceship_pos[0] < 0:
                spaceship_pos[0] = SCREEN_WIDTH
            elif spaceship_pos[0] > SCREEN_WIDTH:
                spaceship_pos[0] = 0
            if spaceship_pos[1] < 0:
                spaceship_pos[1] = SCREEN_HEIGHT
            elif spaceship_pos[1] > SCREEN_HEIGHT:
                spaceship_pos[1] = 0
    
    # 画面を黒で塗りつぶす
    screen.fill(BLACK)
    
    # 背景の星を描画
    for x, y, size, color in background_stars:
        # 星をゆっくり点滅させる
        brightness_factor = 0.7 + 0.3 * math.sin(current_time / 1000 + x * y)
        current_color = (
            int(color[0] * brightness_factor),
            int(color[1] * brightness_factor),
            int(color[2] * brightness_factor)
        )
        pygame.draw.circle(screen, current_color, (x, y), size)
    
    # パーティクルを更新・描画
    for i in range(len(particles) - 1, -1, -1):
        particle = particles[i]
        # パーティクルを移動
        particle['pos'][0] += particle['velocity'][0]
        particle['pos'][1] += particle['velocity'][1]
        # ライフタイムを減少
        particle['life'] -= 0.02
        # 消滅したパーティクルを削除
        if particle['life'] <= 0:
            particles.pop(i)
        else:
            # パーティクルを描画（ライフタイムに応じて透明度を変更）
            alpha = int(255 * particle['life'])
            if isinstance(particle['color'], tuple):
                if len(particle['color']) == 3:
                    color = (*particle['color'], alpha)
                else:
                    color = particle['color']
            else:
                color = particle['color']  # pygame.Colorオブジェクトの場合
            pygame.draw.circle(screen, color, 
                              (int(particle['pos'][0]), int(particle['pos'][1])), 
                              int(particle['size'] * particle['life']))
    
    # 波紋エフェクトを更新・描画
    for i in range(len(wave_effects) - 1, -1, -1):
        wave = wave_effects[i]
        # 経過時間を計算
        elapsed = current_time - wave['start_time']
        # 波紋の半径を拡大
        progress = elapsed / 1000.0  # 1秒で完了
        wave['radius'] = wave['radius'] + (wave['max_radius'] - wave['radius']) * progress
        # 透明度を減少
        alpha = int(255 * (1 - progress))
        # 波紋を描画
        if progress < 1.0:
            # 色をRGBに制限（アルファは使わない）
            if isinstance(wave['color'], tuple):
                color = wave['color'][:3]  # RGBのみ使用
            else:
                color = wave['color']
                
            pygame.draw.circle(screen, color, 
                              (int(wave['position'][0]), int(wave['position'][1])), 
                              int(wave['radius']), wave['width'])
        else:
            # 完了した波紋を削除
            wave_effects.pop(i)
    
    # 星を描画
    for star in stars:
        # テクスチャがある場合はそれを使用
        if 'texture' in star and star['texture'] is not None:
            # テクスチャの中心位置を計算
            texture_rect = star['texture'].get_rect()
            texture_rect.center = (int(star['pos'][0]), int(star['pos'][1]))
            
            # 回転を適用（もし回転速度が設定されている場合）
            if 'rotation' in star:
                # 回転速度を適用
                if 'rotation_speed' in star:
                    star['rotation'] += star['rotation_speed']
                
                # テクスチャを回転
                rotated_texture = pygame.transform.rotate(star['texture'], star['rotation'])
                # 回転後のテクスチャの中心位置を調整
                rotated_rect = rotated_texture.get_rect(center=texture_rect.center)
                screen.blit(rotated_texture, rotated_rect.topleft)
            else:
                # 回転なしでテクスチャを描画
                screen.blit(star['texture'], texture_rect.topleft)
        else:
            # テクスチャがない場合は単純な円を描画
            pygame.draw.circle(screen, star['color'], (int(star['pos'][0]), int(star['pos'][1])), star['radius'])
        
        # 新しく追加された星の場合は警告エフェクトを表示
        if 'creation_time' in star and current_time - star['creation_time'] < 2000:
            # 点滅する警告円
            if (current_time // 200) % 2 == 0:  # 0.2秒ごとに点滅
                warning_radius = star['radius'] + 10 + 5 * math.sin(current_time / 100)
                pygame.draw.circle(screen, RED, (int(star['pos'][0]), int(star['pos'][1])), 
                                  int(warning_radius), 2)
    
    # 星間の通路を表示（2つ以上の星がある場合）
    if len(stars) >= 2:
        for i in range(len(stars)):
            for j in range(i+1, len(stars)):
                star1 = stars[i]
                star2 = stars[j]
                star_distance = calculate_distance(star1['pos'], star2['pos'])
                
                # 星が近すぎない場合のみ通路を表示
                if star_distance > star1['radius'] + star2['radius'] + spaceship_size * 2:
                    # 星間を線で結ぶ
                    if not bonus_active:
                        # 通常時は太めの線
                        pygame.draw.line(screen, (100, 100, 255), 
                                        (int(star1['pos'][0]), int(star1['pos'][1])),
                                        (int(star2['pos'][0]), int(star2['pos'][1])), 3)
                    # ボーナス中は派手な通路表示
                    else:
                        steps = int(star_distance / 10)
                        for step in range(steps):
                            t = step / steps
                            x = star1['pos'][0] + t * (star2['pos'][0] - star1['pos'][0])
                            y = star1['pos'][1] + t * (star2['pos'][1] - star1['pos'][1])
                            
                            # 虹色のような効果
                            hue = (current_time // 50 + step * 10) % 360
                            color = pygame.Color(0, 0, 0)
                            color.hsva = (hue, 100, 100, 100)
                            
                            size = 3 + math.sin(current_time / 100 + step / 2) * 2
                            pygame.draw.circle(screen, color, (int(x), int(y)), int(size))
    
    # 星間通過エフェクトの描画
    for effect in passage_effects[:]:
        effect_age = current_time - effect['start_time']
        if effect_age > effect['duration']:
            passage_effects.remove(effect)
            continue
            
        # パーティクルの更新と描画
        for particle in effect['particles']:
            # パーティクルの位置を更新
            particle['pos'][0] += particle['velocity'][0]
            particle['pos'][1] += particle['velocity'][1]
            
            # パーティクルのサイズを時間とともに小さくする
            life_ratio = 1 - (effect_age / effect['duration'])
            current_size = particle['size'] * life_ratio * particle['life']
            
            if current_size > 0.5:
                pygame.draw.circle(screen, particle['color'], 
                                  (int(particle['pos'][0]), int(particle['pos'][1])), 
                                  int(current_size))
    
    # 宇宙船を描画
    if not game_over:
        draw_spaceship(spaceship_pos, spaceship_angle)
    
    # スコアを表示
    score_text = font.render(f"Score: {int(score)}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # スコア増加率を表示
    rate_text = font.render(f"Rate: {int(score_rate * score_multiplier)}/sec", True, WHITE)
    screen.blit(rate_text, (10, 50))
    
    # 次の星が追加されるまでの時間を表示
    if not game_over:
        time_left = (star_add_interval - (current_time - last_star_add_time)) // 1000
        next_star_text = font.render(f"Next planet: {time_left}s", True, WHITE)
        screen.blit(next_star_text, (10, 90))
        
        # 星の数を表示
        stars_text = font.render(f"Planets: {len(stars)}", True, WHITE)
        screen.blit(stars_text, (10, 130))
        
        # デバッグモード表示
        if invincible:
            debug_text = font.render("DEBUG MODE: INVINCIBLE", True, GOLD)
            screen.blit(debug_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT - 40))
            
            # ワープ機能の説明
            warp_text = font.render("Collide 3 times with a planet to warp", True, GOLD)
            screen.blit(warp_text, (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT - 70))
    
    # ボーナス状態を表示
    if bonus_active:
        bonus_text = font.render("BONUS x2!", True, GOLD)
        screen.blit(bonus_text, (SCREEN_WIDTH - 150, 10))
        
        # ボーナス残り時間
        bonus_time_left = (bonus_end_time - current_time) // 1000 + 1
        bonus_time_text = font.render(f"{bonus_time_left}s", True, GOLD)
        screen.blit(bonus_time_text, (SCREEN_WIDTH - 150, 50))
        
        # スコア増加率を強調表示
        rate_bonus_text = font.render(f"+{int(score_rate * score_multiplier)}/sec", True, GOLD)
        screen.blit(rate_bonus_text, (SCREEN_WIDTH - 150, 90))
        
        # ボーナス中は画面の周りに輝くエフェクト
        for i in range(0, 360, 30):
            angle_rad = math.radians(i)
            x = SCREEN_WIDTH // 2 + (SCREEN_WIDTH // 2 - 20) * math.cos(angle_rad)
            y = SCREEN_HEIGHT // 2 + (SCREEN_HEIGHT // 2 - 20) * math.sin(angle_rad)
            
            # 時間によって色を変化させる
            hue = (current_time // 50 + i) % 360
            color = pygame.Color(0, 0, 0)
            color.hsva = (hue, 100, 100, 100)
            
            size = 5 + math.sin(current_time / 200 + i / 30) * 3
            pygame.draw.circle(screen, color, (int(x), int(y)), int(size))
    
    # ゲームオーバー表示
    if game_over:
        game_over_text = font.render("GAME OVER - Press R to Restart", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))
    
    # 画面を更新
    pygame.display.flip()
    
    # フレームレートを60FPSに設定
    clock.tick(60)

# Pygameの終了
pygame.quit()
sys.exit()
# 星間通過の履歴を保存する変数
last_passage_stars = None
# HSV色空間からRGB色空間に変換する関数
def hsv_to_rgb(h, s, v):
    """HSV色空間からRGB色空間に変換する関数"""
    if s == 0.0:
        return (v * 255, v * 255, v * 255)
    
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i %= 6
    
    if i == 0:
        return (int(v * 255), int(t * 255), int(p * 255))
    elif i == 1:
        return (int(q * 255), int(v * 255), int(p * 255))
    elif i == 2:
        return (int(p * 255), int(v * 255), int(t * 255))
    elif i == 3:
        return (int(p * 255), int(q * 255), int(v * 255))
    elif i == 4:
        return (int(t * 255), int(p * 255), int(v * 255))
    else:
        return (int(v * 255), int(p * 255), int(q * 255))
