from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from config import russian_cities, headers
from bs4 import BeautifulSoup as BS
import csv, pymysql, requests


def get_good_apartments(url: str) -> list:

    all_good_apartments: list = []
    apartment_num: int = 0

    main_chrome_options: webdriver.ChromeOptions = webdriver.ChromeOptions()
    main_chrome_options.add_argument('--headless')

    try:

        with webdriver.Chrome(options=main_chrome_options) as main_browser:
            
            main_browser.get(url)

            main_browser.execute_script(f"scrollBy(0, {main_browser.execute_script('return document.body.scrollHeight')})")

            apartments: list[WebElement] = main_browser.find_element(By.CSS_SELECTOR, '[data-marker="catalog-serp"]').find_elements(By.CLASS_NAME, 'iva-item-sliderLink-uLz1v')
                
            for apartment in apartments:

                product_url: str = apartment.get_attribute('href')
                
                if product_url is None:
                    raise ProductUrlError('Не найдена ссылка на товар')
                
                sub_browser: requests.Response = requests.get(product_url, headers=headers.generate())
                sub_browser.encoding: str = 'utf-8'
                soup: BS = BS(sub_browser.text, 'lxml')

                all_good_apartments(dict(info.text.strip().split(': ') for info in soup.find_all('li', class_='params-paramsList__item-appQw')))

                apartment_num += 1
                print(apartment_num)

    except Exception:
        print('Была ошибка')
        pass
    
    return all_good_apartments
                    
class ProductUrlError(Exception):
    pass


class CityError(Exception):
    pass


class DelAttrError(Exception):
    pass


class Parser:
    def __init__(self, city: str) -> None:
        try:
            self._url: str = f'https://www.avito.ru/{russian_cities[city.lower()]}/kvartiry/prodam/rynochnaya_cena-ASgBAQICAUSSA8YQAUCo0hEUAg?f=ASgBAQECA0SSA8YQwMENuv036sEN_s45CEDkBzT8UZbrmQL4UcoIpIZZ_M8yilmarAGYrAGWrAGUrAGIWYJZhFnmFhTm_AGQvg0klK41kq41rL4NFKTHNdrEDRSCnzqo0hEUAuLIExQCAkWECRV7ImZyb20iOjYwLCJ0byI6bnVsbH3GmgweeyJmcm9tIjoyNTAwMDAwLCJ0byI6MTUwMDAwMDB9'
            self._good_apartments: list[list[str], list[str]] = get_good_apartments(self.url)
        except KeyError:
            raise CityError('Вы неправильно ввели город, пожалуйста повторите ещё раз')

    def __delitem__(self, _) -> None:
        raise DelAttrError('Удалять атрибуты экземпляра класса Parser нельзя')
    
    @property
    def url(self) -> str:
        return self._url
    
    @property
    def good_apartments(self) -> list[list[str], list[str]]:
        return self._good_apartments
    

if __name__ == '__main__':
    parser: Parser = Parser('Кострома')
    print(parser.good_apartments)