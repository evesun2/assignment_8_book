#!/usr/bin/env python
# coding: utf-8

# # Chapter 3: Road to the Finals!
# 
# The finals for the World Cup this year is on Dec 18. With the finals quickly approaching, people are placing their bets on who might take home the trophy. But you don't want to bet blindly so here we're going to develop a method to calculate the odds of a country winning dependent on which round of the tournament they are in and their historical record.

# ## Data used for calculations
# 
# We are going to use data provided here: https://github.com/jfjelstul/worldcup
# 
# The data that we are going to use specifically is the matches.csv dataset which contains information about all the World Cup matches played since 1930 including information on which stage of the tournament and who won {cite}`fjelstul_fjelstul_2022`. 

# In[1]:


#Import pandas and altair
import pandas as pd
import altair as alt


# In[2]:


#Import matches.csv data from worldcup database on github
matches = pd.read_csv('https://raw.githubusercontent.com/jfjelstul/worldcup/master/data-csv/matches.csv')
matches = matches.drop(columns = ['key_id', 'tournament_id', 'match_id', 'match_name', 'group_name','group_stage', 'knockout_stage', 'replayed','replay', 'match_date', 'match_time', 'stadium_id', 'stadium_name', 'city_name', 'country_name', 'home_team_id', 'home_team_code', 'away_team_id','away_team_code', 'score', 'home_team_score_margin', 'away_team_score_margin', 'extra_time', 'penalty_shootout', 'score_penalties', 'home_team_score_penalties','away_team_score_penalties', 'draw'])
matches.head(10)


# ## Calculating historical success rate
# We want to use the historical record available in the matches dataset to calculate the likelihood of winning depending on which stage of the tournament the country is playing in.

# Let's try to figure how what the chances are that Argentina ({numref}`argentina`) wins one of their group stage matches based on their historical record. 
# 
# ```{figure} https://upload.wikimedia.org/wikipedia/commons/1/1a/Flag_of_Argentina.svg
# :height: 150px
# :name: argentina
# 
# The flag of Argentina.
# ```
# 
# To calculate this we will need to using the following formula:
# 
# ```{math}
# :name: hist_win
# WinOdds = \frac {AwayWins + HomeWins}{TotalGames}
# ```

# In[3]:


#Divide the data into only group stage matches based on Argentina as the home or away team
group_only = matches[matches['stage_name'] == 'group stage']
arg_home = group_only[group_only['home_team_name'] == 'Argentina']
arg_away = group_only[group_only['away_team_name'] == 'Argentina']


# After subdividing the dataset, we can use {eq}`hist_win` using the following codes:
# 
# ```
# total_home = arg_home['home_team_win'].sum()
# total_away = arg_away['away_team_win'].sum()
# total_arg_win = total_home + total_away
# arg_win_rate = (total_arg_win/(arg_home.shape[0] + arg_away.shape[0]))*100
# arg_win_rate
# ```

# In[4]:


total_home = arg_home['home_team_win'].sum()
total_away = arg_away['away_team_win'].sum()
total_arg_win = total_home + total_away
arg_win_rate = (total_arg_win/(arg_home.shape[0] + arg_away.shape[0]))*100
arg_win_rate


# Let's create a function that automates the process by taking in a which stage of the tournament we are betting on and which country. The code for the function should:
# 
# 1. parse the dataset down to only the stage of interest and only the country of interest
# 2. calculate the total wins from the country in that stage
# 3. based on the total games played, determine the chances of winning
# 
# ```
# def chance_win(country,stage):
#     stage_only = matches[matches['stage_name'] == stage]
#     home = group_only[group_only['home_team_name'] == country]
#     away = group_only[group_only['away_team_name'] == country]
#     win_rate = ((home['home_team_win'].sum() + away['away_team_win'].sum())/(arg_home.shape[0] + arg_away.shape[0]))*100
#     return win_rate
# ```

# In[5]:


def chance_win(country,stage):
    stage_only = matches[matches['stage_name'] == stage]
    home = group_only[group_only['home_team_name'] == country]
    away = group_only[group_only['away_team_name'] == country]
    win_rate = ((home['home_team_win'].sum() + away['away_team_win'].sum())/(arg_home.shape[0] + arg_away.shape[0]))*100
    return win_rate


# In[6]:


#Test above function
chance_win('Argentina','group stage')


# ## 2022 Predictions for Quarter Finals
# 
# Using the `chance_win` formula, we can determine the chances that the remaining teams currently have in the quarter finals.
# 
# Currently, we have the following teams left:
# 
# ```{figure} https://pbs.twimg.com/media/FjUrHd-WYAA5_8k?format=jpg&name=900x900
# :height: 400px
# :name: quarters
# 
# Teams remaining the quarter finals of the 2022 World Cup.
# ```
# 
# Let's create a table that includes the remaining 8 countries as shown in {numref}`quarters` and their chances of winning their quarter finals match. 

# In[7]:


remaining_teams = ['Netherlands', 'Argentina', 'Croatia', 'Brazil', 
                   'England', 'France', 'Morocco', 'Portugal']

win_dict = {'country':[],'odds_of_winning':[]}

for teams in remaining_teams:
    win_dict['country'] += [teams]
    win_dict['odds_of_winning'] += [chance_win(teams,'quarter-finals')]

quar_win_table = pd.DataFrame.from_dict(win_dict)
quar_win_table


# In[8]:


#graph the above data
chart3 = alt.Chart(quar_win_table, width=500, height=300).mark_bar().encode(
                   x=alt.X('country', title='Country'), 
                   y=alt.Y('odds_of_winning', title='Percent chance of winning their quarter finals match')
         ).properties(title="Odds of remaining countries passing the quarter finals")
chart3


# ### Apperance rate to determine a winner
# 
# We can also determine how often these teams have history been in the semi-finals (ie. passed the quarter finals) by parsing the data based on the semi-finals and which countries have appeared regardless of win or loss at that stage. But this time let's try to predict who can win it all using the appearance rate method. 

# Let's use Argentina as an example again:
# 
# 1. We need to subset the data by finals
# 2. Count the number of appearances Argentina has made
# 3. Count the total number of tournaments represented in the dataset
# 4. Determine the rate of appearance in the semi-finals using the formula:
# 
# ```{math}}
# :name: appear_rate
# %AppearanceRate = /frac{Apperances}{Tournaments_Total}100
# ```

# In[9]:


finals = matches[matches['stage_name'] == 'final']
arg_appearance = finals['home_team_name'].str.count('Argentina').sum() + finals['away_team_name'].str.count('Argentina').sum()
arg_appearance


# In[10]:


total_fifas = matches['tournament_name'].nunique()


# Rate of appearances in the semi-finals for Argentina as per the above formula {eq}`appear_rate`.

# In[11]:


arg_final_appearance = (arg_appearance/total_fifas)*100
arg_final_appearance


# As per above, we can create a function to automate this and graph the rate of finals appearances by the remaining 8 countries in the 2022 World Cup. 

# In[12]:


def rate_appear(country,stage):
    stage_div = matches[matches['stage_name'] == stage]
    appears = stage_div['home_team_name'].str.count(country).sum() + stage_div['away_team_name'].str.count(country).sum()
    total = matches['tournament_name'].nunique()
    appearance_rate = (appears/total)*100
    return appearance_rate


# In[13]:


#Test the function using Argentina
rate_appear('Argentina','final')


# In[14]:


remaining_teams = ['Netherlands', 'Argentina', 'Croatia', 'Brazil', 
                   'England', 'France', 'Morocco', 'Portugal']

appear_dict = {'country':[],'appearance_rate':[]}

for teams in remaining_teams:
    appear_dict['country'] += [teams]
    appear_dict['appearance_rate'] += [rate_appear(teams,'final')]

appear_rate_table = pd.DataFrame.from_dict(appear_dict)
appear_rate_table


# In[15]:


#graph the above data
chart4 = alt.Chart(appear_rate_table, width=500, height=300).mark_bar().encode(
                   x=alt.X('country', title='Country'), 
                   y=alt.Y('appearance_rate', title='Rate of appearance in the semi-finals')
         ).properties(title="Historical rate of appearance in the semi-finals since 1930")
chart4


# According to the data, Brazil appears to have the highest chance of passing the quarter finals and making it to the finals!

# ```{bibliography}
# :filter: docname in docnames
# ```
