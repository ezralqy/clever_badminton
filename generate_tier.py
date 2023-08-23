#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os
from collections import defaultdict


def run():
    players_elo_file = os.path.join(os.getcwd(), 'data', 'rank_score.txt')
    if not os.path.exists(players_elo_file):
        print(players_elo_file + " not found, stop generate")
        return

    players_elo = dict()
    with open(players_elo_file, 'r') as file:
        for line in file:
            player_data = line.strip().split(' ')
            player = player_data[0]
            score = float(player_data[1])
            players_elo[player] = score

    # 正态分布拟合
    elo_scores = list(players_elo.values())
    mu, sigma = norm.fit(elo_scores)
    print(f"mean={mu}, sigma={sigma}")

    # 绘制拟合前后数据
    plt.hist(elo_scores, bins=6, density=True, alpha=0.6, color='g', label='Data')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, sigma)
    plt.plot(x, p, 'k', linewidth=2, label='Fit')
    plt.legend()
    plt.xlabel('Elo Score')
    plt.ylabel('Frequency')
    plt.title('Elo Score Distribution')
    plt.show()

    for player, score in sorted(players_elo.items(), key=lambda x: x[1], reverse=True):
        print(f"{player} score={score:.2f} level={(score - mu)/sigma:.2f}")


if __name__ == "__main__":
    run()
