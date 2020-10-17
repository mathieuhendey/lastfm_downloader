# A tool to create a CSV of all your last.fm scrobbles ever

https://mathieuhendey.com/2020/10/download-all-your-historical-last.fm-data/

The last.fm only lets you generate reports up to a year back, this tool will let
you download *all* your scrobbles in a CSV format with the artist, song, and the
timestamp.

From here you can do cool things like plot your top 20 artists on a graph using `plot.py`.
**Make sure you've run `downloader.py` first, or you won't have any data to plot!**


![scrobbles plot](https://mathieuhendey.com/img/top_scrobbles.png)

Or see how many times you've listened to a specific song:

```bash
rg "little wing" data/lastfm_scrobbles.csv| wc -l
      33
```

Read the source code for `downloader.py`, it has some information about setting
up your credentials.

N.B. this can take a **long** time. The script prints out an estimated time
remaining, but for a large last.fm history (e.g. 280,000 scrobbles) you're going
to be looking at about an hour.
