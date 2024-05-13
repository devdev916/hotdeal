import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 크롤링할 웹사이트 정보
url = 'https://www.fmkorea.com/index.php?mid=hotdeal&sort_index=pop&order_type=desc'

def crawl_hotdeals(url):
    html = get_page_html_from_url(url)
    print(html)


def get_page_html_from_url(url):
    user_agent = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument("--headless")
    chrome_option.add_argument("--no-sandbox")
    chrome_option.add_argument("--disable-dev-shm-usage")
    chrome_option.add_argument(f'--user-agent={user_agent["User-Agent"]}')
    chrome_option.add_argument("--disable-gpu")
    browser = webdriver.Chrome(options=chrome_option)
    browser.get(url)
    # WebDriverWait(browser, 30).until(
    #     EC.presence_of_element_located((By.ID, "reviewListFragment"))
    # )
    time.sleep(5)

    html = browser.page_source
    browser.quit()

    
    # HTML을 파일로 저장
    save_html_to_file(html)
    return html

def save_html_to_file(html):
    file_path = "deal.html"  # 저장할 파일의 경로와 이름
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html)


crawl_hotdeals(url)  # 함수 호출 추가
