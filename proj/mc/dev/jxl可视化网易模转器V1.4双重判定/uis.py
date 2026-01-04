# coding=utf-8

import os
import json
from collections import OrderedDict
import inspect

from tkinter import messagebox  # 弹窗
from datetime import datetime  # 获取时间

# 获取当前时间
Now = datetime.now()

ToolName = "JXL网易模型转换器"

Ver = 1.4

BGC4 = '#F0F0F0'  # 辅助底色

ReadMe0 = '==========\njxl井桢 版权所有\n++++++++++\n\n'

ReadMe2 = '\n\n********************\n版本说明：V' + str(Ver) + '\n' \
          '1.支持批量模型转换\n' \
          '2.支持筛选功能\n' \
          '3.支持报错弹窗\n' \
          '4.支持同步生成res配置文件\n'\
          '5.支持同步生成beh配置文件\n'\
          '6.修复textures的格式\n'\
          '7.支持链接双重判定'

ReadMe1 = ToolName + '\n这是一个将Blockbench导出的基岩版模型json模型转换为网易方块模型的工具\n\n***jxl井桢 版权所有***\n***反馈Q群：436506487***\n-2025.5.9-\n\n*【使用方法】\ninp  文件夹放入原模型\noutp  ' \
                     '文件夹查看转换结果\n【注意事项】请确保原模型json中没有注释！！\n\n【其他补充】\n转换后的方块的res/beh信息将以json形式储存在xres/xbeh文件夹中\n\n' \
                     '*方块自动连接使用说明：\nBlockbench中命名code或组为\nd、u、n、s、e、w(链接后隐藏)\nd2、u2、n2、s2、e2、w2(链接后显示)\n\n' \
                     '*链接双重判定*(目前支持的是&&)\nuw、ue、dw、de、、du、ns、we(链接后隐藏)\nuw2、ue2、dw2、de2、、du2、ns2、we2(链接后隐藏)\n\n'\
                     '*方块四角链接法*(模型N右下角顺时针)\nx1x2x3x4(链接隐藏)y1y2y3y4(链接显示)\n\n' \
                     '*模型物品贴图示例：\n"item_texture": "jxl:item0022", \n\n' \
                     '*注意：贴图ID不变  即贴图ID=方块ID' + ReadMe2

folders = ["inp", "outp", "xres", "xbeh"]

BGC0 = '#fff'  # 白色
BGC1 = '#c3c3c3'  # 列表颜色
BGC2 = '#313335'  # 输入框字体颜色
BGC3 = '#d9d9d9'  # 辅助底色

# 获取当前路径
Get_Xpath = inspect.getfile(inspect.currentframe())

# 使用os.path.dirname获取目录路径
Get_path = os.path.dirname(Get_Xpath)

# 如果不需要打包exe，直接获取  Get_path = os.path.dirname(os.path.abspath(__file__))

# print Get_path

# 生成readme txt
with open(Get_path + '\ReadMe.txt', mode='w') as T:
    T.write(ReadMe0 + ReadMe1)

# 遍历文件夹列表，检查每个文件夹是否存在，如果不存在则创建，并打印路径
for folder_name in folders:
    folder_path = os.path.join(Get_path, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print '创建了', folder_name, folder_path
    else:
        print '已存在', folder_name, folder_path

# 刷新文件目录
AllB = []  # 正式方块列表
AllF = []  # 文件列表


def GetAllJson(*args):
    # args 为要搜索的字符串

    blocks_list = []
    file_list = []

    # 遍历目录及其子目录
    for root, dirs, files in os.walk(Get_path + '\inp'):
        for file in files:
            if file.endswith('.json'):  # 检查文件扩展名是否为.json
                nfile = file.replace('.json', '')
                file_list.append(nfile)

                nfile = nfile.replace('.geo', '')

                if args and args[0]:
                    if args[0] in nfile:
                        blocks_list.append(nfile)


                else:
                    blocks_list.append(nfile)
    global AllB, AllF
    AllB = blocks_list
    AllF = file_list
    return blocks_list


RPath = Get_path + '\\xres\\'  # res 配置路径
BPath = Get_path + '\\xbeh\\'  # 方块基础行为路径


def MAKE(data):
    print '正式处理文件'
    # 开关状态
    Psx = data[0]  # 筛选
    Pmm = data[2]  # 命名
    Ptt = data[4]  # 贴图
    Pao = data[6]  # 遮罩

    # 内容提取
    Pdmm = data[3]  # 命名
    Pdtt = data[5]  # 贴图

    # print Psx,Pmm,Ptt,Pao,'|',Pdmm,Pdtt
    lang_blocklist = ''  # zh_CN文件

    B_json = {}  # 构建 blocks.json 文件
    T_json = {
        'resource_pack_name': 'vanilla',
        'texture_name': 'atlas.terrain',
        'texture_data': {}
    }  # 构建 terrain_texture 文件

    LogTxt = ToolName + 'LOG\n\n以下Json模型文件检查到错误！！\n请自行检查并修改，不排除是因为格式错误(不允许有注释)：'
    LogFile = []
    for k, block in enumerate(AllB):

        Path = Get_path + '\inp\\' + AllF[k] + '.json'  # 原方块路径
        NPath = Get_path + '\outp\\' + block + '.json'  # 新方块路径

        DP = {
            'textures': [''],
            'identifier': '',
            'use_ao': True
        }
        mmkj = 'jxl'

        if Pmm:
            mmkj = Pdmm

        bln = mmkj + ':' + block

        ttmc = bln
        if Ptt:
            ttmc = mmkj + ':' + Pdtt

        DP['identifier'] = bln
        DP['textures'] = [ttmc]
        DP['use_ao'] = Pao

        # 88
        lang_blocklist += 'tile.' + mmkj + ':' + block + '.name=方块' + '\n'

        # 构建网易模型
        NED = {
            'format_version': '1.13.0',
            'netease:block_geometry': {
                'description': {},
                'bones': []
            }
        }

        # 构建 方块基础行为文件
        MakeBlocks(bln, block)

        NED['netease:block_geometry']['description'] = DP

        # 构建 blocks.json 文件
        B_json[bln] = {
            'netease_model': '%s' % bln,
            'sound': 'stone'
        }
        # 构建 terrain_texture 文件
        T_json['texture_data'][bln] = {
            'textures': 'textures/blocks/' + bln
        }

        # -------检查Json格式是否合法
        # -------Json内请不要有注释
        res = None

        if os.path.exists(Path):
            try:
                with open(Path, 'r') as F:
                    res = json.load(F)
            except ValueError:
                print("由于解码错误，JSON 加载失败。")

        # -------------------

        if res != None:
            # 读取json内容
            with open(Path, mode='r') as F:
                res = json.load(F)
                Bones = res['minecraft:geometry'][0]['bones']

            # 方块连接
            for k, code in enumerate(Bones):
                cdn = code['name']

                connect_txt = '!query.is_connect'

                fw1 = ['d', 'u', 'n', 's', 'w', 'e', 'd2', 'u2', 'n2', 's2', 'w2', 'e2']
                fw2 = ['(0)', '(1)', '(2)', '(3)', '(4)', '(5)', '(0)', '(1)', '(2)', '(3)', '(4)', '(5)']

                if cdn in fw1:
                    if cdn[-1] == '2':
                        connect_txt = 'query.is_connect'
                    else:
                        connect_txt = '!query.is_connect'

                    cdp = fw1.index(cdn)
                    # print cdn,cdp
                    Bones[k]['enable'] = connect_txt + fw2[cdp]

                fw1 = ['x1', 'x2', 'x3', 'x4', 'y1', 'y2', 'y3', 'y4']
                fw2 = ['%s(2) && %s(4)', '%s(5) && %s(2)', '%s(3) && %s(5)', '%s(4) && %s(3)',
                       '%s(2) && %s(4)', '%s(5) && %s(2)', '%s(3) && %s(5)', '%s(4) && %s(3)']

                #ew-54  du-01  ns-23
                #ew2 du2

                if cdn in fw1:
                    if cdn[0] == 'y':
                        connect_txt = 'query.is_connect'
                    else:
                        connect_txt = '!query.is_connect'

                    cdp = fw1.index(cdn)
                    Bones[k]['enable'] = fw2[cdp] % (connect_txt, connect_txt)

                fw1 = ['du', 'ns', 'we', 'ud', 'sn', 'ew',   'du2', 'ns2', 'we2', 'ud2', 'sn2', 'ew2']
                fw2 = ['%s(0) && %s(1)', '%s(2) && %s(3)', '%s(4) && %s(5)',
                       '%s(0) && %s(1)', '%s(2) && %s(3)', '%s(4) && %s(5)',
                       '%s(0) && %s(1)', '%s(2) && %s(3)', '%s(4) && %s(5)',
                       '%s(0) && %s(1)', '%s(2) && %s(3)', '%s(4) && %s(5)'
                       ]

                if cdn in fw1:
                    if cdn[-1] == '2':
                        connect_txt = 'query.is_connect'
                    else:
                        connect_txt = '!query.is_connect'

                    cdp = fw1.index(cdn)
                    Bones[k]['enable'] = fw2[cdp] % (connect_txt, connect_txt)

                fw1 = ['dw', 'de', 'uw', 'ue',   'dw2', 'de2', 'uw2', 'ue2']
                fw2 = ['%s(0) && %s(4)', '%s(0) && %s(5)', '%s(1) && %s(4)', '%s(1) && %s(5)',
                       '%s(0) && %s(4)', '%s(0) && %s(5)', '%s(1) && %s(4)', '%s(1) && %s(5)',
                       ]

                if cdn in fw1:
                    if cdn[-1] == '2':
                        connect_txt = 'query.is_connect'
                    else:
                        connect_txt = '!query.is_connect'

                    cdp = fw1.index(cdn)
                    Bones[k]['enable'] = fw2[cdp] % (connect_txt, connect_txt)



            NED['netease:block_geometry']['bones'] = Bones

            #******字典排序******
            #=====排序模型内部=====
            # 获取所有键并进行倒序排序
            nedb = NED['netease:block_geometry']
            nedkk = sorted(nedb.keys(), reverse=True)
            nedb = OrderedDict((key, nedb[key]) for key in nedkk)

            NED['netease:block_geometry'] = nedb

            nedss = sorted(NED.keys(), reverse=False)
            NED = OrderedDict((key, NED[key]) for key in nedss)

            #-----排序B_json-----
            toboto = sorted(B_json.keys(), reverse=False)
            B_json = OrderedDict((key, B_json[key]) for key in toboto)
            #-----排序T_json-----
            toboto = sorted(T_json['texture_data'].keys(), reverse=False)
            T_json['texture_data'] = OrderedDict((key, T_json['texture_data'][key]) for key in toboto)
            #===================

            with open(NPath, mode='w') as F:
                json.dump(NED, F, ensure_ascii=False, indent=4)

            with open(RPath + '\\blocks.json', mode='w') as F:
                json.dump(B_json, F, ensure_ascii=False, indent=4)

            with open(RPath + '\\terrain_texture.json', mode='w') as F:
                json.dump(T_json, F, ensure_ascii=False, indent=4)


        else:
            LogFile += [block]

    else:
        # for循环结束
        if len(LogFile) >= 1:
            LogTxt += '\n\n' + str(LogFile) + Now.strftime("\n\n%Y-%m-%d %H:%M:%S")
            print LogTxt
            # 生成Log txt
            with open(Get_path + '\Error_Log.log', mode='w') as T:
                T.write(LogTxt)

            # 发送弹窗
            messagebox.showerror("错误", LogTxt)
        else:
            print '一切正常'

        # 生成res 其他配置文件

        with open(RPath + '\zh_CN.lang', mode='w') as T:
            T.write(lang_blocklist)


def MakeBlocks(bln, block):

    # 一个常用模板
    blockdict = {
        'format_version': '1.10.0',
        'minecraft:block': {
            'description': {
                'identifier': '%s' %bln,
                'register_to_creative_menu': True,
                'is_experimental': False,
                'category': 'tab_jxl'
            },
            'components': {
                'netease:render_layer': {
                    'value': 'alpha'
                },
                'netease:aabb': {
                    'collision': [{
                        'min': [0.0, 0.0, 0.0],
                        'max': [1.0, 1.0, 1.0]
                    }],
                    'clip': {
                        'min': [0.0, 0.0, 0.0],
                        'max': [1.0, 1.0, 1.0]
                    }
                },
                'minecraft:block_light_emission': {
                    'emission': 0.0
                },
                'minecraft:block_light_absorption': {
                    'value': 0
                },
                'minecraft:destroy_time': {
                    'value': 0.7
                },
                'netease:face_directional': {
                    'type': 'direction'
                },
                'minecraft:explosion_resistance': {
                    'value': 10
                },
                'netease:tier': {
                    'digger': 'pickaxe'
                },
                'netease:solid': {
                    'value': False
                },
                'netease:pathable': {
                    'value': True
                }
            }
        }
    }

    with open(BPath + '\\%s.json' %block, mode='w') as F:
        json.dump(blockdict, F, ensure_ascii=False, indent=4)
