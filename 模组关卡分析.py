# -*- mode: python ; coding: utf-8 -*-
import csv
import json

# 关卡数据源 = 'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/stage_table.json'
# 干员数据源 = 'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json'
# 模组数据源 = 'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/uniequip_table.json'

干员数据 = json.load(open('character_table.json', encoding='utf-8'))
模组数据 = json.load(open('uniequip_table.json', encoding='utf-8'))
关卡数据 = json.load(open('stage_table.json', encoding='utf-8'))

模组任务集合 = {}
关卡集合 = {}

for 模组任务 in 模组数据["missionList"]:
    if 模组数据["missionList"][模组任务]["uniEquipMissionSort"] == 2:
        模组 = 模组数据['missionList'][模组任务]['uniEquipId']
        模组名 = 模组数据['equipDict'][模组]["uniEquipName"]
        干员 = 模组数据['equipDict'][模组]["charId"]
        干员名 = 干员数据[干员]["name"]
        关卡 = 模组数据['missionList'][模组任务]['paramList'][1]
        关卡名 = 关卡数据["stages"][关卡]["code"]
        描述 = 模组数据['missionList'][模组任务]['desc']
        模组任务集合[模组名] = {
            "干员名": 干员名,
            "关卡名": 关卡名,
            "描述": 描述
        }
for 模组名, 模组信息 in 模组任务集合.items():
    干员名 = 模组信息["干员名"]
    关卡名 = 模组信息["关卡名"]
    描述 = 模组信息["描述"]
    if 关卡名 not in 关卡集合: 关卡集合[关卡名] = [(干员名, 模组名, 描述)]
    else: 关卡集合[关卡名].append((干员名, 模组名, 描述))

with open('模组任务关卡分析.csv', 'w', newline="") as 模组关卡分析:
    模组关卡分析记录 = csv.writer(模组关卡分析)
    模组关卡分析记录.writerow(['关卡名', '干员名', '模组名', '任务描述'])
    for 关卡名, 关卡模组 in sorted(关卡集合.items()):
        for 干员名, 模组名, 描述 in 关卡模组:
            关卡模组信息 = '\n'.join([f"{干员名}「{模组名}」：{描述}"])
            模组关卡分析记录.writerow([f"关卡{关卡名}", 干员名, 模组名, 描述])
            print(f"{关卡名}\n{关卡模组信息}")
