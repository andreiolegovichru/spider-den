from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)


driver.get("https://www.heihei.ru/")

elements = driver.find_elements(By.TAG_NAME, 'a')

for e in elements:
    print(e.text)