from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import mariadb
import sys
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-offset', help=' : Please set the offset', type=int)
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

source_type = '0'  # 출처 구분, 필요에 따라 수정
ready_update_sql = "update gn_scrap_ready set status = ?, update_dt = now() where seq_no = ?"
ready_select_sql = f"select seq_no, source_url from gn_scrap_ready where source_type = '{source_type}' and status = '0' order by seq_no limit ?, 10"

offset = args.offset if args.offset is not None else 0

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    main_page = browser.new_page()

    while True:
        cur = conn.cursor()
        print(f'{datetime.now()} - Selecting URLs from gn_scrap_ready offset {offset}')

        cur.execute(ready_select_sql, (offset,))
        res = cur.fetchall()
        print(f'fetched {len(res)} records')

        if res is None or len(res) == 0:
            print("No URLs to process. Exiting.")
            break

        for record in res:
            ready_seq_no = record[0]
            ready_source_url = record[1]

            # 상태 변경: 수집처리대기
            cur.execute(ready_update_sql, ('1', ready_seq_no))
            conn.commit()

            print(f'[debug] seq_no : {ready_seq_no}')
            print(f'[debug] URL : {ready_source_url}')

            # 중복 검사
            cur.execute("select seq_no from gn_master where news_url = ?", (ready_source_url,))
            exist_news = cur.fetchall()
            if exist_news and len(exist_news) > 0:
                cur.execute(ready_update_sql, ('8', ready_seq_no))  # 중복취소
                conn.commit()
                print('[debug] break : 중복취소')
                continue

            try:
                time.sleep(5)  # 사이트 부담 완화용 대기
                main_page.goto(ready_source_url)
            except TimeoutError:
                if browser is not None:
                    browser.close()
                browser = p.firefox.launch(headless=True)
                main_page = browser.new_page()
                time.sleep(5)
                main_page.goto(ready_source_url)

            # 상태 변경: 수집중
            cur.execute(ready_update_sql, ('2', ready_seq_no))
            conn.commit()

            content = main_page.content()
            soup = BeautifulSoup(content, "html.parser")

            # 제목
            title_soup = soup.select_one('body > main > article > div.topic-table > div.topic > div.topictitle.link > a > h1')
            if title_soup is None:
                cur.execute(ready_update_sql, ('5', ready_seq_no))  # 실패 상태
                conn.commit()
                print('[debug] title parse error --> break')
                continue
            news_title = title_soup.get_text().strip()
            print(f'news_title : {news_title}')

            # 발행일
            news_pub_date = ''

            # 본문
            desc_select = soup.select_one('#topic_contents')
            if desc_select is None:
                cur.execute(ready_update_sql, ('5', ready_seq_no))
                conn.commit()
                print('[debug] desc parse error --> break')
                continue
            news_desc = desc_select.get_text(separator='\n').strip()
            print(f'news_desc : {news_desc}')
            
            #댓글내용
            comments_select = soup.select_one('div.commentTD > span')
            if comments_select is None:
                cur.execute(ready_update_sql, ('5', ready_seq_no))
                conn.commit()
                print('[debug] desc parse error --> break')
                continue
            news_comments = comments_select.get_text(separator='\n').strip()
            print(f'news_comments : {news_comments}')

            full_contents = ''
            # DB 삽입
            bm_insert_sql = '''
                INSERT INTO gn_master
                
                (news_title, news_desc, news_url, news_comments, full_contents, news_update)
                VALUES (?, ?, ?, ?, ?, now())
            '''
            cur.execute(bm_insert_sql, (
                news_title,
                news_desc,
                ready_source_url,
                news_comments,
                content
            ))
            conn.commit()
            print('[debug] master insert complete')

            # 상태 변경: 수집완료c
            cur.execute(ready_update_sql, ('9', ready_seq_no))
            conn.commit()
            print("-----------------------------------------------------------------------------------------------")

        time.sleep(10)
        break

    browser.close()
