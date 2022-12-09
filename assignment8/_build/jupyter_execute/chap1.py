#!/usr/bin/env python
# coding: utf-8

# # Chapter 1: Automating the betting system
# 
# In this chapter we will create a function that automatically calculates the team's odds of winning based on the American odds number introduced in the intro. 

# ```{figure} https://cdn.vox-cdn.com/thumbor/-8Qp7ERm0PsTttyQjAGRVmpsp-U=/1400x1400/filters:format(png)/cdn.vox-cdn.com/uploads/chorus_asset/file/23119960/1unnamed.png
# :name: gambling
# 
# A child playing poker.
# ```

# In[1]:


import pandas as pd
import altair as alt


# ## Calculate winnings
# We want to create a function that calculates how much you win based on the American odds and the amount wagered.
# 
# When the odds are negative:
# 
# ```{math}
# :label: win_eqn
# AmtWin = (\frac{AmtBet}{100})\lvert odds \rvert
# ```
# 
# You need to define an if function for this that reflects the following where a is the odds and b is the amount wagered as per {eq}`win_eqn`.
# 
# ```
# def win_calc(odds,bet):
#     if odds > 0:
#         win = (bet/(abs(odds)))*100
#     else:
#         win = (bet/100)* (abs(odds))
#     return win
# ```
# 

# In[2]:


def win_calc(odds,bet):
    if odds > 0:
        win = (bet/(abs(odds)))*100
    else:
        win = (bet/100)* (abs(odds))
    return win


# In[3]:


#Test function using an odd of -100 and a bet of $20
win_calc(-200,20)


# Next we want to create a graph that shows you what happens to the amount you win when the odds are increasing from -100 to 100. First we want to create a python dictionary that contains a series of odds and their respective wins using the `win_calc` function as follows:
# 
# ```
# for num in list_of_odds:
#     win_dict['odds'] += [num]
#     win_dict['wins'] += [win_calc(num,100)]
# ```

# In[4]:


chg_odds = [-75, -50, -25, -10, 10, 25, 50, 75]

win_dict = {'odds':[],'wins':[]}

for num in chg_odds:
    win_dict['odds'] += [num]
    win_dict['wins'] += [win_calc(num,100)]

odds_win_table = pd.DataFrame.from_dict(win_dict)
odds_win_table


# In[5]:


#graph the above data
chart1 = alt.Chart(odds_win_table, width=500, height=300).mark_bar().encode(
                   x=alt.X('odds', bin=alt.Bin(maxbins=10), title='American odds'), 
                   y=alt.Y('wins', title='Amount of money won in $ per $100 bet')
         ).properties(title="Relationship between odds and amount of winnings based $100 bet")
chart1


# ## Calculate odds
# Now we create a function that calcuates your team's chance of winning based on the odds and amount you can win based on the following equation:
# 
# If the amount you win is greater than what you bet:
# ```{math}
# :label: odds_great
# PercentOdds = (\frac{AmtWin-AmtBet}{AmtWin})100
# ```
# 
# If the amount you win is less than what you bet:
# ```{math}
# :label: odds_less
# PercentOdds = 100+(\frac{AmtWin-AmtBet}{AmtWin})
# ```
# 
# To the following function:
# 
# ```
# def odds_calc(win,bet):
#     if win <= bet:
#         odds = 100 + ((win-bet)/win)
#     else:
#         odds = ((win-bet)/win)*100
#     return odds
# ```
# 
# The wins can be calculated using the `win_calc` function.

# In[6]:


def odds_calc(win,bet):
    if win <= bet:
        odds = 100 + ((win-bet)/win)
    else:
        odds = ((win-bet)/win)*100
    return odds


# In[7]:


#Test function
odds_calc(5,10)


# We can graph the American odds against the % chance of winning using the `odds_calc` and the `wins_calc` function in the following code:
# 
# 1. Create a list of winnings based on the odds chances using the `win_calc` function and looping it through a list of odds:
# 
# ```
# for num in list_of_odds:
#     win_list.append(win_calc(num,100))
# ```
# 
# 2. Looping through the list of winnings which correspond to the winnings per odds per $100 bet and calculating the percent chance of winning using the `odds_calc` function:
# 
# ```
# for nums in list_of_odds:
#     win_dict2['odds'] += [nums]
# 
# for wins in win_list:
#     win_dict2['percent_chance'] += [odds_calc(wins,100)] 
# ```

# In[8]:


chg_odds2 = [-75, -50, -25, -10, 10, 25, 50, 75]

win_list = []

for num in chg_odds2:
    win_list.append(win_calc(num,100))

win_list


# In[9]:


win_dict2 = {'odds':[],'percent_chance':[]}

for nums in chg_odds2:
    win_dict2['odds'] += [nums]

for wins in win_list:
    win_dict2['percent_chance'] += [odds_calc(wins,100)] 

odds_chance_table = pd.DataFrame.from_dict(win_dict2)
odds_chance_table


# In[10]:


#graph the above data
chart2 = alt.Chart(odds_chance_table, width=500, height=300).mark_bar().encode(
                   x=alt.X('odds', bin=alt.Bin(maxbins=10), title='American odds'), 
                   y=alt.Y('percent_chance', title='Corresponding Percent Chance of Winning')
         ).properties(title="Relationship between odds and % chance of your betting team winning based $100 bet")
chart2


# ```{figure} https://scx2.b-cdn.net/gfx/news/hires/2013/studyshowsmo.jpg
# :name: money
# 
# Loads of money.
# ```
# 
# Bottom line is if you bet on a team with lower odds and they win, you would triple or quadruple your money ({numref}`money`).
