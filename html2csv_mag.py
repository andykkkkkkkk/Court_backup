from bs4 import BeautifulSoup
from os.path import relpath
import pandas as pd
from func import flat_tag, group_by


# The .html files on and after 20221109 are parsed with lxml
# DC and HC: Court | Judges | Time | Case No. | Parties | Offences / Nature | Representation
# MC: Time | Case No | Defendant/ Respondent | Offences/ Nature | Hearing

dir_open = relpath('html')
dir_save = relpath('csv')
date = str(input('Please input the date in yyyymmdd format: '))
filename = f'{date}_ALLMAG.html'

with open(f'{dir_open}\\{filename}', 'r', encoding='utf-8') as file:
    html = file.read()
# print(f'Size: {len(html)}')
soup = BeautifulSoup(html, 'lxml')

# This part gets all strings in to a flat list
td_tags = soup.find_all('td')
str_list = flat_tag(td_tags)

# This part create a list of list by different mags
str_list_by_mag = group_by(str_list, 'Magistrate :')
for lst in str_list_by_mag:
    i = str_list_by_mag.index(lst)
    if i < len(str_list_by_mag) - 1:  # The last list doesn't have '法 庭'
        lst = lst[:lst.index('法 庭')]
    del lst[1:6]
    str_list_by_mag[i] = lst
# del str_list_by_mag[-1][1:6]
str_list_by_mag = str_list_by_mag[1:]

# print(str_list_by_mag[7])

headers = ['Time', 'Case Number', 'Defendant', 'Offences/ Natures', 'Hearing']

i = 0
for lst in str_list_by_mag:
    mag = str_list_by_mag[i][0]
    time = str_list_by_mag[i][1::5]
    case_no = str_list_by_mag[i][2::5]
    defendant = str_list_by_mag[i][3::5]
    offences = str_list_by_mag[i][4::5]
    hearing = str_list_by_mag[i][5::5]
    zipped = list(zip(time, case_no, defendant, offences, hearing))
    if i == 0:
        df = pd.DataFrame(zipped, columns=headers)
        df = df.assign(Magistrate=mag, Date=date)
    else:
        df2 = pd.DataFrame(zipped, columns=headers)
        df2 = df2.assign(Magistrate=mag, Date=date)
        df = pd.concat([df, df2])
    i += 1

df = df.mask(df == '')
df = df.ffill(axis=0)
df['Court'] = 'MAG'
df = df[['Date', 'Time', 'Court', 'Case Number', 'Magistrate', 'Defendant', 'Offences/ Natures', 'Hearing']]

# append data frame to CSV file
# Check if it has been appended
with open(f'{dir_save}\\memory_mag.txt', 'r') as f:
    memory = f.read()
memory = memory.split('\n')[1:]

if not (date in memory):
    df.to_csv(f'{dir_save}\\{date[:6]}_ALLMAG.csv', mode='a', index=False, header=False)
    with open(f'{dir_save}\\memory_mag.txt', 'a') as f:
        f.write(f'\n{date}')
    print(f'{date} has been appended into the .csv.')
else:
    print(f'{date} was appended into the .csv. No action is done.')
