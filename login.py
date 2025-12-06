import tkinter as tk
from tkinter import messagebox
import json
import os
import main
import webbrowser

USER_FILE = 'users.json'
HISTORY_FILE = 'history.json'

# 初始化
def init_files():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, 'w') as file:
            json.dump([], file)
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w') as file:
            json.dump([{"best_score": 0}], file)

# 登入界面
def load_data(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

# 保存数据
def save_data(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file)

# 用户登录管理
def login(username, password):
    users = load_data(USER_FILE)
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    return None

# 注册用户
def register_user(username, password):
    users = load_data(USER_FILE)
    for user in users:
        if user['username'] == username:
            print("Username already exists.")
            return False
    users.append({'username': username, 'password': password})
    save_data(USER_FILE, users)
    return True

# 创建登录窗口
def create_login_window():
    # 注册功能实现
    def attempt_register():
        # 获取用户名和密码
        username = username_entry.get()
        password = password_entry.get()
        user = login(username, password)
        if register_user(username, password):
            messagebox.showinfo("Registration Success", "Registration successful.")
        else:
            password_entry.delete(0, tk.END)
            messagebox.showerror("Registration Failed", "Registration failed.")

    # 登录功能实现
    def attempt_login():
        # 获取用户名和密码
        username = username_entry.get()
        password = password_entry.get()
        user = login(username, password)
        if user:
            messagebox.showinfo("Login Success", f"Logged in as {user['username']}")
            login_window.destroy()
            main.main()

        else:
            password_entry.delete(0, tk.END)
            messagebox.showerror("Login Failed", "The account or password is incorrect, login failed.")

    # 打开说明HTML界面
    def open_html():
        webbrowser.open('operate_introduction.html')  # 本地文件

    messagebox.showinfo("提醒","先查看游戏介绍，再登录进入游戏玩。")
    # 登录页面尺寸
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry('500x350')
    login_window.config(bg="#f0f8ff")  # 设置背景颜色

    # 设置字体样式
    font_label = ('Arial', 12)
    font_button = ('Arial', 12, 'bold')

    # 用户名输入框
    tk.Label(login_window, text="Username:", font=font_label, bg="#f0f8ff").pack(pady=(20, 5))
    username_entry = tk.Entry(login_window, font=font_label, width=25, relief="solid", borderwidth=2)
    username_entry.pack(pady=5)

    # 用户密码输入框
    tk.Label(login_window, text="Password:", font=font_label, bg="#f0f8ff").pack(pady=5)
    password_entry = tk.Entry(login_window, font=font_label, show='*', width=25, relief="solid", borderwidth=2)
    password_entry.pack(pady=5)


    # 按钮设置
    tk.Button(login_window, text="Login", command=attempt_login, font=font_button, height=1,width=9, bg="#4CAF50", fg="white", relief="raised", borderwidth=2).place(x=130, y=180)
    tk.Button(login_window, text="Register", command=attempt_register, font=font_button, height=1,width=9, bg="#ff9800", fg="white", relief="raised", borderwidth=2).place(x=270, y=180)
    tk.Button(login_window, text="游戏介绍", command=open_html, font=font_button, height=2, width=15, bg="#2196F3", fg="white", relief="raised", borderwidth=2).place(x=170, y=250)

    # 关闭窗口
    login_window.mainloop()

if __name__ == "__main__":
    init_files()
    create_login_window()