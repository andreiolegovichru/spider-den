from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

#chrome_options = Options()
#chrome_options.add_argument("--headless")
#driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()

firefox_options = Options()
firefox_options.headless = True
#firefox_options.headless = False

ffdriver = webdriver.Firefox(options=firefox_options)


#driver.get("https://www.heihei.ru/")

urls = driver.find_elements(By.TAG_NAME, 'a')

list_of_urls = []
list_of_checked_urls = []
urls_to_check = []
list_of_broken_urls = [("address", "broken_url")]
list_of_good_urls   = [("address", "good_url")]
counter = 0

def open_url(address):
    assert isinstance(address, object)
    driver.get(address)

def validate_url(parent_url, url_to_validate):
    url = url_to_validate
    url_tuple = (parent_url, url_to_validate)
    print(f"validate url {url} started")
    if isinstance(url, str):
        try:
            if url[0] == "h" or url[0] == "/":
                #print("h or / found")
                # Uncomment for heihei
                #if url[:21] == "https://www.heihei.ru" or url[:20] == "http://www.heihei.ru":
                if url[:30] == "https://www.andreyolegovich.ru" or url[:2] == "http://www.andreyolegovich.ru":
                    #print("valid url 1: heihei")
                    #f = open("spider_log.txt", "a")
                    #f.write(f"address: {address} good url: {url}\n")
                    #f.close()
                    return True
                elif url[:22] == "https://ad.admitad.com" or url[:21] == "http://ad.admitad.com":
                    try:
                        ffdriver.get(url)
                        h1 = ffdriver.find_element(By.TAG_NAME, 'h1')
                        new_h1 = h1.text
                        lower_h1 = new_h1.lower()
                        new_title = ffdriver.title
                        lower_title = new_title.lower()
                        #print(f"title = {new_title}")
                        #print(f"h1 = {new_h1}")
                        #print(f"lower_h1 = {lower_h1}")
                        print("valid url 2: admitad")

                        if (    lower_h1 == "unfortunately, the link that you’ve used is not valid."
                                or lower_h1 == "запрашиваемая страница не найдена"
                                or lower_h1 == "404"
                                or lower_title == "кэшбэк сервис letyshops. возвращай деньги за покупки обратно"):

                            if url_tuple not in list_of_broken_urls:
                                list_of_broken_urls.append(url_tuple)
                                f = open("./logs/spider_log.txt", "a")
                                f.write(f"broken url: {url_tuple}\n")
                                f.close()
                                print(f"broken url: {url_tuple}")

                        else:
                            #pass
                            print("admitad url is good 3")

                            #if url_tuple not in list_of_good_urls:
                                #list_of_good_urls.append(url_tuple)
                                #f = open("./logs/good_urls.txt", "a")
                                #f.write(f"good url: {url_tuple}\n")
                                #f.close()

                        return True
                    except:
                        print(f"{url} is not admitad url")
                        return False


                elif url[0] == "/":
                    print(f"Potentianlly valid url: {url}")
                    return True
                else:
                    #print(url[:21])
                    print("bad url 1")
                    return False
            else:
                #print("bad url 2")
                return False
        except:
            return False
    else:
        #print("bad url 3")
        return False

def scan_url(urls_to_check, url_to_scan, counter):

    counter = counter
    print(f"scan url {url_to_scan} started")
    assert isinstance(url_to_scan, object)

    list_of_urls.append(url_to_scan)
    list_of_checked_urls.append(url_to_scan)
    #urls_to_check.append(address)

    driver.get(url_to_scan)
    urls = driver.find_elements(By.TAG_NAME, 'a')

    f = open("./logs/list_of_urls.txt", "a")
    f.write(f"counter: {counter} url: {url_to_scan}\n")
    f.close()
    
    for u in urls:
        child_url = u.get_attribute('href')
        print(child_url)
        if validate_url(url_to_scan, child_url):
            #first parameter of validate_url(,) is a parent url. It is passed for better logging

            print(f"valid url {child_url}")
            if ((child_url != url_to_scan) and (child_url not in list_of_urls)):
                urls_to_check.append(child_url)
                list_of_urls.append(child_url)

            else:
                #pass
                print(f"url {child_url} is already in the list")
        else:
            continue

    for u in urls_to_check:
        if counter < 10000:
            counter+=1
            print("11111111111111111111111111111111111111111111111111111111111111")
            print(f"counter = {counter}")
            print("recursive scan started")
            if u not in list_of_checked_urls:
                scan_url(urls_to_check, u, counter)

        else:
            #continue_run = False
            print(f"{counter} iterations done")
            #for url in urls_to_check:
                #print(f"url: {url}")
            break


def run_script(list_of_urls, address):
    scan_url(address)
    for l in list_of_urls:
        scan(l)

if __name__=='__main__':
    scan_url(urls_to_check, "https://www.andreyolegovich.ru", 0)
    #scan_url(urls_to_check, "https://www.heihei.ru/", 0)
    #scan_url(urls_to_check, "https://www.heihei.ru/Finland/travel/SPb-Helsinki.php", 0)
    #scan_url(urls_to_check, "https://ad.admitad.com/g/wwnyjpeeiod74ba13facdafaee847b/?i=4&subid=homePage", 0)
    #scan_url(urls_to_check, "https://www.heihei.ru/Finland/life/medicine.php", 0)

    #validate_url("https://www.heihei.ru/Finland/")
    #validate_url("https://www.heihei.ru","http://ad.admitad.com/g/tierscbnmxd74ba13face6d9523204/?ulp=https%3A%2F%2Fprintio.ru%2Fstore%2Fpage-2%3Fq%3D%25D0%25B8%25D0%25B3%25D1%2580%25D0%25B0%2520%25D0%25BF%25D1%2580%25D0%25B5%25D1%2581%25D1%2582%25D0%25BE%25D0%25BB%25D0%25BE%25D0%25B2%26sort_by%3Dmoderated_date")
    #open_url("https://www.topbicycle.ru")
    #print("list of urls: ")
    #for l in list_of_urls:
        #print(l)