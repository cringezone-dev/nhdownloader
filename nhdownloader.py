import requests
import re
import wget
import os
import sys
from bs4 import BeautifulSoup

def main():

    if not sys.argv[1].isdigit():
        print 'usage: nhdownloader.py <Doujin code>'
        sys.exit(1)
    else:
        query = sys.argv[1]

    nhURL = requests.get('https://nhentai.net/g/'+str(query)).text
    soup = BeautifulSoup(nhURL,'lxml')
    #Extract Media ID via Meta Tag

    for meta in soup.findAll('meta'):
        if(meta.get('itemprop',None) == 'image'):
            meta_link = meta.get('content',None)

    #Extract Page Count

    djs_page = soup.findAll('span',{'class':'tags'})
    for x in djs_page:
        if(x.select_one('a[href*=search]') != None):
            pagecount = x.find('span').text.strip()

    djsTitle = soup.select('h1.title')[0].text.strip()
    media_ID = re.findall('[0-9]+',meta_link)[0]

    try:
        if not os.path.exists('Downloads'):
            os.mkdir('Downloads')
        os.mkdir('Downloads/'+djsTitle)
    except OSError:
        print('Error Creatng Directory')

    print('Doujin Title: '+djsTitle)
    print('Media ID: '+media_ID)
    print('Page Count: '+pagecount)

    for n in range(1, int(pagecount)+2):
        filename = 'https://i.nhentai.net/galleries/'+media_ID+'/'+str(n)+'.jpg'
        print("Downloading Page :"+str(n))
        r = requests.get(filename, stream=True)
        if(r.status_code == 200):
            with open('Downloads/'+djsTitle+'/'+str(n)+'.jpg','wb') as f:
                for chunk in r:
                    f.write(chunk)
if __name__ == '__main__':
    main()