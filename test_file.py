import os
from bs4 import BeautifulSoup
import datetime
import pprint

import data_collector

day_name = datetime.datetime.now() - datetime.timedelta(days=2)
day_name = day_name.strftime("%A")

file_path = "youtube_history_professional.html"
file_path2 = "youtube_history_personal.html"

data_collector.save_youtube_data("auth.json", file_path)
# data_collector.save_youtube_data("auth2.json", file_path2)

class video:
    def __init__(self, title, link,type, length, length_watched, time_watched, category):
        self.title = title
        self.link = link
        self.type = type # short or video
        self.length = length
        self.length_watched = length_watched
        self.time_watched = time_watched
        self.category = category


data = []
with open(file_path, "r") as f:
    data.append(f.read())
# with open(file_path2, "r") as f:
    # data.append(f.read())

shorts_watched = []
vidoes_watched = []
# Gathering data from the professional account
for val in data:
    soup = BeautifulSoup(val, "html.parser")
    # daily_elements = soup.find_all("ytd-item-section-renderer", class_="style-scope ytd-section-list-renderer")
    daily_elements = soup.find_all("ytd-item-section-renderer")
    print(len(soup))
    print(len(daily_elements))

    elements_to_search = []
    to_search = ["Today", "Yesterday", day_name]
    for day in to_search:
        for elem in daily_elements:
            header_selector = "ytd-item-section-header-renderer"
            section_header = elem.find(header_selector)
            section_header_text = section_header.find(id="title").text

            if section_header_text == day:
                elements_to_search.append(elem)
                break
    print(len(elements_to_search))

    for elem in elements_to_search:
        shorts_reels = []
        # short_elements = elem.find_all("ytd-reel-shelf-renderer", class_="scope ytd-item-section-renderer")
        short_elements = elem.find_all("ytd-reel-shelf-renderer")
        for short_element in short_elements:
            vids = short_element.find_all("a")
            for vid in vids:
                shorts_reels.append(vid['href'])
        shorts_watched.append(shorts_reels)

        vidoes = []
        video_elements = elem.find_all("ytd-video-renderer")
        for video_element in video_elements:
            video = video_element.find("a")
            vidoes.append(video['href'])
        vidoes_watched.append(vidoes)

# Make a new json file called youtube_history.json, this file has for
pprint.pprint(shorts_watched)
pprint.pprint(vidoes_watched)
