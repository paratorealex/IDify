import pandas as pd
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


def getTracks (url):
    #url = 'https://www.1001tracklists.com/tracklist/1fv6ym9k/loods-rinse-fm-2020-02-05.html'
    # open client and parse website
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    # html parse
    page_soup = soup(page_html, "html.parser")

    # find all track artist and names
    track = page_soup.findAll("div", {"class": "tlToogleData"})

    # add to array
    songs = []
    for name in track:
        text = name.find(itemprop="name")
        if text is not None:
            songs.append(text["content"])

    # convert to dataframe and split

    df = pd.DataFrame(songs)
    df.columns = ['row']
    df = pd.DataFrame(df.row.str.split(' - ', 1).tolist(),
                      columns=['Artist', 'Song'])

    # get title
    title = page_soup.find(id="pageTitle").get_text().strip()

    return df, title

