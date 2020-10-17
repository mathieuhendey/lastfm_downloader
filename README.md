# A tool to create a CSV of all your last.fm scrobbles ever

https://mathieuhendey.com/2020/10/download-all-your-historical-last.fm-data/

The last.fm only lets you generate reports up to a year back, this tool will let
you download *all* your scrobbles in a CSV format with the artist, song, and the
timestamp.

From here you can do cool things like plot your top 20 artists on a graph:

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib


df = pd.read_csv("data/lastfm_scrobbles.csv")
df['scrobbles'] = df.groupby('artist')['artist'].transform('count')
df = df.drop_duplicates()
df = df.sort_values(by='scrobbles', ascending=False)

print(df.iloc[0:20])
df = df.iloc[0:20]
df.plot(x="artist", y="scrobbles", kind="bar")
x_axis=range(20)
t_axis=range(1700)
plt.tick_params(axis='x', pad=6) 
plt.margins(0.2)
plt.xticks(fontsize=8, horizontalalignment="left")
plt.tight_layout()
plt.xticks(rotation=-45)
plt.ylabel("Scrobbles")
plt.tick_params(axis='x', which='major', pad=10)
plt.subplots_adjust(right=0.9, bottom=0.3)
plt.tight_layout()

plt.savefig("chart.png", dpi=500)
```

Or see how many times you've listened to a specific song:

```bash
rg "Little Wing" data/lastfm_scrobbles.csv | wc -l
```

Read the source code for `downloader.py`, it has some information about setting
up your credentials.

N.B. this can take a **long** time. The script prints out an estimated time
remaining, but for a large last.fm history (e.g. 280,000 scrobbles) you're going
to be looking at about an hour.
