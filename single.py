import sys
import requests

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


def main():
    run_from_new_url()
    # run_from_file()


def run_from_new_url():
    try:
        url_under_test = sys.argv[1]
        print(url_under_test)

    except:
        print("No url provided for testing")

    firefox_options = Options()
    firefox_options.headless = True
    ffdriver = webdriver.Firefox(options=firefox_options)
    driver = ffdriver
    hrefs = get_unique_ahref(driver, url_under_test)
    write_hrefs_to_file(hrefs)
    all_hrefs = read_hrefs_from_file()
    status_codes = get_response_codes(all_hrefs)
    driver.close()


def run_from_file():
    all_hrefs = read_hrefs_from_file()
    status_codes = get_response_codes(all_hrefs)


def write_hrefs_to_file(hrefs):
    with open('all_hrefs.txt', 'w') as f:
        for href in hrefs:
            f.writelines(f"{href}\n")


def read_hrefs_from_file():
    with open('all_hrefs.txt', 'r') as f:
        return f.readlines()


def get_response_codes(hrefs):
    codes = []
    for href in hrefs:
        href = href[:-1]
        try:
            # print(href)
            code = requests.get(href)
            # print(code.status_code)
            if (code.url == "https://andreyolegovich.ru/404.php"):
                print(f"ERROR: href {href} returns local 404")
                with open('local_404.log', 'w') as f:
                    f.writelines(f"ERROR: href {href} returns local 404\n")
                codes.append((href, 404))
            else:
                with open('request.log', 'w') as f:
                    f.writelines(f"INFO: href {href} returns {code.status_code}\n")
                codes.append((href, code.status_code))
        except:
            print(f"WARNING: href {href} is not reachable")
            with open('error.log', 'a') as f:
                f.writelines(f"WARNING: href {href} is not reachable\n")
            codes.append((href, 412))

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
