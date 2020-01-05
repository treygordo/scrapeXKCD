#! python3
# downloadXkcd.py - Downloads all XKCD comics and saves to hard drive

import requests
import os
import bs4

url= 'https://xkcd.com'  #starting URL
os.makedirs('xkcd', exist_ok = True) # store comics in /.xkcd
iteration = 0
number = 'test'



#TODO: Download the page

while not url.endswith('#'):
    print('downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()
    if iteration > 0:
        number = url.split('/')[3:4]
        number = number[0] + '_'

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    comicElem = soup.select('#comic img')

    if comicElem == []:
        print('Could not find comic image.')
    else:
        try:
            comicUrl = 'https:' + comicElem[0].get('src')
              #Download the image
            print('Downloading image %s...' % (comicUrl))
            res = requests.get(comicUrl)
            res.raise_for_status()
        except requests.exceptions.InvalidURL:
            # skip this comic
            # prevLink = soup.select('a[rel^="prev"]')[0]
            prevLink = soup.select('a[rel="prev"]')[0]
            url = 'http://xkcd.com' + prevLink.get('href')
            iteration += 1
            continue


    #TODO: save the image to ./xkcd

    imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)),
    'wb')

    for chunk in res.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()

    #TODO: get the prev buttons url

    prevLink = soup.select('a[rel="prev"]')[0]
    url ='https://xkcd.com' + prevLink.get('href')
    iteration += 1

    print('done')
    #TODO: find the url of the comic image


