import pygame, sys

# 初始化
pygame.init()
# 屏幕分辨率
screen = pygame.display.set_mode((640, 480))
# 游戏名字
pygame.display.set_caption("Hello World")

while True:
    # 固定模板
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()

        # 键鼠事件--能够返回按下的键
        if event.type == pygame.KEYDOWN:
         key=pygame.key.name(event.key)
         print (key, "Key is pressed")

        if event.type == pygame.KEYUP:
         key=pygame.key.name(event.key)
         print (key, "Key is released")

        # 鼠标事件
        if event.type == pygame.MOUSEBUTTONDOWN:
          pos = pygame.mouse.get_pos()
          btn = pygame.mouse
          print("x = {}, y = {}".format(pos[0], pos[1]))

