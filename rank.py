#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from score import elo_score

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

# print(matches)

# 为每个球员分配初始ELO分数
elo_scores = defaultdict(lambda: elo_score.INITIAL)

# 遍历每场比赛，更新每个球员的ELO分数
for match in matches:
    # 计算每个球员的胜率期望值
    player_a, player_b = match['player_a'], match['player_b']
    player_c, player_d = match['player_c'], match['player_d']
    team1_elo = elo_scores[player_a] + elo_scores[player_b]
    team2_elo = elo_scores[player_c] + elo_scores[player_d]

    # 根据比赛结果更新每个球员的ELO分数
    elo_delta = elo_score.calculate_elo(team1_elo, team2_elo, match['score1'] > match['score2'])
    # 计算每个球员的新ELO分数
    # 将新的ELO分数保存到字典中
    elo_scores[player_a] += elo_delta
    elo_scores[player_b] += elo_delta
    elo_scores[player_c] -= elo_delta
    elo_scores[player_d] -= elo_delta

# 打印每个球员的最终ELO分数
with open('data/rank_score.txt', 'w') as f:
    for player, score in sorted(elo_scores.items(), key=lambda x: x[1], reverse=True):
        f.write(f"{player} {score:.2f}\n")
        print(f"{player} {score:.2f}")
