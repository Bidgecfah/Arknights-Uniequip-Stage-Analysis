# -*- mode: python ; coding: utf-8 -*-
import csv
import json

关卡数据源 = 'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/stage_table.json'
干员数据源 = 'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json'
模组数据源 = 'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/uniequip_table.json'

干员数据 = json.load(open('character_table.json', encoding='utf-8'))
模组数据 = json.load(open('uniequip_table.json', encoding='utf-8'))
关卡数据 = json.load(open('stage_table.json', encoding='utf-8'))

模组任务信息 = {}
关卡模组任务信息 = {}

for 模组任务 in 模组数据["missionList"]:
    if 模组数据["missionList"][模组任务]["uniEquipMissionSort"] == 2:
        模组 = 模组数据['missionList'][模组任务]['uniEquipId']
        干员 = 模组数据['equipDict'][模组]["charId"]
        关卡 = 模组数据['missionList'][模组任务]['paramList'][1]
        模组任务信息[模组数据['equipDict'][模组]["uniEquipName"]] = {
            "干员名": 干员数据[干员]["name"],
            "干员星级": 干员数据[干员]["rarity"],
            "关卡": 关卡,
            "关卡名": 关卡数据["stages"][关卡]["code"],
            "关卡类型": 关卡数据["stages"][关卡]["stageType"],
            "任务描述": 模组数据['missionList'][模组任务]['desc']
        }

for 模组名, 模组信息 in 模组任务信息.items():
    干员名 = 模组信息["干员名"]
    干员星级 = 模组信息["干员星级"]
    关卡 = 模组信息["关卡"]
    关卡名 = 模组信息["关卡名"]
    关卡类型 = 模组信息["关卡类型"]
    任务描述 = 模组信息["任务描述"]
    if 关卡类型 not in 关卡模组任务信息: 关卡模组任务信息[关卡类型] = {}
    if 关卡 not in 关卡模组任务信息[关卡类型]: 关卡模组任务信息[关卡类型][关卡] = [(关卡名, 干员名, 模组名, 任务描述)]
    else: 关卡模组任务信息[关卡类型][关卡].append((关卡名, 干员名, 模组名, 任务描述))

with open('模组关卡分析.csv', 'w', newline="") as 模组关卡分析:
    模组关卡分析记录 = csv.writer(模组关卡分析)
    模组关卡分析记录.writerow(['关卡名', '干员名', '模组名', '任务描述'])
    for 关卡类型 in sorted(关卡模组任务信息):
        for 关卡, 关卡模组任务 in sorted(关卡模组任务信息[关卡类型].items()):
            print(关卡数据["stages"][关卡]["code"])
            for 关卡名, 干员名, 模组名, 任务描述 in 关卡模组任务:
                关卡模组信息 = '\n'.join([f"{干员名}「{模组名}」：{任务描述}"])
                模组关卡分析记录.writerow([f"关卡{关卡名}", 干员名, 模组名, 任务描述])
                print(关卡模组信息)
