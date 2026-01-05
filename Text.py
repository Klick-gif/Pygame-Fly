# 这个文件负责管理所有与文字相关的事情

import pygame
import os 
import sys
from config import *

# 获取资源路径函数
def resource_path(relative_path):
    """获取资源路径, 兼容打包"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

pygame.font.init()
fp_font = pygame.font.Font(resource_path("fonts/zh-cn.ttf"), 72)
s_font = pygame.font.Font(resource_path("fonts/zh-cn.ttf"), 45)
s_size = s_font.size("start")
s_original_pos = ((WINDOW_SIZE[0] - s_size[0]) // 2, (WINDOW_SIZE[1] - s_size[1]) * 1.4 // 2)
s_rect = pygame.rect.Rect(s_original_pos, s_size)

def show_text(window, text, bias, font=s_font):
    t = font.render(text, True, (255, 255, 255))
    rect = t.get_rect()
    rect.left = (WINDOW_SIZE[0] - rect.width) // 2 + bias[0]
    rect.top = (WINDOW_SIZE[1] - rect.height) * 0.618 // 2 + bias[1]
    window.blit(t, rect)


def in_start():
    """判断鼠标是否在start文字区域内"""
    pos = pygame.mouse.get_pos()
    return s_rect.left < pos[0] < s_rect.right and s_rect.top < pos[1] < s_rect.bottom


def start_Button(window, bias):
    s_rect[:2] = s_original_pos[0] + bias[0], s_original_pos[1] + bias[1]
    if in_start():
        color = (255, 200, 200)
    else:
        color = (255, 255, 255)
    text = s_font.render("start", True, color)
    window.blit(text, s_rect)

def show_image(window, img, bias):
    rect = img.get_rect()
    rect.left = (WINDOW_SIZE[0] - rect.width) // 2 + bias[0]
    rect.top = (WINDOW_SIZE[1] - rect.height) * 0.618 // 2 + bias[1]
    window.blit(img, rect)


