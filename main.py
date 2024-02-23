import csv
import json
import requests
import os


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options


def start_crawler(city):
    current_count = 1
    try:
        page_url = f'https://krisha.kz/prodazha/kvartiry/{city}'
        page_response = requests.get(page_url)
        soup = BeautifulSoup(page_response.text, 'lxml')
        page_count = int(soup.find('nav', class_='paginator').find_all('a')[-2].get('data-page'))
    except Exception:
        print(f'[ERROR] FIND PAGE FUNCTION ERROR')

    for page in range(1, page_count):

        page_headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
        }

        try:
            page_url = f'https://krisha.kz/prodazha/kvartiry/{city}/?page={page}'
            page_response = requests.get(page_url, headers=page_headers)

            soup = BeautifulSoup(page_response.text, 'lxml')
            page_data = soup.find('script', id='jsdata')
            another_data = page_data.text.replace('var data =', '').replace(';', '').strip()

            json_data = json.loads(another_data)
            ids_value = json_data["search"]["ids"]

        except Exception:
            print(f'[ERROR] PAGE SECTION URL OR IDS')

        if not os.path.exists('KRISHA_DATA'):
            os.mkdir('KRISHA_DATA')

        if not os.path.exists(f'KRISHA_DATA/{city}_COMPLETE_IDS.txt'):
            with open(f'KRISHA_DATA/{city}_COMPLETE_IDS.txt', 'w', encoding='utf-8') as file:
                file.write('')

        with open(f'KRISHA_DATA/{city}.csv', mode='w', encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter=',', lineterminator='\r')
            file_writer.writerow(["USERNAME", "CITY", "PHONE"])

        with open(f'KRISHA_DATA/{city}_COMPLETE_IDS.txt', 'r', encoding='UTF-8') as file:
            complete_ids = file.readlines()

        try:
            for id in ids_value:
                if id not in complete_ids:
                    edge_options = Options()
                    edge_options.add_argument('log-level=3')
                    edge_options.add_argument("--headless")
                    driver = webdriver.Edge(options=edge_options)
                    url = f'https://krisha.kz/a/show/{id}'
                    driver.get(url)

                    try:
                        close_note = WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, 'fi-close-big')))
                        close_note.click()
                    except Exception:
                        pass

                    try:
                        button_2 = WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, 'tutorial__close')))
                        button_2.click()
                    except Exception:
                        pass

                    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, 'show-phones')))
                    button.click()

                    phone_number = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "offer__contacts-phones")))

                    username = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "owners__name")))

                    with open(f'KRISHA_DATA/{city}.txt', 'a', encoding='UTF-8') as file:
                        file.write(f'{username.text} | {city} | {phone_number.text}' + '\n')
                    
                    with open(f'KRISHA_DATA/{city}.csv', mode='a', encoding='utf-8') as w_file:
                        file_writer = csv.writer(w_file, delimiter=',', lineterminator='\r')
                        file_writer.writerow([username.text, city, phone_number.text])

                    with open(f'KRISHA_DATA/{city}_COMPLETE_IDS.txt', 'a', encoding='UTF-8') as file:
                        file.write(str(id) + '\n')

                    print(f'[CURRENT STATUS] ID: {id} | {current_count}/{int(page_count) * 23 - len(complete_ids)}')
                    current_count += 1
                    driver.quit()

        except Exception as e:
            print(f'[INTERNAL ERROR] IN IDS SECTION')


if __name__ == '__main__':
    print('''
///////////////////////////////////////////////////////////////////
 _   _ ______ _____ _   _ _  _   __  __       _______ _____ _____ 
| \ | |  ____|_   _| \ | | || | |  \/  |   /\|__   __|_   _/ ____|
|  \| | |__    | | |  \| | || |_| \  / |  /  \  | |    | || |     
| . ` |  __|   | | | . ` |__   _| |\/| | / /\ \ | |    | || |     
| |\  | |____ _| |_| |\  |  | | | |  | |/ ____ \| |   _| || |____ 
|_| \_|______|_____|_| \_|  |_| |_|  |_/_/    \_\_|  |_____\_____|

///////////////////////////////////////////////////////////////////
    ''')
    print('''
CITY CODE:
---------------------------------------
1 -> ASTANA
2 -> ALMATY
3 -> SHYMKENT
4 -> ABAYSKAYA OBLAST
5 -> AKMOLINSKAYA OBLAST
6 -> AKTUBINSKAYA OBLAST
7 -> ALMATINSKAYA OBLAST
8 -> ATYRAUSKAYA OBLAST
9 -> VOSTOCHNO-KAZAHSTANSKAYA OBLAST
10 -> JAMBYLSKAYA OBLAST
11 -> JETISUSKAYA OBLAST
12 -> ZAPADNO-KAZAHSTANSKAYA OBLAST
13 -> KARAGANDINSKAYA OBLAST
14 -> KOSTANAISKAYA OBLAST
15 -> KYZYLORDINSKAYA OBLAST
16 -> MANGISTAUSKAYA OBLAST
17 -> PAVLODARSKAYA OBLAST
18 -> SEVERO-KAZAHSTANSKAYA OBLAST
19 -> TURKESTANSKAYA OBLAST
20 -> ULYTAUSKAYA OBLAST
---------------------------------------
    ''')

    current_city = input('ENTER CITY CODE: ')

    match current_city:
        case '1':
            current_city = 'astana'
        case '2':
            current_city = 'almaty'
        case '3':
            current_city = 'shymkent'
        case '4':
            current_city = 'abay-oblast'
        case '5':
            current_city = 'akmolinskaja-oblast'
        case '6':
            current_city = 'aktjubinskaja-oblast'
        case '7':
            current_city = 'almatinskaja-oblast'
        case '8':
            current_city = 'atyrauskaja-oblast'
        case '9':
            current_city = 'vostochno-kazahstanskaja-oblast'
        case '10':
            current_city = 'zhambylskaja-oblast'
        case '11':
            current_city = 'jetisyskaya-oblast'
        case '12':
            current_city = 'zapadno-kazahstanskaja-oblast'
        case '13':
            current_city = 'karagandinskaja-oblast'
        case '14':
            current_city = 'kostanajskaja-oblast'
        case '15':
            current_city = 'kyzylordinskaja-oblast'
        case '16':
            current_city = 'mangistauskaja-oblast'
        case '17':
            current_city = 'pavlodarskaja-oblast'
        case '18':
            current_city ='severo-kazahstanskaja-oblast'
        case '19':
            current_city = 'juzhno-kazahstanskaja-oblast'
        case '20':
            current_city = 'ulitayskay-oblast'
        case _:
            print(f'NO MATCH FOUND')
            exit()

    start_crawler(current_city)
