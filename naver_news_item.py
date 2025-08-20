from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import mariadb
import sys
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-offset', help=' : Please set the offset')
args = parser.parse_args()

try:
    conn = mariadb.connect(
        user="lguplus7",
        password="lg7p@ssw0rd~!",
        host="localhost",
        port=3310,
        database="cp_data"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


# source_type - 0:네이버뉴스
source_type = '0'

ready_update_sql = "update news_scrap_ready set status = ?, update_dt = now() where seq_no = ?"
ready_insert_sql = "insert into news_scrap_ready(source_type, source_url, create_dt) values (?,?, now())"

list_cnt = 0
offset = args.offset
if offset is None:
    offset = 0
ready_select_sql = f"select seq_no, source_url from news_scrap_ready where source_type = '{source_type}' and status = '0' order by seq_no limit {offset}, 10"

# Playwright 실행
with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    main_page = browser.new_page()

    while True:
        cur = conn.cursor()
        print(f'{datetime.now()} - {ready_select_sql}')

        cur.execute(ready_select_sql)
        res = cur.fetchall()
        print(f'fetched {len(res)} records')
        if res is not None and res.__len__() > 0:
            for record in res:
                list_cnt += 1
                action = 'insert'
                bm_seq_no = '' # news_master의 seq_no
                news_title = ''
                news_category = ''
                news_author = ''
                news_desc = ''
                publisher = ''
                news_pub_date = ''
                news_url = ''
                ready_seq_no = record[0]
                ready_source_url = record[1]

                # status : 1 수집처리대기
                cur.execute(ready_update_sql, ('1', ready_seq_no))
                conn.commit()
                print('[debug] seq_no : ', ready_seq_no)
                print('[debug] URL : ', ready_source_url)

                # news_master에서 news_url 존재 검사 = 있으면 중복취소
                cur.execute("select seq_no from news_master where news_url = ?", (ready_source_url,))
                exist_news = cur.fetchall()
                if exist_news is not None and exist_news.__len__() > 0:
                    # status : 8 중복취소
                    cur.execute(ready_update_sql, ('8', ready_seq_no))
                    conn.commit()
                    print('[debug] break : 중복취소')
                    continue

                try:
                    time.sleep(10)
                    main_page.goto( ready_source_url )
                except TimeoutError as te:
                    #print(f"Error browser: {te}")
                    if browser is not None:
                        browser.close()
                    browser = p.firefox.launch(headless=True)
                    main_page = browser.new_page()
                    time.sleep(10)
                    main_page.goto( ready_source_url)

                # status : 2 수집중
                cur.execute(ready_update_sql, ('2', ready_seq_no))
                conn.commit()

                content = main_page.content()
                soup = BeautifulSoup(content, "html.parser")

                title_soup = soup.select_one('#title_area > span')
                if title_soup is None:
                    # status : 5 실패
                    cur.execute(ready_update_sql, ('5', ready_seq_no))
                    conn.commit()
                    print('[debug] title parse error --> break')
                    continue

                news_title = title_soup.get_text().strip()
                print('news_title : ', news_title)

                pubdate_soup = soup.select_one('div.media_end_head_info_datestamp > div > span')
                if pubdate_soup is None:
                    # status : 5 실패
                    cur.execute(ready_update_sql, ('5', ready_seq_no))
                    conn.commit()
                    print('[debug] publish date parse error --> break')
                    continue
                temp_str = pubdate_soup.get_text().strip()
                news_pub_date = temp_str.replace('. ', '').replace('.', '-')
                print('news_pub_date : ', news_pub_date)

                desc_select = soup.select_one('#dic_area')
                if desc_select is None:
                    # status : 5 실패
                    cur.execute(ready_update_sql, ('5', ready_seq_no))
                    conn.commit()
                    print('[debug] desc parse error --> break')
                    continue
                news_desc = desc_select.get_text().strip()
                print('desc : ', news_desc)

                # insert
                bm_insert_sql = 'insert into news_master (news_title, news_desc, publisher, news_pub_date, news_url, news_update) values (?,?,?,?,?,now())'
                cur.execute(bm_insert_sql, (news_title, news_desc, publisher, news_pub_date, ready_source_url))
                conn.commit()
                print('[debug] master insert complete')

                # status : 9 수집완료
                cur.execute(ready_update_sql, ('9', ready_seq_no))
                conn.commit()
                print(f"-----------------------------------------------------------------------------------------------")
        time.sleep(10)
        break
