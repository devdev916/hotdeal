import mysql.connector
from datetime import datetime, timedelta
from crawler import crawl_hotdeal
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # 크롤링할 웹사이트 정보
    source = 'https://www.fmkorea.com'
    base_url = f'{source}/index.php?mid=hotdeal&sort_index=pop&order_type=desc'

    # MySQL 연결 설정
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="0916",
        database="hotdeal"
    )
    
    # 셀레니움 설정 정보
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    )

    # ChromeDriver Service 설정
    service = Service(ChromeDriverManager().install(), port=9515)
    # 브라우저 초기화
    browser = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 핫딜 데이터 가져오기
        hotdeals = crawl_hotdeal(source, base_url, browser, connection)

        # MySQL에 데이터 삽입
        if hotdeals:
            insert_into_mysql(hotdeals, connection)
        else:
            print("No new hot deals found.")

    finally:
        # 브라우저 종료 및 MySQL 연결 종료
        browser.quit()
        connection.close()

def insert_into_mysql(hotdeals, connection):
    """ 크롤링한 데이터를 MySQL에 삽입하는 함수 """
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
        sql = """
        INSERT INTO deals (title, category, date, url, deal_url, mall_name, product_name, price, delivery, content, insert_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        val = (
            deal['title'], 
            deal.get('category', None),  # 카테고리 정보가 없는 경우 기본값 None 사용
            deal.get('date', None),  # 날짜 정보가 없는 경우 기본값 None 사용
            deal['url'],  # URL
            deal.get('deal_url', None),  # deal_url이 없는 경우 기본값 None 사용
            deal.get('mall_name', None),  # mall_name이 없는 경우 기본값 None 사용
            deal.get('product_name', None),  # product_name이 없는 경우 기본값 None 사용
            deal.get('price', None),  # price가 없는 경우 기본값 None 사용
            deal.get('delivery', None),  # delivery가 없는 경우 기본값 None 사용
            deal.get('content', None),  # content가 없는 경우 기본값 None 사용
            current_time
        )
        cursor.execute(sql, val)

    connection.commit()
    cursor.close()

if __name__ == '__main__':
    main()



# # 크롤링할 웹사이트 정보
# source = 'https://www.fmkorea.com'
# base_url = f'{source}/index.php?mid=hotdeal&sort_index=pop&order_type=desc'

# # MySQL 연결 설정
# connection = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="0916",
#     database="hotdeal"
# )
# user_agent = {
#         'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
#     }

# # 셀레니움 설정 정보
# chrome_option = webdriver.ChromeOptions()
# chrome_option.add_argument("--headless")
# chrome_option.add_argument("--no-sandbox")
# chrome_option.add_argument("--disable-dev-shm-usage")
# chrome_option.add_argument(f'--user-agent={user_agent["User-Agent"]}')
# chrome_option.add_argument("--disable-gpu")

# # 핫딜 데이터 가져오기
# hotdeals = crawl_hotdeal(source, base_url, chrome_option, connection)

# # MySQL에 데이터 삽입
# insert_into_mysql(hotdeals, connection)

# # MySQL 연결 종료
# connection.close()