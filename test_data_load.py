import requests
import re
import time
import pyshorteners
from bs4 import BeautifulSoup
# from telegram import Bot

# TELEGRAM_BOT_TOKEN = '6417926677:AAFpFVg4zGjjytISsI7h5qsg6QHIEophjqc'
# TELEGRAM_CHAT_ID = '7090041263'
headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
s = pyshorteners.Shortener()
source = 'https://www.fmkorea.com/'
url = f'{source}/index.php?mid=hotdeal&sort_index=pop&order_type=desc'
res = requests.get(url, headers=headers, timeout=5)
print(res)
res.raise_for_status()
soup = BeautifulSoup(res.text, 'lxml')
deal = soup.find_all('li', attrs={'class':re.compile('hotdeal0$')})[0]
deal_link = source + deal.find('a')['href']  # hotdeal별 링크 추출
deal_res = requests.get(deal_link, headers=headers, timeout=5)  # 해당 링크에 대한 요청
deal_res.raise_for_status()
deal_soup = BeautifulSoup(deal_res.text, 'lxml')  # 해당 링크의 HTML 파싱
# # time.sleep(5)
with open('deal_html.html', 'w', encoding='utf-8') as file:
    file.write(str(deal_soup))