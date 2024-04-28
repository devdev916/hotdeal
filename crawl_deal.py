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
# print(soup)
deal = soup.find_all('li', attrs={'class':re.compile('hotdeal0$')})[0]
# 우선 링크만 가져와도되는게 아닐지?
# print(deals[0])
# for deal in deals[0]:
# print(deal)
deal_link = source + deal.find('a')['href']  # hotdeal별 링크 추출
deal_res = requests.get(deal_link, headers=headers, timeout=5)  # 해당 링크에 대한 요청
deal_res.raise_for_status()
deal_soup = BeautifulSoup(deal_res.text, 'lxml')  # 해당 링크의 HTML 파싱
# # time.sleep(5)
with open('deal_html.html', 'w', encoding='utf-8') as file:
    file.write(str(deal_soup))
# print(deal_soup)
# deal_title_name = deal_soup.find_all('span', attrs={'class':'np_18px_span'}).text.strip()
# print(deal_title_name)
# deal_url_name = deal_soup.find('a', attrs={'class':'hotdeal_url'}).get_text()

# print(f'''{deal_title_name}, {deal_url_name}''')
    # deal_product_name = deal_soup.find('h3', attrs={'class':'title'}).get_text()
    # print(product_name)
#     # 이후 원하는 정보를 추출하여 사용할 수 있습니다.




# for deal in deals:
#     title = re.sub(r'\[[0-9]{1,4}\]','',deal.find('h3', attrs={'class':'title'}).get_text())
#     # if '포텐' in title:
#     #     title = title.replace('포텐','')
#     # else:
#     #     continue
#     deal_info = deal.find_all('a', attrs={'class':'strong'})
#     link = deal.find_all('a', attrs={'class':'strong'})[0]['href']
#     price = deal.find_all('a', attrs={'class':'strong'})[1].get_text()
#     delivery = deal.find_all('a', attrs={'class':'strong'})[2].get_text()
#     deal_data = {
#         'title': title.strip(),
#         'price': deal_info[1].get_text(),
#         'delivery': deal_info[2].get_text(),
#         'link': s.tinyurl.short(source + deal_info[0]['href'])
#     }    
#     print(f'''{title.strip()}, 가격 : {deal_info[1].get_text()}, 배송 : {deal_info[2].get_text()}, 링크 : {s.tinyurl.short(source + deal_info[0]['href'])}''')
#     time.sleep(3)


# def get_page_html_from_url(url):
#     user_agent = {
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
#     }
#     chrome_option = webdriver.ChromeOptions()
#     chrome_option.add_argument("--headless")
#     chrome_option.add_argument("--no-sandbox")
#     chrome_option.add_argument("--disable-dev-shm-usage")
#     chrome_option.add_argument(f'--user-agent={user_agent["User-Agent"]}')
#     chrome_option.add_argument("--disable-gpu")

#     browser = webdriver.Chrome(options=chrome_option)
#     browser.get(url)
#     WebDriverWait(browser, 20).until(
#         EC.presence_of_element_located((By.ID, "reviewListFragment"))
#     )

#     html = browser.page_source
#     browser.quit()

#     return print(html)

# def get_soup_object_from_html(html):
#     soup = BeautifulSoup(html, "lxml")

#     return soup