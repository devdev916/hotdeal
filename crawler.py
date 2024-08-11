import re
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def crawl_hotdeal(source, base_url, chrome_option, connection):
    hotdeal_bowl = []

    # MySQL에서 지난 7일 동안 저장된 URL 가져오기
    cursor = connection.cursor()
    seven_days_ago = datetime.now() - timedelta(days=7)
    cursor.execute(
        "SELECT url FROM deals WHERE STR_TO_DATE(date, '%Y.%m.%d %H:%i') >= %s", 
        (seven_days_ago.strftime('%Y.%m.%d'),)
    )
    existing_urls = set([row[0] for row in cursor.fetchall()])
    cursor.close()

    # 가져온 URL 리스트 출력 (디버깅 용도)
    print(f"{seven_days_ago}")
    print(f"최근 7일 동안의 기존 URL: {existing_urls}")

    # 1~10 페이지 순회
    for page in range(1, 3):
        url = f"{base_url}&page={page}"
        # 핫딜 게시판 인기탭 게시판
        browser = webdriver.Chrome(options=chrome_option)
        browser.get(url)
        time.sleep(5)
        html = browser.page_source
        browser.quit()
        soup = BeautifulSoup(html, 'lxml') # HTML 파싱
        deals = soup.find_all('li', attrs={'class':re.compile('hotdeal0$')})

    # 핫딜 게시글별 크롤링
        for deal in deals:
            try:
                full_deal_link = source + deal.find('a')['href']  # 핫딜 링크 추출 # document_srl 부분만 추출
                
                # document_srl 숫자만 추출하여 deal_link에 저장
                deal_link = re.search(r'document_srl=(\d+)&', full_deal_link).group(1)

                # 비교를 위한 디버깅 출력
                print(f"크롤링된 URL: {deal_link}")
                
                # 이미 지난 7일 이내에 데이터베이스에 존재하는 URL인지 확인
                if deal_link in existing_urls:
                    print(f"중복된 URL: {deal_link}, 크롤링 패스")
                    continue  # 중복된 URL은 크롤링하지 않음

                # Selenium #
                browser = webdriver.Chrome(options=chrome_option)
                browser.get(full_deal_link)
                time.sleep(10)
                html = browser.page_source
                browser.quit()
                # # # # # # #

                soup = BeautifulSoup(html, 'lxml')  # 해당 링크의 HTML 파싱
                title = soup.find_all('span', attrs={'class':'np_18px_span'})[0].get_text() # 핫딜 게시글 제목
                category = soup.find('a', attrs={'class':'category'}).get_text() # 핫딜 분류
                url = soup.find('div', attrs={'class':'document_address'}).find('a')['href'].replace('/', '') # 핫딜 게시글 URL
                date = soup.find('span', attrs={'class':'date m_no'}).get_text() # 핫딜 등록일
                table = soup.find('table', attrs={'class':'hotdeal_table'}) # 핫딜 정보 테이블
                table_info = table.find_all('div', attrs={'class': 'xe_content'})
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
                print(title)
                time.sleep(10)
            except (IndexError, AttributeError):
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
    return hotdeal_bowl

def insert_into_mysql(hotdeals, connection):
    cursor = connection.cursor()
    for deal in hotdeals:
        current_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')  # 현재 시간을 YYYY/MM/DD HH:MM:SS 포맷으로 가져옴
        # URL 값이 이미 존재하는지 확인하는 쿼리 실행
        cursor.execute("SELECT COUNT(*) FROM deals WHERE url = %s", (deal['url'],))
        result = cursor.fetchone()
        # URL 값이 이미 존재하는 경우 데이터를 삽입하지 않음
        if result[0] > 0:
            continue
        # URL 값이 존재하지 않는 경우 데이터를 삽입
        sql = "INSERT INTO deals (title, category, date, url, deal_url, mall_name, product_name, price, delivery, content, insert_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (deal['title'], deal['category'], deal['date'], deal['url'], deal['deal_url'], deal['mall_name'], deal['product_name'], deal['price'], deal['delivery'], deal['content'], current_time)
        cursor.execute(sql, val)
    connection.commit()
    cursor.close()




        # file_path = "deal0.html"  # 저장할 파일의 경로와 이름
        # with open(file_path, "w", encoding="utf-8") as file:
        #     file.write(str(soup))