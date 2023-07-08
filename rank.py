#!/usr/bin/env python
# -*- coding: utf-8 -*-

matches = []

with open('data/match_data.txt', 'r') as file:
    for line in file:
        match_data = line.strip().split(' ')
        player_a, player_b = match_data[0], match_data[1]
        score1, score2 = int(match_data[2]), int(match_data[3])
        player_c, player_d = match_data[4], match_data[5]
        matches.append({
            'player_a': player_a,
            'player_b': player_b,
            'score1': score1,
            'score2': score2,
            'player_c': player_c,
            'player_d': player_d
        })

#print(matches)

from collections import defaultdict
import math

# 定义初始ELO分数
INITIAL_ELO = 1000

# 定义K值，它是用于调整ELO分数变化的常数
K_FACTOR = 32

# 为每个球员分配初始ELO分数
elo_scores = defaultdict(lambda: INITIAL_ELO)

# 遍历每场比赛，更新每个球员的ELO分数
for match in matches:
    # 计算每个球员的胜率期望值
    player_a, player_b = match['player_a'], match['player_b']
    player_c, player_d = match['player_c'], match['player_d']
    rating_a, rating_b = elo_scores[player_a], elo_scores[player_b]
    rating_c, rating_d = elo_scores[player_c], elo_scores[player_d]
    expected_a = 1 / (1 + math.pow(10, (rating_c + rating_d - rating_b - rating_a) / 400))
    expected_b = 1 / (1 + math.pow(10, (rating_c + rating_d - rating_b - rating_a) / 400))
    expected_c = 1 / (1 + math.pow(10, (rating_a + rating_b - rating_c - rating_d) / 400))
    expected_d = 1 / (1 + math.pow(10, (rating_a + rating_b - rating_c - rating_d) / 400))

    # 根据比赛结果更新每个球员的ELO分数
    score1, score2 = match['score1'], match['score2']
    if score1 > score2:
        # Player A/B 赢了
        actual_ab, actual_cd = 1, 0
    elif score2 > score1:
        # Player C/D 赢了
        actual_ab, actual_cd = 0, 1
    else:
        # 平局
        actual_ab, actual_cd = 0.5, 0.5

    # 计算每个球员的新ELO分数
    new_rating_a = rating_a + K_FACTOR * (actual_ab - expected_a)
    new_rating_b = rating_b + K_FACTOR * (actual_ab - expected_b)
    new_rating_c = rating_c + K_FACTOR * (actual_cd - expected_c)
    new_rating_d = rating_d + K_FACTOR * (actual_cd - expected_d)

    # 将新的ELO分数保存到字典中
    elo_scores[player_a] = new_rating_a
    elo_scores[player_b] = new_rating_b
    elo_scores[player_c] = new_rating_c
    elo_scores[player_d] = new_rating_d

# 打印每个球员的最终ELO分数
with open('data/rank_score.txt', 'w') as f:
    for player, score in sorted(elo_scores.items(), key=lambda x: x[1], reverse=True):
        f.write(f"{player} {score:.2f}\n")
        print(f"{player} {score:.2f}")
