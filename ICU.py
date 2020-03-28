#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
from datetime import datetime


def scrape():
    data = {
        'filter[search]':'',
        'list[fullordering]':'a.title+ASC',
        'list[limit]':'0',
        'filter[federalstate]':'0',
        'filter[chronosort]':'0',
        'filter[icu_highcare_state]':'',
        'filter[ecmo_state]':'',
        'filter[ards_network]':'',
        'limitstart':'0',
        'task':'','boxchecked':'0',
        '51557187c01c6d57161ec579f0174250':'1'
    }
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'}
    r = requests.post('https://www.divi.de/register/intensivregister?view=items', data=data, headers=headers)
    return BeautifulSoup(r.content, "html.parser")


def parse_clinic(table_row):
    data = {}
    tds = table_row.find_all('td')
        
    td0 = tds[0].text.splitlines()
    data['name'] = td0[1].strip()
    data['description'] = [s.strip() for s in td0[2:]]

    data['contact_text'] = tds[1].text.replace('Website', '').replace('\n', '').strip()
    data['website'] = ''
    a = tds[1].find('a')
    if a:
        data['website'] = a['href']

    data['state'] = tds[2].text.strip()

    status_map = {'hr-icon-green':'available', 'hr-icon-yellow':'limited', 'hr-icon-red':'occupied', 'hr-icon-unavailable':'unavailable'}
    data['status_icu_low_care'] = status_map[tds[3].find('span')['class'][0]]
    data['status_icu_high_care'] = status_map[tds[4].find('span')['class'][0]]
    data['status_ecmo'] = status_map[tds[5].find('span')['class'][0]]
    
    data['last_update'] = ' '.join([l.strip() for l in tds[6].text.splitlines()]).strip()
    return data


def parse_soup(soup):
    return [parse_clinic(tr) for tr in soup.select('#dataList > tbody')[0].find_all('tr')]


def main():
    soup = scrape()
    clinics = parse_soup(soup)

    with open(datetime.now().strftime('%y%m%d_%H%M%S.json'), 'w') as f:
        f.write(json.dumps(clinics, indent=4))


if __name__ == '__main__':
    main()