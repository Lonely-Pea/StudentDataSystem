"""
登录界面

"""
import tkinter as tk  # 导入tkinter库并重命名为tk
from tkinter import ttk, messagebox as msg  # 导入tkinter.ttk模块(美化包)和tkinter.messagebox库并重命名为msg

import configparser  # 导入configparser模块以读取配置文件
import time  # 导入time模块实现一些动画

import Desktop  # 导入自定义模块Desktop显示学生信息管理系统主要内容


class SignIn:  # 登录界面对象
    def __init__(self):
        super(SignIn, self).__init__()
        self.cfg = configparser.ConfigParser()  # 实例化configparser
        self.cfg.read("Date\\Config.ini", encoding="utf-8")  # 读取文件

        self.win = self.Window()  # 生成窗口
        self.desktop = self.Desktop()  # 生成桌面主要内容
        # 变量
        self.login_next = tk.IntVar()  # 下次自动登录
        self.username_enter = tk.StringVar()
        self.userpwd_enter = tk.StringVar()
        self.userpwd_enter_second = tk.StringVar()  # 注册界面的二次确认密码

        self.decide()  # 启用判断

        self.win.mainloop()  # 显示窗口

    def Window(self, ):  # 窗口
        win = tk.Tk()  # 生成窗口
        win.title("学生信息管理系统 - 登录界面")  # 设置窗口标题
        width, height = 400, 300  # 窗口长和宽
        screenwidth, screenheight = win.winfo_screenwidth(), win.winfo_screenheight()  # 屏幕长和宽
        size = "%dx%d+%d+%d" % (width, height,
                                (screenwidth - width) / 2, (screenheight - height) / 2  # 使窗口居于屏幕中间
                                )
        win.geometry(size)  # 设置窗口的大小和位置
        win.resizable(False, False)  # 设置窗口大小不可更改
        return win  # 返回窗口变量

    def Desktop(self, ):  # 桌面内容
        desktop = tk.Frame(self.win, )  # 桌面框架
        desktop.pack(fill=tk.BOTH, expand=True)  # 放置框架

        return desktop  # 返回桌面框架变量

    def login_(self, ):  # 登录界面
        tk.Label(self.desktop, text="登录用户", font=("微软雅黑", 30)).pack()
        tk.Label(self.desktop, text="用户名：", font=("微软雅黑",), anchor="w").place(x=10, y=80, width=80, height=25)
        tk.Label(self.desktop, text="密码：", font=("微软雅黑",), anchor="w").place(x=10, y=115, width=80, height=25)

        ttk.Entry(self.desktop, textvariable=self.username_enter).place(x=90, y=80, width=150, height=25)
        ttk.Entry(self.desktop, textvariable=self.userpwd_enter).place(x=90, y=115, width=150, height=25)

        ttk.Button(self.desktop, text="X", cursor="hand2", command=lambda: self.username_enter.set("")).place(x=240, y=80, width=25, height=25)
        ttk.Button(self.desktop, text="X", cursor="hand2", command=lambda: self.userpwd_enter.set("")).place(x=240, y=115, width=25, height=25)

        ttk.Checkbutton(self.desktop, text="下次自动登录", cursor="hand2", variable=self.login_next).place(x=90, y=145, height=25)

        ttk.Button(self.desktop, text="确定登录", cursor="hand2", command=self.login_in).place(x=10, y=215, width=122, height=25)
        ttk.Button(self.desktop, text="退出", cursor="hand2", command=lambda: self.win.destroy()).place(x=143, y=215, width=122, height=25)

        # 右半边提示文本
        tk.Label(self.desktop, bg="black").place(x=270, y=80, width=1, height=160)  # 分隔线
        text = tk.Text(self.desktop, wrap="none")  # 文本框
        text.place(x=275, y=80, width=105, height=140)
        scrollbar = ttk.Scrollbar(self.desktop, command=text.yview)
        scrollbar.place(x=380, y=80, height=140)
        scrollbar2 = ttk.Scrollbar(self.desktop, command=text.xview, orient=tk.HORIZONTAL)  # 横向滚动轴
        scrollbar2.place(x=275, y=220, width=105)
        text.config(yscrollcommand=scrollbar.set)
        text.config(xscrollcommand=scrollbar2.set)

        help_text = """登录提示
(1)如何登录
输入正确的账号和密码即可登录！
(2)为什么要登录
登录可以打开学生信息管理系统！
(3)注意事项
登录错误次数超过3次就会删除用户全部信息！
"""
        text.insert(tk.END, help_text)
        text.config(state="disabled")

        # 判断是否自动登录
        if self.cfg.get("User", "login_next") == "1":
            self.login_next.set(1)
            self.username_enter.set(self.cfg.get("User", "username"))
            self.userpwd_enter.set(self.cfg.get("User", "userpwd"))
            msg.showinfo("登陆成功！",
                         "你好，" + self.cfg.get("User", "username") + "。即将进入学生信息管理系统！按确定进入！")
            self.win.destroy()

    def login_in(self, ):  # 确定登录
        username_enter = self.username_enter.get()
        userpwd_enter = self.userpwd_enter.get()
        if username_enter != "" and userpwd_enter != "":
            if username_enter == self.cfg.get("User", "username") and userpwd_enter == self.cfg.get("User", "userpwd"):
                self.cfg.set("User", "login_next", str(self.login_next.get()))
                self.cfg.write(open("Date\\Config.ini", "w"))
                msg.showinfo("登陆成功！", "你好，" + self.cfg.get("User", "username") + "。即将进入学生信息管理系统！按确定进入！")
                self.win.destroy()
            else:
                if username_enter != self.cfg.get("User", "username"):
                    self.light(self.username_enter, "用户名输入错误！")
                elif userpwd_enter != self.cfg.get("User", "userpwd"):
                    self.light(self.userpwd_enter, "密码输入错误！")
        else:
            if username_enter == "":
                self.light(self.username_enter, "用户名不能为空！")
            elif userpwd_enter == "":
                self.light(self.userpwd_enter, "密码不能为空！")

    def enroll_(self, ):  # 注册界面
        tk.Label(self.desktop, text="注册用户", font=("微软雅黑", 30)).pack()
        tk.Label(self.desktop, text="用户名：", font=("微软雅黑", ), anchor="w").place(x=10, y=80, width=80, height=25)
        tk.Label(self.desktop, text="密码：", font=("微软雅黑", ), anchor="w").place(x=10, y=115, width=80, height=25)
        tk.Label(self.desktop, text="确定密码：", font=("微软雅黑", ), anchor="w").place(x=10, y=150, width=80, height=25)

        ttk.Entry(self.desktop, textvariable=self.username_enter).place(x=90, y=80, width=150, height=25)
        ttk.Entry(self.desktop, textvariable=self.userpwd_enter).place(x=90, y=115, width=150, height=25)
        ttk.Entry(self.desktop, textvariable=self.userpwd_enter_second).place(x=90, y=150, width=150, height=25)

        ttk.Button(self.desktop, text="X", cursor="hand2", command=lambda: self.username_enter.set("")).place(x=240, y=80, width=25, height=25)
        ttk.Button(self.desktop, text="X", cursor="hand2", command=lambda: self.userpwd_enter.set("")).place(x=240, y=115, width=25, height=25)
        ttk.Button(self.desktop, text="X", cursor="hand2", command=lambda: self.userpwd_enter_second.set("")).place(x=240, y=150, width=25, height=25)

        ttk.Checkbutton(self.desktop, text="下次自动登录", cursor="hand2", variable=self.login_next).place(x=90, y=180, height=25)

        ttk.Button(self.desktop, text="确定注册", cursor="hand2", command=self.enroll_in).place(x=10, y=215, width=122, height=25)
        ttk.Button(self.desktop, text="退出", cursor="hand2", command=lambda: self.win.destroy()).place(x=143, y=215, width=122, height=25)

        # 右半边提示文本
        tk.Label(self.desktop, bg="black").place(x=270, y=80, width=1, height=160)  # 分隔线
        text = tk.Text(self.desktop, wrap="none")  # 文本框
        text.place(x=275, y=80, width=105, height=140)
        scrollbar = ttk.Scrollbar(self.desktop, command=text.yview)
        scrollbar.place(x=380, y=80, height=140)
        scrollbar2 = ttk.Scrollbar(self.desktop, command=text.xview, orient=tk.HORIZONTAL)  # 横向滚动轴
        scrollbar2.place(x=275, y=220, width=105)
        text.config(yscrollcommand=scrollbar.set)
        text.config(xscrollcommand=scrollbar2.set)

        help_text = """注册提示
(1)账号密码格式
账号：账号格式可以自由设置，但不能为None且不能为空
密码：密码格式必须包含数字和字母两种类型，并且密码长度必须为8
(2)账号密码用途
账号密码用于储存用户信息。
(3)注意事项
[1]请勿更改Date文件夹下的config.ini文件！否则可能会使数据丢失
[2]输入的账号和密码将会保存到本地。该软件不会窃取用户的个人信息。
        """
        text.insert(tk.END, help_text)
        text.config(state="disabled")

    def enroll_in(self, ):  # 确定注册
        username_enter = self.username_enter.get()
        userpwd_enter = self.userpwd_enter.get()
        userpwd_enter_second = self.userpwd_enter_second.get()
        login_next = self.login_next.get()
        if username_enter == "":
            self.light(self.username_enter, "用户名不能为空！")
        elif userpwd_enter == "":
            self.light(self.userpwd_enter, "密码不能为空！")
        elif userpwd_enter_second == "":
            self.light(self.userpwd_enter_second, "密码二次确认不能为空！")
        elif userpwd_enter_second != userpwd_enter:
            self.light(self.userpwd_enter_second, "密码二次确认输入与密码不相同！")
        else:
            if len(userpwd_enter) == 8:
                if username_enter != "None":
                    self.cfg.set("User", "username", self.username_enter.get())
                    self.cfg.set("User", "userpwd", self.userpwd_enter.get())
                    self.cfg.set("User", "login_next", str(self.login_next.get()))
                    self.cfg.write(open("Date\\Config.ini", "w"))
                    msg.showinfo("注册成功！", "你好，" + self.cfg.get("User", "username")+"。即将进入学生信息管理系统！按确定进入！")
                    self.win.destroy()
                else:
                    self.light(self.username_enter, "账号名称不能是None！")
            else:
                self.light(self.userpwd_enter, "密码长度必须为八位！")

    def light(self, option, text):  # 闪烁文本
        for i in range(0, 4):
            for i2 in range(0, 2):
                if i2 == 0:
                    option.set(text)
                else:
                    option.set("")
                self.win.update()
                time.sleep(0.05)
        option.set(text)

    def decide(self, ):  # 判断是登录界面还是注册界面
        if self.cfg.get("User", "username") == "None" and self.cfg.get("User", "userpwd") == "None":
            self.enroll_()  # 启用注册
        else:
            self.login_()  # 启用登录界面


if __name__ == "__main__":
    main = SignIn()  # 登录界面主要程序
