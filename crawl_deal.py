import requests
import re
import time
from bs4 import BeautifulSoup
import mysql.connector

# from telegram import Bot

# TELEGRAM_BOT_TOKEN = '6417926677:AAFpFVg4zGjjytISsI7h5qsg6QHIEophjqc'
# TELEGRAM_CHAT_ID = '7090041263'
headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }

source = 'https://www.fmkorea.com/'
url = f'{source}/index.php?mid=hotdeal&sort_index=pop&order_type=desc' # 핫딜 게시판 인기탭
res = requests.get(url, headers=headers, timeout=5)
res.raise_for_status()
soup = BeautifulSoup(res.text, 'lxml')
deals = soup.find_all('li', attrs={'class':re.compile('hotdeal0$')})
for deal in deals:
    try:
        link = source + deal.find('a')['href']  # hotdeal별 링크 추출
        res = requests.get(link, headers=headers, timeout=5)  # 해당 링크에 대한 요청
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')  # 해당 링크의 HTML 파싱
        title = soup.find_all('span', attrs={'class':'np_18px_span'})[0].get_text() # 핫딜 게시글 제목
        category = soup.find('a', attrs={'class':'category'}).get_text()
        id = soup.find('div', attrs={'class':'document_address'}).find('a')['href'].replace('/', '') # 핫딜 게시글 URL
        date = soup.find('span', attrs={'class':'date m_no'}).get_text() # 핫딜 등록일
        table = soup.find('table', attrs={'class':'hotdeal_table'}) # 핫딜 정보 테이블
        table_info = table.find_all('div', attrs={'class': 'xe_content'})
        deal_url = table_info[0].find('a', attrs={'class':'hotdeal_url'}).get_text() # 핫딜URL
        mall_name = table_info[1].get_text().strip() # 핫딜 쇼핑몰
        product_name = table_info[2].get_text() # 핫딜 상품명
        price = table_info[3].get_text() # 핫딜 가격
        delivery = table_info[4].get_text() # 핫딜 배송
        
        # 본문내용
        main_text = soup.find('div', attrs={'class':re.compile(fr'.*{re.escape(id)}.*')})
        content = re.sub(re.compile(r'<[^>]+>'), '', str(main_text)) # 모든 태그를 제거하는 패턴
        print(f'''
                핫딜 : {title}
                분류 : {category}
                등록일 : {date}
                게시글URL : {source}{id}
                쇼핑몰 : {mall_name}
                핫딜URL : {deal_url}
                상품명 : {product_name}
                가격 : {price}
                배송 : {delivery}
                내용 ::
                {content}
            ''')
        time.sleep(90)
    except IndexError:
        title = None
        category = None
        date = None
        id = None
        mall_name = None
        deal_url = None
        product_name = None
        price = None
        delivery = None
        content = None
        continue

# print(deal_soup)
# deal_title_name = deal_soup.find_all('span', attrs={'class':'np_18px_span'}).text.strip()
# print(deal_title_name)
# deal_url_name = deal_soup.find('a', attrs={'class':'hotdeal_url'}).get_text()

# print(f'''{deal_title_name}, {deal_url_name}''')
    # deal_product_name = deal_soup.find('h3', attrs={'class':'title'}).get_text()
    # print(product_name)
#     # 이후 원하는 정보를 추출하여 사용할 수 있습니다.

    # pattern = re.compile(r'<div>(.*?)</div>')
    # matches = re.findall(pattern, re.sub(re.compile(r'<br\s*/?>'), '', str(content)))
            # 본문 : {' '.join([text for text in matches if text.strip()])} 



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