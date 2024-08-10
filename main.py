import mysql.connector
from crawler import crawl_hotdeal, insert_into_mysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# 핫딜 데이터 가져오기
hotdeals = crawl_hotdeal(source, base_url, chrome_option)

# MySQL에 데이터 삽입
insert_into_mysql(hotdeals, connection)

# MySQL 연결 종료
connection.close()
