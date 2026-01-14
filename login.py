import tkinter as tk
from tkinter import messagebox
import json
import os
import main
import webbrowser
import sys
import hashlib
import secrets

APP_NAME = "Pygame-Fly"
LEGACY_USER_FILE = "users.json"
LEGACY_HISTORY_FILE = "history.json"

PASSWORD_SCHEME = "pbkdf2_sha256"
PASSWORD_ITERATIONS = 120_000
MIN_USERNAME_LEN = 1
MIN_PASSWORD_LEN = 4
MAX_FIELD_LEN = 64

def get_data_dir():
    # Prefer user profile app data; fall back to current working dir.
    base = os.getenv("LOCALAPPDATA") or os.getenv("APPDATA") or os.path.abspath(".")
    return os.path.join(base, APP_NAME)

def get_data_path(filename):
    return os.path.join(get_data_dir(), filename)

USER_FILE = get_data_path("users.json")
HISTORY_FILE = get_data_path("history.json")

def _hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PASSWORD_ITERATIONS,
    )
    return f"{PASSWORD_SCHEME}${PASSWORD_ITERATIONS}${salt}${dk.hex()}"

def _verify_password(stored, password):
    if not stored.startswith(f"{PASSWORD_SCHEME}$"):
        return stored == password
    try:
        _, iterations, salt, digest = stored.split("$", 3)
        dk = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            int(iterations),
        )
        return secrets.compare_digest(dk.hex(), digest)
    except Exception:
        return False

def _maybe_migrate_legacy_files():
    os.makedirs(get_data_dir(), exist_ok=True)
    if not os.path.exists(USER_FILE) and os.path.exists(LEGACY_USER_FILE):
        users = load_data(LEGACY_USER_FILE)
        save_data(USER_FILE, users)
    if not os.path.exists(HISTORY_FILE) and os.path.exists(LEGACY_HISTORY_FILE):
        history = load_data(LEGACY_HISTORY_FILE)
        save_data(HISTORY_FILE, history)


def resource_path(relative_path):
    """获取资源的绝对路径，兼容PyInstaller打包后的路径"""
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 初始化
def init_files():
    _maybe_migrate_legacy_files()
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, 'w', encoding='utf-8') as file:
            json.dump([], file)
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as file:
            json.dump([{"best_score": 0}], file)

# 登入界面
def load_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return json.load(file)

# 保存数据
def save_data(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file)

def _is_valid_field(value, min_len):
    return isinstance(value, str) and min_len <= len(value) <= MAX_FIELD_LEN

# 用户登录管理
def login(username, password):
    users = load_data(USER_FILE)
    for user in users:
        if user.get('username') == username and _verify_password(user.get('password', ''), password):
            if not user['password'].startswith(f"{PASSWORD_SCHEME}$"):
                user['password'] = _hash_password(password)
                save_data(USER_FILE, users)
            return user
    return None

# 注册用户
def register_user(username, password):
    if not _is_valid_field(username, MIN_USERNAME_LEN):
        print("Invalid username.")
        return False
    if not _is_valid_field(password, MIN_PASSWORD_LEN):
        print("Invalid password.")
        return False
    users = load_data(USER_FILE)
    for user in users:
        if user['username'] == username:
            print("Username already exists.")
            return False
    users.append({'username': username, 'password': _hash_password(password)})
    save_data(USER_FILE, users)
    return True

# 创建登录窗口
def create_login_window():
    # 注册功能实现
    def attempt_register():
        # 获取用户名和密码
        username = username_entry.get()
        password = password_entry.get()
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
            try:
                messagebox.showinfo("Login Success", f"Logged in as {user['username']}")
                login_window.destroy()
                main.main()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        else:
            password_entry.delete(0, tk.END)
            messagebox.showerror("Login Failed", "The account or password is incorrect, login failed.")

    # 打开说明HTML界面
    def open_html():
        webbrowser.open(resource_path('operate_introduction.html'))  # 本地文件

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
