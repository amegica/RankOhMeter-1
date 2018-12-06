import sys
import re
from contextlib import closing
from bs4 import BeautifulSoup
import time
import threading
import queue
import csv
from urlconnect import simple_get
from urlconnect import is_good_response

def get_current_leaderboard(soup):
    current_players_list = []
    table = soup.find("table",{"class":"table table1 s-c-table lb-table"})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [elem.text.strip() for elem in cols]
        current_players_list.append([elem for elem in cols if elem])
    #[print(item) for item in current_players_list]
    return current_players_list

def get_leaderboard(root_url = str(), region = str()):
    full_url = root_url + region + '/' # after / there will be the number of the page appended
    page_number = 0
    exit_loop = False
    while True:
        raw_html = simple_get(full_url + str(page_number))
        soup = BeautifulSoup(raw_html, 'html.parser')
        current_leaderboard = get_current_leaderboard(soup)

        #check if we get to the end of leaderboard
        for current_list in current_leaderboard:
            # the list contains only ['No summoners recorded.'] in case the leaderboard is empty
            if len(current_list) <= 1:
                exit_loop = True

        if exit_loop is True:
            break

        with open('output.csv', 'a+') as output_file:
            for current_list in current_leaderboard:
                for item in current_list:
                    item = item.replace(',', '')
                    output_file.write(str(item) + ',')
                output_file.write('\n')
        print(page_number)
        page_number += 1

## 22 486 EUNE

# https://lolprofile.net/leaderboards

ROOT_URL = 'https://lolprofile.net/leaderboards'

BR = '/br'
EUNE = '/eune'
EUW = '/euw'
JP = '/jp'
KR = '/kr'
LAN = '/lan'
LAS = '/las'
NA = '/na'
OCE = '/oce'
TR = '/tr'
RU = '/ru'

if __name__ == '__main__':
    get_leaderboard(ROOT_URL, EUNE)
