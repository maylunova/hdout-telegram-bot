from datetime import datetime, timedelta

import feedparser

from constants import BASE_URL


def parse_rss(hdout_id, delta=timedelta(days=1)):
    episodes = []
    rss = '{}{}/'.format(BASE_URL, hdout_id)
    favorite_series = feedparser.parse(rss)
    if len(favorite_series.entries) == 0:
        return None
    for series in favorite_series.entries:
        published_datetime = datetime.strptime(series.published, '%a, %d %b %Y %H:%M:%S %Z')
        if delta is not None:
            tdelta = datetime.now() - published_datetime
            if tdelta <= delta:
                episodes.append((series.title, series.published, series.link))
        else:
            episodes.append((series.title, series.published, series.link))
    return episodes


if __name__ == '__main__':
    res = parse_rss('4064')
    print(res)
