The Python script `facts.py` show us different facts about the dataset of Soccer.
To launch this code, use the command `python3 facts.py`.
This dataset show us all match between 1993 and 2022.
We can see the date, home team and the away team, where they are from, who win, the score and the score of players.

This is what we get when we launch the code:
`Team that scored the most goals at Home is: USA with 589 goals`
`Team that scored the most goals Away is: Brazil with 396 goals`
`Team that scored the most goals Overall is: Brazil with 954 goals`

`Team that have the highest goals per match at Home is: New Caledonia with 2.6785714285714284 goals`
`Team that have the highest goals per match Away is: Vanuatu with 2.314814814814815 goals`
`Team that have the highest goals per match overall is: New Caledonia with 2.2582046332046333 goals`

`The team who have to most clean sheet at Home is: USA with 152 clean sheets`
`This is 48.40764331210191 % clean sheets`
`The team who have to most clean sheet Away is: Zambia with 96 clean sheets`
`This is 39.50617283950617 % clean sheets`
`The team who have to most clean sheet overall is: Brazil with 229 clean sheets`
`This is 52.88683602771363 % clean sheets`

`The team at home have: 49.166004765687056 % chances to win`
`The away team have: 28.305672839764224 % chances to win`
`There is 22.528322394548724 % chances to have a draw`

`The team who won the most of match is: USA with 194 victory at Home which is 61.78343949044586 % victory`
`The team who won the most of match is: Brazil with 120 victory Away which is 60.0 % victory`
`The team who won the most of match is: Brazil with 301 victory Overall which is 69.5150115473441 % victory`

**1 Who scored the more goals ?**

In the first part, I wanted to know which team scored the more goals at Home, Away and Overall.
The USA scored 589 goals at Home, Away it’s Brazil with 396 goals and overall the team who score the more goals is Brazil with 954 goals.

To find this results, I used Pandas with `groupby` to group all home and away teams and then I use `.sum()` to take all goals. Then I used the function `max()` to know who scored the more goals.
