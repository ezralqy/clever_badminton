#!/usr/bin/env python
# -*- coding: utf-8 -*-


import shutil
import os
from datetime import date, datetime
from collections import defaultdict
from score import elo_score
import argparse


def run(current_date):
    # 创建以日期作为名字的文件夹
    folder_name = os.path.join(os.getcwd(), 'data', current_date)
    print(folder_name)
    if not os.path.exists(folder_name):
        print(folder_name + " not found, stop update")
        return

    # 读取当前日期的比赛记录
    matches = []
    matches_file = os.path.join(folder_name, "matches.txt")
    with open(matches_file, 'r') as file:
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
    print(matches)

    # 读取上次运行时存储的输出数据
    last_elo_scores_file = os.path.join(os.getcwd(), 'data', 'rank_score.txt')
    if not os.path.exists(last_elo_scores_file):
        print(last_elo_scores_file + " not found, stop update")
        return

    shutil.copy(last_elo_scores_file, os.path.join(folder_name, "before_rank_score.txt"))
    last_elo_scores = defaultdict(lambda: elo_score.INITIAL)
    with open(last_elo_scores_file, 'r') as file:
        for line in file:
            player_data = line.strip().split(' ')
            player = player_data[0]
            score = float(player_data[1])
            last_elo_scores[player] = score

    # 根据比赛结果更新rank_score并获取新的输出数据
    elo_scores = last_elo_scores.copy()
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
    new_elo_scores_file = os.path.join(folder_name, "after_rank_score.txt")
    with open(new_elo_scores_file, 'w') as f:
        for player, score in sorted(elo_scores.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{player} {score:.2f}\n")
            delta = score - last_elo_scores[player]
            if delta != 0:
                print(f"player: {player} score: {score:.2f} delta: {delta}")

    shutil.copy(new_elo_scores_file, last_elo_scores_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='parse date')
    parser.add_argument('--date', '-n', type=str, default=date.today().strftime("%Y-%m-%d"), required=True, help="update rank score based on $date match")

    args = parser.parse_args()
    print(args.date)

    run(args.date)
