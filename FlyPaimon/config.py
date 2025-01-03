
# 这个文件用来存储一些常量/超参数，主要是为了让游戏渲染得更加流畅

# 帧率
FPS = 60  # 最好是240的因数
TIMESPAN = 1 / FPS

# 背景的加速度
BG_AC = 0.001
# 背景的速度
BG_SPEED = 240
# 移动的距离
BG_DX = round(BG_SPEED * TIMESPAN)

# 加速度的加速度
PAIMON_DROP_AACC = 0
# 派蒙下落的加速度
PAIMON_DROP_ACC = 800
# 派蒙跳跃的速度
PAIMON_JUMP_SPD = -270

# 窗口大小
WINDOW_SIZE = [1080, 640]

# 音乐
MUSIC_VOLUME = 0.3


