import urllib.request
import csv
from bs4 import BeautifulSoup

def getUrl (url):
    opener = urllib.request.build_opener()

    urllib.request.install_opener(opener)
    html = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')

    bs = BeautifulSoup(html,'html.parser')

    links = bs.select('.title-article-author > a')
    return links

def getContext (link, title):
    opener = urllib.request.build_opener()

    urllib.request.install_opener(opener)
    html = urllib.request.urlopen(link).read().decode('utf-8', 'ignore')

    bs = BeautifulSoup(html,'html.parser')

    date = bs.select(".published")[0].text
    data = []

    for target in bs.find_all('div', attrs={'class':'col-md-12'})[2:4]:
        for p in target.find_all('p'):
            t = p.text.strip()
            t = t.replace(u'\xa0', u' ')
            t = t.replace(u'\xa2', u'¢')
            t = t.replace(u'“', u'\"')
            t = t.replace(u'”', u'\"')
            t = t.replace(u'‘', u'\'')
            t = t.replace(u'’', u'\'')
            data.append([title, date, t])
    return data


def saveTextLink (url, titles, links):
    linklist = getUrl(url)
    for link in linklist:
        titles.append(link.text.strip())
        links.append(link.get('href'))
    return titles, links

def main():
    titles = []
    links = []
    for i in range(1000):
        url = 'https://www.investmentexecutive.com/page/' + str(i) + '/?s&post_type=post'
        titles, links = saveTextLink(url, titles, links)

    data = []
    for title, link in zip(titles, links):
        if title != 'When a client names you executor of their estate':
            data = data + getContext(link, title)

    with open("out.csv", "w", newline="", encoding='gb18030') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    for d in data:
        print(d)

main()