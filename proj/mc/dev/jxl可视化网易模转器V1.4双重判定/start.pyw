# coding=utf-8

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import ctypes

import uis as uis
from tkinter import font



# 创建Tkinter的根窗口
root = tk.Tk()
root.title(uis.ToolName)
# 禁止调整窗口大小
root.resizable(False, False)

#root.geometry("1200x600")

# 设置窗口图标
#root.iconbitmap('jxl addons icon-128.ico') # 无法直接隐藏logo，但是可以用透明ico代替
#root.overrideredirect(1)  # 设置为1时，窗口标题栏隐藏

# 获取窗口大小
GetW = root.winfo_screenwidth()
GetH = root.winfo_screenheight()
print GetW,GetH
# 设置DPI感知
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# 获取缩放因子
try:
    # Windows 8.1 或更高版本
    ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
except AttributeError:
    # Windows 8 及更低版本
    ScaleFactor = ctypes.windll.shcore.GetProcessDpiAwareness()

# 设置Tkinter的缩放
if ScaleFactor:
    root.tk.call('tk', 'scaling', ScaleFactor / 60.0)



#=====|配置|====================================================
PZ_sx = None # 筛选字符串
PZ_tt = None # 贴图
PZ_mm = None # 命名
PZ_ao = True # 遮罩



#=====|配置|====================================================



# 创建一个样式对象
style = ttk.Style()

# 设置主题
style.theme_use('default')  # 你可以选择 'clam', 'alt', 'default', 'classic' 等主题



# 圆角按钮案例
style = ttk.Style()

style.configure('bt1.TButton', relief='solid', font=('微软雅黑', 16))
style.configure('bt2.TButton', relief='solid', font=('微软雅黑', 12), background=uis.BGC0)
style.configure('bt3.TButton', relief='solid', font=('微软雅黑', 8))



font_t1 = font.Font(family="Microsoft YaHei", size=16, weight="bold")
font_t2 = font.Font(family="Microsoft YaHei", size=12, weight="bold")
font_t3 = font.Font(family="Microsoft YaHei", size=8)

font_p1 = font.Font(family="Microsoft YaHei", size=12, weight="normal")
font_p2 = font.Font(family="幼圆", size=12)
font_p3 = font.Font(family="幼圆", size=10)
font_p4 = font.Font(family="幼圆", size=7)
# 创建顶部的grid布局



#columnspan=2 占几列的意思
FG1 = tk.Frame(root)
FG1.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

FG2 = tk.Frame(FG1, bg=uis.BGC3)
FG2.grid(row=0, column=0, sticky="nsew", ipadx=20)

FG3 = tk.Frame(FG1, bg=uis.BGC3)
FG3.grid(row=0, column=1, sticky="nsew", ipadx=20)

LB = None

def start():
    global PZ_sx


    # 点击刷新按钮
    def ShuaXin():
        if cbvk.get() == True:
            PZ_sx = entryk.get()
            ListBox(PZ_sx)
        else:
            ListBox('')



    label = tk.Label(FG2, text="---模型检索---", font=font_p2, bg=uis.BGC3)
    label.grid(row=0, column=0)

    button = ttk.Button(FG2, text='刷新', style='bt2.TButton', width=15, command=ShuaXin)
    button.grid(row=1, column=0, padx=10, pady=20)

    label = tk.Label(FG2, text="点击刷新方块列表", font=font_p3, bg=uis.BGC3)
    label.grid(row=2, column=0)


    FGk = tk.Frame(FG2, bg=uis.BGC3)
    FGk.grid(row=3, column=0)

    def OnC1():

        type = cbvk.get()
        if type == True:
            PZ_sx = entryk.get()
            entryk.grid(row=0, column=2, pady=10, sticky='nsew')
        else:
            PZ_sx = ''
            entryk.grid_forget()




    cbvk = BooleanVar()
    Checkbutton(FGk, text="筛选", variable=cbvk, command=OnC1).grid(row=0, column=1, padx=10, pady=10, sticky='nsew')


    entryk = tk.Entry(FGk, foreground=uis.BGC2, width=14, font=font_p3)
    #entryk.configure(validate="focusout", validatecommand=Entryk)
    entryk.grid_forget()



    def ZhuanHuan():
        PZ_mm = radtxt1.get()
        PZ_tt = radtxt2.get()

        AllData = [cbvk.get(), entryk.get(), radval1.get(), PZ_mm, radval2.get(), PZ_tt, PZ_ao]
        #print '信息整理  筛选%s-%s|命名%s-%s|贴图%s-%s|遮罩%s' %(cbvk.get(), entryk.get(), radval1.get(), PZ_mm, radval2.get(), PZ_tt, PZ_ao)

        uis.MAKE(AllData)


    #分割Separator(FG2).grid(row=3, column=0)


    label = tk.Label(FG3, text="---模型配置---", font=font_p2, bg=uis.BGC3)
    label.grid(row=0, column=0)

    button = ttk.Button(FG3, text='转换', style='bt2.TButton', width=15, command=ZhuanHuan)
    button.grid(row=1, column=0, padx=10, pady=20, columnspan=3)


    FGx1 = tk.Frame(FG3, bg=uis.BGC3)
    FGx1.grid(row=2, column=0, sticky="nsew")



    label = tk.Label(FGx1, text="命名空间", font=font_p3, bg=uis.BGC3)
    label.grid(row=1, column=0, sticky="nsew")


    # 响应式 输入框
    def OnC2():
        xznum = radval1.get()
        if xznum == False:
            radtxt1.grid_forget()
        else:
            radtxt1.grid(row=1, column=3)


    radval1 = tk.BooleanVar(value=False)
    radio1 = ttk.Radiobutton(FGx1, text="  jxl ", variable=radval1, value=False, command=OnC2)
    radio1.grid(row=1, column=1)

    radio1 = ttk.Radiobutton(FGx1, text="自定", variable=radval1, value=True, command=OnC2)
    radio1.grid(row=1, column=2)

    radtxt1 = tk.Entry(FGx1, foreground=uis.BGC2, width=14, font=font_p3)
    radtxt1.grid(row=1, column=3)
    radtxt1.grid_forget()

    # ----------

    # 响应式 输入框
    def OnC3():

        xznum = radval2.get()
        if xznum == False:
            radtxt2.grid_forget()
        else:
            radtxt2.grid(row=2, column=3)


    label = tk.Label(FGx1, text="贴图ID", font=font_p3, bg=uis.BGC3)
    label.grid(row=2, column=0, sticky="nsew")

    radval2 = tk.BooleanVar(value=False)
    radio = ttk.Radiobutton(FGx1, text="不变", variable=radval2, value=False, command=OnC3)
    radio.grid(row=2, column=1)

    radio = ttk.Radiobutton(FGx1, text="自定", variable=radval2, value=True, command=OnC3)
    radio.grid(row=2, column=2)

    radtxt2 = tk.Entry(FGx1, foreground=uis.BGC2, width=14, font=font_p3)
    radtxt2.grid(row=2, column=3)
    radtxt2.grid_forget()

    def OnC4():
        global PZ_ao
        if cbv.get() == True:
            PZ_ao = True
        else:
            PZ_ao = False
        print PZ_ao

    label = tk.Label(FGx1, text="环境光遮罩", font=font_p3, bg=uis.BGC3)
    label.grid(row=3, column=0, sticky="nsew")

    cbv = BooleanVar(value=True)
    Checkbutton(FGx1, text="开启", variable=cbv, command=OnC4).grid(row=3, column=1)




    text = tk.Text(FGx1, height=17, width=34, wrap='word', bg=uis.BGC4, relief='flat', selectbackground=uis.BGC1, font=font_p3)
    text.grid(row=4, column=0, sticky="nsew", columnspan=2)

    scrollbar = ttk.Scrollbar(FGx1, command=text.yview)  # 创建一个Scrollbar，用于滚动
    scrollbar.grid(row=4, column=2, sticky="nsew")

    text.config(yscrollcommand=scrollbar.set)  # 将Scrollbar与Text控件绑定

    text.insert('0.0', uis.ReadMe1)

    text.config(state='disabled')  # 禁用Text控件的编辑功能



def ListBox(str):
    # 创建一个Listbox
    PZ_sx = str

    FGL = tk.Frame(FG2)
    FGL.grid(row=5, column=0, sticky="nsew")

    LB = tk.Listbox(FGL, height=11, width=30, background=uis.BGC4, selectbackground=uis.BGC1, font=font_p1)
    LB.grid(row=0, column=0,sticky="nsew")

    # 创建一个滚动条
    scrollbar = ttk.Scrollbar(FGL, orient="vertical")
    scrollbar.grid(row=0, column=1, sticky="nsew")

    # 配置滚动条与Listbox的关联
    scrollbar.config(command=LB.yview)
    LB.config(yscrollcommand=scrollbar.set)



    if PZ_sx != '':
        data = uis.GetAllJson(PZ_sx)
        for item in data:
            LB.insert(tk.END, item)
    else:
        data = uis.GetAllJson()
        for item in data:
            LB.insert(tk.END, item)







































start()
ListBox('')

# 启动事件循环
root.mainloop()
