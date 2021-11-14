import sys
import requests

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


def main():
    try:
        url_under_test = sys.argv[1]
        print(url_under_test)

    except:
        print("No url provided for testing")

    firefox_options = Options()
    firefox_options.headless = True

    ffdriver = webdriver.Firefox(options=firefox_options)
    driver = ffdriver
    # 1
    # open_url(driver, url_under_test)
    # 2
    # read_h1(driver, url_under_test)
    # 3
    # urls = get_a(driver, url_under_test)
    # print(urls)
    # 4
    # hrefs = get_ahref(driver, url_under_test)
    # 5
    hrefs = get_unique_ahref(driver, url_under_test)
    # for href in hrefs:
    #    print(href)
    status_codes = get_response_codes(hrefs)
    # print(status_codes)

    with open('status_codes.txt', 'a') as f:
        for line in status_codes:
            f.write(str(line))
            f.write("\n")

    #driver.close()
    driver.quit()

def get_response_codes(hrefs):
    codes = []
    for href in hrefs:
        try:
            # print(href)
            code = requests.get(href)
            # print(code.status_code)
            codes.append((href, code.status_code))
        except:
            print(f"href {href} is nok")

    return codes

def open_url(driver, url):
    assert isinstance(url, object)
    driver.get(url)

def read_h1(driver, url):
    driver.get(url)
    # print(url)
    h1 = driver.find_element(By.TAG_NAME, 'h1')
    # print(h1.text)
    return h1.text

def get_a(driver, url):
    driver.get(url)
    urls = driver.find_elements(By.TAG_NAME, 'a')
    return urls


def get_ahref(driver, url):
    hrefs = []
    driver.get(url)
    urls = driver.find_elements(By.TAG_NAME, 'a')
    for u in urls:
        href = u.get_attribute('href')
        hrefs.append(href)
    return hrefs

def get_unique_ahref(driver, url):
    hrefs = []
    driver.get(url)
    urls = driver.find_elements(By.TAG_NAME, 'a')
    for u in urls:
        href = u.get_attribute('href')
        if href not in hrefs:
            assert isinstance(href, object)
            hrefs.append(href)
    return hrefs

if __name__=='__main__':
    main()