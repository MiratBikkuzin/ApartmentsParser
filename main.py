from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from config import russian_cities
import csv, pymysql


def get_good_apartments(url: str) -> list:

    all_good_apartments: list[list[str]] = [[]]
    header_limit: int = 1

    main_chrome_options: webdriver.ChromeOptions = webdriver.ChromeOptions()
    main_chrome_options.add_argument('--headless')

    with webdriver.Chrome(options=main_chrome_options) as main_browser:
        
        main_browser.get(url)

        apartments: list[WebElement] = main_browser.find_element(By.CSS_SELECTOR, '[data-marker="catalog-serp"]').find_elements(By.CLASS_NAME, 'iva-item-sliderLink-uLz1v')
        page_count: int = int(main_browser.find_elements(By.CLASS_NAME, 'styles-module-text-InivV')[-1].text.strip())
        
        for _ in range(page_count):

            main_browser.execute_script(f"scrollBy(0, {main_browser.execute_script('return document.body.scrollHeight')})")
            
            for apartment in apartments:

                current_apartment_info: list[str] = []

                product_url: str = apartment.get_attribute('href')

                if product_url is None:
                    raise ProductUrlError('Не найдена ссылка на товар')

                subord_chrome_options: webdriver.ChromeOptions = webdriver.ChromeOptions()
                subord_chrome_options.add_argument('--headless')

                with webdriver.Chrome(options=subord_chrome_options) as sub_browser:

                    sub_browser.get(product_url)

                    product_info: list[WebElement] = sub_browser.find_elements(By.CLASS_NAME, 'params-paramsList__item-appQw')

                    for info in product_info:

                        info_type, info_value = info.text.strip().split(': ')

                        if header_limit == 1:
                            all_good_apartments[0].append(info_type)

                        current_apartment_info.append(info_value)

                header_limit = 0
                all_good_apartments.append(current_apartment_info)

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
            self._good_apartments: dict[str] = get_good_apartments(self.url)
        except KeyError:
            raise CityError('Вы неправильно ввели город, пожалуйста повторите ещё раз')

    def __delitem__(self, _) -> None:
        raise DelAttrError('Удалять атрибуты экземпляра класса Parser нельзя')
    
    @property
    def url(self) -> str:
        return self._url
    
    @property
    def good_apartments(self) -> dict[str]:
        return self._good_apartments
    

if __name__ == '__main__':
    parser: Parser = Parser('Кострома')
    print(parser.good_apartments)