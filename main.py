from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from config import russian_cities
import csv, pymysql


def get_good_apartments(url: str) -> list:

    main_chrome_options: webdriver.ChromeOptions = webdriver.ChromeOptions()
    main_chrome_options.add_argument('--headless')

    with webdriver.Chrome(options=main_chrome_options) as main_browser:
        
        main_browser.get(url)

        products: list[WebElement] = main_browser.find_element(By.CSS_SELECTOR, '[data-marker="catalog-serp"]').find_elements(By.CLASS_NAME, 'iva-item-sliderLink-uLz1v')
        page_count: int = int(main_browser.find_elements(By.CLASS_NAME, 'styles-module-text-InivV')[-1].text.strip())
        
        for _ in range(page_count):

            main_browser.execute_script(f"scrollBy(0, {main_browser.execute_script('return document.body.scrollHeight')})")
            
            for product in products:

                product_url: str = product.get_attribute('href')

                if product_url is None:
                    raise ProductUrlError('Не найдена ссылка на товар')

                subord_chrome_options: webdriver.ChromeOptions = webdriver.ChromeOptions()
                subord_chrome_options.add_argument('--headless')

                with webdriver.Chrome(options=subord_chrome_options) as sub_browser:
                    pass
                    
                    
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
        except KeyError:
            raise CityError('Вы неправильно ввели город, пожалуйста повторите ещё раз')

    def __delitem__(self, _) -> None:
        raise DelAttrError('Удалять атрибуты экземпляра класса Parser нельзя')
    
    @property
    def url(self) -> str:
        return self._url
    

if __name__ == '__main__':
    parser: Parser = Parser('уфа')