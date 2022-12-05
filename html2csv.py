from bs4 import BeautifulSoup
from os.path import relpath
import pandas as pd
from func import tags2strlist

dir_open = relpath('html')
dir_save = relpath('csv')
date = '20221111'
# date = str(input('Please input the date in yyyymmdd format: '))
courts = ['DC', 'CACFI']
str_dict = {}
widths = {'cols': ['Location', 'Judge', 'Time', 'Case', 'Party', 'Offence', 'Rep'],
          'DC': ['104', '104', '88', '160', '192', '232', '200'],
          'CACFI': ['84', '154', '140', '112', '184', '173', '196']}

col_dict = {'DC': {}, 'CACFI': {}}
for court in courts:
    with open(f'{dir_open}\\{date}_{court}.html', 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'lxml')
    i = 0
    for col in widths['cols']:
        if court == 'DC' and i < 2:
            td_tags = soup.find_all('td', attrs={'width': widths[court][i]})[i::2]
        else:
            td_tags = soup.find_all('td', attrs={'width': widths[court][i]})
        col_dict[court][col] = tags2strlist(td_tags)
        i += 1

# Manually trim the col_dict
for k in col_dict['DC'].keys():
    col_dict['DC'][k] = col_dict['DC'][k][1:]

col_dict['HC'] = col_dict.pop('CACFI')
start_list = [9, 3, 3, 4, 4, 4, 4]
i = 0
for k in col_dict['HC'].keys():
    start = start_list[i]
    col_dict['HC'][k] = col_dict['HC'][k][start:]
    i += 1

col_dict['HC']

def get_df(dict: dict, court: str):
    df = pd.DataFrame.from_dict(dict[court], orient='index').transpose()
    df.drop_duplicates()
    # df.pop('Location')
    # df.pop('Time')
    df = df.mask(df == '')
    df = df.mask(df == '\n')
    df = df.ffill(axis=0)
    return df


df_DC = get_df(col_dict, 'DC')
df_HC = get_df(col_dict, 'HC')
dfs = {'DC': df_DC, 'HC': df_HC}
for k, v in dfs.items():
    v['Court'] = k
    v['Date'] = date
    dfs[k] = v[['Date', 'Time', 'Court', 'Case', 'Judge', 'Party', 'Offence', 'Location', 'Rep']]

print(dfs['HC'].head())
dfs['HC'].to_csv(f'{dir_save}\\{date}_HC.csv', index=False, header=False)

# DC_t_tags = str_dict['DC']
# print(tags2strlist())

#     td_tags = soup.find_all('td')
#     str_dict[court] = flat_tag(td_tags)
#
# str_dict['DC'] = str_dict['DC'][10:-25]
# str_dict['CACFI'] = str_dict['CACFI'][50:-30]
# del_idx = str_dict['CACFI'].index('原訟法庭')
# del str_dict['CACFI'][del_idx:del_idx + 13]
# # for st in str_dict['DC'][:20]:
# #     print(st)
# #     print('================DC====================')
# #
# # for st in str_dict['CACFI'][:20]:
# #     print(st)
# #     print('================HC====================')
# print(str_dict['CACFI'][4::7])
