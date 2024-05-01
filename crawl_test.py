import requests
import re
import time
import pyshorteners
from bs4 import BeautifulSoup

source = 'https://www.fmkorea.com/'

with open('deal_html.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')
# 핫딜 기본 정보
deal_title_name = soup.find_all('span', attrs={'class':'np_18px_span'})[0].get_text() # 핫딜 게시글 제목
deal_post_url_name = soup.find('div', attrs={'class':'document_address'}).find('a')['href'].replace('/', '') # 핫딜 게시글 URL
# 핫딜 정보 테이블
deal_info_table = soup.find('table', attrs={'class':'hotdeal_table'}) 
deal_date = soup.find('span', attrs={'class':'date m_no'}).get_text()
deal_table_values = deal_info_table.find_all('div', attrs={'class': 'xe_content'})
deal_url = deal_table_values[0].find('a', attrs={'class':'hotdeal_url'}).get_text()
deal_mall_name = deal_table_values[1].get_text().strip()
deal_product_name = deal_table_values[2].get_text()
deal_price = deal_table_values[3].get_text()
deal_delivery = deal_table_values[4].get_text()
# 본문내용
deal_content = soup.find(['div'], attrs={'class':re.compile(fr'.*{re.escape(deal_post_url_name)}.*')})
pattern = re.compile(r'<[^>]+>')  # 모든 태그를 제거하는 패턴
content_text = re.sub(pattern, '', str(deal_content))

print(content_text)
# content_pattern = re.compile(r'<[^>]+>')
# matches = re.findall(content_pattern, re.sub(re.compile(r'<br\s*/?>'), '', str(deal_content)))
# 정규표현식으로 가져온 내용을 리스트가 아닌 하나의 문자열로 결합하여 출력

# print(f'''
#         핫딜 : {deal_title_name} {deal_date}
#         게시글URL : {source}{deal_post_url_name}
#         쇼핑몰 : {deal_mall_name}/{deal_url}
#         상품명/가격/배송 : {deal_product_name}/{deal_price}/{deal_delivery}
#         본문 : {' '.join([text for text in matches if matches.append(text.strip())])} 
#     ''')








# print(deal_delivery)
# deal_post_url_name = deal_info_table[0]
# deal_post_url_name = soup.find('div', attrs={'class':'document_address'}).find('a').get_text()
# deal_mall_name = soup.find('div', attrs={'class':'xe_content'}).get_text()
# deal_mall_url_name = soup.find('a', attrs={'class':'hotdeal_url'})['href']

# print(deal_post_url_name)
# deal_shopping_url_name = soup.find_all('a', attrs={'class':'hotdeal_url'}).get_text()
