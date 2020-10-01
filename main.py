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


driver.get("https://www.heihei.ru/")

urls = driver.find_elements(By.TAG_NAME, 'a')

list_of_urls = []
list_of_checked_urls = []
urls_to_check = []
counter = 0

def open_url(address):
    assert isinstance(address, object)
    driver.get(address)

def validate_url(address, url):
    url = url
    print(f"validate url {url} started")
    if isinstance(url, str):
        try:
            if url[0] == "h" or url[0] == "/":
                if url[:21] == "https://www.heihei.ru" or url[:20] == "http://www.heihei.ru":
                    #print("valid url 1")
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
                        print(f"title = {new_title}")
                        print(f"h1 = {new_h1}")
                        print(f"lower_h1 = {lower_h1}")

                        if lower_h1 == "unfortunately, the link that you’ve used is not valid." or lower_h1 == "запрашиваемая страница не найдена" or lower_h1 == "404":
                            f = open("spider_log.txt", "a")
                            f.write(f"address: {address} broken url: {url}\n")
                            f.close()
                            print(f"address: {address} broken url: {url}")
                        elif lower_title == "кэшбэк сервис letyshops. возвращай деньги за покупки обратно":
                            f = open("spider_log.txt", "a")
                            f.write(f"address: {address} broken url: {url}\n")
                            f.close()
                            print(f"address: {address} broken url: {url}")
                        else:
                            #f = open("spider_log.txt", "a")
                            #f.write(f"address: {address} good url: {url}\n")
                            #f.close()
                            print(f"address: {address} good url: {url}")

                        return True
                    except:
                        return True


                elif url[0] == "/":
                    #print("valid url 2")
                    return True
                else:
                    #print(url[:21])
                    #print("bad url 1")
                    return False
            else:
                #print("bad url 2")
                return False
        except:
            return False
    else:
        #print("bad url 3")
        return False

def scan_url(urls_to_check, address, counter):
    counter = counter
    print(f"scan url {address} started")
    assert isinstance(address, object)
    urls_to_check.append(address)
    driver.get(address)
    urls = driver.find_elements(By.TAG_NAME, 'a')
    
    for u in urls:
        link = u.get_attribute('href')
        if validate_url(address, link):
            #print(f"new url {link}")
            if link not in list_of_urls:
                urls_to_check.append(link)
                list_of_urls.append(link)

            else:
                print(f"url {link} is already in the list")
        else:
            continue

    for u in urls_to_check:
        if counter < 1000:
            counter+=1
            print("11111111111111111111111111111111111111111111111111111111111111")
            print(f"counter = {counter}")
            print("recursive scan started")
            scan_url(urls_to_check, u, counter)

        else:
            print(f"{counter} iterations done")
            for url in urls_to_check:
                print(f"url: {url}")
            break



def run_script(list_of_urls, address):
    scan_url(address)
    for l in list_of_urls:
        scan(l)

#for u in urls:
    #link = u.get_attribute('href')
    #print(type(link))
    #print(link)
    #
     #   if link[:20] == "https://www.heihei.ru/":
    #print(link)
    #if isinstance(link, str):
        #print(link[0])
        #if link[0] == "h":
            #print(link[0])
            #print(link[:21])
            #if link[:21] == "https://www.heihei.ru":
                #print(link[0])



    #if link not in list_of_checked_urls:
       #list_of_urls.append(link)
    #print(u.text)






if __name__=='__main__':
    scan_url(urls_to_check, "https://www.heihei.ru/", counter)
    #validate_url("https://www.heihei.ru/Finland/")
    #validate_url("https://www.heihei.ru","http://ad.admitad.com/g/tierscbnmxd74ba13face6d9523204/?ulp=https%3A%2F%2Fprintio.ru%2Fstore%2Fpage-2%3Fq%3D%25D0%25B8%25D0%25B3%25D1%2580%25D0%25B0%2520%25D0%25BF%25D1%2580%25D0%25B5%25D1%2581%25D1%2582%25D0%25BE%25D0%25BB%25D0%25BE%25D0%25B2%26sort_by%3Dmoderated_date")
    #open_url("https://www.topbicycle.ru")
    print("list of urls: ")
    for l in list_of_urls:
        print(l)