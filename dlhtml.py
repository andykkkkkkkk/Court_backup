import requests
from bs4 import BeautifulSoup
from os.path import relpath

date = str(input('Please input the date in yyyymmdd format: '))
day = date[6:]
month = date[4:6]
year = date[:4]
print(f'day: {day}, month: {month}, year: {year}')
courts = ['CACFI', 'DC', 'ALLMAG']
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'}
directory = relpath('html')

for court in courts:
    url = f'https://e-services.judiciary.hk/dcl/view.jsp?lang=tc&date={day}{month}{year}&court={court}'
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.content, 'lxml')
    filename = f'{year}{month}{day}_{court}.html'
    print(f'Requesting {court}...')
    if r.status_code == 200:
        print(f'Status: {r.status_code} OK')
        if len(soup.prettify()) > 20000:
            # Write .html file if not blank
            with open(f'{directory}\\{filename}', 'w', encoding='utf-8') as file:
                file.write(soup.prettify())
            print(f'{filename} has been saved.')
        else:
            print(f'{filename} looks blank and is not saved.')
    else:
        print(f'Status: {r.status_code}\n {filename} is not downloaded.')

    # print(r.headers)
    # print(soup.prettify())
    # print(r.text)
    # print(r.url)




