import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import re

print("Scraping KenPom...")

# Create scraper
browser = cloudscraper.create_scraper()
response = browser.get("https://kenpom.com/index.php")

# Parse HTML
soup = BeautifulSoup(response.content, "html.parser")
tables = soup.find_all("table")

if not tables:
    raise Exception("No tables found — KenPom may have changed layout")

# Read first table into pandas
df = pd.read_html(StringIO(str(tables[0])))[0]

# Clean up columns
df.columns = [
    'Rk', 'Team', 'Conference','W-L','NetRtg','ORtg','ORtg_rk','DRtg','DRtg_rk',
    'AdjT','AdjT_rk','Luck','Luck_rk','OPP_NetRtg','OPP_NetRtg_rk','OPP_ORtg',
    'OPP_ORtg_rk','OPP_DRtg','OPP_DRtg_rk','NCSOS','NCSOS_rk'
]

# Clean and format
df = df[df['Team'] != 'Team'].dropna().reset_index(drop=True)
##df['Seed'] = df['Team'].apply(lambda x: re.search(r'\d+', x).group() if re.search(r'\d+', x) else None)
##df['Team'] = df['Team'].apply(lambda x: re.sub(r'\d+', '', x)).str.strip()

# Save locally
df.to_csv("kenpom.csv", index=False)
print(f"✅ Saved kenpom.csv with {len(df)} teams.")