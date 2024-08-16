import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

login_url = 'https://www.jobplanet.co.kr/users/sign_in'

# email and password placeholders
email = 'xxxx@gmail.com'
password = 'xxxxxxx'

LOGIN_INFO = {
    'user[email]': email,
    'user[password]': password,
    'commit': '로그인'
}

session = requests.session()
res = session.post(login_url, data=LOGIN_INFO, verify=False)
res.raise_for_status()

result = []

def clean_str(text):
    pattern = '([ㄱ-ㅎㅏ-ㅣ]+)'
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '<[^>]*>'
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '[^\w\s]'
    text = re.sub(pattern=pattern, repl='', string=text)
    text = text.replace('\r', '. ')
    return text

last_page = 1291
for idx in range(1, last_page):
    url = f'https://www.jobplanet.co.kr/companies/19514/reviews/lg%EC%A0%84%EC%9E%90?page={idx}'
    res = session.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    count3, count4, count5 = 0, 0, 0

    try:
        for k in range(5):
            reviewer_info = []
            position = soup.select('.content_top_ty2 > span.txt1')[0 + count4].text
            status = soup.select('.content_top_ty2 > span.txt1')[1 + count4].text
            loc = soup.select('.content_top_ty2 > span.txt1')[2 + count4].text
            day = soup.select('.content_top_ty2 > span.txt1')[3 + count4].text
            star_rating = soup.select('.us_star_m > div.star_score')[0 + k]['style'][6:-1]
            promotion = soup.select('.bl_score')[0 + count5]['style'][6:-1]
            welfare = soup.select('.bl_score')[1 + count5]['style'][6:-1]
            balance = soup.select('.bl_score')[2 + count5]['style'][6:-1]
            culture = soup.select('.bl_score')[3 + count5]['style'][6:-1]
            top = soup.select('.bl_score')[4 + count5]['style'][6:-1]

            # 변화 if 절
            if star_rating == '0%':
                star_rating = '0'
            elif star_rating == '20%':
                star_rating = '1'
            elif star_rating == '40%':
                star_rating = '2'
            elif star_rating == '60%':
                star_rating = '3'
            elif star_rating == '80%':
                star_rating = '4'
            elif star_rating == '100%':
                star_rating = '5'

            if promotion == '0%':
                promotion = '0'
            elif promotion == '20%':
                promotion = '1'
            elif promotion == '40%':
                promotion = '2'
            elif promotion == '60%':
                promotion = '3'
            elif promotion == '80%':
                promotion = '4'
            elif promotion == '100%':
                promotion = '5'

            if welfare == '0%':
                welfare = '0'
            elif welfare == '20%':
                welfare = '1'
            elif welfare == '40%':
                welfare = '2'
            elif welfare == '60%':
                welfare = '3'
            elif welfare == '80%':
                welfare = '4'
            elif welfare == '100%':
                welfare = '5'

            if balance == '0%':
                balance = '0'
            elif balance == '20%':
                balance = '1'
            elif balance == '40%':
                balance = '2'
            elif balance == '60%':
                balance = '3'
            elif balance == '80%':
                balance = '4'
            elif balance == '100%':
                balance = '5'

            if culture == '0%':
                culture = '0'
            elif culture == '20%':
                culture = '1'
            elif culture == '40%':
                culture = '2'
            elif culture == '60%':
                culture = '3'
            elif culture == '80%':
                culture = '4'
            elif culture == '100%':
                culture = '5'

            if top == '0%':
                top = '0'
            elif top == '20%':
                top = '1'
            elif top == '40%':
                top = '2'
            elif top == '60%':
                top = '3'
            elif top == '80%':
                top = '4'
            elif top == '100%':
                top = '5'

            content = soup.select('h2.us_label')[0 + k].text
            merit = soup.select('dl.tc_list > dd.df1 > span')[0 + count3].text
            disadvantages = soup.select('dl.tc_list > dd.df1 > span')[1 + count3].text
            df_tit = soup.select('dl.tc_list > dd.df1 > span')[2 + count3].text

            reviewer_info = [position, status, loc, day, star_rating, promotion, welfare, balance, culture, top, clean_str(content), clean_str(merit), clean_str(disadvantages), clean_str(df_tit)]
            result.append(reviewer_info)

            count3 += 3
            count4 += 4
            count5 += 5
            print(f"pass :{idx}-{k}")

    except:
        print(f"fail :{idx}")

colname = ['직무', '상황', '지역', '작성일', '총점', '승진 기회 및 가능성', '복지 및 급여', '업무와 삶의 균형', '사내문화', '경영진', '총평', '장점', '단점', '바라는점']
df = pd.DataFrame(result, columns=colname)
df.to_excel("jobplanet_기업명.xlsx")


## 코랩이 아닌경우 주석처리 필요
from google.colab import files
files.download('jobplanet_기업명.xlsx')