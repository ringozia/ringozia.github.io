#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JXL MCBE合成配方生成器
Python 2.7 + ttk
"""

import os
import sys
import json
import Tkinter as tk
import ttk
from collections import OrderedDict

try:
    import tkFileDialog as filedialog
except ImportError:
    pass

try:
    import tkMessageBox as messagebox
except ImportError:
    pass

import ScrolledText as scrolledtext

Best_N = 'JXL MCBE合成配方生成器'
Best_Va = 'V1.0'
Best_Vb = Best_Va + ' *适配网易3.4即微软1.21.00*'

Best_A = 'jxl井桢'
Best_T = '2026.3.22'

class RecipeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title(Best_N + ' | ' + Best_Vb)
        self.root.geometry("800x700")
        self.root.minsize(1000, 600)

        # 初始化变量
        self.selected_file = tk.StringVar(value=u"未选择")
        self.selected_material = tk.StringVar(value=u"未选择")
        self.custom_id_enabled = tk.BooleanVar(value=False)
        self.namespace = tk.StringVar(value="jxl")
        self.block_id = tk.StringVar(value="")
        self.output_count = tk.IntVar(value=1)
        self.info_text = tk.StringVar(value=u"准备就绪")
        self.recipe_type = tk.StringVar(value=u"有序合成")

        # 材料分页
        self.material_tab = tk.StringVar(value="items")

        # 九宫格数据 - 存储(item_id, data)元组
        self.grid_data = [None] * 9
        self.grid_buttons = []
        self.grid_labels = []

        # 材料数据 - 使用OrderedDict保持顺序
        self.materials_data = OrderedDict([
            ("items", OrderedDict()),
            ("blocks", OrderedDict()),
            ("star", OrderedDict())
        ])

        # 删除模式
        self.delete_mode = False

        # 字母映射
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

        # 当前选中的材料
        self.current_material_id = None
        self.current_material_name = None
        self.current_material_data = 0
        self.current_is_placeholder = False

        # 检查并创建文件夹
        self.check_folders()

        # 加载材料数据
        self.load_materials()

        # 创建界面
        self.create_ui()

        # 刷新文件列表
        self.refresh_files()

    def check_folders(self):
        u"""检查并创建必要的文件夹"""
        if not os.path.exists("file"):
            os.makedirs("file")
            print(u"创建文件夹: file")
        if not os.path.exists("newFile"):
            os.makedirs("newFile")
            print(u"创建文件夹: newFile")

    def load_materials(self):
        u"""加载材料数据 - 使用OrderedDict保持JSON中的顺序"""
        recipe_data_path = "recipeData.json"
        if os.path.exists(recipe_data_path):
            try:
                with open(recipe_data_path, 'r') as f:
                    content = f.read().decode('utf-8')
                    # 使用object_pairs_hook=OrderedDict保持JSON中的顺序
                    loaded_data = json.loads(content, object_pairs_hook=OrderedDict)

                    # 检查是否是新格式（包含分页键）
                    if isinstance(loaded_data, OrderedDict):
                        if "items" in loaded_data or "blocks" in loaded_data or "star" in loaded_data:
                            # 确保每个分页都是OrderedDict
                            self.materials_data = OrderedDict()
                            for tab_key in ["items", "blocks", "star"]:
                                if tab_key in loaded_data:
                                    tab_data = loaded_data[tab_key]
                                    if isinstance(tab_data, dict):
                                        # 转换为OrderedDict保持顺序
                                        self.materials_data[tab_key] = OrderedDict(tab_data)
                                    else:
                                        self.materials_data[tab_key] = OrderedDict()
                                else:
                                    self.materials_data[tab_key] = OrderedDict()
                        else:
                            # 旧格式，全部放入items
                            self.materials_data["items"] = OrderedDict(loaded_data)
                    else:
                        self.materials_data["items"] = OrderedDict()
            except Exception as e:
                print(u"加载材料数据失败:", str(e))
                self.create_default_materials()
        else:
            self.create_default_materials()

    def create_default_materials(self):
        u"""创建默认材料数据 - 使用OrderedDict保持顺序"""
        self.materials_data = OrderedDict([
            ("items", OrderedDict([
                ("*0", [u"netease.V3.4|MCBE.V1.21.00", 0]),
                ("*00", [u"", 0]),
                ("stick", [u"木棍", 0]),
                ("paper", [u"纸", 0]),
                ("string", [u"线", 0]),
                ("leather", [u"皮革", 0]),
                ("feather", [u"羽毛", 0]),
                ("book", [u"书", 0]),
                ("bone", [u"骨头", 0]),
                ("bone_meal", [u"骨粉", 0]),
                ("clay_ball", [u"粘土球", 0]),
                ("slime_ball", [u"粘液球", 0]),
                ("bucket", [u"铁桶", 0]),
                ("brick", [u"红砖", 0]),
                ("gunpowder", [u"火药", 0]),
                ("wheat", [u"小麦", 0]),
                ("blaze_rod", [u"烈焰棒", 0]),
                ("blaze_powder", [u"烈焰粉", 0]),
                ("*01", [u"", 0]),
                ("glowstone_dust", [u"萤石粉", 0]),
                ("coal", [u"煤炭", 0]),
                ("redstone", [u"红石粉", 0]),
                ("iron_ingot", [u"铁锭", 0]),
                ("gold_ingot", [u"金锭", 0]),
                ("lapis_lazuli", [u"青金石", 0]),
                ("diamond", [u"钻石", 0]),
                ("emerald", [u"绿宝石", 0]),
                ("amethyst_shard", [u"紫水晶碎片", 0]),
                ("netherite_ingot", [u"下界合金锭", 0]),
                ("quartz", [u"下界石英", 0]),
                ("netherbrick", [u"下界砖", 0]),
                ("gold_nugget", [u"金粒", 0]),
                ("iron_nugget", [u"铁粒", 0]),
                ("*1", [u"", 0]),
                ("ink_sac", [u"墨囊", 0]),
                ("glow_ink_sac", [u"发光墨囊", 0]),
                ("black_dye", [u"黑色染料", 0]),
                ("red_dye", [u"红色染料", 0]),
                ("green_dye", [u"绿色染料", 0]),
                ("brown_dye", [u"棕色染料", 0]),
                ("blue_dye", [u"蓝色染料", 0]),
                ("purple_dye", [u"紫色染料", 0]),
                ("cyan_dye", [u"青色染料", 0]),
                ("light_gray_dye", [u"淡灰色染料", 0]),
                ("gray_dye", [u"灰色染料", 0]),
                ("pink_dye", [u"粉红色染料", 0]),
                ("lime_dye", [u"黄绿色染料", 0]),
                ("yellow_dye", [u"黄色染料", 0]),
                ("light_blue_dye", [u"淡蓝色染料", 0]),
                ("magenta_dye", [u"品红色染料", 0]),
                ("orange_dye", [u"橙色染料", 0]),
                ("white_dye", [u"白色染料", 0]),
                ("*2", [u"", 0]),
                ("oak_sapling", [u"橡树树苗", 0]),
                ("spruce_sapling", [u"云杉树苗", 0]),
                ("birch_sapling", [u"白桦树苗", 0]),
                ("jungle_sapling", [u"丛林树苗", 0]),
                ("acacia_sapling", [u"金合欢树苗", 0]),
                ("dark_oak_sapling", [u"深色橡树苗", 0]),
                ("cherry_sapling", [u"樱花树苗", 0]),
                ("*3", [u"", 0]),
                ("short_grass", [u"矮草丛", 0]),
                ("fern", [u"蕨", 0]),
                ("poppy", [u"虞美人", 0]),
                ("blue_orchid", [u"兰花", 0]),
                ("allium", [u"绒球葱", 0]),
                ("azure_bluet", [u"蓝花美耳草", 0]),
                ("red_tulip", [u"红色郁金香", 0]),
                ("orange_tulip", [u"橙色郁金香", 0]),
                ("white_tulip", [u"白色郁金香", 0]),
                ("pink_tulip", [u"粉红色郁金香", 0]),
                ("oxeye_daisy", [u"滨菊", 0]),
                ("cornflower", [u"矢车菊", 0]),
                ("lily_of_the_valley", [u"铃兰", 0]),
                ("sunflower", [u"向日葵", 0]),
                ("lilac", [u"丁香", 0]),
                ("tall_grass", [u"高草丛", 0]),
                ("large_fern", [u"大型蕨", 0]),
                ("rose_bush", [u"玫瑰丛", 0]),
                ("peony", [u"牡丹", 0]),
                ("*4", [u"", 0])
            ])),
            ("blocks", OrderedDict([
                ("dirt", [u"泥土", 0]),
                ("stone", [u"石头", 0]),
                ("cobblestone", [u"圆石", 0]),
                ("quartz_block", [u"石英块", 0]),
                ("obsidian", [u"黑曜石", 0]),
                ("**1", [u"", 0]),
                ("beacon", [u"信标", 0]),
                ("flower_pot", [u"花盆", 0]),
                ("chest", [u"箱子", 0]),
                ("lever", [u"拉杆", 0]),
                ("noteblock", [u"音符盒", 0]),
                ("torch", [u"火把", 0]),
                ("coal_block", [u"煤炭块", 0]),
                ("iron_block", [u"铁块", 0]),
                ("gold_block", [u"金块", 0]),
                ("diamond_block", [u"钻石块", 0]),
                ("emerald_block", [u"绿宝石块", 0]),
                ("redstone_block", [u"红石块", 0]),
                ("lapis_block", [u"青金石块", 0]),
                ("nether_wart_block", [u"下界疣块", 0]),
                ("end_stone", [u"末地石", 0]),
                ("sponge", [u"海绵", 0]),
                ("**2", [u"", 0]),
                ("oak_planks", [u"橡木木板", 0]),
                ("spruce_planks", [u"云杉树木板", 0]),
                ("birch_planks", [u"白桦木板", 0]),
                ("jungle_planks", [u"丛林树木板", 0]),
                ("acacia_planks", [u"金合欢木板", 0]),
                ("dark_oak_planks", [u"深色橡木板", 0]),
                ("mangrove_planks", [u"红树木板", 0]),
                ("cherry_planks", [u"樱花木板", 0]),
                ("bamboo_planks", [u"竹板", 0]),
                ("crimson_planks", [u"绯红木板", 0]),
                ("warped_planks", [u"诡异木板", 0]),
                ("**3", [u"", 0]),
                ("oak_log", [u"橡木原木", 0]),
                ("spruce_log", [u"云杉原木", 0]),
                ("birch_log", [u"白桦原木", 0]),
                ("jungle_log", [u"丛林原木", 0]),
                ("acacia_log", [u"金合欢原木", 0]),
                ("dark_oak_log", [u"深色橡木原木", 0]),
                ("mangrove_log", [u"红树原木", 0]),
                ("cherry_log", [u"樱花原木", 0]),
                ("crimson_stem", [u"绯红菌柄", 0]),
                ("warped_stem", [u"诡异菌柄", 0]),
                ("**4", [u"", 0]),
                ("stripped_oak_wood", [u"去皮橡木", 0]),
                ("stripped_spruce_wood", [u"去皮云杉木", 0]),
                ("stripped_birch_wood", [u"去皮桦木", 0]),
                ("stripped_jungle_wood", [u"去皮丛林木", 0]),
                ("stripped_acacia_wood", [u"去皮金合欢木", 0]),
                ("stripped_dark_oak_wood", [u"去皮深色橡木", 0]),
                ("stripped_mangrove_log", [u"去皮红树木", 0]),
                ("stripped_cherry_log", [u"去皮樱花木", 0]),
                ("stripped_crimson_stem", [u"去皮绯红菌柄", 0]),
                ("stripped_warped_stem", [u"去皮诡异菌柄", 0]),
                ("**5", [u"", 0]),
                ("oak_wood", [u"橡木木块", 0]),
                ("spruce_wood", [u"云杉木木块", 0]),
                ("birch_wood", [u"白桦木木块", 0]),
                ("jungle_wood", [u"丛林木木块", 0]),
                ("acacia_wood", [u"金合欢木木块", 0]),
                ("dark_oak_wood", [u"深色橡木木块", 0]),
                ("mangrove_wood", [u"红树木木块", 0]),
                ("cherry_wood", [u"樱花木木块", 0]),
                ("crimson_hyphae", [u"绯红菌柄木块", 0]),
                ("warped_hyphae", [u"诡异菌柄木块", 0]),
                ("**6", [u"", 0]),
                ("white_wool", [u"白色羊毛", 0]),
                ("orange_wool", [u"橙色羊毛", 0]),
                ("magenta_wool", [u"品红色羊毛", 0]),
                ("light_blue_wool", [u"淡蓝色羊毛", 0]),
                ("yellow_wool", [u"黄色羊毛", 0]),
                ("lime_wool", [u"黄绿色羊毛", 0]),
                ("pink_wool", [u"粉红色羊毛", 0]),
                ("gray_wool", [u"灰色羊毛", 0]),
                ("light_gray_wool", [u"淡灰色羊毛", 0]),
                ("cyan_wool", [u"青色羊毛", 0]),
                ("purple_wool", [u"紫色羊毛", 0]),
                ("blue_wool", [u"蓝色羊毛", 0]),
                ("brown_wool", [u"棕色羊毛", 0]),
                ("green_wool", [u"绿色羊毛", 0]),
                ("red_wool", [u"红色羊毛", 0]),
                ("black_wool", [u"黑色羊毛", 0]),
                ("**7", [u"", 0]),
                ("glass", [u"玻璃块", 0]),
                ("white_stained_glass", [u"白色染色玻璃", 0]),
                ("orange_stained_glass", [u"橙色玻璃", 0]),
                ("magenta_stained_glass", [u"品红色玻璃", 0]),
                ("light_blue_stained_glass", [u"淡蓝色玻璃", 0]),
                ("yellow_stained_glass", [u"黄色玻璃", 0]),
                ("lime_stained_glass", [u"黄绿色玻璃", 0]),
                ("pink_stained_glass", [u"粉红色玻璃", 0]),
                ("gray_stained_glass", [u"灰色玻璃", 0]),
                ("light_gray_stained_glass", [u"淡灰色玻璃", 0]),
                ("cyan_stained_glass", [u"青色玻璃", 0]),
                ("purple_stained_glass", [u"紫色玻璃", 0]),
                ("blue_stained_glass", [u"蓝色玻璃", 0]),
                ("brown_stained_glass", [u"棕色玻璃", 0]),
                ("green_stained_glass", [u"绿色玻璃", 0]),
                ("red_stained_glass", [u"红色玻璃", 0]),
                ("black_stained_glass", [u"黑色玻璃", 0]),
                ("**8", [u"", 0]),
                ("glass_pane", [u"玻璃板", 0]),
                ("white_stained_glass_pane", [u"白色玻璃板", 0]),
                ("orange_stained_glass_pane", [u"橙色玻璃板", 0]),
                ("magenta_stained_glass_pane", [u"品红色玻璃板", 0]),
                ("light_blue_stained_glass_pane", [u"淡蓝色玻璃板", 0]),
                ("yellow_stained_glass_pane", [u"黄色玻璃板", 0]),
                ("lime_stained_glass_pane", [u"黄绿色玻璃板", 0]),
                ("pink_stained_glass_pane", [u"粉红色玻璃板", 0]),
                ("gray_stained_glass_pane", [u"灰色玻璃板", 0]),
                ("light_gray_stained_glass_pane", [u"淡灰色玻璃板", 0]),
                ("cyan_stained_glass_pane", [u"青色玻璃板", 0]),
                ("purple_stained_glass_pane", [u"紫色玻璃板", 0]),
                ("blue_stained_glass_pane", [u"蓝色玻璃板", 0]),
                ("brown_stained_glass_pane", [u"棕色玻璃板", 0]),
                ("green_stained_glass_pane", [u"绿色玻璃板", 0]),
                ("red_stained_glass_pane", [u"红色玻璃板", 0]),
                ("black_stained_glass_pane", [u"黑色玻璃板", 0]),
                ("**9", [u"", 0]),
                ("hardened_clay", [u"陶瓦", 0]),
                ("white_terracotta", [u"白色陶瓦", 0]),
                ("orange_terracotta", [u"橙色陶瓦", 0]),
                ("magenta_terracotta", [u"品红色陶瓦", 0]),
                ("light_blue_terracotta", [u"淡蓝色陶瓦", 0]),
                ("yellow_terracotta", [u"黄色陶瓦", 0]),
                ("lime_terracotta", [u"黄绿色陶瓦", 0]),
                ("pink_terracotta", [u"粉红色陶瓦", 0]),
                ("gray_terracotta", [u"灰色陶瓦", 0]),
                ("light_gray_terracotta", [u"淡灰色陶瓦", 0]),
                ("cyan_terracotta", [u"青色陶瓦", 0]),
                ("purple_terracotta", [u"紫色陶瓦", 0]),
                ("blue_terracotta", [u"蓝色陶瓦", 0]),
                ("brown_terracotta", [u"棕色陶瓦", 0]),
                ("green_terracotta", [u"绿色陶瓦", 0]),
                ("red_terracotta", [u"红色陶瓦", 0]),
                ("black_terracotta", [u"黑色陶瓦", 0]),
                ("**10", [u"", 0]),
                ("white_concrete_powder", [u"白色混凝土粉末", 0]),
                ("orange_concrete_powder", [u"橙色混凝土粉末", 0]),
                ("magenta_concrete_powder", [u"品红色混凝土粉末", 0]),
                ("light_blue_concrete_powder", [u"淡蓝色混凝土粉末", 0]),
                ("yellow_concrete_powder", [u"黄色混凝土粉末", 0]),
                ("lime_concrete_powder", [u"黄绿色混凝土粉末", 0]),
                ("pink_concrete_powder", [u"粉红色混凝土粉末", 0]),
                ("gray_concrete_powder", [u"灰色混凝土粉末", 0]),
                ("light_gray_concrete_powder", [u"淡灰色混凝土粉末", 0]),
                ("cyan_concrete_powder", [u"青色混凝土粉末", 0]),
                ("purple_concrete_powder", [u"紫色混凝土粉末", 0]),
                ("blue_concrete_powder", [u"蓝色混凝土粉末", 0]),
                ("brown_concrete_powder", [u"棕色混凝土粉末", 0]),
                ("green_concrete_powder", [u"绿色混凝土粉末", 0]),
                ("red_concrete_powder", [u"红色混凝土粉末", 0]),
                ("black_concrete_powder", [u"黑色混凝土粉末", 0]),
                ("**11", [u"", 0]),
                ("smooth_stone_slab", [u"平滑石台阶", 0]),
                ("sandstone_slab", [u"砂岩台阶", 0]),
                ("petrified_oak_slab", [u"石化橡木台阶", 0]),
                ("cobblestone_slab", [u"圆石台阶", 0]),
                ("brick_slab", [u"红砖台阶", 0]),
                ("stone_brick_slab", [u"石砖台阶", 0]),
                ("quartz_slab", [u"石英台阶", 0]),
                ("nether_brick_slab", [u"下界砖台阶", 0]),
                ("oak_slab", [u"橡木台阶", 0]),
                ("spruce_slab", [u"云杉木台阶", 0]),
                ("birch_slab", [u"白桦木台阶", 0]),
                ("jungle_slab", [u"丛林木台阶", 0]),
                ("acacia_slab", [u"金合欢木台阶", 0]),
                ("dark_oak_slab", [u"深色橡木台阶", 0]),
                ("**13", [u"", 0]),
                ("granite", [u"花岗岩", 0]),
                ("polished_granite", [u"磨制花岗岩", 0]),
                ("diorite", [u"闪长岩", 0]),
                ("polished_diorite", [u"磨制闪长岩", 0]),
                ("andesite", [u"安山岩", 0]),
                ("polished_andesite", [u"磨制安山岩", 0]),
                ("**14", [u"", 0]),
                ("oak_leaves", [u"橡树树叶", 0]),
                ("spruce_leaves", [u"云杉树叶", 0]),
                ("birch_leaves", [u"白桦树叶", 0]),
                ("jungle_leaves", [u"丛林树叶", 0]),
                ("acacia_leaves", [u"金合欢树叶", 0]),
                ("dark_oak_leaves", [u"深色橡树叶", 0]),
                ("azalea_leaves", [u"杜鹃树叶", 0]),
                ("azalea_leaves_flowered", [u"开花杜鹃树叶", 0]),
                ("mangrove_leaves", [u"红树树叶", 0]),
                ("cherry_leaves", [u"樱花树叶", 0]),
                ("**15", [u"", 0]),
                ("oak_fence", [u"橡木栅栏", 0]),
                ("spruce_fence", [u"云杉木栅栏", 0]),
                ("birch_fence", [u"白桦木栅栏", 0]),
                ("jungle_fence", [u"丛林木栅栏", 0]),
                ("acacia_fence", [u"金合欢木栅栏", 0]),
                ("dark_oak_fence", [u"深色橡木栅栏", 0]),
                ("mangrove_fence", [u"红树木栅栏", 0]),
                ("cherry_fence", [u"樱花木栅栏", 0]),
                ("bamboo_fence", [u"竹栅栏", 0]),
                ("crimson_fence", [u"绯红木栅栏", 0]),
                ("warped_fence", [u"诡异木栅栏", 0]),
                ("**16", [u"", 0]),
                ("white_carpet", [u"白色地毯", 0]),
                ("orange_carpet", [u"橙色地毯", 0]),
                ("magenta_carpet", [u"品红色地毯", 0]),
                ("light_blue_carpet", [u"淡蓝色地毯", 0]),
                ("yellow_carpet", [u"黄色地毯", 0]),
                ("lime_carpet", [u"黄绿色地毯", 0]),
                ("pink_carpet", [u"粉红色地毯", 0]),
                ("gray_carpet", [u"灰色地毯", 0]),
                ("light_gray_carpet", [u"淡灰色地毯", 0]),
                ("cyan_carpet", [u"青色地毯", 0]),
                ("purple_carpet", [u"紫色地毯", 0]),
                ("blue_carpet", [u"蓝色地毯", 0]),
                ("brown_carpet", [u"棕色地毯", 0]),
                ("green_carpet", [u"绿色地毯", 0]),
                ("red_carpet", [u"红色地毯", 0]),
                ("black_carpet", [u"黑色地毯", 0]),
                ("**17", [u"", 0]),
                ("white_concrete", [u"白色混凝土", 0]),
                ("orange_concrete", [u"橙色混凝土", 0]),
                ("magenta_concrete", [u"品红色混凝土", 0]),
                ("light_blue_concrete", [u"淡蓝色混凝土", 0]),
                ("yellow_concrete", [u"黄色混凝土", 0]),
                ("lime_concrete", [u"黄绿色混凝土", 0]),
                ("pink_concrete", [u"粉红色混凝土", 0]),
                ("gray_concrete", [u"灰色混凝土", 0]),
                ("light_gray_concrete", [u"淡灰色混凝土", 0]),
                ("cyan_concrete", [u"青色混凝土", 0]),
                ("purple_concrete", [u"紫色混凝土", 0]),
                ("blue_concrete", [u"蓝色混凝土", 0]),
                ("brown_concrete", [u"棕色混凝土", 0]),
                ("green_concrete", [u"绿色混凝土", 0]),
                ("red_concrete", [u"红色混凝土", 0]),
                ("black_concrete", [u"黑色混凝土", 0]),
                ("**18", [u"", 0])
            ])),
            ("star", OrderedDict([
                ("jxl:debug_item", [u"测试物品", 0])
            ]))
        ])
        self.save_materials()

    def save_materials(self):
        u"""保存材料数据"""
        try:
            with open("recipeData.json", 'w') as f:
                content = json.dumps(self.materials_data, ensure_ascii=False, indent=2)
                f.write(content.encode('utf-8'))
        except Exception as e:
            print(u"保存材料数据失败:", str(e))

    def create_ui(self):
        u"""创建用户界面"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.create_file_panel(main_frame)
        self.create_material_panel(main_frame)
        self.create_editor_panel(main_frame)

    def create_file_panel(self, parent):
        u"""创建文件浏览面板"""
        frame = ttk.LabelFrame(parent, text=u"文件浏览", width=200)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=2)
        frame.pack_propagate(False)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=2, pady=2)

        ttk.Button(btn_frame, text=u"刷新", command=self.refresh_files).pack(side=tk.LEFT)

        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.file_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                       selectmode=tk.SINGLE, font=('Arial', 10))
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)

        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)

        ttk.Label(frame, text=u"当前选择:").pack(anchor=tk.W, padx=2)
        self.file_label = ttk.Label(frame, textvariable=self.selected_file,
                                    wraplength=180, foreground="blue")
        self.file_label.pack(fill=tk.X, padx=2, pady=2)

    def create_material_panel(self, parent):
        u"""创建材料选择面板"""
        frame = ttk.LabelFrame(parent, text=u"合成材料", width=240)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=2)
        frame.pack_propagate(False)

        # 分页选择按钮
        tab_frame = ttk.Frame(frame)
        tab_frame.pack(fill=tk.X, padx=2, pady=2)

        ttk.Radiobutton(tab_frame, text=u"物品", variable=self.material_tab,
                       value="items", command=self.on_tab_change).pack(side=tk.LEFT, padx=2)
        ttk.Radiobutton(tab_frame, text=u"方块", variable=self.material_tab,
                       value="blocks", command=self.on_tab_change).pack(side=tk.LEFT, padx=2)
        ttk.Radiobutton(tab_frame, text=u"收藏", variable=self.material_tab,
                       value="star", command=self.on_tab_change).pack(side=tk.LEFT, padx=2)

        # 刷新和删除按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=2, pady=2)

        ttk.Button(btn_frame, text=u"刷新", command=self.refresh_materials).pack(side=tk.LEFT)
        self.delete_btn = ttk.Button(btn_frame, text=u"删除", command=self.toggle_delete_mode)
        self.delete_btn.pack(side=tk.LEFT, padx=5)

        # 材料列表
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.material_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                           selectmode=tk.SINGLE, font=('Arial', 9))
        self.material_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.material_listbox.yview)

        self.material_listbox.bind('<<ListboxSelect>>', self.on_material_select)

        self.update_material_list()

        # 底部显示 - 蓝色
        ttk.Label(frame, text=u"当前材料:").pack(anchor=tk.W, padx=2)
        self.material_label = ttk.Label(frame, textvariable=self.selected_material,
                                        wraplength=220, foreground="blue")
        self.material_label.pack(fill=tk.X, padx=2, pady=2)

    def create_editor_panel(self, parent):
        u"""创建编辑面板"""
        frame = ttk.LabelFrame(parent, text=u"合成编辑")
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)

        # 合成类型选择
        type_frame = ttk.LabelFrame(frame, text=u"合成类型")
        type_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Radiobutton(type_frame, text=u"有序合成", variable=self.recipe_type,
                       value=u"有序合成").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(type_frame, text=u"无序合成", variable=self.recipe_type,
                       value=u"无序合成").pack(side=tk.LEFT, padx=10)

        # 自定义ID设置
        id_frame = ttk.LabelFrame(frame, text=u"输出物品设置")
        id_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Checkbutton(id_frame, text=u"是否自定义方块ID", variable=self.custom_id_enabled,
                       command=self.on_custom_id_toggle).pack(anchor=tk.W, padx=5, pady=2)

        input_frame = ttk.Frame(id_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(input_frame, text=u"命名空间:").grid(row=0, column=0, sticky=tk.W)
        self.namespace_entry = ttk.Entry(input_frame, textvariable=self.namespace, width=15)
        self.namespace_entry.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text=u"方块ID:").grid(row=0, column=2, sticky=tk.W, padx=(10,0))
        self.block_id_entry = ttk.Entry(input_frame, textvariable=self.block_id, width=15, state="disabled")
        self.block_id_entry.grid(row=0, column=3, padx=5)

        # 产出数量
        count_frame = ttk.Frame(id_frame)
        count_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(count_frame, text=u"产出数量:").pack(side=tk.LEFT)
        self.count_scale = tk.Scale(count_frame, from_=1, to=16, orient=tk.HORIZONTAL,
                                   variable=self.output_count, length=200)
        self.count_scale.pack(side=tk.LEFT, padx=10)
        ttk.Label(count_frame, textvariable=self.output_count).pack(side=tk.LEFT)

        # 九宫格区域 - 左对齐，加宽
        grid_frame = ttk.LabelFrame(frame, text=u"合成配方 (3x3) - 点击下方格子填入材料")
        grid_frame.pack(fill=tk.X, padx=5, pady=5, anchor=tk.W)

        grid_container = ttk.Frame(grid_frame)
        grid_container.pack(padx=10, pady=10, anchor=tk.W)

        # 创建九宫格 - 矩形按钮，左对齐
        button_width = 12
        button_height = 2
        label_width = 14

        for row in range(3):
            for col in range(3):
                idx = row * 3 + col

                btn = tk.Button(grid_container, text="", width=button_width, height=button_height,
                              command=lambda i=idx: self.on_grid_click(i))
                btn.grid(row=row*2, column=col, padx=3, pady=2, sticky="w")
                self.grid_buttons.append(btn)

                lbl = ttk.Label(grid_container, text="", width=label_width, font=('SimHei', 9),
                               background="#f0f0f0", relief="solid", anchor="center")
                lbl.grid(row=row*2+1, column=col, padx=3, pady=1, sticky="w")
                self.grid_labels.append(lbl)

        # 生成按钮、清空按钮、说明按钮
        action_frame = ttk.Frame(frame)
        action_frame.pack(fill=tk.X, padx=5, pady=10)

        ttk.Button(action_frame, text=u"生成配方", command=self.generate_recipe).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=u"清空九宫格", command=self.clear_grid).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=u"使用说明", command=self.show_help).pack(side=tk.LEFT, padx=5)

        # 信息标签
        info_frame = ttk.Frame(frame)
        info_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(info_frame, text=u"状态:").pack(side=tk.LEFT)
        self.info_label = ttk.Label(info_frame, textvariable=self.info_text,
                                   foreground="blue", wraplength=600)
        self.info_label.pack(side=tk.LEFT, padx=5)

    def show_help(self):
        u"""显示使用说明"""
        help_text = "【{} 使用说明】\n\
*{}*\n\
*作者: {}\n\n\
【基本流程】\n\
1. 在左侧”文件浏览“中选择基础文件（决定输出文件名/输出物品id）\n\
   或勾选”自定义方块ID“手动输入作为文件名/输出物品id\n\
\n\
2. 在中间”合成材料“中选择分页（物品/方块/收藏）：\n\
   - 点击材料名称选中\n\
\n\
3. 在右侧”合成编辑“中：\n\
   - 选择合成类型：有序/无序\n\
   - 设置合成结果产出物品数量（1-16）\n\
   - 点击九宫格格子填入材料\n\
   - 点击”删除“按钮后再点击格子可清空\n\
\n\
4. 点击”生成配方“，结果保存到newFile文件夹\n\
\n\
【材料ID说明】\n\
- 材料列表中的英文ID如不含冒号，生成时会自动给材料id添加“minecraft:”前缀\n\
- 如包含冒号则保持原样（如jxl:new_item）\n\
\n\
【材料数据】\n\
- recipeData.json结构：（”items“: ..., ”blocks“: ..., ”star“: ...）\n\
- 每个分页内的材料严格按JSON中的原始顺序展示\n\
- 格式：”item_id‘: [“中文名”, 特殊值]\n\
- 占位符：“*”: [“---”, 0]（英文ID含*即为占位符）\n\
\n- {} -".format(Best_N, Best_Vb, Best_A, Best_T)



        help_window = tk.Toplevel(self.root)
        help_window.title(u"使用说明")
        help_window.geometry("600x400")
        help_window.transient(self.root)
        help_window.grab_set()

        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10, font=('SimHei', 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)

        scrollbar = ttk.Scrollbar(text_widget, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)

        ttk.Button(help_window, text=u"关闭", command=help_window.destroy).pack(pady=5)

    def on_tab_change(self):
        u"""分页切换事件"""
        self.update_material_list()
        self.info_text.set(u"已切换到: %s" % self.get_tab_name())

    def get_tab_name(self):
        u"""获取当前分页名称"""
        tab_map = {
            "items": u"物品",
            "blocks": u"方块",
            "star": u"收藏"
        }
        return tab_map.get(self.material_tab.get(), u"未知")

    def on_custom_id_toggle(self):
        u"""自定义ID开关切换"""
        if self.custom_id_enabled.get():
            self.block_id_entry.config(state="normal")
        else:
            self.block_id_entry.config(state="disabled")

    def refresh_files(self):
        u"""刷新文件列表"""
        self.file_listbox.delete(0, tk.END)

        if not os.path.exists("file"):
            os.makedirs("file")

        files = []
        for f in os.listdir("file"):
            if f.endswith(".json"):
                files.append(f[:-5])

        files.sort()
        for f in files:
            self.file_listbox.insert(tk.END, f)

        self.info_text.set(u"文件列表已刷新，共 %d 个文件" % len(files))

    def refresh_materials(self):
        u"""刷新材料列表 - 重新读取文件"""
        self.load_materials()
        self.update_material_list()
        total = sum(len(v) for v in self.materials_data.values())
        self.info_text.set(u"材料数据已重新加载，共 %d 种材料" % total)

    def update_material_list(self):
        u"""更新材料列表显示 - 严格按OrderedDict中的顺序"""
        self.material_listbox.delete(0, tk.END)

        # 获取当前分页
        current_tab = self.material_tab.get()
        # 获取该分页的OrderedDict材料字典
        materials = self.materials_data.get(current_tab, OrderedDict())

        # 遍历OrderedDict，严格保持插入顺序
        for item_id, info in materials.items():
            chinese_name = info[0]
            data = info[1] if len(info) > 1 else 0

            # 检查是否为占位符（英文ID包含*）
            is_placeholder = "*" in item_id

            if is_placeholder:
                # 占位符只显示中文名
                display_text = u"%s" % chinese_name
            else:
                # 普通材料显示中文名和英文ID
                if data != 0:
                    display_text = u"%s\n  %s [data:%d]" % (chinese_name, item_id, data)
                else:
                    display_text = u"%s\n  %s" % (chinese_name, item_id)

            self.material_listbox.insert(tk.END, display_text)

    def on_file_select(self, event):
        u"""文件选择事件"""
        selection = self.file_listbox.curselection()
        if selection:
            idx = selection[0]
            filename = self.file_listbox.get(idx)
            self.selected_file.set(filename)

    def on_material_select(self, event):
        u"""材料选择事件"""
        selection = self.material_listbox.curselection()
        if selection:
            idx = selection[0]

            # 获取当前分页
            current_tab = self.material_tab.get()
            # 获取该分页的OrderedDict
            materials = self.materials_data.get(current_tab, OrderedDict())

            # 转换为列表保持顺序，通过索引获取选中项
            items_list = list(materials.items())

            if idx < len(items_list):
                item_id, info = items_list[idx]
                chinese_name = info[0]
                data = info[1] if len(info) > 1 else 0

                # 检查是否为占位符（英文ID包含*）
                if "*" in item_id:
                    self.selected_material.set(u"[占位符] %s - 无法填入" % chinese_name)
                    self.current_material_id = None
                    self.current_material_name = None
                    self.current_material_data = 0
                    self.current_is_placeholder = True
                    self.delete_mode = False
                    self.delete_btn.config(text=u"删除")
                    return

                self.selected_material.set(chinese_name)
                self.current_material_id = item_id
                self.current_material_name = chinese_name
                self.current_material_data = data
                self.current_is_placeholder = False
                self.delete_mode = False
                self.delete_btn.config(text=u"删除")

    def toggle_delete_mode(self):
        u"""切换删除模式"""
        self.delete_mode = not self.delete_mode
        if self.delete_mode:
            self.delete_btn.config(text=u"[删除中]")
            self.selected_material.set(u"删除模式 - 点击九宫格删除")
        else:
            self.delete_btn.config(text=u"删除")
            self.selected_material.set(u"未选择")

    def on_grid_click(self, idx):
        u"""九宫格点击事件"""
        if self.delete_mode:
            self.grid_data[idx] = None
            self.grid_buttons[idx].config(text="")
            self.grid_labels[idx].config(text="")
            self.info_text.set(u"已清空格子 %d" % (idx + 1))
        else:
            # 检查是否选中了占位符或没有选中材料
            if self.current_is_placeholder:
                self.info_text.set(u"占位符无法填入！")
                return

            if not self.current_material_id:
                self.info_text.set(u"请先选择有效材料！")
                return

            # 存储元组 (item_id, data)
            self.grid_data[idx] = (self.current_material_id, self.current_material_data)
            # 如果有data不为0，显示在标签中
            if self.current_material_data != 0:
                display_text = u"%s[%d]" % (self.current_material_name, self.current_material_data)
            else:
                display_text = self.current_material_name
            self.grid_labels[idx].config(text=display_text)
            self.info_text.set(u"格子 %d 填入: %s" % (idx + 1, display_text))

    def clear_grid(self):
        u"""清空九宫格"""
        for i in range(9):
            self.grid_data[i] = None
            self.grid_buttons[i].config(text="")
            self.grid_labels[i].config(text="")
        self.info_text.set(u"九宫格已清空")

    def ensure_namespace(self, item_id):
        u"""确保材料ID包含命名空间，如果没有则添加minecraft:"""
        if ":" in item_id:
            return item_id
        return "minecraft:" + item_id

    def generate_recipe(self):
        u"""生成配方JSON"""
        # 确定输出文件名和方块ID
        if self.custom_id_enabled.get():
            if not self.block_id.get().strip():
                self.info_text.set(u"错误：请填写方块ID！")
                messagebox.showerror(u"错误", u"自定义方块ID已启用，请填写方块ID！")
                return
            filename = self.block_id.get().strip()
            full_block_id = "%s:%s" % (self.namespace.get().strip(), filename)
        else:
            if self.selected_file.get() == u"未选择" or not self.selected_file.get():
                self.info_text.set(u"错误：请选择文件或启用自定义ID！")
                messagebox.showerror(u"错误", u"请选择文件列表中的文件，或启用自定义方块ID！")
                return
            filename = self.selected_file.get()
            full_block_id = "%s:%s" % (self.namespace.get().strip(), filename)

        # 收集九宫格中的材料（去重，并确保命名空间）
        used_items = []  # 存储 (full_item_id, data) 元组
        for item in self.grid_data:
            if item:
                raw_item_id, data = item
                # 确保命名空间
                full_item_id = self.ensure_namespace(raw_item_id)
                item_tuple = (full_item_id, data)
                if item_tuple not in used_items:
                    used_items.append(item_tuple)

        if not used_items:
            self.info_text.set(u"错误：九宫格为空！")
            messagebox.showerror(u"错误", u"请在九宫格中至少放置一种材料！")
            return

        # 检查是否超过9种
        if len(used_items) > 9:
            self.info_text.set(u"错误：材料种类超过9种！")
            messagebox.showerror(u"错误", u"无序合成最多支持9种不同材料！")
            return

        # 判断合成类型
        is_shapeless = (self.recipe_type.get() == u"无序合成")

        if is_shapeless:
            # 无序合成格式
            ingredients = []
            for full_item_id, data in used_items:
                ingredient = {"item": full_item_id}
                if data != 0:
                    ingredient["data"] = data
                ingredients.append(ingredient)

            recipe_json = {
                "format_version": "1.12",
                "minecraft:recipe_shapeless": {
                    "description": {
                        "identifier": full_block_id
                    },
                    "tags": ["crafting_table"],
                    "ingredients": ingredients,
                    "result": {
                        "item": full_block_id,
                        "count": self.output_count.get()
                    }
                }
            }
        else:
            # 有序合成格式
            pattern = ["", "", ""]
            key = {}

            # 为每种材料分配字母
            for i, (full_item_id, data) in enumerate(used_items):
                letter = self.letters[i]
                key_entry = {"item": full_item_id}
                if data != 0:
                    key_entry["data"] = data
                key[letter] = key_entry

            # 生成pattern - 需要映射原始ID到字母
            raw_to_letter = {}
            for i, (full_item_id, data) in enumerate(used_items):
                for raw_id, d in [(x[0], x[1]) for x in self.grid_data if x]:
                    if self.ensure_namespace(raw_id) == full_item_id and d == data:
                        raw_to_letter[(raw_id, data)] = self.letters[i]
                        break

            for row in range(3):
                row_str = ""
                for col in range(3):
                    idx = row * 3 + col
                    item = self.grid_data[idx]
                    if item is None:
                        row_str += "0"
                    else:
                        raw_item_id, data = item
                        letter = raw_to_letter.get((raw_item_id, data), "?")
                        row_str += letter
                pattern[row] = row_str

            recipe_json = {
                "format_version": "1.12",
                "minecraft:recipe_shaped": {
                    "description": {
                        "identifier": full_block_id
                    },
                    "tags": ["crafting_table"],
                    "pattern": pattern,
                    "result": {
                        "item": full_block_id,
                        "count": self.output_count.get()
                    },
                    "key": key
                }
            }

        # 保存文件
        output_path = os.path.join("newFile", "%s.json" % filename)
        try:
            with open(output_path, 'w') as f:
                content = json.dumps(recipe_json, ensure_ascii=False, indent=4)
                f.write(content.encode('utf-8'))
        except Exception as e:
            messagebox.showerror(u"错误", u"保存文件失败: %s" % str(e))
            return

        # 成功生成，不弹窗
        recipe_type_str = u"无序" if is_shapeless else u"有序"
        self.info_text.set(u"成功生成%s配方: %s.json (ID: %s)" % (recipe_type_str, filename, full_block_id))


def main():
    root = tk.Tk()
    app = RecipeGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()

'''
Ai训练提示词 2026.3.22


我希望你基于py2.7+ttk写一个可视化操作程序，用于生成相对应的合成方式json，最终输出单一py文件。


运行程序时检测同目录下有没有file、newFile文件夹，没有就重新生成。

file下用户在其中放入待生成合成方式的json（之后会提取这些文件的文件名，不会读取文件内容）
newFile是合成方式结果输出文件的位置。

运行程序后打开界面。

界面由三个部分组成：
左边文件浏览/选择窗口，合成材料选择窗口，右边是合成方式编辑界面。(前两个可以是较窄的结构，内容过多是需要支持垂直滚动)

//文件浏览/选择窗口
每次打开程序后，左边文件浏览窗自动展示file文件夹下所有文件名(只识别json，展示时需要去掉.json后缀)。文件浏览窗顶部有一个刷新按钮，点击刷新实时文件夹内文件列表。

点击文件列表中的某一个文件即选中，文件浏览窗底部是一个文本控件，实时显示用户当前点击选择的文件。

//合成材料选择窗口
展示效果同文件浏览类似，不过所呈现的内容不是从file中获取，而是从同目录下的recipeData.json文件中提取，如果没有这个文件则生成，大致格式为字典：｛'物品id1': ['中文名', 0],  '物品id2': ['中文名2', 0]｝（里面那个数字填0就好）
材料窗口顶部同样有刷新按钮。
材料窗口每一项展示样式：黑体中文名/下一行小字灰体英文名(物品id)
点击材料列表中的某一个材料物品即选中，材料窗底部是一个文本控件，实时显示用户当前点击选择的材料(中文名)。

材料窗口顶部还有个删除按钮，与刷新按钮同一行，下方会说明用处。



//合成方式编辑界面

界面右边是编辑界面。
编辑界面顶部有一个单选项：有序合成(默认选择)/无序合成
这个选项相对应的逻辑功能暂不设计。

再下方是一个开关选项：是否自定义方块id（默认关）
开关之下需要填写两个输入框：命名空间、方块id
命名空间默认被填入jxl，方块id默认置空。

当勾选开关时，方块id输入框的值才有效(勾选后必填此项)，命名空间输入框是必填的。

再下一行是拖动条控件，用于控制该合成方式最终输出物品个数，默认为1，可调节1-16。
大致排版效果：
是否自定义方块id 
方块id：输入框1  输入框2  
产出数：拖动条

再下方是合成九宫格窗，简称九宫格，可以用按钮控件来制作，确保每一个格子是正方形。
与按钮九宫格同一行的还有另一个九宫格：文本九宫格，每一个格子对应合成九宫格对应的格子，用于展示被填入物品的中文名(告诉用户这个格子填入了什么材料)，文本默认为空。文本九宫格每一个格子是矩形的，宽度可以稍宽一些以便适配长文本(6个汉字宽度，字体可以小一些)

再下方是 生成 按钮 和信息文本控件。

//使用流程

玩家选取文件列表中的文件，然后在材料列表中选中材料，然后点击九宫格的格子，文本九宫格同步材料信息。

材料列表顶部的删除按钮，点击后底部材料选择文本显示为“删除”，随后点击九宫格的格子就会删除之前被填入的内容（同步文本九宫格），当重新选择材料列表中的材料时则取消当前的删除功能。

拖拽产出数拖动条以配置物品产出数量。

配置好了后，点击 生成按钮 则将当前配置输出合成.json文件到newFile中，文件名=文件列表中选取的文件名。
(后面会说明json中各个值对应界面中的值)

生成成功底部信息文本控件说明xx(方块id/文件名)生成成功！

当勾选了 是否自定义方块id 时，文件列表中被选取的文件名则无效，而是根据输入框中的值来生成合成方式（注意，完整的方块id为 命名空间+方块id，作为文件名时不需要命名空间，json内的方块id才需要命名空间+方块id）

完整方块id：命名空间:方块id   例：jxl:block  (注意有英文冒号)
作为文件名的方块id：方块id   例：block

当勾选了 是否自定义方块id 后，方块id输入框必须有内容！如果未填写就点击生成，底部信息文本控件可以弹出说明。



//示例json：
//记住最后输出的json不能带注释
{
	"format_version": "1.12",
	"minecraft:recipe_shaped": {
		"description": {
			"identifier": "jxl:wjxga_new_wood" //（完整方块id）
		},
		"tags": ["crafting_table"],
		"pattern": [
			"000", //这里的0是空占位符，意思是空
			"0a0", //这里的ab是材料占位符
			"bbb" //排版位置根据用户的九宫格配置来同步生成
		],
		"result": {
			"item": "jxl:wjxga_new_wood",  //（完整方块id，同上）

			"count": 1  //产出数量
		},
		"key": {
			"a": { //这里的ab是材料占位符，因为一个合成方式最多支持9种材料
				//也就是对应九宫格，那么材料占位符就从abcdefghi中按顺序选择，
				//不可以同时出现两个一样的字母
				
				"item": "minecraft:log"  //被填入的材料，也就是前面所说的英文id
			},
			"b": {
				"item": "minecraft:planks" 			}
		}

	}
}

/////////////////////
另外，九宫格按钮上不需要显示 材料映射字母

//////////////////////
非常好！！
现在九宫格按钮不强制为正方形，而是矩形，每个格子需要宽一些，下方的文本宽度相应大一些。

九宫格尽量往左边靠拢，以免浪费大量空间。

材料列表排版更新：
材料列表窗口顶部新增三个选择分页：物品/方块/收藏，现在分开展示
同时recipeData.json中的配置也拆分为三个字典｛'items': {...}, 'blocks': {...}, 'star': {...}｝
适配选中、置入材料功能。

材料列表的刷新按钮，按下后并没有重新提取recipeData.json的内容进行更新！

材料列表底部 选择材料的文本颜色 改为蓝色即可。

成功生成合成配方json后，无需弹窗说明。


//无序


很好！现在来落实无序配方。
当勾选了无序配方后，按照这样的格式来生成：

{
  "format_version": "1.12",
  "minecraft:recipe_shapeless": {
    "description": {
    "identifier": "minecraft:andesite" //（完整方块id）

    },
    "tags": [ "crafting_table" ],
    "ingredients": [
      {
        "item": "minecraft:stone",  //无序合成不需要字母映射，直接把九宫格填入的所有材料依次写入
        "data": 3 //这个数字取决于｛'物品id1': ['中文名', 3]} ←这里的数字，如果数字为0，直接不写"data"(前面有序配方也请同步更新这个"data")
      },
      {
        "item": "minecraft:cobblestone"  //此处直接不写"data"，因为对应的材料特殊值为0(前面有序配方也请同步更新这个"data")

      } //注意：最多写入9种材料，并且不允许出现重复的材料！(物品id、中文名、特殊值都相等的)
    ],
    "result": {
      "item": "minecraft:stone",  //（完整方块id）
      "count": 2  //产出数量
    }
  }
}



//说明，窗口大小



很好，现在需要更新一些功能

现在读取recipeData中英文id时，有可能此英文id并不包含命名空间如“stick”,我需要在生成json时，判定英文id是否包含命名空间,最直观的判定方法是判定字符串中是否包含英文冒号，如果不包含则加上默认命名空间 “minecraft:”，即最终写入json的材料id格式是 “minecraft:stick”。(材料列表的展示时无需判断英文id有无命名空间，英文id是什么就显示什么即可)

希望材料列表按照英文id来正序排序(abcd...)，先英文后数字。

我希望在 recipeData.json 加入空占位符，用于在材料列表中做上下项隔离：
在recipeData中的格式  "*": ["---", 0],  区别于普通材料项的地方是英文id中包含“*”，所有英文id包含*的都会被视为占位符，在材料列表刷新和初始化时，显示效果逻辑与其他材料无异，但是用户在材料列表中不能点选该项(占位符)，或者在选中该项后，无法再在九宫格中填入。

新增一个说明按钮，在生成按钮、清空九宫格之后。点击按钮弹窗，内有文本说明该项目大致使用方法。

没有提及的地方不做修改或删减！！

///////////////////////////


我现在希望 材料列表中的占位符，只显示中文名，英文id显示为空字符串 即''，
报错了：
Traceback (most recent call last):
  File "D:/WORK/pyW/.. ºϳ / ºϳ .pyw", line 670, in <module>
    main()
  File "D:/WORK/pyW/.. ºϳ / ºϳ .pyw", line 665, in main
    app = RecipeGenerator(root)
  File "D:/WORK/pyW/.. ºϳ / ºϳ .pyw", line 78, in __init__
    self.create_ui()
  File "D:/WORK/pyW/.. ºϳ / ºϳ .pyw", line 160, in create_ui
    self.create_file_panel(main_frame)
  File "D:/WORK/pyW/.. ºϳ / ºϳ .pyw", line 186, in create_file_panel
    self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)
AttributeError: RecipeGenerator instance has no attribute 'on_file_select'

////////////////////////////////////////////////////



由于recipeData是字典格式，且py2.7字典不支持顺序，占位符会因为此前排序逻辑而位列前列，故取消此前的根据英文id来排序的方法，而是改用recipeData字典中的每一项材料的顺序来对材料进行最终排序(字典里什么顺序，展示就什么顺序)。请确保程序能在py2.7中运行。

没有提及的地方不做修改或删减！！



/////////////////////////
材料列表排序展示非常混乱，毫无规律可言，也不是按照字典顺序来排，你看看这个recipeData文件，你是不是忘了recipeData之下还有一个分页键，然后才是材料项。

没有提及的地方不做修改或删减！！

//////////////////////////////
我找到原因了，你在py程序中写了一个materials_data字典来初始化recipeData，并且我前面要求按照字典排序，你是直接拿这个materials_data来排序，而忽略了当存在recipeData时需要读取recipeData，导致recipeData和materials_data不一致时，材料列表排序混乱。

没有提及的地方不做修改或删减！！


//适用于网易3.4版本(3.7暂不更新)







'''