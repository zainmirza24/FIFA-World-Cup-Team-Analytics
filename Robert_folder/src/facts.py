#!/usr/bin/env python3
## SFSU, 2022
## Robert Harakaly
## File description:
## GroupProject, Fifa WorldCup
##

import pandas as pd
import numpy as np
from math import *
from collections import Counter
import matplotlib.pyplot as plt

file = "../doc/sport/fifa_world_cup.csv"
data = pd.read_csv(file)


def max_goal(type):
    if type == "sum":
        most_goal = pd.DataFrame(data.groupby(['home_team']).sum())
        most_goal_a = pd.DataFrame(data.groupby(['away_team']).sum())
    if type == "mean":
        most_goal = pd.DataFrame(data.groupby(['home_team']).mean())
        most_goal_a = pd.DataFrame(data.groupby(['away_team']).mean())
    most_goal = pd.DataFrame(most_goal.iloc[0:, [4]]).to_numpy()
    most_goal_a = pd.DataFrame(most_goal_a.iloc[0:, [5]]).to_numpy()
    tot = []
    for idx, i in enumerate(most_goal_a):
        if type == "sum":
            tot.append(int(i+most_goal[idx]))
        if type == "mean":
            tot.append(float((i+most_goal[idx])/2))
    country = data.groupby('home_team')['home_team'].apply(list)
    c = []
    for idx, i in enumerate(country):
        c.append(i[0])
    m_h = max(most_goal)
    m_a = max(most_goal_a)
    m = max(tot)
    j = 0
    j_h = 0
    j_a = 0
    for idx, i in enumerate(c):
        if tot[idx] == m:
            j = idx
        if most_goal[idx] == m_h:
            j_h = idx
        if most_goal_a[idx] == m_a:
            j_a = idx
    if type == "sum":
        print("Team that scored the most goals at Home is:", c[j_h], "with", m_h[0], "goals")
        print("Team that scored the most goals Away is:", c[j_a], "with", m_a[0], "goals")
        print("Team that scored the most goals Overall is:", c[j], "with", m, "goals")
    if type == "mean":
        print("Team that have the highest goals per match at Home is:", c[j_h], "with", m_h[0], "goals")
        print("Team that have the highest goals per match Away is:", c[j_a], "with", m_a[0], "goals")
        print("Team that have the highest goals per match overall is:", c[j], "with", m, "goals")
    return c

def who_scored_the_most_goals():
    c = max_goal("sum")
    print()
    max_goal("mean")
    return c

def home_clean_sheet(home, team):
    clean_sheet = pd.DataFrame(data[data[home] == 0])
    clean_sheet = clean_sheet[team].to_numpy()
    cs = []
    for i in clean_sheet:
        cs.append(i)
    a = dict(Counter(cs))
    t = max(a, key=a.get)
    if team == 'home_team':
        tot_game = len(data[data['home_team'] == t])
        print("The team who have to most clean sheet at Home is:", t, "with", a[t], "clean sheets")
        print("This is", (a[t]/tot_game)*100, "% clean sheets")
    if team == 'away_team':
        tot_game = len(data[data['away_team'] == t])
        print("The team who have to most clean sheet Away is:", t, "with", a[t], "clean sheets")
        print("This is", (a[t]/tot_game)*100, "% clean sheets")
    return a, cs, tot_game

def clean_sheet(c):
    a_h, cs, tot_game_h = home_clean_sheet("away_team_score", "home_team")
    a_a, cs, tot_game_a = home_clean_sheet("home_team_score", "away_team")
    tot = []
#    tot_game = tot_game_h + tot_game_a
    for idx, i in enumerate(cs):
        try:
            tot.append(a_h[i]+a_a[i])
        except:
            continue
    m = max(tot)
    j = 0
    for idx, i in enumerate(cs):
        if m == tot[idx]:
            j = idx
            break
    tot_game = len(data[(data['home_team'] == cs[j]) | (data['away_team'] == cs[j])])
    print("The team who have to most clean sheet overall is:", cs[j], "with", m, "clean sheets")
    print("This is", (m/tot_game)*100, "% clean sheets")

def Home_or_Away():
    global data
    print()
    win = (len(data[data['home_team_result'] == 'Win'])/(len(data))*100)
    lose = (len(data[data['home_team_result'] == 'Lose'])/(len(data))*100)
    draw = (len(data[data['home_team_result'] == 'Draw'])/(len(data))*100)
    print("The team at home have:", win, "% chances to win")
    print("The away team have:", lose, "% chances to win")
    print("There is", draw, "% chances to have a draw")

def who_win_the_most(c, team, score, data):
#    global data
    win = []
    for i in c:
        win.append(len(data[(data[team] == i) & (data['home_team_result'] == score)]))
    m = max(win)
    j = 0
    for idx, i in enumerate(win):
        if m == i:
            j = idx
    tot_game = len(data[data[team] == c[j]])
    # if team == 'home_team':
    #     print("The team who won the most of match is:", c[j], "with", m, "victory at Home which is", m/tot_game*100, "% victory")
    # if team == 'away_team':
    #     print("The team who won the most of match is:", c[j], "with", m, "victory Away which is", m/tot_game*100, "% victory")
    return win


def best_country(c, data):
    win_h = who_win_the_most(c, 'home_team', "Win", data)
    win_a = who_win_the_most(c, 'away_team', "Lose", data)
    lose_h = who_win_the_most(c, 'home_team', "Lose", data)
    lose_a = who_win_the_most(c, 'away_team', "Win", data)
    draw_h = who_win_the_most(c, 'home_team', "Draw", data)
    draw_a = who_win_the_most(c, 'away_team', "Draw", data)
    win = []
    lose = []
    draw = []
    for idx, i in enumerate(win_h):
        win.append(i + win_a[idx])
        lose.append(lose_h[idx] + lose_a[idx])
        draw.append(draw_h[idx] + draw_a[idx])
    m = max(win)
    j = 0
    for idx, i in enumerate(win):
        if m == i:
            j = idx
    tot_game = len(data[(data['home_team'] == c[j]) | (data['away_team'] == c[j])])
#    print("The team who won the most of match is:", c[j], "with", m, "victory Overall which is", m/tot_game*100, "% victory")
    return win, lose, draw

def data_for_a_certain_y(y, data):
#    global data
    for idx, d in enumerate(data["date"]):
        if str(2022-y) == d[:4]:
            pastYearsData = data.iloc[1+idx:, 0:]
    print(pastYearsData)
    return pastYearsData

def new_df(c, w, l, d, df, bl, y):
    percent_w = []
    percent_l = []
    percent_d = []
    tot = []
    for idx, i in enumerate(c):
        tot.append(w[idx]+l[idx]+d[idx])
        try:
            percent_w.append(w[idx]/(tot[idx])*100)
            percent_l.append(l[idx]/(tot[idx])*100)
            percent_d.append(d[idx]/(tot[idx])*100)
        except:
            percent_w.append("NaN")
            percent_l.append("NaN")
            percent_d.append("NaN")
    if bl == False:
        data2 = {'TEAM': c,
        'WIN': w,
        'LOSE': l,
        'DRAW': d,
        'PLAY': tot
#            '% WIN': percent_w, '% LOSE': percent_l, '% DRAW': percent_d
        }
        df = pd.DataFrame(data2)
    else:
        df["last " + str(y) + "y WIN"] = w
        df["last " + str(y) + "y LOSE"] = l
        df["last " + str(y) + "y DRAW"] = d
        df["last " + str(y) + "y PLAY"] = tot
        # df["last " + str(y) + "y % WIN"] = percent_w
        # df["last " + str(y) + "y % LOSE"] = percent_l
        # df["last " + str(y) + "y % DRAW"] = percent_d
    return df

GroupA = {"Qatar":0, "Ecuador":0, "Senegal":0, "Netherlands":0}
GroupB = {"England":0, "IR Iran":0, "USA":0, "Wales":0}
GroupC = {"Argentina":0, "Saudi Arabia":0, "Mexico":0, "Poland":0}
GroupD = {"Australia":0, "France":0, "Denmark":0, "Tunisia":0}
GroupE = {"Spain":0, "Germany":0, "Japan":0, "Costa Rica":0}
GroupF = {"Belgium":0, "Canada":0, "Morocco":0, "Croatia":0}
GroupG = {"Brazil":0, "Serbia":0, "Switzerland":0, "Cameroon":0}
GroupH = {"Portugal":0, "Ghana":0, "Uruguay":0, "Korea Republic":0}

GROUP = [GroupA, GroupB, GroupC, GroupD, GroupE, GroupF, GroupG, GroupH]

def rank(df):
    r = data.loc[:len(data), ['home_team', 'away_team', 'home_team_fifa_rank', 'away_team_fifa_rank', 'home_team_result']]
    bins = [0, 10, 30, 40, 70, 100, 211]
    ranking = ["World class", "Really Good", "Average", "Bad", "Really Bad", "Worst"]
    r["home ranking"] = pd.cut(x=data['home_team_fifa_rank'], bins=bins, labels=ranking)
    r["away ranking"] = pd.cut(x=data['away_team_fifa_rank'], bins=bins, labels=ranking)
    rr = r.loc[:len(r), ['home ranking', 'away ranking', 'home_team_result']]
    for g1 in ranking:
        for g2 in ranking:
            game = rr[((rr["home ranking"] == g1) & (rr["away ranking"] == g2))]
            nb_games = len(rr[((rr["home ranking"] == g1) & (rr["away ranking"] == g2))])
            for g in ["Win", "Lose", "Draw"]:
                print(g, g1, "against", g2, "\t", (len(game[game["home_team_result"] == g]) / nb_games * 100))
            print()

def main():
    print()
    c = who_scored_the_most_goals()
    print()
    clean_sheet(c)
    Home_or_Away()
    print()
    # for t in GROUP:
    #     for tt in t:
    #         WorldCupData = data[(data['home_team'] == tt) | (data['away_team'] == tt)]
    # print("ONLY WORLD CUP TEAMS\n", WorldCupData)
    w, l, d = best_country(c, data)
    df = new_df(c, w, l, d, None, False, 0)
    pastYearsData = data_for_a_certain_y(5, data)
    p_w, p_l, p_d = best_country(c, pastYearsData)
    df = new_df(c, p_w, p_l, p_d, df, True, 5)
    pastYearsData = data_for_a_certain_y(2, data)
    p_w, p_l, p_d = best_country(c, pastYearsData)
    df = new_df(c, p_w, p_l, p_d, df, True, 2)
    lst = list(df.iloc[0])
    print(len(df))
    pts_A = []
    pts_N = []
    for idx in range(0, len(df)):
        lst = list(df.iloc[idx])
#        print(lst[0], "\tAVERAGE", lst[5]*3+lst[7], "\tNOW", lst[9]*3+lst[11])
        pts_A.append(((lst[5]*3+lst[7])/lst[8])*100)
        pts_N.append(((lst[9]*3+lst[11])/lst[12])*100)
#    df["Last pts"] = pts_A
#    df["Now pts"] = pts_N
    stats = []
    s = []
    for idx, i in enumerate(pts_A):
        stats.append(pts_N[idx] / i)
        s.append('Cold' if stats[idx] < 0.9 else 'Hot' if stats[idx] > 1.1 else 'Regular')
    df["strike"] = s
    print(df)
    worldCup = []
    for i in GROUP:
        worldCup.append(df.loc[df['TEAM'].isin(i)])
    worldCup = pd.concat(worldCup)
    print(worldCup)



    rank(df)


if __name__ == "__main__":
    main()