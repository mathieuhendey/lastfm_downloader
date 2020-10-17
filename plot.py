import matplotlib.pyplot as plt
import pandas as pd


def arrange_data_frame(dataframe=pd.read_csv("data/lastfm_scrobbles.csv")):
    """Get the the artist out of the dataframe and drop other columns.

    Relies on you having run downloader.py first to populate the CSV.
    """
    dataframe = dataframe.drop(['album', 'track', 'timestamp', 'datetime'], axis=1)
    dataframe['scrobbles'] = dataframe.groupby('artist')['artist'].transform('count')
    dataframe = dataframe.drop_duplicates()
    return dataframe.sort_values(by='scrobbles', ascending=False)


def get_plot(dataframe):
    """Arrange the plot.

    Creates a bar chart with Artist on the x axis and number of scrobbles of
    that artist on the y axis.

    Rotates the artist names on the x axis so they fit on the chart.
    """
    plt.xkcd()
    dataframe = dataframe.iloc[0:20]
    dataframe.plot(x="artist", y="scrobbles", kind="bar")
    plt.tick_params(axis='x', pad=6)
    plt.margins(0.2)
    plt.xticks(fontsize=8, horizontalalignment="left")
    plt.tight_layout()
    plt.xticks(rotation=-45)
    plt.ylabel("Scrobbles")
    plt.tick_params(axis='x', which='major', pad=10)
    plt.subplots_adjust(right=0.9, bottom=0.3)
    plt.tight_layout()
    return plt


arranged_dataframe = arrange_data_frame()
plot = get_plot(arranged_dataframe)

# Save plot to ./chart.png
plt.savefig("chart.png", dpi=500)
