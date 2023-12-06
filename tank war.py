import pgzrun,os
from math import *
from time import *
from random import *
from easygui import *
uk = ccbox('为了提升游戏体验,请先选择您电脑的键盘类型:', '键盘类型', ['含有小键盘', '不含小键盘'])
wk = not uk

TITLE = '羊羊大作战'
WIDTH = 1800
HEIGHT = 1200

# 控制游戏的物理常数
GRAVITY = 0.4
SPEED = 5
STRENGTH = 8

# directory
x = Actor('bomb')
x.begin = True
x.gaming = False
x.death = False
x.manuals = False
sounds_played = False

# icons
begin_gaming = Actor('icon_begin', center=(900, 650))  # 从begin传送到gaming
begin_manuals = Actor('icon_manuals', center=(900, 900))  # 从begin传送到manuals
manuals_begin = Actor('icon_delete', (30, 30))  # 从manuals传送到begin
death_gaming = Actor('icon_replay', center=(900, 900))  # 从death传送到gaming
exit_gaming = Actor('icon_exit',center=(900,650))

# actors
ground = []
cara = Actor('sheep_1_rt')
balla = Actor('bomb')
tonga = Actor('gun_1', anchor=(12, 23))
carb = Actor('sheep_2_lt')
ballb = Actor('bomb')
tongb = Actor('gun_2', anchor=(24, 24))

def reset():
    global ground
    # 生成地图元素
    # 使用列表推导式生成草地和泥土块
    # 使用 for 循环和 randint 函数生成随机的山体元素
    ground = [Actor('block_soil', bottomleft=(60*i, 1200-60*t)) for i in range(0, 30) for t in range(6)]\
        + [Actor('block_grass', bottomleft=(60*i, 840)) for i in range(0, 30)]\
        + [Actor('block_mout', bottomleft=(60*i, 1200-60*t)) for i in range(7, 9) for t in range(7, randint(8, 11))]\
        + [Actor('block_mout', bottomleft=(60*i, 1200-60*t)) for i in range(21, 23) for t in range(7, randint(8, 11))]\
        + [Actor('block_mout', bottomleft=(60*i, 1200-60*t)) for i in range(11, 19) for t in range(7, randint(12, 19))]\
        + [Actor('block_mout', bottomleft=(60*i, 1200-60*t)) for i in range(9, 11) for t in range(7, randint(9, 13))]\
        + [Actor('block_mout', bottomleft=(60*i, 1200-60*t))
           for i in range(19, 21) for t in range(7, randint(9, 13))]
    # 重置两只羊的状态
    # 设置位置、跳跃状态和移动方向等
    cara.pos = (150, 300)
    cara.win = False
    cara.vy = 0
    cara.jump = False
    carb.pos = (1650, 300)
    carb.win = False
    carb.vy = 0
    cara.goright = True
    cara.goleft = True
    carb.goright = True
    carb.goleft = True
    cara.jump = True
    carb.jump = True
    # 重置两只羊的生命值为3
    cara.hp = 3
    carb.hp = 3
    # 重置两只羊的死亡状态为未死亡
    cara.dying = False
    carb.dying = False
    # 重置两只羊的朝向
    cara.rt = True
    carb.lt = True
    cara.image = 'sheep_1_rt.png'
    carb.image = 'sheep_2_lt.png'
    # 重置炮状态
    tonga.angle = 0
    tongb.angle = 0
    # 重置炮弹状态
    balla.on = False
    ballb.on = False
reset()


def update():
    if x.gaming:
        update_ground()
        update_tong()
        update_car()
        update_ball()
    if x.death:
        update_sounds()


def update_sounds():
    global sounds_played
    if not sounds_played:
        sounds.fail.play()
        sounds_played = True

# 更新地面的状态
def update_ground():
    global ground
    # 循环遍历所有地图元素
    for block in ground[:]:
        # 如果炮弹 A 和地图元素发生碰撞，则移除该地图元素，并将炮弹 A 的状态置为非在地图上
        if balla.on and block.colliderect(balla):
            ground.remove(block)
            balla.on = False
        # 如果炮弹 B 和地图元素发生碰撞，则移除该地图元素，并将炮弹 B 的状态置为非在地图上
        if ballb.on and block.colliderect(ballb):
            ground.remove(block)
            ballb.on = False

# 更新武器（炮筒）的状态
def update_tong():
    # 位置追随
    if cara.rt:
        tonga.pos = (cara.x+12, cara.top+5)
    else:
        tonga.pos = (cara.x-12, cara.top+5)
    if carb.lt:
        tongb.pos = (carb.x-12, carb.top+5)
    else:
        tongb.pos = (carb.x+12, carb.top+5)
    # 调整角度
    if uk:
        if keyboard.G:
            tonga.angle += 2
        if keyboard.H:
            tonga.angle -= 2
        if keyboard.KP2:
            tongb.angle -= 2
        if keyboard.KP1:
            tongb.angle += 2
    if wk:
        if keyboard.C:
            tonga.angle += 2
        if keyboard.V:
            tonga.angle -= 2
        if keyboard.RIGHTBRACKET:
            tongb.angle -= 2
        if keyboard.LEFTBRACKET:
            tongb.angle += 2

# 更新角色（绵羊）的状态
def update_car():
    # 基本运动
    carb.y += carb.vy
    cara.y += cara.vy
    cara.vy += GRAVITY
    carb.vy += GRAVITY
    cara.goright = True
    cara.goleft = True
    carb.goright = True
    carb.goleft = True
    cara.jump = False
    carb.jump = False
    # 碰撞检测
    for block in ground:
        # 如果地面块和绵羊之间发生了碰撞
        if cara.x-100 < block.x < cara.x+100 and cara.y-100 < block.y < cara.y+100:
            # 如果绵羊撞到了地面块的顶部，则将其弹回上升
            if cara.colliderect(Rect([block.left+9, block.top], [42, 10])):  # up
                cara.vy = - 0.9
             # 如果绵羊撞到了地面块的左侧，则不能向右走
            if cara.colliderect(Rect([block.left, block.top+9], [10, 42])):  # left
                cara.goright = False
            # 如果绵羊撞到了地面块的底部，则不能再往下掉
            if cara.colliderect(Rect([block.left+9, block.bottom-10], [42, 10])):  # down
                cara.vy = 0.8
            # 如果绵羊撞到了地面块的右侧，则不能向左走
            if cara.colliderect(Rect([block.right-10, block.top+8], [10, 42])):  # right
                cara.goleft = False
            if cara.colliderect(Rect([block.left+3, block.top-8], [54, 12])):  # jump
                cara.jump = True
    for block in ground:
        if carb.x-100 < block.x < carb.x+100 and carb.y-100 < block.y < carb.y+100:
            if carb.colliderect(Rect([block.left+9, block.top], [42, 10])):  # up
                carb.vy = - 0.9
            if carb.colliderect(Rect([block.left, block.top+9], [10, 42])):  # left
                carb.goright = False
            if carb.colliderect(Rect([block.left+9, block.bottom-10], [42, 10])):  # down
                carb.vy = 0.8
            if carb.colliderect(Rect([block.right-10, block.top+9], [10, 42])):  # right
                carb.goleft = False
            if carb.colliderect(Rect([block.left+3, block.top-8], [54, 12])):  # jump
                carb.jump = True
    # 控制运动
    if uk:
        if keyboard.A and cara.goleft:
            cara.x -= SPEED*(1+cara.dying)
        if keyboard.D and cara.goright:
            cara.x += SPEED*(1+cara.dying)
        if keyboard.LEFT and carb.goleft:
            carb.x -= SPEED*(1+carb.dying)
        if keyboard.RIGHT and carb.goright:
            carb.x += SPEED*(1+carb.dying)
    if wk:
        if keyboard.A and cara.goleft:
            cara.x -= SPEED*(1+cara.dying)
        if keyboard.D and cara.goright:
            cara.x += SPEED*(1+cara.dying)
        if keyboard.J and carb.goleft:
            carb.x -= SPEED*(1+carb.dying)
        if keyboard.L and carb.goright:
            carb.x += SPEED*(1+carb.dying)
    # 血量
    if cara.hp == 1:
        cara.dying = True
    if carb.hp == 1:
        carb.dying = True
    if carb.hp == 0 or carb.y > HEIGHT:
        reset()
        sounds.sheep_2.play()
        cara.win = True
        x.death = True
        x.gaming = False
    if cara.hp == 0 or cara.y > HEIGHT:
        reset()
        sounds.sheep_2.play()
        carb.win = True
        x.death = True
        x.gaming = False

#更新炮弹的状态
def update_ball():
    # 位置追随 如果 balla 或 ballb 没有发射（on=False），则 ball 的位置与对应的炮筒位置重合
    if not ballb.on:
        ballb.pos = tongb.pos
    if not balla.on:
        balla.pos = tonga.pos
    # 基本运动 如果 balla 在空中（on=True），则更新 balla 的位置和速度
    if balla.on:
        balla.x += balla.vx
        balla.vy += GRAVITY
        balla.y += balla.vy
        balla.angle = -atan(balla.vy / balla.vx) * (180 / pi)
    if ballb.on:
        ballb.x += ballb.vx
        ballb.vy += GRAVITY
        ballb.y += ballb.vy
        ballb.angle = -atan(ballb.vy / ballb.vx) * (180 / pi)
    # 装弹 如果 balla 落地了，将其 on 置为 False
    if balla.on and balla.y > HEIGHT:
        balla.on = False
    if ballb.on and ballb.y > HEIGHT:
        ballb.on = False
    # 击中敌人 如果 balla 击中了 carb，将 carb 的血量减少 1，播放击中音效，并将 balla 的 on 置为 False
    if balla.colliderect(carb) and balla.on:
        carb.hp -= 1
        sounds.sheep.play()
        balla.on = False
    if ballb.colliderect(cara) and ballb.on:
        cara.hp -= 1
        sounds.sheep.play()
        ballb.on = False

# 绘制游戏场景
def draw():
    screen.clear()
    if x.gaming:
        show_gaming()
    if x.death:
        show_death()
        # sounds.fail.play()
    if x.begin:
        show_begin()
    if x.manuals:
        show_manuals()

# 展示开始界面
def show_begin():
    screen.blit('img_palebegin', (0, 0))
    screen.blit('tank_war', (440, 230))
    # 展示“开始游戏”和 “操作说明”按钮
    begin_gaming.draw()
    begin_manuals.draw()

# 展示游戏进行中的界面
def show_gaming():
    screen.blit('img_background', (0, 0))
    # 展示角色当前剩余生命值，如果角色处于受伤状态则展示为心形图案有变化，否则展示为普通心形图案
    for i in range(cara.hp):
        if cara.dying:
            screen.blit('heart1.png', (50+80*i, 40+randint(0, 3)))
        else:
            screen.blit('heart.png', (50+80*i, 40+randint(0, 3)))
    for i in range(carb.hp):
        if carb.dying:
            screen.blit('heart1.png', (1700-80*i, 40+randint(0, 3)))
        else:
            screen.blit('heart.png', (1700-80*i, 40+randint(0, 3)))
    # 展示地面和各角色、子弹等物体
    for block in ground:
        block.draw()
    cara.draw()
    carb.draw()
    if balla.on:
        balla.draw()
    tonga.draw()
    if ballb.on:
        ballb.draw()
    tongb.draw()

# 展示死亡界面
def show_death():
    # 判断哪个角色胜利并展示对应的背景图像
    music.stop()
    if carb.win:
        screen.blit('img_whitewin', (0, 0))
    if cara.win:
        screen.blit('img_blackwin', (0, 0))
    # 展示“再玩一次”按钮
    death_gaming.draw()
    exit_gaming.draw()
 # 展示操作说明界面
def show_manuals():
    screen.blit('img_palebegin', (0, 0))
    if uk:
        screen.blit('img_manuals_uk', (30, 100))
    if wk:
        screen.blit('img_manuals_wk', (30, 100))
    # 展示“返回主菜单”按钮
    manuals_begin.draw()


def on_mouse_down(pos):
    # 当游戏处于死亡状态时，点击“再玩一次”按钮可以重新开始游戏
    global sounds_played
    if x.death:
        if death_gaming.collidepoint(pos):
            music.play('xyy')
            sounds.choose.play()
            sounds.motor.play()
            sounds_played = False
            x.gaming = True
            x.death = False
        if exit_gaming.collidepoint(pos):
            exit()
    # 当游戏处于开始界面时，点击“开始游戏”按钮可以进入游戏界面，点击“操作说明”按钮可以进入操作说明界面
    if x.begin:
        if begin_gaming.collidepoint(pos):
            sounds.choose.play()
            sounds.motor.play()
            x.gaming = True
            x.begin = False
        if begin_manuals.collidepoint(pos):
            sounds.choose.play()
            x.manuals = True
            x.begin = False
    # 当游戏处于操作说明界面时，点击“返回主菜单”按钮可以返回开始界面
    if x.manuals:
        if manuals_begin.collidepoint(pos):
            sounds.choose.play()
            x.begin = True
            x.manuals = False

def on_key_down(key):
    # 如果当前处于游戏场景（即x.gaming为True），则进入到按键响应部分
    if x.gaming:
        # 根据当前所选的语言类型（使用了uk和wk进行判断），响应用户的按键操作
        # 对于uk键盘类型的按键响应
        if uk:
            # 如果用户按下W（或I）键且对应角色正在跳跃，则修改该角色的vy值，使其向上进行跳跃；
            if key == key.W and cara.jump:
                cara.vy = -STRENGTH*(1+cara.dying/2)
            if key == key.UP and carb.jump:
                carb.vy = -STRENGTH*(1+carb.dying/2)
            # 如果用户按下J（或B）键，则记录当前时间，用于控制子弹发射频率；
            if key == key.J:
                balla.time0 = time()
            if key == key.KP3:
                ballb.time0 = time()
            # 如果用户按下A键（或L），则修改对应角色的朝向，并修改瞄准射击的角度以及角色展示的图片；
            if key == key.A:
                if cara.rt:
                    tonga.angle = 90 - tonga.angle
                cara.rt = False
                if cara.dying:
                    cara.image = 'sheep_11_lt.png'
                else:
                    cara.image = 'sheep_1_lt.png'
            # 如果用户按下D键，则修改对应角色的朝向，并修改瞄准射击的角度以及角色展示的图片；
            if key == key.D:
                if not cara.rt:
                    tonga.angle = 90 - tonga.angle
                cara.rt = True
                if cara.dying:
                    cara.image = 'sheep_11_rt.png'
                else:
                    cara.image = 'sheep_1_rt.png'
            # 如果用户按下RIGHT键，则同样操作另一个角色，但方向与D键相反。
            if key == key.RIGHT:
                if carb.lt:
                    tongb.angle = -90 - tongb.angle
                carb.lt = False
                if carb.dying:
                    carb.image = 'sheep_22_rt.png'
                else:
                    carb.image = 'sheep_2_rt.png'
            # 如果用户按下LEFT键，则修改另一个角色的朝向、瞄准角度和展示的图片，同样包括方向与A键相反；
            if key == key.LEFT:
                if not carb.lt:
                    tongb.angle = -90 - tongb.angle
                carb.lt = True
                if carb.dying:
                    carb.image = 'sheep_22_lt.png'
                else:
                    carb.image = 'sheep_2_lt.png'
        # 对于wk键盘类型的按键响应
        if wk:
            # 如果用户按下W（或I）键且对应角色正在跳跃，则修改该角色的vy值，使其向上进行跳跃；
            if key == key.W and cara.jump:
                cara.vy = -STRENGTH*(1+cara.dying/2)
            if key == key.I and carb.jump:
                carb.vy = -STRENGTH*(1+carb.dying/2)
            # 如果用户按下B键，则记录当前时间，用于控制子弹发射频率；
            if key == key.B:
                balla.time0 = time()
            if key == key.BACKSLASH:
                ballb.time0 = time()
            # 如果用户按下A键，则修改对应角色的朝向、瞄准角度和展示的图片，同样包括方向与D键相反；
            if key == key.A:
                if cara.rt:
                    tonga.angle = 90 - tonga.angle
                if cara.dying:
                    cara.image = 'sheep_11_lt.png'
                else:
                    cara.image = 'sheep_1_lt.png'
                cara.rt = False
            # 如果用户按下D键，则同样操作对应角色，但方向与A键相反。
            if key == key.D:
                if not cara.rt:
                    tonga.angle = 90 - tonga.angle
                if cara.dying:
                    cara.image = 'sheep_11_rt.png'
                else:
                    cara.image = 'sheep_1_rt.png'
                cara.rt = True
            # 如果用户按下L键，则修改另一个角色的朝向、瞄准角度和展示的图片，同样包括方向与LEFT键相反；
            if key == key.L:
                if carb.lt:
                    tongb.angle = -90 - tongb.angle
                if carb.dying:
                    carb.image = 'sheep_22_rt.png'
                else:
                    carb.image = 'sheep_2_rt.png'
                carb.lt = False
            # 如果用户按下J键，则同样操作另一个角色，但方向与LEFT键相反。
            if key == key.J:
                if not carb.lt:
                    tongb.angle = -90 - tongb.angle
                if carb.dying:
                    carb.image = 'sheep_22_lt.png'
                else:
                    carb.image = 'sheep_2_lt.png'
                carb.lt = True

# 定义键盘松开事件函数，参数为key
def on_key_up(key):
    # 如果当前处于游戏场景（即x.gaming为True），则进入到按键响应部分
    if x.gaming:
        # 根据当前所选的语言类型（使用了uk和wk进行判断），响应用户的按键操作
        # 对于uk键盘类型的按键响应
        if uk:
            # 如果用户松开J键，且对应球还未发射，则响应球的发射操作，并在发射前播放对应音效、记录发射时间以及计算球的初速度；
            if key == key.J:
                if not balla.on:
                    balla.on = True
                    sounds.shoot.play()
                    balla.strength = min(time() - balla.time0 + 0.1, 2.5)
                    balla.angle = tonga.angle + 45
                    balla.vx = 50*balla.strength * cos(balla.angle*pi/180)
                    balla.vy = -50*balla.strength * sin(balla.angle*pi/180)
            # 如果用户松开KP3键，且对应球还未发射，则同样响应球的发射操作，并播放音效、记录时间、计算球的初速度。
            if key == key.KP3:
                if not ballb.on:
                    ballb.on = True
                    sounds.shoot.play()
                    ballb.strength = min(time() - ballb.time0 + 0.1, 2.5)
                    ballb.angle = tongb.angle - 45
                    ballb.vx = -50*ballb.strength * cos(ballb.angle*pi/180)
                    ballb.vy = 50*ballb.strength * sin(ballb.angle*pi/180)
        # 对于wk键盘类型的按键响应
        if wk:
            # 如果用户松开B键，且对应球还未发射，则响应球的发射操作，并在发射前播放对应音效、记录发射时间以及计算球的初速度；
            if key == key.B:
                if not balla.on:
                    balla.on = True
                    sounds.shoot.play()
                    balla.strength = min(time() - balla.time0 + 0.1, 2.5)
                    balla.angle = tonga.angle + 45
                    balla.vx = 50*balla.strength * cos(balla.angle*pi/180)
                    balla.vy = -50*balla.strength * sin(balla.angle*pi/180)
            # 如果用户松开BACKSLASH键，且对应球还未发射，则同样响应球的发射操作，并播放音效、记录时间、计算球的初速度。
            if key == key.BACKSLASH:
                if not ballb.on:
                    ballb.on = True
                    sounds.shoot.play()
                    ballb.strength = min(time() - ballb.time0 + 0.1, 2.5)
                    ballb.angle = tongb.angle - 45
                    ballb.vx = -50*ballb.strength * cos(ballb.angle*pi/180)
                    ballb.vy = 50*ballb.strength * sin(ballb.angle*pi/180)

music.play('xyy')
os.environ['SDL_VIDEO_CENTERED']='1'
pgzrun.go()
