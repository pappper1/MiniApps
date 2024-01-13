import requests
from bs4 import BeautifulSoup


class WeatherParser:
    def __init__(self):
        self.base_url = 'https://www.gismeteo.ru'
        self.cookies = {
                'ab_audience_2': '28',
                'cityIP': '3196',
                '_ym_uid': '1703764566998884122',
                '_ym_d': '1703764566',
                '_gid': 'GA1.2.1801300829.1705161793',
                '_ym_isad': '2',
                'PHPSESSID': 'afo6d4b26jh7f3poe97jbqm9r9',
                '_gat': '1',
                '_ga': 'GA1.1.222626131.1703764565',
                '_ga_JQ0KX9JMHV': 'GS1.1.1705185122.5.0.1705185122.60.0.0',
                '_ym_visorc': 'b',
            }

        self.headers = {
                'authority': 'www.gismeteo.ru',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,pl;q=0.6',
                'cache-control': 'max-age=0',
                # 'cookie': 'ab_audience_2=28; cityIP=3196; _ym_uid=1703764566998884122; _ym_d=1703764566; _gid=GA1.2.1801300829.1705161793; _ym_isad=2; _ym_visorc=b; _ga_JQ0KX9JMHV=GS1.1.1705161793.2.1.1705162523.60.0.0; _ga=GA1.1.222626131.1703764565',
                'referer': 'https://www.google.com/',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'cross-site',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }


    def get_weather(self, url: str) -> dict | None:
        response = requests.get(f"{url}", cookies=self.cookies, headers=self.headers).text
        soup = BeautifulSoup(response, 'lxml')
        temperature = soup.find('div', class_='widget-row-chart widget-row-chart-temperature row-with-caption').find('div', class_='values').find('span', class_='unit unit_temperature_c').text
        wind_speed = soup.find('div', class_='widget-items').find_all('span', class_='wind-unit unit unit_wind_m_s')[0].text
        if wind_speed and temperature:
            return {'temperature': temperature, 'wind_speed': wind_speed}
        else:
            return None


    def get_cities(self, country: str) -> list[dict] | None:
        response = requests.get(f'https://www.gismeteo.ru/search/{country}', cookies=self.cookies, headers=self.headers).text
        soup = BeautifulSoup(response, 'lxml')
        cities = soup.find('div', class_='catalog-list').find_all('div', class_='catalog-item')
        if cities:
            city_info = list()
            for city in cities:
                city_url = f"{self.base_url}{city.find('a').get('href')}"
                city_name = city.find('a').text.strip()
                city_info.append({'name': city_name, 'url': city_url})
            return city_info
        else:
            return None