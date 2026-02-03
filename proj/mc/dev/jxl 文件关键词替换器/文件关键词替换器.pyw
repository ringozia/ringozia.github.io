#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import re
import json
import shutil
import ctypes
import io  # 新增：用于更好的编码处理
import Tkinter as tk
import ttk
import tkFileDialog
import tkMessageBox
import tkFont


class FileOperationApp:
    def __init__(self, root):
        self.root = root
        self.root.title(u"文件关键词替换器 - jxl井桢")
        self.root.geometry("900x720")
        self.root.minsize(800, 600)

        # ========== 界面美化设置 ==========
        self.setup_styles()

        # 数据存储
        self.file_list = []  # [(filename, fullpath, status), ...]
        self.mode = tk.StringVar(value="root")  # root/local
        self.rename_enabled = tk.BooleanVar(value=True)
        self.content_replace_enabled = tk.BooleanVar(value=False)
        self.extra_replace = tk.BooleanVar(value=False)

        # 关键词
        self.match_var = tk.StringVar()
        self.replace_var = tk.StringVar()
        self.extra_match_var = tk.StringVar()
        self.extra_replace_var = tk.StringVar()

        # 创建界面
        self.create_widgets()
        self.setup_layout()

        # 初始化本地模式文件夹
        self.init_local_folders()

        # 绑定事件
        self.bind_events()

        # 初始状态更新
        self.on_mode_change()
        self.on_content_replace_toggle()

    def setup_styles(self):
        """配置界面样式（美化 - Xpnative 风格）"""
        style = ttk.Style()
        # 修改：使用 xpnative 主题
        try:
            style.theme_use('xpnative')
        except:
            # 如果系统不支持 xpnative，尝试回退
            pass

        # 定义字体
        main_font = ("Microsoft YaHei", 10)
        bold_font = ("Microsoft YaHei", 10, "bold")
        header_font = ("Microsoft YaHei", 16, "bold")

        # 配置颜色和字体
        style.configure(".", font=main_font)
        style.configure("TFrame", font=main_font)
        style.configure("TLabelframe", font=bold_font)
        style.configure("TLabelframe.Label", font=bold_font)

        # 按钮样式
        style.configure("TButton", font=main_font, padding=6)

        # 强调按钮样式
        style.configure("Action.TButton", font=bold_font)

        # 树形列表样式
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=28,
                        font=main_font
                        )
        style.configure("Treeview.Heading", font=bold_font)

        # 标题样式
        style.configure("Header.TLabel", font=header_font, foreground="#2c3e50")

        # 状态栏样式
        style.configure("Status.TLabel", foreground="#006600", font=("Microsoft YaHei", 9, "bold"))

        # 设置窗口背景色
        self.root.configure(background="#f0f0f0")

    def init_local_folders(self):
        """初始化本地模式文件夹"""
        if not os.path.exists("inp"):
            os.makedirs("inp")
        if not os.path.exists("outp"):
            os.makedirs("outp")

    def create_widgets(self):
        """创建所有控件"""
        # ========== 顶部标题栏区域 ==========
        self.header_frame = ttk.Frame(self.root, padding="10 15 10 5")

        # 标题
        self.title_label = ttk.Label(
            self.header_frame,
            text=u"📁 文件关键词替换器",
            style="Header.TLabel"
        )

        # 说明按钮
        self.help_btn = ttk.Button(
            self.header_frame,
            text=u"📖 使用说明",
            command=self.show_help,
            width=12
        )

        # ========== 配置区域 ==========
        self.config_frame = ttk.LabelFrame(self.root, text=u" ⚙️ 操作配置 ", padding=15)

        # 模式选择 (增加背景容器)
        self.mode_frame = ttk.Frame(self.config_frame)
        ttk.Label(self.mode_frame, text=u"操作模式：", font=("Microsoft YaHei", 10, "bold")).pack(side=tk.LEFT)
        self.root_radio = ttk.Radiobutton(
            self.mode_frame, text=u"根模式（直接修改源文件）",
            variable=self.mode, value="root", command=self.on_mode_change
        )
        self.local_radio = ttk.Radiobutton(
            self.mode_frame, text=u"本地模式（inp/outp文件夹）",
            variable=self.mode, value="local", command=self.on_mode_change
        )
        self.root_radio.pack(side=tk.LEFT, padx=15)
        self.local_radio.pack(side=tk.LEFT, padx=5)

        # 分割线
        self.sep1 = ttk.Separator(self.config_frame, orient="horizontal")

        # 选项区域
        self.options_frame = ttk.Frame(self.config_frame)

        # 重命名选项
        self.rename_check = ttk.Checkbutton(
            self.options_frame,
            text=u"替换文件名",
            variable=self.rename_enabled
        )

        # 内部替换选项
        self.content_check = ttk.Checkbutton(
            self.options_frame,
            text=u"内部替换",
            variable=self.content_replace_enabled,
            command=self.on_content_replace_toggle
        )

        # 额外替换选项
        self.extra_frame = ttk.Frame(self.options_frame)
        self.extra_check = ttk.Checkbutton(
            self.extra_frame,
            text=u"启用额外替换",
            variable=self.extra_replace,
            command=self.on_extra_toggle
        )

        # 关键词输入区域
        self.keyword_frame = ttk.Frame(self.config_frame)

        # 主关键词
        self.main_keyword_frame = ttk.Frame(self.keyword_frame)
        ttk.Label(self.main_keyword_frame, text=u"查找内容：", width=10).pack(side=tk.LEFT)
        self.match_entry = ttk.Entry(self.main_keyword_frame, textvariable=self.match_var, width=30)
        self.match_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(self.main_keyword_frame, text=u"替换为：", width=8).pack(side=tk.LEFT, padx=(20, 0))
        self.replace_entry = ttk.Entry(self.main_keyword_frame, textvariable=self.replace_var, width=30)
        self.replace_entry.pack(side=tk.LEFT, padx=5)

        # 额外关键词
        self.extra_keyword_frame = ttk.Frame(self.keyword_frame)
        ttk.Label(self.extra_keyword_frame, text=u"额外查找：", width=10).pack(side=tk.LEFT)
        self.extra_match_entry = ttk.Entry(self.extra_keyword_frame, textvariable=self.extra_match_var, width=30)
        self.extra_match_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(self.extra_keyword_frame, text=u"替换为：", width=8).pack(side=tk.LEFT, padx=(20, 0))
        self.extra_replace_entry = ttk.Entry(self.extra_keyword_frame, textvariable=self.extra_replace_var, width=30)
        self.extra_replace_entry.pack(side=tk.LEFT, padx=5)

        # ========== 文件列表区域 ==========
        self.file_frame = ttk.LabelFrame(self.root, text=u" 📋 待处理文件 ", padding=10)

        # 工具栏
        self.file_toolbar = ttk.Frame(self.file_frame)
        self.refresh_btn = ttk.Button(self.file_toolbar, text=u"🔄 刷新列表", command=self.refresh_files)
        self.remove_btn = ttk.Button(self.file_toolbar, text=u"❌ 移除选中", command=self.remove_selected)
        self.clear_btn = ttk.Button(self.file_toolbar, text=u"🗑️ 清空列表", command=self.clear_files)

        # 粘贴路径按钮
        self.paste_btn = ttk.Button(self.file_toolbar, text=u"📋 粘贴文件/路径", command=self.paste_files_from_clipboard,
                                    style="Action.TButton")

        # 文件表格
        self.tree_frame = ttk.Frame(self.file_frame)

        # 滚动条
        self.vsb = ttk.Scrollbar(self.tree_frame, orient="vertical")
        self.hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal")

        # Treeview
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("filename", "path", "status"),
            show="headings",
            yscrollcommand=self.vsb.set,
            xscrollcommand=self.hsb.set,
            height=10
        )

        self.vsb.config(command=self.tree.yview)
        self.hsb.config(command=self.tree.xview)

        # 设置列
        self.tree.heading("filename", text=u"文件名")
        self.tree.heading("path", text=u"完整路径")
        self.tree.heading("status", text=u"当前状态")

        self.tree.column("filename", width=220, anchor="w")
        self.tree.column("path", width=450, anchor="w")
        self.tree.column("status", width=180, anchor="w")

        # ========== 底部区域 ==========
        self.bottom_frame = ttk.Frame(self.root, padding="10")

        # 通知文本
        self.status_var = tk.StringVar(value=u"就绪 - 请选择操作模式并配置文件")
        self.status_label = ttk.Label(
            self.bottom_frame,
            textvariable=self.status_var,
            style="Status.TLabel"
        )

        # 按钮区域
        self.btn_frame = ttk.Frame(self.bottom_frame)
        self.match_btn = ttk.Button(
            self.btn_frame,
            text=u"🔍 匹配",
            command=self.do_match,
            width=15
        )
        self.execute_btn = ttk.Button(
            self.btn_frame,
            text=u"▶️ 执行",
            command=self.do_execute,
            style="Action.TButton",
            width=15
        )

        self.match_btn.pack(side=tk.LEFT, padx=10)
        self.execute_btn.pack(side=tk.LEFT, padx=10)

    def setup_layout(self):
        """布局管理 - 调整顺序以确保底部按钮可见"""
        # 1. 顶部标题栏
        self.header_frame.pack(fill=tk.X)
        self.title_label.pack(side=tk.LEFT, padx=10)
        self.help_btn.pack(side=tk.RIGHT, padx=10)

        # 2. 配置区域
        self.config_frame.pack(fill=tk.X, padx=15, pady=5)

        self.mode_frame.pack(fill=tk.X, pady=(0, 5))
        self.sep1.pack(fill=tk.X, pady=8)

        self.options_frame.pack(fill=tk.X, pady=5)
        self.rename_check.pack(side=tk.LEFT, padx=5)
        self.content_check.pack(side=tk.LEFT, padx=20)
        self.extra_frame.pack(side=tk.LEFT, padx=20)
        self.extra_check.pack()

        self.keyword_frame.pack(fill=tk.X, pady=5)
        self.main_keyword_frame.pack(fill=tk.X, pady=4)
        self.extra_keyword_frame.pack(fill=tk.X, pady=4)

        # 3. 底部区域 (关键修改：先pack底部，固定在下方，防止被列表挤出)
        self.bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_label.pack(side=tk.LEFT, padx=5)
        self.btn_frame.pack(side=tk.RIGHT)

        # 4. 文件列表区域 (最后pack，填充剩余空间)
        self.file_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        self.file_toolbar.pack(fill=tk.X, pady=(0, 5))

        # 按钮布局
        self.refresh_btn.pack(side=tk.LEFT, padx=2)
        self.remove_btn.pack(side=tk.LEFT, padx=2)
        self.clear_btn.pack(side=tk.LEFT, padx=2)
        # paste_btn 在回调中动态 pack

        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def bind_events(self):
        """绑定事件"""
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.tree.bind("<Delete>", lambda e: self.remove_selected())
        # 新增：Ctrl+C 复制文件名
        self.tree.bind("<Control-c>", self.copy_filename_to_clipboard)
        # 新增：Ctrl+V 粘贴文件（同按钮功能）
        self.tree.bind("<Control-v>", lambda e: self.paste_files_from_clipboard())

    def copy_filename_to_clipboard(self, event):
        """复制选中文件的文件名（去除 .json）"""
        selection = self.tree.selection()
        if not selection:
            return

        filenames = []
        for item in selection:
            # 获取文件名列 (index 0)
            fname = self.tree.item(item, "values")[0]

            # 过滤 .json (忽略大小写)
            # 使用正则替换：以 .json 结尾的字符串，替换为空
            fname = re.sub(r'(?i)\.json$', '', fname)

            filenames.append(fname)

        if filenames:
            # 多选时换行分隔
            text_to_copy = "\n".join(filenames)
            self.root.clipboard_clear()
            self.root.clipboard_append(text_to_copy)
            self.root.update()  # 确保剪贴板写入生效
            self.status_var.set(u"已复制文件名到剪贴板")

    def on_mode_change(self):
        """模式切换回调"""
        mode = self.mode.get()

        if mode == "root":
            self.file_list = []  # 切换模式清空列表
            self.update_tree()
            self.refresh_btn.pack_forget()
            self.paste_btn.pack(side=tk.LEFT, padx=5)
            self.status_var.set(u"根模式：请复制文件或路径，然后点击“粘贴文件/路径”按钮")
        else:
            self.paste_btn.pack_forget()
            self.refresh_btn.pack(side=tk.LEFT, padx=2, before=self.remove_btn)
            self.refresh_files()
            self.status_var.set(u"本地模式：已加载 inp 文件夹中的文件")

    def on_content_replace_toggle(self):
        """内部替换选项切换"""
        if self.content_replace_enabled.get():
            self.extra_frame.pack(side=tk.LEFT, padx=20)
        else:
            self.extra_frame.pack_forget()
            self.extra_replace.set(False)
            self.on_extra_toggle()

    def adjust_window_height(self, delta):
        """动态调整窗口高度"""
        # 仅在窗口已经渲染后调整（避免初始化时尺寸为1导致的问题）
        if self.root.winfo_width() > 1:
            try:
                # 获取当前窗口尺寸
                w = self.root.winfo_width()
                h = self.root.winfo_height()
                # 调整高度
                self.root.geometry("{}x{}".format(w, h + delta))
            except:
                pass

    def on_extra_toggle(self):
        """额外替换切换"""
        if self.extra_replace.get():
            self.extra_keyword_frame.pack(fill=tk.X, pady=4, after=self.main_keyword_frame)
            # 界面撑高，增加窗口高度
            self.adjust_window_height(40)
        else:
            # 检查是否可见，如果从可见变为不可见，则减少高度
            if self.extra_keyword_frame.winfo_ismapped():
                self.adjust_window_height(-40)
            self.extra_keyword_frame.pack_forget()

    def truncate_path(self, path, max_len=60):
        """截断过长路径"""
        if len(path) <= max_len:
            return path
        return "..." + path[-(max_len - 3):]

    def show_help(self):
        """显示使用说明弹窗（修改：使用 Toplevel 和大字体）"""
        # 创建新的顶级窗口
        top = tk.Toplevel(self.root)
        top.title(u"📖 使用说明")
        top.geometry("700x550")

        # 配置文本框的字体（放大）
        help_font = ("Microsoft YaHei", 12)

        # 使用 Text 控件以便更好地显示多行文本
        text_area = tk.Text(top, font=help_font, padx=15, pady=15, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True)

        # 滚动条
        scrollbar = ttk.Scrollbar(text_area, orient="vertical", command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        msg = u"""
*文件关键词替换器*
        
使用说明：

1. **根模式**
   适用于直接修改任意位置的文件。
   **添加文件**：在资源管理器中选中文件（Ctrl+C）后在窗口内粘贴，或复制文件路径文本，然后点击本工具的“📋 粘贴文件/路径”按钮。
   工具会自动识别剪贴板内容，排除文件夹。

2. **本地模式**
   适用于处理工具目录下的文件。
   请把待修改的文件放在 'inp' 文件夹中。
   处理结果生成在 'outp'。

3. **功能配置**
   **替换文件名**：修改替换文件名中的关键词。
   **内部替换**：修改替换文件内容中的关键词。
   **额外替换**：若同时启用内部替换和额外替换，文件内部替换将使用“额外查找/替换”输入框的内容。

4. **快捷键**
   **Ctrl+C** (在列表中选中文件)：复制选中文件的文件名（自动去除 .json 后缀）。
   **Ctrl+V** (在列表中)：粘贴添加文件（同“粘贴文件/路径”按钮）。
   **Delete** (在列表中选中文件)：可以移除列表中的相应文件。


   版本：V1.0.0
   作者：jxl井桢
   QQ群：436506487
   2026/02/03
        """

        text_area.insert(tk.END, msg)
        text_area.config(state=tk.DISABLED)  # 设置为只读

    def get_clipboard_files_win(self):
        """
        使用 ctypes 读取 Windows 剪贴板中的文件列表 (CF_HDROP)
        """
        f_list = []
        if os.name != 'nt':
            return f_list

        try:
            user32 = ctypes.windll.user32
            shell32 = ctypes.windll.shell32

            CF_HDROP = 15

            if user32.OpenClipboard(None):
                try:
                    if user32.IsClipboardFormatAvailable(CF_HDROP):
                        hDrop = user32.GetClipboardData(CF_HDROP)
                        if hDrop:
                            count = shell32.DragQueryFileW(hDrop, 0xFFFFFFFF, None, 0)
                            for i in range(count):
                                length = shell32.DragQueryFileW(hDrop, i, None, 0)
                                buf = ctypes.create_unicode_buffer(length + 1)
                                shell32.DragQueryFileW(hDrop, i, buf, length + 1)
                                f_list.append(buf.value)
                finally:
                    user32.CloseClipboard()
        except Exception:
            pass
        return f_list

    def paste_files_from_clipboard(self):
        """从剪贴板粘贴文件路径（支持文本路径和复制的文件）"""

        # 修改：本地模式禁止粘贴
        if self.mode.get() == "local":
            tkMessageBox.showwarning(u"提示", u"本地模式禁止粘贴文件。\n请将文件直接放入 inp 文件夹并点击刷新。")
            return

        raw_paths = []

        # 1. 尝试获取普通文本数据
        try:
            text_data = self.root.clipboard_get()
            if text_data:
                raw_paths.extend(text_data.split('\n'))
        except tk.TclError:
            pass
        except Exception:
            pass

        # 2. 尝试获取 Windows 文件对象
        file_drop_paths = self.get_clipboard_files_win()
        if file_drop_paths:
            raw_paths.extend(file_drop_paths)

        if not raw_paths:
            self.status_var.set(u"剪贴板为空或不支持的格式")
            tkMessageBox.showwarning(u"提示", u"未能从剪贴板获取文件。\n请选中文件按 Ctrl+C，或复制文件路径文本。")
            return

        # 3. 处理路径列表
        added_count = 0
        for path in raw_paths:
            path = path.strip().strip('"').strip("'")
            if not path:
                continue

            if os.path.exists(path):
                if os.path.isfile(path):
                    filename = os.path.basename(path)
                    if not any(item[1] == path for item in self.file_list):
                        self.file_list.append((filename, path, u"等待操作"))
                        added_count += 1

        self.update_tree()

        if added_count > 0:
            self.status_var.set(u"成功添加了 {} 个文件".format(added_count))
        else:
            self.status_var.set(u"未添加新文件（可能是文件夹或重复项）")

    def refresh_files(self):
        """刷新文件列表"""
        self.file_list = []

        if self.mode.get() == "local":
            if os.path.exists("inp"):
                for filename in os.listdir("inp"):
                    fullpath = os.path.join("inp", filename)
                    if os.path.isfile(fullpath):
                        self.file_list.append((filename, fullpath, u"等待操作"))

        self.update_tree()
        self.status_var.set(u"已刷新，共 {} 个文件".format(len(self.file_list)))

    def remove_selected(self):
        """移除选中文件"""
        selection = self.tree.selection()
        if not selection:
            self.status_var.set(u"请先选择要移除的文件")
            return

        indices = []
        for item in selection:
            idx = self.tree.index(item)
            indices.append(idx)

        indices.sort(reverse=True)

        for idx in indices:
            if 0 <= idx < len(self.file_list):
                filename, fullpath, status = self.file_list[idx]

                if self.mode.get() == "local" and os.path.exists(fullpath):
                    try:
                        os.remove(fullpath)
                    except Exception as e:
                        self.status_var.set(u"删除文件失败: {}".format(str(e)))
                        return

                self.file_list.pop(idx)

        self.update_tree()
        self.status_var.set(u"已移除 {} 个文件".format(len(indices)))

    def clear_files(self):
        """清空所有文件"""
        if not self.file_list:
            return

        if tkMessageBox.askyesno(u"确认", u"确定要清空所有文件吗？"):
            if self.mode.get() == "local":
                for filename, fullpath, status in self.file_list:
                    if os.path.exists(fullpath):
                        try:
                            os.remove(fullpath)
                        except:
                            pass

            self.file_list = []
            self.update_tree()
            self.status_var.set(u"已清空所有文件")

    def update_tree(self):
        """更新树形显示"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for filename, fullpath, status in self.file_list:
            display_path = self.truncate_path(fullpath)
            self.tree.insert("", tk.END, values=(filename, display_path, status))

    def on_tree_double_click(self, event):
        """双击查看完整路径"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            idx = self.tree.index(item)
            if 0 <= idx < len(self.file_list):
                fullpath = self.file_list[idx][1]
                tkMessageBox.showinfo(u"完整路径", fullpath)

    def read_file_as_string(self, filepath):
        """统一读取文件为 Unicode 字符串，不进行 JSON 解析"""
        # 优先尝试 UTF-8
        try:
            with io.open(filepath, 'r', encoding='utf-8') as f:
                return f.read(), None
        except UnicodeDecodeError:
            pass

        # 尝试 GBK
        try:
            with io.open(filepath, 'r', encoding='gbk') as f:
                return f.read(), None
        except Exception as e:
            return None, str(e)

    def get_unique_path(self, directory, filename):
        """
        获取不冲突的文件路径：
        如果 output/a.json 存在，返回 output/a2.json
        如果 output/a2.json 存在，返回 output/a3.json
        """
        base_name, ext = os.path.splitext(filename)
        candidate = filename
        counter = 2

        while True:
            full_path = os.path.join(directory, candidate)
            if not os.path.exists(full_path):
                return full_path

            candidate = u"{}{}{}".format(base_name, counter, ext)
            counter += 1

    def do_match(self):
        """匹配操作"""
        if not self.file_list:
            self.status_var.set(u"错误：文件列表为空")
            return

        # 获取当前勾选状态
        rename = self.rename_enabled.get()
        content_op = self.content_replace_enabled.get()

        # 关键词获取
        match_keyword = self.match_var.get()
        if not isinstance(match_keyword, unicode):
            match_keyword = match_keyword.decode('utf-8')

        new_list = []
        files_found_count = 0  # 统计找到的文件数量（统一说法）

        # 修改：如果只勾选了替换文件名
        if rename and not content_op:
            if not match_keyword:
                self.status_var.set(u"错误：请输入查找内容")
                return

            for filename, fullpath, status in self.file_list:
                if match_keyword in filename:
                    new_status = u"*文件名：找到关键词！"
                    files_found_count += 1
                else:
                    new_status = u"文件名：无效关键词"
                new_list.append((filename, fullpath, new_status))

            self.file_list = new_list
            self.update_tree()
            self.status_var.set(u"匹配完成，共找到 {} 个文件".format(files_found_count))
            return

        # 下面是原有的内容匹配逻辑（如果勾选了内部替换）

        # 逻辑判断，如果启用内部替换且启用额外替换，则使用额外关键词进行匹配预览
        use_extra_as_main = content_op and self.extra_replace.get()
        if use_extra_as_main:
            match_keyword = self.extra_match_var.get()
            source_msg = u"(使用额外查找框)"
        else:
            match_keyword = self.match_var.get()
            source_msg = u""

        # 再处理一次编码，因为上面逻辑可能重新取值
        if not isinstance(match_keyword, unicode):
            match_keyword = match_keyword.decode('utf-8')

        if not match_keyword:
            self.status_var.set(u"错误：请输入匹配关键词 {}".format(source_msg))
            return

        for filename, fullpath, status in self.file_list:
            try:
                content, error = self.read_file_as_string(fullpath)

                if error:
                    new_status = u"读取失败: {}".format(error)
                else:
                    count = content.count(match_keyword)
                    if count > 0:
                        new_status = u"查找到 {} 个关键词".format(count)
                        files_found_count += 1
                    else:
                        new_status = u"未找到关键词"

            except Exception as e:
                new_status = u"错误: {}".format(str(e))

            new_list.append((filename, fullpath, new_status))

        self.file_list = new_list
        self.update_tree()
        self.status_var.set(u"匹配完成，共找到 {} 个文件".format(files_found_count))

    def do_execute(self):
        """执行操作"""
        rename = self.rename_enabled.get()
        content_op = self.content_replace_enabled.get()

        if not rename and not content_op:
            self.status_var.set(u"错误：请至少选择一个操作")
            return

        if not self.file_list:
            self.status_var.set(u"错误：文件列表为空")
            return

        # 获取变量
        match_kw = self.match_var.get()
        replace_kw = self.replace_var.get()
        extra_match = self.extra_match_var.get()
        extra_replace = self.extra_replace_var.get()

        # Unicode 转换
        if not isinstance(match_kw, unicode): match_kw = match_kw.decode('utf-8')
        if not isinstance(replace_kw, unicode): replace_kw = replace_kw.decode('utf-8')
        if not isinstance(extra_match, unicode): extra_match = extra_match.decode('utf-8')
        if not isinstance(extra_replace, unicode): extra_replace = extra_replace.decode('utf-8')

        # 逻辑：判断内容替换使用哪组输入框
        use_extra_for_content = content_op and self.extra_replace.get()

        # 验证输入
        if rename and not match_kw:
            self.status_var.set(u"错误：文件名替换需要'查找内容'不能为空")
            return

        if content_op:
            if use_extra_for_content:
                if not extra_match:
                    self.status_var.set(u"错误：内部替换已切换至'额外查找'，该框不能为空")
                    return
            else:
                if not match_kw:
                    self.status_var.set(u"错误：内部替换需要'查找内容'不能为空")
                    return

        # 确认对话框构建
        op_details = []
        if rename:
            op_details.append(u"替换文件名: '{}' -> '{}'".format(match_kw, replace_kw))

        if content_op:
            if use_extra_for_content:
                # 如果启用了额外替换，内容替换使用额外输入框
                op_details.append(u"内部文本替换 (使用额外框): '{}' -> '{}'".format(extra_match, extra_replace))
            else:
                op_details.append(u"内部文本替换: '{}' -> '{}'".format(match_kw, replace_kw))

        confirm_msg = u"即将执行以下操作（共 {} 个文件）：\n\n{}\n\n所有文件（包括JSON）将视为纯文本处理。\n是否继续？".format(
            len(self.file_list), "\n".join(op_details)
        )

        if not tkMessageBox.askyesno(u"确认执行", confirm_msg):
            return

        success_count = 0
        renamed_count = 0  # 统计成功修改文件名的数量
        new_list = []

        for filename, fullpath, status in self.file_list:
            try:
                current_op_success = True
                replace_count = 0

                # 计算新文件名 (不论本地还是根模式，先算出来)
                final_filename = filename
                filename_changed = False
                if rename:
                    final_filename = filename.replace(match_kw, replace_kw)
                    if final_filename != filename:
                        filename_changed = True

                # 根据模式执行不同的逻辑
                if self.mode.get() == "local":
                    # ========== 本地模式 (创建副本到 outp) ==========
                    target_fullpath = self.get_unique_path("outp", final_filename)

                    if content_op:
                        # 读取内容
                        content, error = self.read_file_as_string(fullpath)
                        if error:
                            new_list.append((filename, fullpath, u"读取失败: {}".format(error)))
                            continue

                        # 替换内容
                        if use_extra_for_content:
                            replace_count = content.count(extra_match)
                            content = content.replace(extra_match, extra_replace)
                        else:
                            replace_count = content.count(match_kw)
                            content = content.replace(match_kw, replace_kw)

                        # 写入新文件
                        with io.open(target_fullpath, 'w', encoding='utf-8') as f:
                            f.write(content)
                    else:
                        # 仅复制并重命名
                        shutil.copy2(fullpath, target_fullpath)

                    # 本地模式最终路径引用 (逻辑上列表显示仍为inp)
                    display_target = fullpath

                else:
                    # ========== 根模式 (直接修改源文件) ==========
                    target_fullpath = fullpath  # 初始指向源文件

                    # 1. 先修改文件内容 (如果启用)
                    if content_op:
                        content, error = self.read_file_as_string(fullpath)
                        if error:
                            new_list.append((filename, fullpath, u"读取失败: {}".format(error)))
                            continue

                        if use_extra_for_content:
                            replace_count = content.count(extra_match)
                            content = content.replace(extra_match, extra_replace)
                        else:
                            replace_count = content.count(match_kw)
                            content = content.replace(match_kw, replace_kw)

                        # 覆盖写入源文件
                        with io.open(fullpath, 'w', encoding='utf-8') as f:
                            f.write(content)

                    # 2. 再重命名文件 (如果启用且文件名改变)
                    if rename and filename_changed:
                        new_target = os.path.join(os.path.dirname(fullpath), final_filename)
                        os.rename(fullpath, new_target)
                        target_fullpath = new_target  # 更新路径指向新文件名

                    display_target = target_fullpath

                # 统计和状态更新
                if current_op_success:
                    success_count += 1

                    status_text = u"操作成功"

                    # 场景1: 仅替换文件名
                    if rename and not content_op:
                        if filename_changed:
                            renamed_count += 1
                            status_text = u"成功修改文件名"
                        else:
                            status_text = u""  # 未修改文件名的，清空状态

                    # 场景2: 包含内部替换
                    elif content_op:
                        status_text = u"成功替换{}个关键词".format(replace_count)
                        if rename and filename_changed:
                            renamed_count += 1

                    # 更新列表数据
                    if self.mode.get() == "local":
                        # 本地模式列表保持显示源文件（inp）和源文件名
                        new_list.append((filename, fullpath, status_text))
                    else:
                        # 根模式更新为新文件 (如果有改名)
                        new_filename = os.path.basename(display_target)
                        new_list.append((new_filename, display_target, status_text))

                else:
                    new_list.append((filename, fullpath, status))

            except Exception as e:
                new_list.append((filename, fullpath, u"执行异常: {}".format(str(e))))

        self.file_list = new_list
        self.update_tree()

        # 构建底部的状态文本，不再弹窗
        status_msg = u"执行完成"

        if rename and not content_op:
            status_msg += u"，成功修改 {} 个文件名".format(renamed_count)
        else:
            status_msg += u"，成功处理 {} / {} 个文件".format(success_count, len(self.file_list))

        if self.mode.get() == "local" and success_count > 0:
            status_msg += u"。修改后的文件 保存在outp文件夹中"

        self.status_var.set(status_msg)


def main():
    root = tk.Tk()
    app = FileOperationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()