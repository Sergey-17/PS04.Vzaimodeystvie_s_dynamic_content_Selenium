from selenium import webdriver
import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

browser = webdriver.Firefox()
browser.get("https://ru.wikipedia.org/wiki/")

time.sleep(5)
assert "Википедия" in browser.title

# browser.get("https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D1%88%D0%BA%D0%B0")

time.sleep(5)

search_box = browser.find_element(By.ID, "searchInput")
search_box.send_keys("Солнечная система")
search_box.send_keys(Keys.ENTER)

time.sleep(5)

print("Найденые ссылки по запросу")
link_elements = browser.find_elements(By.LINK_TEXT, "Солнечная система")
for element in link_elements:
    print(element.text)

#a.click()

time.sleep(5)

assert "Солнечная система" in browser.title

paragrafs = browser.find_elements(By.TAG_NAME, "p")

for paragraf in paragrafs:
    print(f"Текст параграфа: {paragraf.text}")
    # input()
    time.sleep(3)

browser.quit()








