#!/usr/bin/env python3
## SFSU, 2022
## Robert Harakaly
## File description:
## GroupProject, Fifa WorldCup
##

import pandas as pd
import numpy as np
from math import *

file = "../doc/sport/fifa_world_cup.csv"
data = pd.read_csv(file)

GroupA = {"Qatar":0, "Ecuador":0, "Senegal":0, "Netherlands":0}
GroupB = {"England":0, "IR Iran":0, "USA":0, "Wales":0}
GroupC = {"Argentina":0, "Saudi Arabia":0, "Mexico":0, "Poland":0}
GroupD = {"Australia":0, "France":0, "Denmark":0, "Tunisia":0}
GroupE = {"Spain":0, "Germany":0, "Japan":0, "Costa Rica":0}
GroupF = {"Belgium":0, "Canada":0, "Morocco":0, "Croatia":0}
GroupG = {"Brazil":0, "Serbia":0, "Switzerland":0, "Cameroon":0}
GroupH = {"Portugal":0, "Ghana":0, "Uruguay":0, "Korea Republic":0}

GROUP = [GroupA, GroupB, GroupC, GroupD, GroupE, GroupF, GroupG, GroupH]

def getPoint(w1, w2, d, team1, team2, G):
    if w1 > w2 and w1 > d:
        G[team1] += 3
    elif w2 > w1 and w2 > d:
        G[team2] += 3
    else:
        G[team1] += 1
        G[team2] += 1


def whoWin(oneVStwo, home, away, nb_game_played, G):
    team1_win = oneVStwo[((oneVStwo['home_team'] == home) & (oneVStwo['home_team_result'] == "Win")) | (oneVStwo['home_team'] == away) & (oneVStwo['home_team_result'] == "Lose")]
    team2_win = oneVStwo[((oneVStwo['home_team'] == away) & (oneVStwo['home_team_result'] == "Win")) | (oneVStwo['home_team'] == home) & (oneVStwo['home_team_result'] == "Lose")]
    draw = nb_game_played - (len(team1_win) + len(team2_win))
    nb_team1_win = len(team1_win)
    nb_team2_win = len(team2_win)
    try:
        team1_percent_win = (nb_team1_win/nb_game_played) * 100
        team2_percent_win = (nb_team2_win/nb_game_played) * 100
        draw_percent = (draw/nb_game_played) * 100
    # print("WIN for", home, "\t\t\t\t", nb_team1_win, "\t", team1_percent_win)
    # print("WIN for", away, "\t\t\t", nb_team2_win, "\t", team2_percent_win)
    # print("DRAW between", home, "and", away, "\t", draw, "\t", draw_percent)
        getPoint(team1_percent_win, team2_percent_win, draw_percent, home, away, G)
    except:
        G[home] = G[home]
        G[away] = G[away]

def how_many_times_one_team_played_another(home, away, G):
    oneVStwo = data[((data['home_team'] == home) & (data['away_team'] == away)) | ((data['home_team'] == away) & (data['away_team'] == home))].iloc[0:, :19]
#    print(oneVStwo)
    nb_game_played = len(oneVStwo)
#    print(nb_game_played)
    whoWin(oneVStwo, home, away, nb_game_played, G)
    return nb_game_played

def getGroupPoints(GroupName):
    already_played = []
    for H in list(GroupName.keys()):
        for A in list(GroupName.keys()):
            if H == A:
                continue
            already_played.append([H, A])
            if [A, H] in already_played:
                continue
            how_many_times_one_team_played_another(H, A, GroupName)
    return GroupName

def main():
    global GROUP
    for G in GROUP:
        G = getGroupPoints(G)
        print(G)
    


if __name__ == "__main__":
    main()