# -*- coding: utf-8 -*-
"""
jxl网易方块json批量修改器
V1.0.4  2026-01-11
Python 2.7 + ttk 单文件版
author : Kimi
"""
from __future__ import print_function
import os
import re
import json
import Tkinter as tk
import ttk
import tkMessageBox as msgbox

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BLOCKS_DIR = os.path.join(SCRIPT_DIR, 'blocks')

# ---------- 可调整的三个区域初始权重 ----------
PANE_WEIGHTS = [1, 5, 5]   # 左、中、右，可自由改

# ---------- 汉化映射表（可自行修改） ----------
DESC_ZH = {
    "identifier": u"标识符",
    "register_to_creative_menu": u"注册到创造菜单",
    "is_experimental": u"实验性",
    "category": u"分类"
}
COMP_ZH = {
    "netease:water_source": u"水源",
    "minecraft:block_light_absorption": u"吸光值",
    "minecraft:block_light_emission": u"发光值",
    "minecraft:destroy_time": u"破坏时间",
    "netease:tier": u"挖掘等级",
    "netease:aabb": u"碰撞箱",
    "netease:face_directional": u"朝向",
    "netease:solid": u"是否固体",
    "netease:pathable": u"可行走",
    "netease:connection": u"连接"
}

# ---------- 系统内置键模板 ----------
BUILTIN_KEYS = [
    {"section": "description", "key": "identifier", "zh": u"标识符", "default": "jxl:your_block"},
    {"section": "description", "key": "register_to_creative_menu", "zh": u"注册到创造菜单", "default": True},
    {"section": "components", "key": "minecraft:destroy_time", "zh": u"破坏时间", "default": 1.0},
    {"section": "components", "key": "netease:water_source", "zh": u"水源", "default": {"value": True}},
    {"section": "components", "key": "minecraft:block_light_emission", "zh": u"发光值", "default": {"emission": 0}},
    {"section": "components", "key": "netease:aabb", "zh": u"碰撞箱", "default": {
        "collision": {"min": [0, 0, 0], "max": [1, 0.5, 1]},
        "clip": {"min": [0, 0, 0], "max": [1, 1, 1]}
    }}
]

# ---------- 工具函数 ----------
def strip_comment(text):
    """删除 // 行注释和 /* */ 块注释（简单实现）"""
    text = re.sub(r'//.*?$', '', text, flags=re.M)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    return text

def load_json(path):
    with open(path, 'rb') as f:
        raw = f.read()
    raw = strip_comment(raw)
    return json.loads(raw)

def save_json(obj, path):
    new_root = {}
    for k in sorted(obj.keys(), reverse=True):
        new_root[k] = obj[k]
    block = new_root.get('minecraft:block', {})
    if 'description' in block and 'components' in block:
        new_block = {}
        desc = block['description']
        new_desc = {}
        for k in sorted(desc.keys(), reverse=True):
            new_desc[k] = desc[k]
        new_block['description'] = new_desc
        comp = block['components']
        new_comp = {}
        for k in sorted(comp.keys(), reverse=True):
            new_comp[k] = comp[k]
        new_block['components'] = new_comp
        for k in sorted(block.keys(), reverse=True):
            if k not in new_block:
                new_block[k] = block[k]
        new_root['minecraft:block'] = new_block
    with open(path, 'wb') as f:
        json.dump(new_root, f, indent=2, ensure_ascii=False, sort_keys=False)

def scan_blocks():
    if not os.path.isdir(BLOCKS_DIR):
        os.makedirs(BLOCKS_DIR)
    files = [f for f in os.listdir(BLOCKS_DIR) if f.lower().endswith('.json')]
    return sorted(files)

def collect_keys(files):
    desc_keys = set(); comp_keys = set()
    for f in files:
        try:
            data = load_json(os.path.join(BLOCKS_DIR, f))
            block = data.get('minecraft:block', {})
            desc_keys.update(block.get('description', {}).keys())
            comp_keys.update(block.get('components', {}).keys())
        except Exception:
            continue
    return sorted(desc_keys, reverse=True), sorted(comp_keys, reverse=True)

def center_window(win, parent):
    parent.update_idletasks()
    pw, ph = parent.winfo_width(), parent.winfo_height()
    px, py = parent.winfo_x(), parent.winfo_y()
    win.update_idletasks()
    w, h = win.winfo_width(), win.winfo_height()
    win.geometry('+%d+%d' % (px + (pw - w) / 2, py + (ph - h) / 2))

# ---------- 主界面 ----------
class MainApp(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.master.title(u'jxl网易方块json批量修改器  V1.0.4  20260111')
        self.master.geometry('1000x700')
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.refresh_all()

    # ---------------- 界面布局 ----------------
    def create_widgets(self):
        top = ttk.Frame(self)
        top.pack(fill='x', padx=5, pady=5)
        ttk.Label(top, text=u'jxl网易方块json批量修改器  V1.0.4  20260111',
                  font=('微软雅黑', 14, 'bold')).pack(side='left')
        ttk.Button(top, text=u'说明', command=self.show_help).pack(side='right')

        main = ttk.PanedWindow(self, orient='horizontal')
        main.pack(fill='both', expand=True)

        # ---- 区域1：文件列表 ----
        left = ttk.Labelframe(main, text=u'文件列表（单击预览）')
        main.add(left, weight=PANE_WEIGHTS[0])
        self.file_listbox = tk.Listbox(left, activestyle='none')
        self.file_listbox.pack(side='left', fill='both', expand=True)
        self.file_scroll = ttk.Scrollbar(left, orient='vertical')
        self.file_scroll.pack(side='right', fill='y')
        self.file_listbox.config(yscrollcommand=self.file_scroll.set)
        self.file_scroll.config(command=self.file_listbox.yview)
        self.file_listbox.bind('<ButtonRelease-1>', self.on_file_click)

        # ---- 区域2：快捷键列表 ----
        mid = ttk.Labelframe(main, text=u'快捷键选择（description / components）')
        main.add(mid, weight=PANE_WEIGHTS[1])
        self.key_notebook = ttk.Notebook(mid)
        self.key_notebook.pack(fill='both', expand=True)
        self.desc_frame = ttk.Frame(self.key_notebook)
        self.comp_frame = ttk.Frame(self.key_notebook)
        self.key_notebook.add(self.desc_frame, text='description')
        self.key_notebook.add(self.comp_frame, text='components')

        self.desc_canvas = tk.Canvas(self.desc_frame, highlightthickness=0)
        self.desc_inner = ttk.Frame(self.desc_canvas)
        self.desc_scroll = ttk.Scrollbar(self.desc_frame, orient='vertical')
        self.desc_canvas.config(yscrollcommand=self.desc_scroll.set)
        self.desc_scroll.config(command=self.desc_canvas.yview)
        self.desc_canvas.create_window((0, 0), window=self.desc_inner, anchor='nw')
        self.desc_canvas.bind('<Configure>', lambda e: self.desc_canvas.configure(scrollregion=self.desc_canvas.bbox('all')))
        self.desc_canvas.pack(side='left', fill='both', expand=True)
        self.desc_scroll.pack(side='right', fill='y')
        # 滚轮绑定
        self.desc_canvas.bind('<Enter>', lambda e: self.bind_mousewheel(self.desc_canvas))
        self.desc_canvas.bind('<Leave>', lambda e: self.unbind_mousewheel())

        self.comp_canvas = tk.Canvas(self.comp_frame, highlightthickness=0)
        self.comp_inner = ttk.Frame(self.comp_canvas)
        self.comp_scroll = ttk.Scrollbar(self.comp_frame, orient='vertical')
        self.comp_canvas.config(yscrollcommand=self.comp_scroll.set)
        self.comp_scroll.config(command=self.comp_canvas.yview)
        self.comp_canvas.create_window((0, 0), window=self.comp_inner, anchor='nw')
        self.comp_canvas.bind('<Configure>', lambda e: self.comp_canvas.configure(scrollregion=self.comp_canvas.bbox('all')))
        self.comp_canvas.pack(side='left', fill='both', expand=True)
        self.comp_scroll.pack(side='right', fill='y')
        # 滚轮绑定
        self.comp_canvas.bind('<Enter>', lambda e: self.bind_mousewheel(self.comp_canvas))
        self.comp_canvas.bind('<Leave>', lambda e: self.unbind_mousewheel())

        # ---- 区域3：编辑器 ----
        right = ttk.Labelframe(main, text=u'编辑器（修改后点保存）')
        main.add(right, weight=PANE_WEIGHTS[2])
        self.editor_text = tk.Text(right, wrap='none', font=('Consolas', 11))
        self.editor_text.pack(fill='both', expand=True)
        btn_bar = ttk.Frame(right)
        btn_bar.pack(fill='x', pady=2)
        ttk.Button(btn_bar, text=u'保存到全部JSON', command=self.save_to_all).pack(side='left', padx=5)
        ttk.Button(btn_bar, text=u'格式化JSON', command=self.format_editor).pack(side='left', padx=5)
        ttk.Button(btn_bar, text=u'删除该键', command=self.delete_key).pack(side='left', padx=5)

        # ---- 底部状态 ----
        bottom = ttk.Frame(self)
        bottom.pack(fill='x', padx=5, pady=2)
        self.status = ttk.Label(bottom, text=u'就绪')
        self.status.pack(side='left')
        self.key_label = ttk.Label(bottom, text=u'当前未选择键')
        self.key_label.pack(side='left', padx=20)

        # ---- 新增键区域 ----
        add_bar = ttk.Frame(self)
        add_bar.pack(fill='x', padx=5, pady=5)
        ttk.Button(add_bar, text=u'新增键', command=self.add_new_key).pack(side='left')

        # 当前选中
        self.cur_key = None
        self.cur_section = None   # 'description' or 'components'

    # ---------------- 滚轮辅助 ----------------
    def bind_mousewheel(self, canvas):
        self.master.bind_all('<MouseWheel>', lambda e: canvas.yview_scroll(-1*(e.delta/120), 'units'))
    def unbind_mousewheel(self):
        self.master.unbind_all('<MouseWheel>')

    # ---------------- 事件 ----------------
    def refresh_all(self):
        self.files = scan_blocks()
        self.file_listbox.delete(0, 'end')
        for f in self.files:
            self.file_listbox.insert('end', f)
        self.refresh_key_buttons()

    def refresh_key_buttons(self):
        for child in self.desc_inner.winfo_children():
            child.destroy()
        for child in self.comp_inner.winfo_children():
            child.destroy()
        desc_keys, comp_keys = collect_keys(self.files)
        for k in desc_keys:
            zh = DESC_ZH.get(k, '')
            text = k if not zh else (k + '\n' + zh)
            btn = tk.Button(self.desc_inner, text=text, anchor='center', padx=4, pady=2,
                            command=lambda key=k: self.on_key_select('description', key))
            btn.pack(fill='x', padx=1, pady=1)
        for k in comp_keys:
            zh = COMP_ZH.get(k, '')
            text = k if not zh else (k + '\n' + zh)
            btn = tk.Button(self.comp_inner, text=text, anchor='center', padx=4, pady=2,
                            command=lambda key=k: self.on_key_select('components', key))
            btn.pack(fill='x', padx=1, pady=1)
        # 预留底部空隙，确保最后一个按钮也能滚到
        ttk.Frame(self.desc_inner, height=20).pack(fill='x')
        ttk.Frame(self.comp_inner, height=20).pack(fill='x')

        # 强制刷新 scrollregion，确保新增按钮可见
        self.desc_canvas.configure(scrollregion=self.desc_canvas.bbox('all'))
        self.comp_canvas.configure(scrollregion=self.comp_canvas.bbox('all'))

    def on_file_click(self, event):
        sel = self.file_listbox.curselection()
        if not sel:
            return
        fname = self.files[sel[0]]
        path = os.path.join(BLOCKS_DIR, fname)
        try:
            data = load_json(path)
        except Exception as e:
            msgbox.showerror(u'错误', u'无法加载JSON：\n' + str(e))
            return
        top = tk.Toplevel(self)
        top.title(fname + u'  预览')
        center_window(top, self)
        txt = tk.Text(top, wrap='none', font=('Consolas', 10))
        txt.pack(fill='both', expand=True, padx=5, pady=5)
        txt.insert('end', json.dumps(data, indent=2, ensure_ascii=False))
        txt.config(state='disabled')
        ttk.Button(top, text=u'关闭', command=top.destroy).pack(pady=5)

    def on_key_select(self, section, key):
        # 先清除所有按钮颜色
        for child in self.desc_inner.winfo_children():
            if isinstance(child, tk.Button):
                child.config(bg='SystemButtonFace')
        for child in self.comp_inner.winfo_children():
            if isinstance(child, tk.Button):
                child.config(bg='SystemButtonFace')
        # 高亮当前按钮
        self.cur_section = section
        self.cur_key = key
        zh = (DESC_ZH if section == 'description' else COMP_ZH).get(key, '')
        self.key_label.config(text=u'当前选择：%s / %s%s' % (section, key, (' (' + zh + ')' if zh else '')))
        found = None
        for f in self.files:
            try:
                data = load_json(os.path.join(BLOCKS_DIR, f))
                block = data.get('minecraft:block', {})
                sec_data = block.get(section, {})
                if key in sec_data:
                    found = sec_data[key]
                    break
            except Exception:
                continue
        if found is None:
            found = u''
        self.editor_text.delete('1.0', 'end')
        self.editor_text.insert('end', json.dumps(found, indent=2, ensure_ascii=False))

    def save_to_all(self):
        if self.cur_section is None or self.cur_key is None:
            msgbox.showwarning(u'提示', u'请先选择一个键！')
            return
        txt = self.editor_text.get('1.0', 'end').strip()
        try:
            new_val = json.loads(txt)
        except Exception as e:
            msgbox.showerror(u'格式错误', u'JSON格式不正确：\n' + str(e))
            return
        count = 0
        for f in self.files:
            path = os.path.join(BLOCKS_DIR, f)
            try:
                data = load_json(path)
                block = data.setdefault('minecraft:block', {})
                sec = block.setdefault(self.cur_section, {})
                sec[self.cur_key] = new_val
                save_json(data, path)
                count += 1
            except Exception as e:
                print(u'跳过文件', f, e)
                continue
        self.status.config(text=u'成功修改 %d 个JSON' % count)
        self.refresh_key_buttons()

    def format_editor(self):
        try:
            txt = self.editor_text.get('1.0', 'end')
            obj = json.loads(txt)
            self.editor_text.delete('1.0', 'end')
            self.editor_text.insert('end', json.dumps(obj, indent=2, ensure_ascii=False))
        except Exception as e:
            msgbox.showerror(u'格式错误', str(e))

    def delete_key(self):
        if self.cur_section is None or self.cur_key is None:
            msgbox.showwarning(u'提示', u'请先选择一个键！')
            return
        if not msgbox.askyesno(u'确认', u'确定要从所有JSON中删除键 "%s" 吗？' % self.cur_key):
            return
        count = 0
        for f in self.files:
            path = os.path.join(BLOCKS_DIR, f)
            try:
                data = load_json(path)
                block = data.get('minecraft:block', {})
                sec = block.get(self.cur_section, {})
                if self.cur_key in sec:
                    del sec[self.cur_key]
                    save_json(data, path)
                    count += 1
            except Exception as e:
                print(u'跳过', f, e)
                continue
        self.status.config(text=u'已删除 %d 个JSON中的该键' % count)
        self.refresh_key_buttons()

    def add_new_key(self):
        w = tk.Toplevel(self)
        w.title(u'新增键')
        center_window(w, self)
        notebook = ttk.Notebook(w)
        notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # ---- 自定义页 ----
        custom_tab = ttk.Frame(notebook)
        notebook.add(custom_tab, text=u'自定义键')
        ttk.Label(custom_tab, text=u'所属区域').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        section_var = tk.StringVar(value='components')
        ttk.Radiobutton(custom_tab, text='description', variable=section_var, value='description').grid(row=0, column=1)
        ttk.Radiobutton(custom_tab, text='components', variable=section_var, value='components').grid(row=0, column=2)
        ttk.Label(custom_tab, text=u'键名').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        key_entry = ttk.Entry(custom_tab, width=30)
        key_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='we')
        ttk.Label(custom_tab, text=u'内容（JSON）').grid(row=2, column=0, padx=5, pady=5, sticky='nw')
        cont_text = tk.Text(custom_tab, height=8, width=40, font=('Consolas', 10))
        cont_text.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        def do_custom():
            sec = section_var.get()
            key = key_entry.get().strip()
            txt = cont_text.get('1.0', 'end').strip()
            if not sec or not key:
                msgbox.showwarning(u'输入不全', u'区域和键名都必须填写！')
                return
            try:
                val = json.loads(txt)
            except Exception as e:
                msgbox.showerror(u'JSON错误', str(e))
                return
            self.apply_new_key(sec, key, val)
            w.destroy()

        ttk.Button(custom_tab, text=u'保存到全部', command=do_custom).grid(row=3, column=1, pady=5)
        ttk.Button(custom_tab, text=u'取消', command=w.destroy).grid(row=3, column=2, pady=5)

        # ---- 系统内置页 ----
        builtin_tab = ttk.Frame(notebook)
        notebook.add(builtin_tab, text=u'系统内置键')
        notebook.select(builtin_tab)  # 默认显示
        builtin_paned = ttk.PanedWindow(builtin_tab, orient='horizontal')
        builtin_paned.pack(fill='both', expand=True, padx=5, pady=5)

        # 左侧分区域笔记本
        left_nb = ttk.Notebook(builtin_paned)
        builtin_paned.add(left_nb, weight=1)
        desc_tab = ttk.Frame(left_nb)
        comp_tab = ttk.Frame(left_nb)
        left_nb.add(desc_tab, text='description')
        left_nb.add(comp_tab, text='components')

        # description 列表
        desc_canvas = tk.Canvas(desc_tab, highlightthickness=0)
        desc_inner = ttk.Frame(desc_canvas)
        desc_scroll = ttk.Scrollbar(desc_tab, orient='vertical')
        desc_canvas.config(yscrollcommand=desc_scroll.set)
        desc_scroll.config(command=desc_canvas.yview)
        desc_canvas.create_window((0, 0), window=desc_inner, anchor='nw')
        desc_canvas.bind('<Configure>', lambda e: desc_canvas.configure(scrollregion=desc_canvas.bbox('all')))
        desc_canvas.pack(side='left', fill='both', expand=True)
        desc_scroll.pack(side='right', fill='y')
        desc_canvas.bind('<Enter>', lambda e: self.bind_mousewheel(desc_canvas))
        desc_canvas.bind('<Leave>', lambda e: self.unbind_mousewheel())

        # components 列表
        comp_canvas = tk.Canvas(comp_tab, highlightthickness=0)
        comp_inner = ttk.Frame(comp_canvas)
        comp_scroll = ttk.Scrollbar(comp_tab, orient='vertical')
        comp_canvas.config(yscrollcommand=comp_scroll.set)
        comp_scroll.config(command=comp_canvas.yview)
        comp_canvas.create_window((0, 0), window=comp_inner, anchor='nw')
        comp_canvas.bind('<Configure>', lambda e: comp_canvas.configure(scrollregion=comp_canvas.bbox('all')))
        comp_canvas.pack(side='left', fill='both', expand=True)
        comp_scroll.pack(side='right', fill='y')
        comp_canvas.bind('<Enter>', lambda e: self.bind_mousewheel(comp_canvas))
        comp_canvas.bind('<Leave>', lambda e: self.unbind_mousewheel())

        # 右侧预览（宽度减半）
        right_frame = ttk.Labelframe(builtin_paned, text=u'内容预览')
        builtin_paned.add(right_frame, weight=1)
        self.builtin_prev = tk.Text(right_frame, wrap='none', font=('Consolas', 10), width=40)
        self.builtin_prev.pack(fill='both', expand=True, padx=5, pady=5)
        self.builtin_prev.config(state='disabled')  # 只读
        btn_bar = ttk.Frame(right_frame)
        btn_bar.pack(fill='x', pady=2)
        ttk.Button(btn_bar, text=u'加入', command=lambda: self.builtin_add_current(w)).pack(side='right', padx=5)

        # 填充内置键按钮
        self.builtin_current = None
        for tpl in BUILTIN_KEYS:
            sec, key, zh, default = tpl['section'], tpl['key'], tpl['zh'], tpl['default']
            text = key if not zh else (key + '\n' + zh)
            if sec == 'description':
                btn = tk.Button(desc_inner, text=text, anchor='center', padx=4, pady=2,
                                command=lambda t=tpl: self.builtin_select(t))
                btn.pack(fill='x', padx=1, pady=1)
            else:
                btn = tk.Button(comp_inner, text=text, anchor='center', padx=4, pady=2,
                                command=lambda t=tpl: self.builtin_select(t))
                btn.pack(fill='x', padx=1, pady=1)
        # 预留底部空隙
        ttk.Frame(desc_inner, height=20).pack(fill='x')
        ttk.Frame(comp_inner, height=20).pack(fill='x')

    def builtin_select(self, tpl):
        self.builtin_current = tpl
        self.builtin_prev.config(state='normal')
        self.builtin_prev.delete('1.0', 'end')
        self.builtin_prev.insert('end', json.dumps(tpl['default'], indent=2, ensure_ascii=False))
        self.builtin_prev.config(state='disabled')

    def builtin_add_current(self, win):
        if not self.builtin_current:
            msgbox.showwarning(u'提示', u'请先选择一个内置键！')
            return
        tpl = self.builtin_current
        self.apply_new_key(tpl['section'], tpl['key'], tpl['default'])
        win.destroy()

    def apply_new_key(self, section, key, value):
        count = 0
        for f in self.files:
            path = os.path.join(BLOCKS_DIR, f)
            try:
                data = load_json(path)
                block = data.setdefault('minecraft:block', {})
                sec_dict = block.setdefault(section, {})
                sec_dict[key] = value
                save_json(data, path)
                count += 1
            except Exception as e:
                print(u'跳过', f, e)
                continue
        self.status.config(text=u'新增键成功，已写入 %d 个JSON' % count)
        self.refresh_key_buttons()

    def show_help(self):
        top = tk.Toplevel(self)
        top.title(u'使用说明')
        center_window(top, self)
        # 调大窗口与字体
        ttk.Label(top, text=u'使用说明', font=('微软雅黑', 14, 'bold')).pack(pady=5)
        txt = tk.Text(top, wrap='word', font=('微软雅黑', 11), width=60, height=10)
        txt.pack(fill='both', expand=True, padx=5, pady=5)
        txt.insert('end', u'1. 把需要修改的 json 放到本程序同目录下的 blocks 文件夹\n'
                          u'2. 左侧单击文件名可预览\n'
                          u'3. 中间单击键按钮，右侧编辑器会加载该键内容\n'
                          u'4. 在右侧编辑后点“保存到全部JSON”即可批量同步\n'
                          u'5. 支持新增键，程序会自动补全到所有文件\n'
                          u'6. 所有修改直接写回源文件，建议先备份')
        txt.config(state='disabled')
        ttk.Button(top, text=u'关闭', command=top.destroy).pack(pady=5)

# ---------- 启动 ----------
if __name__ == '__main__':
    root = tk.Tk()
    MainApp(root)
    root.mainloop()