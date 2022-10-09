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

def who_win_the_most(c, team, score):
    global data
    win = []
    for i in c:
        win.append(len(data[(data[team] == i) & (data['home_team_result'] == score)]))
    m = max(win)
    j = 0
    for idx, i in enumerate(win):
        if m == i:
            j = idx
    tot_game = len(data[data[team] == c[j]])
    if team == 'home_team':
        print("The team who won the most of match is:", c[j], "with", m, "victory at Home which is", m/tot_game*100, "% victory")
    if team == 'away_team':
        print("The team who won the most of match is:", c[j], "with", m, "victory Away which is", m/tot_game*100, "% victory")
    return win


def best_country(c):
    win_h = who_win_the_most(c, 'home_team', "Win")
    win_a = who_win_the_most(c, 'away_team', "Lose")
    win = []
    for idx, i in enumerate(win_h):
        win.append(i + win_a[idx])
    m = max(win)
    j = 0
    for idx, i in enumerate(win):
        if m == i:
            j = idx
    tot_game = len(data[(data['home_team'] == c[j]) | (data['away_team'] == c[j])])
    print("The team who won the most of match is:", c[j], "with", m, "victory Overall which is", m/tot_game*100, "% victory")

def main():
    print()
    c = who_scored_the_most_goals()
    print()
    clean_sheet(c)
    Home_or_Away()
    print()
    best_country(c)
    

if __name__ == "__main__":
    main()