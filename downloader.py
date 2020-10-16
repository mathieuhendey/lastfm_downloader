import requests
import time
import pandas as pd
import json

lastfm_api_key = None  # Generate your own at https://www.last.fm/api/account/create
lastfm_user_name = None  # Provide your own or someone else's user name

if lastfm_user_name is None or lastfm_api_key is None:
    print(
        """
    You need to generate some creds, see the source code
    """
    )

time_between_requests = 0.1


def get_scrobbles(
    method="recenttracks",
    username=lastfm_user_name,
    key=lastfm_api_key,
    limit=200,
    extended=0,
    page=1,
    pages=0,
):
    """
    method: api method
    username/key: api credentials
    limit: api lets you retrieve up to 200 records per call
    extended: api lets you retrieve extended data for each track, 0=no, 1=yes
    page: page of results to start retrieving at
    pages: how many pages of results to retrieve. if 0, get as many as api can return.
    """
    # initialize url and lists to contain response fields
    url = (
        "https://ws.audioscrobbler.com/2.0/?method=user.get{}"
        "&user={}"
        "&api_key={}"
        "&limit={}"
        "&extended={}"
        "&page={}"
        "&format=json"
    )

    # make first request, just to get the total number of pages
    request_url = url.format(method, username, key, limit, extended, page)
    response = requests.get(request_url).json()
    total_pages = int(response[method]["@attr"]["totalPages"])
    if pages > 0:
        total_pages = min([total_pages, pages])

    print("Total pages to retrieve: {}".format(total_pages))

    # request each page of data one at a time
    for page in range(1, int(total_pages) + 1, 1):
        print(
            "\rPage: {}. Estimated time remaining: {} seconds.".format(
                page, 2.5 * int(total_pages - page)
            ), end=""
        )
        time.sleep(time_between_requests)
        request_url = url.format(method, username, key, limit, extended, page)
        response = requests.get(request_url)
        if method in response.json():
            response_json = response.json()[method]["track"]
            artist_names = []
            album_names = []
            track_names = []
            timestamps = []
            for track in response_json:
                if "@attr" not in track:
                    artist_names.append(track["artist"]["#text"])
                    album_names.append(track["album"]["#text"])
                    track_names.append(track["name"])
                    timestamps.append(track["date"]["uts"])

            del response

    # create and populate a dataframe to contain the data
    df = pd.DataFrame()
    df["artist"] = artist_names
    df["album"] = album_names
    df["track"] = track_names
    df["timestamp"] = timestamps
    # In UTC. Last.fm returns datetimes in the user's locale when they listened
    df["datetime"] = pd.to_datetime(df["timestamp"].astype(int), unit="s")

    return df


scrobbles = get_scrobbles(page=1, pages=0)  # Default to all Scrobbles
scrobbles.to_csv("./data/lastfm_scrobbles.csv", index=1, encoding="utf-8")
print("{:,} total rows".format(len(scrobbles)))
scrobbles.head()
