import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 크롤링할 웹사이트 정보
source = 'https://www.fmkorea.com'
url = f'{source}/index.php?mid=hotdeal&sort_index=pop&order_type=desc'
user_agent = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

# 셀레니움 설정 정보
chrome_option = webdriver.ChromeOptions()
chrome_option.add_argument("--headless")
chrome_option.add_argument("--no-sandbox")
chrome_option.add_argument("--disable-dev-shm-usage")
chrome_option.add_argument(f'--user-agent={user_agent["User-Agent"]}')
chrome_option.add_argument("--disable-gpu")

browser = webdriver.Chrome(options=chrome_option)
browser.get(url)
time.sleep(5)
html = browser.page_source
browser.quit()
soup = BeautifulSoup(html, 'lxml')
deals = soup.find_all('li', attrs={'class':re.compile('hotdeal0$')})
hotdeal_bowl = []

# 핫딜 게시글별 크롤링
for deal in deals[0:1]:
    try:
        deal_link = source + deal.find('a')['href']  # 핫딜 링크 추출
        # Selenium #
        browser = webdriver.Chrome(options=chrome_option)
        browser.get(deal_link)
        time.sleep(5)
        html = browser.page_source
        browser.quit()
        # # # # # # #

        soup = BeautifulSoup(html, 'lxml')  # 해당 링크의 HTML 파싱
        title = soup.find_all('span', attrs={'class':'np_18px_span'})[0].get_text() # 핫딜 게시글 제목
        category = soup.find('a', attrs={'class':'category'}).get_text() # 핫딜 분류
        url = soup.find('div', attrs={'class':'document_address'}).find('a')['href'].replace('/', '') # 핫딜 게시글 URL
        date = soup.find('span', attrs={'class':'date m_no'}).get_text() # 핫딜 등록일
        table = soup.find('table', attrs={'class':'hotdeal_table'}) # 핫딜 정보 테이블
        print(table)
        table_info = table.find_all('div', attrs={'class': 'xe_content'})
        print(table_info)
        deal_url = table_info[0].find('a', attrs={'target':'_blank'}).get_text() # 핫딜 URL
        mall_name =re.sub(r"\[.*\]", "", table_info[1].get_text()).strip()  # 핫딜 쇼핑몰
        product_name = table_info[2].get_text() # 핫딜 상품명
        price = table_info[3].get_text() # 핫딜 가격
        delivery = table_info[4].get_text() # 핫딜 배송

        # 본문내용
        main_text = soup.find('div', attrs={'class':re.compile(fr'.*{re.escape(url)}.*')})
        content = re.sub(re.compile(r'<[^>]+>'), '', str(main_text)) # 모든 태그를 제거하는 패턴

        hotdeal_bowl.append({
            'title': title,
            'category': category,
            'date': date,
            'url': url,
            'deal_url': deal_url,
            'mall_name': mall_name,
            'product_name': product_name,
            'price': price,
            'delivery': delivery,
            'content': content
        })
        print(hotdeal_bowl)
        # time.sleep(30)
    except IndexError:
        title = None
        category = None
        date = None
        url = None
        mall_name = None
        deal_url = None
        product_name = None
        price = None
        delivery = None
        content = None
        continue
    # return hotdeal_bowl

# def insert_into_mysql(hotdeals, connection):
#     cursor = connection.cursor()
#     for deal in hotdeals:
#         current_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')  # 현재 시간을 YYYY/MM/DD HH:MM:SS 포맷으로 가져옴
#         # URL 값이 이미 존재하는지 확인하는 쿼리 실행
#         cursor.execute("SELECT COUNT(*) FROM deals WHERE url = %s", (deal['url'],))
#         result = cursor.fetchone()
#         # URL 값이 이미 존재하는 경우 데이터를 삽입하지 않음
#         if result[0] > 0:
#             continue
#         # URL 값이 존재하지 않는 경우 데이터를 삽입
#         sql = "INSERT INTO deals (title, category, date, url, deal_url, mall_name, product_name, price, delivery, content, insert_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#         val = (deal['title'], deal['category'], deal['date'], deal['url'], deal['deal_url'], deal['mall_name'], deal['product_name'], deal['price'], deal['delivery'], deal['content'], current_time)
#         cursor.execute(sql, val)
#     connection.commit()
#     cursor.close()




        # file_path = "deal0.html"  # 저장할 파일의 경로와 이름
        # with open(file_path, "w", encoding="utf-8") as file:
        #     file.write(str(soup))