#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from score import elo_score


class Player:
    def __init__(self, name):
        self.name = name
        self.elo_rank = elo_score.INITIAL
        self.half = None

    def repr(self):
        return self.name


# 初始化player列表，按照随机顺序分为上下半区
players = [
    Player("player1"),
    Player("player2"),
    Player("player3"),
    Player("player4"),
    Player("player5"),
    Player("player6"),
    Player("player7"),
    Player("player8"),
    Player("player9"),
    Player("player10"),
    Player("player11"),
    Player("player12")
]
random.shuffle(players)

# 将player分为上半区和下半区
upper_half = players[:6]
lower_half = players[6:]
for player in upper_half:
    player.half = "top"
for player in lower_half:
    player.half = "bottom"


def arrange_match():
    # 在同一半区中随机选择4名player参加比赛
    team1 = random.sample(upper_half, 2) + random.sample(lower_half, 2)
    team2 = random.sample(upper_half, 2) + random.sample(lower_half, 2)
    print("比赛安排：")
    print("队伍1：", team1)
    print("队伍2：", team2)

    # 输入比赛结果
    result = input("请输入比赛结果（1表示队伍1胜利，2表示队伍2胜利）：")
    if result == "1":
        update_player_scores(team1, team2)
    elif result == "2":
        update_player_scores(team2, team1)
    else:
        print("输入无效，请重新运行脚本进行比赛安排。")


# 更新player分数和半区分组函数
def update_player_scores(winning_team, losing_team):
    for player in winning_team:
        player.skill_level += 1
    for player in losing_team:
        player.skill_level -= 1
    adjust_half_teams()


# 调整每名player所在半区函数
def adjust_half_teams():
    upper_half.sort(key=lambda x: x.skill_level, reverse=True)
    lower_half.sort(key=lambda x: x.skill_level, reverse=True)
    for i in range(6):
        upper_half[i].half = "top"
        lower_half[i].half = "bottom"


# 开始比赛安排
arrange_match()