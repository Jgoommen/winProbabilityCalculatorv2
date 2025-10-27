import streamlit as st
import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import re


df = pd.read_csv("kenpom.csv")

df.columns = ['Rk', 'Team', 'Conference','W-L','NetRtg','ORtg','ORtg_rk','DRtg','DRtg_rk','AdjT', 'AdjT_rk','Luck','Luck_rk','OPP_NetRtg','OPP_NetRtg_rk','OPP_ORtg','OPP_ORtg_rk','OPP_DRtg','OPP_DRtg_rk','NCSOS', 'NCSOS_rk']
df = df[df['Team'] != 'Team'].dropna().reset_index(drop=True)
df['Seed'] = df['Team'].apply(lambda x: re.search(r'\d+', x).group() if re.search(r'\d+', x) else None)
df['Team'] = df['Team'].apply(lambda x: re.sub(r'\d+', '', x)).str.strip()
for col in ['NetRtg', 'OPP_NetRtg']:
    df[col] = df[col].astype(str).apply(lambda x: re.sub(r'[^-\d.]+', '', x) if isinstance(x, str) else x)
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Convert numeric columns safely
for col in ['AdjT', 'ORtg', 'DRtg']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
##df['NetRtg'] = df['NetRtg'].apply(lambda x: re.sub(r'[^-\d.]+', '', x)).astype(float)
##df['OPP_NetRtg'] = df['OPP_NetRtg'].apply(lambda x: re.sub(r'[^-\d.]+', '', x)).astype(float)
##df['AdjT'] = df['AdjT'].astype(float)
##df[['ORtg', 'DRtg']] = df[['ORtg', 'DRtg']].astype(float)

import scipy.stats as stats

def compute_score(team1, team2, df):
    team1 = df[df['Team'] == team1]
    team2 = df[df['Team'] == team2]
    # Average Efficiency is 106.7 and tempo is 67.2
    approx_tempo = int((team1['AdjT'].iloc[0] / 67.2) * (team2['AdjT'].iloc[0] / 67.2) * 67.2)
    team1_adj_off = (team1['ORtg'].iloc[0] * team2['DRtg'].iloc[0]) / 106.7
    team2_adj_off = (team2['ORtg'].iloc[0] * team1['DRtg'].iloc[0]) / 106.7
    
    team1_score = team1_adj_off / 100 * approx_tempo
    team2_score = team2_adj_off / 100 * approx_tempo
    
    margin = team1_score - team2_score
    wp = stats.norm.cdf(x=0, loc=margin, scale = 11)
    prob = 1-round(wp, 3)
    

    print(f"""    Here is the Predicted Score Between these teams on a neutral court according to KenPom:\n 
    {team1['Team'].iloc[0]}: {round(team1_score, 0)} | {team2['Team'].iloc[0]}: {round(team2_score, 0)} | Probability {team1['Team'].iloc[0]} Wins: {1-round(wp, 3)}""")

    team1_score = round(team1_score)
    team2_score = round(team2_score)
    return team1_score, team2_score, prob

#compute_score('Duke', 'Purdue', df) # > 75% should be gurantee in theory

teams = df['Team'].tolist()
st.title(" 🏀 NCAA Men's Basketball Predicted Score Calculator 🏀 ")
st.write("Select two teams to predict the score and win probability on a neutral court:")

team1_name = st.selectbox("Team 1", teams)
team2_name = st.selectbox("Team 2", teams)

# --- Display results ---
if st.button("Predict Score"):
    t1_score, t2_score, t1_prob = compute_score(team1_name, team2_name, df)
    st.write(f"### Predicted Score:")
    st.write(f"{team1_name}: {t1_score} | {team2_name}: {t2_score}")
    st.write(f"**Probability {team1_name} Wins:** {t1_prob:.3f}")




