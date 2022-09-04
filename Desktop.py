"""
软件主要界面

"""
import tkinter as tk
from tkinter import ttk, messagebox as msg

import configparser

import time


class Desktop:  # 主要界面
    def __init__(self, ):
        super(Desktop, self).__init__()

        self.cfg = configparser.ConfigParser()  # 实例化configparser
        self.cfg.read("Date\\Config.ini")  # 读取配置文件

        self.win = self.Window()  # 创建窗口
        self.desktop = self.Desktop_()
        # 变量
        self.in_more_data = tk.IntVar()  # 是否打开了更多用户信息
        self.in_more_data.set(0)

        self.frm_user_bar = self.user_bar()
        self.Basic_TreeView()  # 显示表格

        self.win.mainloop()

    def Window(self, ):  # 主窗口
        win = tk.Tk()  # 生成主窗口
        win.title("Python学生信息管理系统 - by Lonely-Pea")  # 设置标题
        width, height, screenwidth, screenheight = 600, 400, win.winfo_screenwidth(), win.winfo_screenheight()
        size = f"{width}x{height}+{int((screenwidth - width) / 2)}+{int((screenheight - height) / 2)}"
        win.geometry(size)  # 设置大小和位置
        win.resizable(False, False)  # 设置窗口大小不可更改

        return win  # 返回win变量

    def Desktop_(self, ):  # 桌面内容
        desktop = tk.Frame(self.win, )
        desktop.pack(fill=tk.BOTH, expand=True)

        return desktop

    def user_bar(self, ):  # 用户信息栏
        global frm_user_bar, username_label  # 将这些变量设置为全局变量方便在其他函数内更改和使用
        frm_user_bar = tk.Frame(self.desktop, bg="white")  # 用户信息栏承载框架
        frm_user_bar.place(x=0, y=0, width=600, height=30)

        username_label = tk.Label(frm_user_bar, text=self.cfg.get("User", "username") + "↓", font=("微软雅黑",),
                                  bg="white", cursor="hand2")
        username_label.place(x=0, y=0)

        username_label.bind("<Button-1>", self.more_data)  # 点击事件

        return frm_user_bar  # 返回框架变量

    def more_data(self, event=None):  # 用户信息栏更多信息
        global frm_more_date
        try:
            frm_more_date.destroy()
        except NameError:
            pass
        if self.in_more_data.get() == 0:
            self.in_more_data.set(1)
            username_label.config(text=self.cfg.get("User", "username") + "↑")
            frm_more_date = tk.Frame(self.desktop, bg="white")
            frm_more_date.place(x=username_label.winfo_reqwidth() - 30, y=35, width=200, height=93)

            entry_username = ttk.Entry(frm_more_date, font=("微软雅黑",), state="normal")
            entry_username.place(x=1, y=0, width=198, height=30)
            entry_userpwd = ttk.Entry(frm_more_date, font=("微软雅黑",), state="normal")
            entry_userpwd.place(x=1, y=31, width=198, height=30)

            entry_username.insert(tk.END, "用户名：" + self.cfg.get("User", "username"))
            entry_userpwd.insert(tk.END, "密码：" + self.cfg.get("User", "userpwd"))

            entry_username.config(state="disabled")
            entry_userpwd.config(state="disabled")

            ttk.Button(frm_more_date, text="更改用户信息", cursor="hand2", command=self.change_user_data).place(x=0,
                                                                                                                y=62,
                                                                                                                width=200,
                                                                                                                height=30)
        else:
            self.in_more_data.set(0)
            username_label.config(text=self.cfg.get("User", "username") + "↓")

    def change_user_data(self, ):  # 更改用户信息
        global change_window
        try:
            self.light_window(change_window)
        except Exception:
            change_name = tk.StringVar()
            change_pwd = tk.StringVar()
            change_window = tk.Toplevel(self.win)  # 新建一个toplevel窗口
            change_window.title("更改用户信息")
            width, height, screenwidth, screenheight = 400, 300, change_window.winfo_screenwidth(), change_window.winfo_screenheight()
            size = f"{width}x{height}+{int((screenwidth - width) / 2)}+{int((screenheight - height) / 2)}"
            change_window.geometry(size)  # 设置窗口大小和位置
            change_window.resizable(False, False)  # 设置窗口不可更改大小和位置
            change_window.attributes("-topmost", True)  # 设置窗口位于顶部

            tk.Label(change_window, text="更改用户信息", font=("微软雅黑", 30)).pack()
            tk.Label(change_window, text="重设用户名：", font=("微软雅黑",), anchor="w").place(x=10, y=80, width=100,
                                                                                              height=25)
            tk.Label(change_window, text="重设密码：", font=("微软雅黑",), anchor="w").place(x=10, y=115, width=100,
                                                                                            height=25)

            ttk.Entry(change_window, textvariable=change_name).place(x=110, y=80, width=150, height=25)

            ttk.Entry(change_window, textvariable=change_pwd).place(x=110, y=115, width=150, height=25)

            ttk.Button(change_window, text="X", cursor="hand2", command=lambda: change_name.set("")).place(
                x=260, y=80, width=25, height=25)
            ttk.Button(change_window, text="X", cursor="hand2", command=lambda: change_pwd.set("")).place(
                x=260, y=115, width=25, height=25)

            ttk.Button(change_window, text="确定更改", cursor="hand2",
                       command=lambda: self.change_(change_name, change_pwd)).place(x=10, y=215, width=122, height=25)
            ttk.Button(change_window, text="退出", cursor="hand2", command=lambda: change_window.destroy()).place(x=143,
                                                                                                                  y=215,
                                                                                                                  width=122,
                                                                                                                  height=25)

    def change_(self, name_var, pwd_var):  # 确定转化
        name_enter = name_var.get()
        pwd_enter = pwd_var.get()
        if name_enter != "" and pwd_enter != "":
            if len(pwd_enter) != 8:
                change_window.attributes("-topmost", False)
                self.light(pwd_var, "密码长度必须是八位！")
                change_window.attributes("-topmost", True)
            else:
                if name_enter != "None":
                    msg.showinfo("更改成功！", "已经成功更改信息！点击确定以退出！")
                    self.cfg.write(open("Date\\Config.ini", "w"))
                    change_window.destroy()
                else:
                    change_window.attributes("-topmost", False)
                    self.light(name_var, "用户名不能为None！")
                    change_window.attributes("-topmost", True)
        else:
            if name_enter == "" and pwd_enter == "":
                change_window.attributes("-topmost", False)
                msg.showinfo("提示", "已取消更改！因为用户没有更改任何内容！")
                change_window.destroy()
            else:
                if pwd_enter == "":
                    change_window.attributes("-topmost", False)
                    msg.showinfo("更改成功！", "已经成功更改信息！点击确定以退出！")
                    self.cfg.set("User", "username", name_enter)
                    self.cfg.write(open("Date\\Config.ini", "w"))
                    change_window.destroy()
                else:
                    change_window.attributes("-topmost", False)
                    msg.showinfo("更改成功！", "已经成功更改信息！点击确定以退出！")
                    self.cfg.set("User", "userpwd", pwd_enter)
                    self.cfg.write(open("Date\\Config.ini", "w"))
                    change_window.destroy()

    def Basic_TreeView(self, ):  # 表格
        global table
        datas = ["姓名", "年龄", "性别", "学号", "班级", "出生年月", "成绩"]

        scrollbar_x = ttk.Scrollbar(self.desktop, orient=tk.HORIZONTAL)
        scrollbar_y = ttk.Scrollbar(self.desktop)
        scrollbar_x.place(x=16, y=250, width=566)
        scrollbar_y.place(x=582, y=50, height=200)

        table = ttk.Treeview(self.desktop, height=10, columns=datas, show="headings", xscrollcommand=scrollbar_x.set,
                             yscrollcommand=scrollbar_y.set)

        for column in datas:
            table.heading(column=column, text=column, anchor=tk.CENTER)  # 定义表头
            if column != "成绩":
                table.column(column=column, width=80, minwidth=80, anchor=tk.CENTER)  # 定义列
            else:
                table.column(column=column, width=250, minwidth=250, anchor=tk.CENTER)

        scrollbar_x.config(command=table.xview)
        scrollbar_y.config(command=table.yview)
        table.place(x=16, y=50, width=566, height=200)

        ttk.Button(self.desktop, text="刷新", cursor="hand2").place(x=16, y=280, width=50, height=25)
        ttk.Button(self.desktop, text="更改", cursor="hand2").place(x=66, y=280, width=50, height=25)
        ttk.Button(self.desktop, text="删除", cursor="hand2").place(x=116, y=280, width=50, height=25)
        ttk.Button(self.desktop, text="添加", cursor="hand2").place(x=166, y=280, width=50, height=25)
        ttk.Button(self.desktop, text="导出", cursor="hand2").place(x=216, y=280, width=50, height=25)
        ttk.Button(self.desktop, text="帮助", cursor="hand2").place(x=266, y=280, width=50, height=25)

        self.insert_()  # 添加信息到table中

    def flushed(self, ):  # 刷新表格内容
        ...

    def change_student(self, ):  # 更改学生信息
        ...

    def delete_student(self, ):  # 删除学生信息
        ...

    def add_student(self, ):  # 添加学生信息
        ...

    def Export(self, ):  # 导出工作表
        ...

    def check_help(self, ):  # 查看帮助信息
        ...

    def insert_(self, ):  # 确定和更改table的内容
        table.delete(*table.get_children())
        all_student = self.cfg.options("all_students")  # 获取全部的学生名单
        print(all_student)
        student_data = [
        ]
        all_options = ["name", "age", "gender", "ID", "class", "birth", "score"]
        for i in range(0, len(all_student)):
            student_data_middle = [0, 0, 0, 0, 0, 0, 0]
            for ii in range(0, 7):
                student_data_middle[ii] = self.cfg.get(f"{all_student[i]}", f"{all_options[ii]}")
            student_data.insert(i, student_data_middle)
            print(student_data)
        for index, data in enumerate(student_data):
            table.insert('', tk.END, values=data)  # 添加数据到末尾

    def light_window(self, master):  # 窗口闪烁
        for i in range(0, 4):
            for i2 in range(0, 2):
                if i2 == 0:
                    change_window.withdraw()  # 隐藏窗口
                else:
                    change_window.deiconify()  # 显示隐藏窗口
                time.sleep(0.05)
            change_window.deiconify()  # 显示隐藏窗口

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


if __name__ == "__main__":
    main = Desktop()  # 显示主要内容
