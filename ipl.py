import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide',page_title='IPL analysis')
st.title("IPL Analysis between (2008 - 2024)")
ipl = pd.read_csv("matches.csv",parse_dates=['date'])
ball_df = pd.read_csv("ball_by_ball.csv")
six_df = pd.read_csv("six_data.csv")
four_df = pd.read_csv("four.csv")
merge_df = pd.read_csv("merge_data.csv",low_memory=False)

#replace in ball_df data
ball_df.replace('RG Sharma','R Sharma',inplace=True)
#replace in ipl data
ipl.replace('Royal Challengers Bangalore','Royal Challengers Bengaluru',inplace=True)
ipl.replace('Delhi Daredevils','Delhi Capitals',inplace=True)
ipl.replace('Kings XI Punjab','Punjab Kings',inplace=True)
ipl.replace('Deccan Chargers','Sunrisers Hyderabad',inplace=True)
ipl.replace('RG Sharma','R Sharma',inplace=True)

# final matches data set hai temp_df
temp_df = ipl[ipl['match_type'] == 'Final']
temp_df = temp_df.drop(columns=['id','city','date','match_type','venue','toss_decision','result','result_margin','target_runs','target_overs','super_over','umpire1','umpire2'])

def final_overall_winner(ipl):
    final_winner = ipl[ipl['match_type'] == 'Final']
    final_winner = final_winner.drop(columns=['id','city','date','match_type','venue','toss_decision','result','result_margin','target_runs','target_overs','super_over','umpire1','umpire2'])
    final_winner.set_index('season',inplace=True)
    st.subheader("All Season Winner")
    st.dataframe(final_winner)
    
def season_winner(temp_df,final_option):
    st.subheader(f"Season {final_option} Winner ")
    st.dataframe(temp_df[temp_df['season']==final_option],hide_index=True)

def total_number_matches(ipl,ball_df):
    a = ipl.shape[0]
    st.subheader(f"Total number of matches = {ipl.shape[0]}")
    st.subheader(f"Total number of six = {(ball_df['total_runs'] == 6).sum()}")
    st.subheader(f"Total number of four = {(ball_df['total_runs'] == 4).sum()}")
    st.subheader(f"Total number of wicket = {(ball_df['is_wicket']==1).sum()}")

def no_of_six_of_batter(ball_df,batter,six_df):
    temp_df = ball_df[ball_df['total_runs'] == 6]
    six = temp_df.groupby('batter')['total_runs'].count()
    st.subheader(f"Total six {six[six.index == batter].values}")
    #graph
    st.text(f"Graph of six {batter}")
    temp = six_df[six_df['batter'] == batter]
    year = ['2007/08','2009','2009/10','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020/21','2021','2022','2023','2024']
    list = []
    for i in year:
        sixcount = temp[temp['season'] == i]['batter'].count()
        list.append(sixcount)
    
    data = {
        'season':year,
        'Total Six':list
    }
    data = pd.DataFrame(data)
    graph = px.bar(data,x='season',y='Total Six')
    st.plotly_chart(graph)
    st.dataframe(data,hide_index=True)

def no_of_four_of_batter(batter,four_df):
    four = four_df[four_df['batter'] == batter]['batter'].count()
    st.subheader(f"Total no. of four {four}")
    #graph
    st.text(f"Graph of Four {batter}")
    year = ['2007/08','2009','2009/10','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020/21','2021','2022','2023','2024']
    temp = four_df[four_df['batter'] == batter]
    list = []
    for i in year:
        fourcount = temp[temp['season'] == i]['batter'].count()
        list.append(fourcount)
    data = {
        'season':year,
        'Total Four':list
    }
    data = pd.DataFrame(data)
    graph = px.bar(data,x='season',y='Total Four')
    st.plotly_chart(graph)
    st.dataframe(data,hide_index=True)
    
def avg(ball_df,batter,merge_df):
    total_run = ball_df[ball_df['batter'] == batter]['batsman_runs'].sum()
    total_out = ball_df[ball_df['batter'] == batter]['is_wicket'].sum()
    strick_rate = np.round(total_run/total_out,decimals=3)
    st.subheader(f"Total run by {batter} is : {total_run}")
    st.subheader(f"Total dismissal : {total_out}")
    st.subheader(f"Batter Avg : {strick_rate}")
    #graph
    st.text(f"Graph of SR vs Season {batter}")
    year = ['2007/08','2009','2009/10','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020/21','2021','2022','2023','2024']
    l = []
    temp_df = merge_df[merge_df['batter'] == batter]
    for i in year:
        run = temp_df[temp_df['season'] == i]['batsman_runs'].sum()
        out = temp_df[temp_df['season'] == i]['is_wicket'].sum()
        if out == 0 :
            avgerage = None
        else:
            avgerage = np.round(run/out,decimals=3)
        l.append(avgerage)
    data = {
        'season':year,
        'avg':l
    }
    data = pd.DataFrame(data)
    graph = px.line(data,x='season',y='avg')
    st.plotly_chart(graph)
    st.dataframe(data,hide_index=True)

def Strike_rate(ball_df,batter,merge_df):
    total_run = ball_df[ball_df['batter'] == batter]['batsman_runs'].sum()
    ball = ball_df[ball_df['batter'] == batter]['batter'].count()
    sr = np.round(total_run/ball,decimals=3)*100
    st.subheader(f"Strike rate of {batter} is : {sr}")
    #graph
    year = ['2007/08','2009','2009/10','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020/21','2021','2022','2023','2024']
    l = []
    temp_df = merge_df[merge_df['batter'] == 'BB McCullum']
    for i in year:
        run = temp_df[temp_df['season'] == i]['batsman_runs'].sum()
        ball = temp_df[temp_df['season'] == i]['batter'].count()
        if ball == 0:
            sr = None
        else:
            sr = np.round(run/ball,decimals=3)*100
        l.append(sr)
    data = {
        'season':year,
        'SR':l
    }
    data = pd.DataFrame(data)
    graph = px.line(data,x='season',y='SR')
    st.plotly_chart(graph)
    st.dataframe(data,hide_index=True)

def win_ratio(ipl,team):
    team_a = ipl['team1'].value_counts()
    team_b = ipl['team2'].value_counts()
    total_match = team_a + team_b
    t_match = total_match[team]
    total_win = ipl['winner'].value_counts()
    loss = total_match[team] - total_win[team]
    win = total_win[team]
    win_ratio = np.round(win/loss,decimals=3)
    st.subheader(f"Win ratio of {team} is {win_ratio}")
    data = {
        'Team':[team],
        'Total match':t_match,
        'Win':win,
        'Loss':loss,
        'Win Ratio':win_ratio
    }
    data = pd.DataFrame(data)
    st.dataframe(data,hide_index=True)

def overall_win_loss(ipl,team):
    team_list = ipl['team1'].unique().tolist()
    team_a = ipl['team1'].value_counts()
    team_b = ipl['team2'].value_counts()
    total_win = ipl['winner'].value_counts()
    total_match = team_a + team_b
    match_list = []
    loss_list = []
    win_list = []
    ratio_list = []
    for i in team_list:
        t_match = total_match[i]
        match_list.append(t_match)
        loss = total_match[i] - total_win[i]
        loss_list.append(loss)
        win = total_win[i]
        win_list.append(win)
        win_ratio = np.round(win/loss,decimals=3)
        ratio_list.append(win_ratio)
    data = {
        'Name of Team':team_list,
        'Match':match_list,
        'Win':win_list,
        'Loss':loss_list,
        'Win Ratio':ratio_list
    }
    data = pd.DataFrame(data)
    st.dataframe(data,hide_index=True)
    #graph
    graph = px.bar(data,x ='Name of Team',y='Win Ratio')
    st.text("Win ratio bar graph")
    st.plotly_chart(graph)

def super_over_matches(ipl):
    st.subheader("Super Over Match")
    super_over = ipl[ipl['super_over'] == 'Y']
    sp = super_over.drop(columns=['id','city','date','match_type','player_of_match','venue','toss_decision','result','result_margin','target_overs','super_over','umpire1','umpire2'])
    st.dataframe(sp,hide_index=True)

def toss_analysis(ipl):
    toss_data = ipl['toss_winner'].value_counts().reset_index()
    st.dataframe(toss_data,hide_index=True)
    #graph
    st.text("Percantage of teams winning toss")
    graph = px.pie(toss_data,names='toss_winner',values='count')
    st.plotly_chart(graph)
    st.text("Decision of Toss Winning team to bat or field")
    decision = ipl['toss_decision'].value_counts().reset_index()
    graph2 = px.pie(decision,names='toss_decision',values='count')
    st.plotly_chart(graph2)

def player_of_matches(ipl):
    player_of_match = ipl['player_of_match'].value_counts().reset_index().head(10)
    st.dataframe(player_of_match,hide_index=True)
    #graph
    st.text("Top ten most player of match")
    graph = px.pie(player_of_match,names='player_of_match',values='count')
    st.plotly_chart(graph)

def top_20_bowler(ball_df):
    top_20 = ball_df[ball_df['is_wicket'] == 1]['bowler'].value_counts().reset_index().head(20)
    st.dataframe(top_20,hide_index=True)
    #graph
    graph = px.bar(top_20,x='bowler',y='count')
    st.plotly_chart(graph)

def each_bowler_wicket(ball_df,bowler):
    each_bowler = ball_df[ball_df['is_wicket'] == 1]['bowler'].value_counts()[bowler]

option = st.sidebar.selectbox('select One',['Final winner','Total matches','No. of six','No. of Four',
                    'Batter Avg','Strike Rate','Win and Loss','Super Over Match','Toss analysis',
                    'Most Player of match','Wicket'])

if option == 'Final winner':
    final_option = st.sidebar.selectbox('select one',['OverAll','2007/08','2009','2009/10','2011','2012','2013','2014','2015','2016',
                    '2017','2018','2019','2020/21','2021','2022','2023','2024'])
    analysis = st.sidebar.button("analysis")
    if analysis:
        
        if final_option == 'OverAll':
            final_overall_winner(ipl)
        
        else:
            season_winner(temp_df,final_option)

elif option == 'Total matches':
    find = st.sidebar.button("Find")
    if find:
        total_number_matches(ipl,ball_df)

elif option == 'No. of six':
    batter = st.sidebar.selectbox('select batter',ball_df['batter'].unique().tolist())
    show = st.sidebar.button("Show")
    if show:
        no_of_six_of_batter(ball_df,batter,six_df)

elif option == 'No. of Four':
    batter = st.sidebar.selectbox('select batter',ball_df['batter'].unique().tolist())
    show = st.sidebar.button("Show")
    if show:
        no_of_four_of_batter(batter,four_df)

elif option == 'Batter Avg':
    batter = st.sidebar.selectbox('select batter',ball_df['batter'].unique().tolist())
    show = st.sidebar.button("Show")
    if show:
        avg(ball_df,batter,merge_df)

elif option == 'Strike Rate':
    batter = st.sidebar.selectbox('select batter',ball_df['batter'].unique().tolist())
    show = st.sidebar.button("Show")
    if show:
        Strike_rate(ball_df,batter,merge_df)

elif option == 'Win and Loss':
    temp = ipl['team1'].unique().tolist()
    temp.append('Overall')
    team = st.sidebar.selectbox('Select Team',temp)
    show = st.sidebar.button("Show")
    if show:
        if team == 'Overall':
            overall_win_loss(ipl,team)
        else:
            win_ratio(ipl,team)

elif option == 'Super Over Match':
    show = st.sidebar.button("Show")
    if show:
        super_over_matches(ipl)

elif option == 'Toss analysis':
    show = st.sidebar.button("Show")
    if show:
        toss_analysis(ipl)
elif option == 'Most Player of match':
    show = st.sidebar.button("Show")
    if show:
        player_of_matches(ipl)

elif option == 'Wicket':
    bowler_list = ball_df['bowler'].unique().tolist()
    bowler_list.insert(0,'Top 20 Bowler')
    bowler = st.sidebar.selectbox('Select Bowler',bowler_list)
    show = st.sidebar.button("Show")
    if show:
        if bowler == 'Top 20 Bowler':
            top_20_bowler(ball_df)
        else:
            pass