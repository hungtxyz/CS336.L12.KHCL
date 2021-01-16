import requests
from bs4 import BeautifulSoup
import pandas as pd

allLinks = []
allTitle = []
allSinger = []
allImg = []
allMp3 = []
allLyrics = []


OriginUrl = "https://chiasenhac.vn/mp3/vietnam.html?tab=album-2020&page="
file = 0

for i in range(100):
    url = OriginUrl + str(i+1)
    response = requests.get(url)
    post = BeautifulSoup(response.content, 'html.parser')

    pageTitle = post.findAll('h3', class_ = 'card-title')

    # titles = [title.find('a').text.replace('\n','').replace('(Single)','') for title in pageTitle]
    links = [link.find('a').attrs["href"] for link in pageTitle]

    for link in links:
        try:
            url_link = "https://vi.chiasenhac.vn" + link
            subResponse = requests.get(url_link)
            subPost = BeautifulSoup(subResponse.content,'html.parser')

            down_list = subPost.findAll('a', class_ ='download_item')

            mp3_link = down_list[1].attrs["href"]

            title = subPost.find('h2', class_ = 'card-title').text

            singer = subPost.find('h1', class_ = "title").text.replace(title + ' - ','').replace(';',' and')

            # Get Source Image
            img = subPost.find('img', class_ = "card-img-top")['src']

            lyric_div = subPost.select('#fulllyric')

            lyrics = [lyric.text.replace('\r','') for lyric in lyric_div][0]

            if (lyrics == '\n'):
                continue

            # dir_path = "./data/" + title + ".txt"
            #
            # f = open(dir_path,'w',encoding='utf-8')
            # f.write(lyrics)
            # f.close()
            file += 1

            allTitle.append(title)
            allSinger.append(singer)
            allImg.append(img)
            allMp3.append(mp3_link)
            allLinks.append(url_link)

        except Exception:
            pass

        if file % 20 == 0:
            print(file)

df = pd.DataFrame({'Title':allTitle,'Singer':allSinger,'Img':allImg,'Mp3':allMp3,'Link':allLinks})
df.to_csv('lyrics_data.csv')
