# Pygame-Fly

借鉴于 *ken-2511* 的飞翔派蒙，改进版本

增加计数器，并添加特色阿玛尼鼠标指针，修改开头原神，以及游戏名，增加游戏的趣味性 <br>
添加了登录设置与本地 *html* 说明和 *json*
数据记录最高数据（本来打算做一个后端可以数据互通，有一个实时排名榜，创建账号的玩家可以比，没能完成）<br>
然后游戏设置了高低间隔不同的管道增加难度，有一个管道加速度设置，但是不知道为什么不能均匀的速度变化，会在某一个时间点爆发....（这里会有穿模）<br>
增加死亡结束画面，参考与 *steam* 游戏 *Dodge Show*

## 启动文件

`python login.py`

> **./fonts:** 存放字体文件 <br>
> **./music:** 存放音频文件 <br>
> **./images:** 存放图片文件 <br>
> **config:** 调整基本参数 <br>
> **main:** 主文件，逻辑存放 <br>
> **login:** 登入逻辑 <br>
> **Sprites:** 精灵类 <br>
> **Text:** 文本图片显示封装 <br>

**环境：**

| 主要模块   | 版本     |
|--------|--------|
| python | 3.11.9 |
| pygame | 2.5.2  |
| tK     | 8.6.12 |

## 登入画面：

可以输入用户名和密码，点击注册后就可以登入了，我事先是保存了一个空账号密码的用户，可以直接登入方便，当然这个功能是为了后面扩展多人游戏准备的
，然后可以先看写的一个小小的游戏介绍，就可以进入游戏啦。

<img alt="登入画面" src="./images/login_huamian.png">

## 开始 && 游戏 && 结束界面：

<div style="display: flex; justify-content: space-around;">
  <div style="text-align: center;">
    <img alt="开始界面" src="./images/start_huamian.png" style="width:80%; max-width:800px;">
    <p>开始界面</p>
  </div>
  <div style="text-align: center;">
    <img alt="游戏界面" src="./images/game_huamian.png" style="width:80%; max-width:800px;">
    <p>游戏界面</p>
  </div>
  <div style="text-align: center;">
    <img alt="死亡界面" src="./images/died_huamian.png" style="width:80%; max-width:800px;">
    <p>死亡界面</p>
  </div>
</div>

最后希望大家可以玩的开心





