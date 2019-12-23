from bs4 import BeautifulSoup
import requests

class lenta_news(self, call, bot):

    def one(call):
        res = requests.get('https://m.lenta.ru')
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        url_m_news = 'https://m.lenta.ru' + soup.find('div', {"class": "main-header"}).find('a')['href']
        res = requests.get(url_m_news)
        html = res.text
        soup2 = BeautifulSoup(html, 'html.parser')
        text = soup2.find('div', {'class': 'content-body'}).text
        answer = ''
        answer += "Главная новость: "
        answer += soup.find('div', {"class": "main-header__top-topic-title"}).text
        answer += 'https://m.lenta.ru' + soup.find('div', {"class": "main-header"}).find('a')['href'] + '\n'
        i = 0
        for news in soup.find_all('a', {"class": "card-mini"}):
            if i != 4:
                newshtml = news.find('div', {"class": "card-mini__title"})
                newshtmltime = news.find('time', {"class": "card-mini__date"})
                answer += newshtml.text + ' (' + newshtmltime.text + ')'
                if 'http' not in news['href']:
                    g = 'https://m.lenta.ru' + news['href'] + '\n'
                else:
                    g = news['href'] + '\n'

                answer += g
                i += 1
                bot.send_message(call.message.chat.id, answer)

    def get_one_news(self):
        self.res = requests.get('https://m.lenta.ru/')
        self.html = res.text
        self.soup = BeautifulSoup(html, 'html.parser')
        self.url_m_news = 'https://m.lenta.ru' + soup.find('div', {"class": "main-header"}).find('a')['href']
        self.res = requests.get(url_m_news)
        self.html = res.text
        self.soup2 = BeautifulSoup(html, 'html.parser')
        self.text = soup2.find('div', {'class':'content-body'}).text
        answer = ''
        answer = print("Главная новость: ")
        print(soup.find('div', {"class": "main-header__top-topic-title"}).text)
        print(text)
        print('https://m.lenta.ru' + soup.find('div', {"class": "main-header"}).find('a')['href'] + '\n')
        i = 0
        for news in soup.find_all('a', {"class": "card-mini"}):
            if i != 4:
                newshtml = news.find('div', {"class": "card-mini__title"})
                newshtmltime = news.find('time', {"class": "card-mini__date"})
                print(newshtml.text + ' (' + newshtmltime.text + ')')
                if 'http' not in news['href']:
                    g = 'https://m.lenta.ru' + news['href'] + '\n'
                else:
                    g = news['href'] + '\n'

                print(g)
                i += 1


one('https://m.lenta.ru/')

