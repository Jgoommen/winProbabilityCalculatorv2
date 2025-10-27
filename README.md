# winProbabilityCalculator
## Matchup calculator using cloudscraped KenPom data



## 🏀 Overview
The goal of this project is to predict the outcomes of an NCAA college basketball game using reliable and continuously updated data.

Since the official KenPom website is subscription-blocked, I had to use a cloudscraper instead of a normal webpage parser to read in the data. Most websites that are subscription blocked will block requests, and the cloudscraper bypasses such blocks. KenPom in particular uses a software called Cloudflare which monitors internet traffic, web requests, and bots among other things. 

I used adjusted offensive/defensive efficiency, adjusted tempo alongside league averages of tempo and efficiency to calculate scores. I used offensive/defensive efficiency to approximate the scoring capability of both teams, and then calculated the approximate tempo to find the possessions in a game. Combining the two is how I was able to estimate the final score.

I calculated the win probability by finding the difference in scores and using a normal CDF function from scipy

---

## 📊 Data Source 
I used data scraped directly from the KenPom website. I collected everything on the main page, but only used offensive/defensive rating, adjusted tempo, and team names for my calculations

---

## 🛠️ Tools and Technologies Used
- **Languages:** *Python*
- **Libraries:** *streamlit, cloudscraper, pandas, bs4 (BeautifulSoup), io (StringIO), SciPy, re*
- **IDE:** *VS Code*

---

## 🚀 How to Run the Project
1. Clone the repository or copy the code into a Jupyter Notebook or Python file
2. Install the required libraries;
   ```bash
   pip install streamlit, cloudscraper, pandas, bs4, io, scipy.stats, re
3. Run the streamlit app
   ```bash
   streamlit run winProbability.py

---

## ⛹🏽‍♂️ Bracket Performance
I used this program to fill out an entire 2024-2025 March Madness bracket
- Bracket finished rank 4.5M
- 82.2%
- 1250 Pts
- The national champion calculated was Duke
<img width="347" height="409" alt="Screenshot 2025-09-21 at 11 55 51 AM" src="https://github.com/user-attachments/assets/148fedb9-47a4-48b7-aa31-bdd222ddfeeb" />

  
