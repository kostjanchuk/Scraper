from bs4 import BeautifulSoup
import requests
from datetime import datetime


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
           }


# def get_date(date):
#     month_list = ['січня', 'лютого', 'березня', 'квітня', 'травня', 'червня', 'липня'
#         , 'серпня', 'вересня', 'жовтня', 'листопаду', 'грудня']
#     date = date.split()
#     return (f'{date[0]}/{month_list.index(date[1]) + 1}/{date[2]}')


def work_ua(base_url):
    vacancies_list = []
    domain = 'https://www.work.ua'
    urls = []
    r = requests.get(base_url, headers=headers)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, features='lxml')
        pagination = soup.find('ul', attrs={'class': 'pagination'})
        if pagination:
            last_page = pagination.find_all('li', attrs={'class': False})[-1].text
            for i in range(int(last_page)):
                urls.append(base_url + '?page={}'.format(i+1))
    for url in urls:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, features='lxml')
            vacancies = soup.find_all('div', class_='job-link')
            for v in vacancies:
                title = v.a.text
                href = v.a['href']
                short = v.p.text
                city = v.find('div', class_='add-top-xs').find('span', class_="middot").find_next('span')
                if city.text == 'VIP' or city.text == 'Агенція':
                    city = city.find_next('span').find_next('span').text.split(',')[0]
                else:
                    city = city.text.split(',')[0]
                company = v.find('div', class_='add-top-xs').find('b').text
                # date_str = v.h2.a['title'].split('від ')[1]
                # date_correct_str = get_date(date_str)
                # created_at = datetime.strptime(date_correct_str, "%d/%m/%Y").date()

                vacancy = {
                    'title': title,
                    'href': domain + href,
                    'short': " ".join(short.split()),
                    'city': city,
                    'company': company,
                }
                vacancies_list.append(vacancy)
    return vacancies_list

