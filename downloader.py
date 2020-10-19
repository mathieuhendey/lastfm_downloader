import sys

import pandas as pd
import requests
import pprint
from requests_toolbelt.threaded import pool

# Generate your own at https://www.last.fm/api/account/create
LASTFM_API_KEY = None
LASTFM_USER_NAME = None
TEXT = "#text"
ESTIMATED_TIME_FOR_PROCESSING_PAGE = 352
ESTIMATED_TIME_FOR_PROCESSING_DATAFRAME_PER_PAGE_OF_RESULTS = 275

if LASTFM_USER_NAME is None or LASTFM_API_KEY is None:
    print(
        """
        You need to generate some credentials, see the source code
        """
    )
    sys.exit(1)


def get_scrobbles(
    endpoint="recenttracks",
    username=LASTFM_USER_NAME,
    key=LASTFM_API_KEY,
    limit=200,
    extended=0,
    page=1,
    pages=0,
):
    """
    endpoint: API endpoint.
    username: Last.fm username to fetch scrobbles for.
    key: API key.
    limit: The number of records per page. Maximum is 200.
    extended: Extended results from API, such as whether user has "liked" the track.
    page: First page to retrieve.
    pages: How many pages of results after "page" argument to retrieve. If 0, get all pages.
    """
    # initialize URL and lists to contain response fields
    url = (
        "https://ws.audioscrobbler.com/2.0/?method=user.get{}"
        "&user={}"
        "&api_key={}"
        "&limit={}"
        "&extended={}"
        "&page={}"
        "&format=json"
    )

    # get total number of pages
    request_url = url.format(endpoint, username, key, limit, extended, page)
    response = requests.get(request_url).json()
    total_pages = int(response[endpoint]["@attr"]["totalPages"])
    if pages > 0:
        total_pages = min([total_pages, pages])

    print(
        "Total pages to retrieve: {}. Estimated time: {}".format(
            total_pages, get_time_remaining(total_pages)
        )
    )

    artist_names = []
    album_names = []
    track_names = []
    timestamps = []
    urls = []
    # add formatted URLs to list to be requested in thread pool
    for page in range(0, int(total_pages) + 1, 1):
        urls.append(url.format(endpoint, username, key, limit, extended, page))
    p = pool.Pool.from_urls(urls)
    p.join_all()

    for response in p.responses():
        if endpoint in response.json():
            response_json = response.json()[endpoint]["track"]
            for track in response_json:
                if "@attr" not in track:
                    artist_names.append(track["artist"][TEXT])
                    album_names.append(track["album"][TEXT])
                    track_names.append(track["name"])
                    timestamps.append(track["date"]["uts"])

    # create and populate a dataframe to contain the data
    df = pd.DataFrame()
    df["artist"] = artist_names
    df["album"] = album_names
    df["track"] = track_names
    df["timestamps"] = timestamps
    # In UTC. Last.fm returns datetimes in the user's locale when they listened
    df["datetime"] = pd.to_datetime(timestamps, unit="s")
    df.sort_values("timestamps", ascending=False, inplace=True)
    return df


def get_time_remaining(pages_remaining):
    """Calculate the estimated time remaining."""
    millis_remaining = int(
        (pages_remaining * ESTIMATED_TIME_FOR_PROCESSING_PAGE)
        + (
            pages_remaining
            * ESTIMATED_TIME_FOR_PROCESSING_DATAFRAME_PER_PAGE_OF_RESULTS
        )
    )
    seconds_remaining = (millis_remaining / 1000) % 60
    seconds_remaining = int(seconds_remaining)
    minutes_remaining = (millis_remaining / (1000 * 60)) % 60
    minutes_remaining = int(minutes_remaining)
    return "{}m{:2}s".format(minutes_remaining, seconds_remaining)


scrobbles = get_scrobbles(page=1, pages=0)  # Default to all Scrobbles
scrobbles.to_csv("./data/lastfm_scrobbles.csv", index=False, encoding="utf-8")
print("{:,} total rows".format(len(scrobbles)))
scrobbles.head()
