import mysql.connector
from crawl_deal import crawl_hotdeal, insert_into_mysql

# MySQL 연결 설정
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0916",
    database="hotdeal"
)

# 크롤링할 웹사이트 정보
source = 'https://www.fmkorea.com/'
headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }

# 핫딜 데이터 가져오기
hotdeals = crawl_hotdeal(source, headers)

# MySQL에 데이터 삽입
insert_into_mysql(hotdeals, connection)

# MySQL 연결 종료
connection.close()
