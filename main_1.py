from selenium import webdriver
import time
import random
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

browser = webdriver.Firefox()

browser.get("https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D0%BB%D0%BD%D1%86%D0%B5")
time.sleep(5)
assert "Солнце" in browser.title
hatnotes = []

elements = browser.find_elements(By.TAG_NAME, "div")
print(f"Всего элементов: {len(elements)}")

for element in elements:
    #time.sleep(3)
    cl = element.get_attribute("class")
    if cl == "hatnote navigation-not-searchable ts-main":
        hatnotes.append(element)

print(f"Всего hatnotes: {len(hatnotes)}")

# hatnote = random.choice(hatnotes)
count = 0
for hatnote in hatnotes:
    count += 1
    link = hatnote.find_element(By.TAG_NAME, "a").get_attribute("href")
    # browser.get(link)
    time.sleep(3)
    #print(link)
    print(f"{count} {hatnote.text}")
browser.quit()