from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By


chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')


with Chrome(options=chrome_options) as browser:

    browser.get('avito.ru/ufa/kvartiry/3-k._kvartira_687m_2627et._2647215927')
    
    print(type(browser.find_element(By.TAG_NAME, 'div')))