import pygame
from pygame import mixer
import sys
import Sprites
from Text import *
from config import *
import login
import time
import random



def main():

    # 初始化
    pygame.init()
    t = time.localtime()

    # initialize window
    # 设置主栏图标
    icon = pygame.image.load("GenshinImpact.ico")
    pygame.display.set_icon(icon)
    # 主栏游戏名
    pygame.display.set_caption("原神启动")
    # 设置窗口大小
    window = pygame.display.set_mode(WINDOW_SIZE)
    # 设置鼠标光标
    png = pygame.image.load("images/aniya.png")
    # imageWidth = png.get_width()
    # imageHeight = png.get_height()
    pygame.mouse.set_cursor((16, 16), png)

    # 加载背景音乐
    mixer.music.load("music/bg_music.mp3")
    mixer.music.set_volume(MUSIC_VOLUME)
    # 加载跳跃声效
    jump = mixer.Sound("music/jump.wav")
    jump.set_volume(MUSIC_VOLUME)
    # 加载碰撞死亡声效
    hit = mixer.Sound("music/hit.mp3")
    hit.set_volume(MUSIC_VOLUME)
    # 标题
    title = pygame.image.load("images/yuanshen1.png")

    # 下载精灵（派蒙）
    paimon = Sprites.Paimon()
    # 柱子对象
    pillars = Sprites.PillarGroup(window, 300)
    # 下载草
    grass = Sprites.Grass()
    # 创建精灵组
    sprites = pygame.sprite.Group(paimon, grass, pillars)
    # 设置时钟
    clock = pygame.time.Clock()


    """
        # 时间管理对象
        # time_manager = TimeManager()
        # pygame自带的计数对象
        
        class TimeManager:
        # 其实pygame.time.Clock有这个功能
        # 一个用于游戏计时的类，通过逐帧累加精确计时
        # 帧数代表一秒钟播放的画面片段


        def __init__(self):
            # 计数归零
            self.count = 0

        def get_time(self):
            # 经过的多少帧画面 * 帧数的倒数 = 对应的时间
            return self.count * TIMESPAN

        def step(self):
            # 每一个画面--一帧计数加一
            self.count += 1
            
    """


    # 准备阶段
    def prepare():
        # 准备阶段音乐播放
        mixer.music.play()
        run = True
        while run:
            # 循环获取事件，监听事件
            # FlyPaimon.display.update()
            for event in pygame.event.get():
                # MOUSEBUTTONDOWN--鼠标事件
                if in_start():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # 点击--准备阶段结束--开始游戏阶段
                        run = False
                        # 跳跃音效播放
                        jump.play()
                        # 派蒙跳一下
                        paimon.jump()
                # 判断用户是否点了关闭按钮
                if event.type == pygame.QUIT:
                    # 卸载所有pygame模块
                    pygame.quit()
                    # 终止程序
                    sys.exit()

                """
                    这样顺序的原因：FlyPaimon.quit()是pygame.init()函数的一种相反的函数，它运行的代码会使得Pygame库停止工作。
                    在调用sys.exit()终止程序之前，总是应该先调用pygame.quit()。通常，由于程序退出之前，Python总是会关闭pygame，
                    这不会真的有什么问题。但是，在IDLE中有一个bug，如果一个Pygame程序在调用pygame.quit()之前就终止了，将会导致IDLE挂起。
                    sys模块的exit函数，通过抛出一个SystemExit异常来尝试结束程序，Python代码可以捕获这个异常来进行一些程序退出前的清理工作，
                    也可以不退出程序。sys.exit函数同样可以带一个参数来作为程序的退出码，默认是0。
                """

            # 屏幕背景图RGB
            window.fill((130, 150, 200))

            # 获取现在的时间
            t = pygame.time.get_ticks()/1000
            # 开始按键
            start_Button(window, (0,0))
            # 派蒙的掉落
            paimon.prepare(window, t)
            # 更新草一帧移动
            grass.update(window, t)
            window.blit(title, ((WINDOW_SIZE[0]-title.get_width())//2, WINDOW_SIZE[1]-title.get_height()-300))

            # 更新屏幕内容
            pygame.display.flip()
            # 代表一帧--计数加一
            # time_manager.step()
            # 设置游戏的FPS
            clock.tick(FPS)
            """
            当肉眼看不清图片动画变化的时候那么将呈现的就是连续的画面--动画片
            """


    def start():
        # run = True
        t_prepare = pygame.time.get_ticks()/1000
        while True:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        jump.play()
                        # 派蒙跳跃
                        paimon.jump()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    jump.play()
                    paimon.jump()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # 填充背景
            window.fill((130, 150, 200))

            # 获取当前时间
            t = pygame.time.get_ticks()/1000

            # 显示时间
            show_text(window, str(round(t - t_prepare, 2)), (0, -130))

            # 更新精灵位置
            pillars.update()
            paimon.start(window)
            grass.update(window)
            # print(pillars.spd, grass.spd)
            pillars.gap = random.randint(180,350)


            # noinspection PyTypeChecker
            check1 = pygame.sprite.spritecollideany(paimon, pillars, pygame.sprite.collide_rect_ratio(0.8))
            # noinspection PyTypeChecker
            check2 = pygame.sprite.collide_rect(paimon, grass)

            # 检测碰撞
            if check1 or check2:
                hit.play()
                paimon.kill()
                return round(t - t_prepare, 2)
                # run = False

            # 更新屏幕
            pygame.display.flip()
            # time_manager.step()
            clock.tick(FPS)


    def end():
        mixer.music.stop()
        dic1 = login.load_data(login.HISTORY_FILE)
        run = True
        while run:
            while paimon.rect.bottom <= WINDOW_SIZE[1] - grass.size[1] + 10:
                paimon.image.get_masks()
                # 灰色
                window.fill((128, 128, 128))
                # 显示时间
                show_text(window, str(round(t_end, 2)), (0, -130))
                pillars.end()
                # t = time_manager.get_time()
                paimon.end(window)
                grass.end(window)
                pygame.display.flip()
                # time_manager.step()
                clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True

            # 黑色
            window.fill((0, 0, 0))
            show_text(window, str(t_end), (0, -100), font=fp_font)
            show_text(window, "最佳记录: " + str(dic1[0]['best_score']), (0, 50))
            img = pygame.image.load("images/siwang.png")
            show_image(window, img,(0, 200))
            show_image(window, paimon.image4, (-200, 200))
            pygame.display.flip()


            # pygame.time.delay(1500)


    r = True
    while r:
        # 下载精灵（派蒙）
        paimon = Sprites.Paimon()
        # 柱子对象
        pillars = Sprites.PillarGroup(window, 300)
        # 下载草
        grass = Sprites.Grass()
        # 创建精灵组
        sprites = pygame.sprite.Group(paimon, grass, pillars)
        # 设置时钟
        clock = pygame.time.Clock()
        prepare()
        t_end = start()
        ls = login.load_data(login.HISTORY_FILE)
        dic = {'time': 0, 'history_score': 0}
        s = "{}-{}-{} {}:{}:{}".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
        dic['time'], dic['history_score'] = s, t_end
        ls.append(dic)
        if t_end > ls[0]['best_score']:
            ls[0]['best_score'] = t_end
        login.save_data(login.HISTORY_FILE, ls)
        r = end()
    pygame.quit()
