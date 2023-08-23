#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

# 定义初始ELO分数
INITIAL = 1000

# 定义K值，它是用于调整ELO分数变化的常数
K_FACTOR = 32


def calculate_elo(player1_elo, player2_elo, actual_score):
    """
    计算两个玩家之间的Elo分数变化

    Args:
        player1_elo (float): 玩家1的Elo分数
        player2_elo (float): 玩家2的Elo分数
        actual_score (float): 比赛结果，取值为1(玩家1获胜)或者0(玩家2获胜)

    Returns:
        delta_elo: 表示玩家1增长的Elo分数和玩家2减少的Elo分数
    """
    # 计算期望胜率和Elo分数变化
    diff = player2_elo - player1_elo
    expected_score = 1 / (1 + math.pow(10, (diff / 400)))
    delta_elo = K_FACTOR * (actual_score - expected_score)

    return delta_elo
