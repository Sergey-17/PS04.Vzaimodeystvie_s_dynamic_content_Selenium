#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый скрипт для проверки работы браузера
"""

import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.edge.service import Service as EdgeService
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.edge.options import Options as EdgeOptions
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    
    print("✓ Selenium и webdriver-manager установлены")
    
    def test_chrome():
        """Тест Chrome"""
        try:
            print("\n--- Тест Chrome ---")
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            print("✓ Chrome WebDriver создан")
            
            driver.get("https://ru.wikipedia.org/wiki/")
            print("✓ Страница загружена")
            
            title = driver.title
            print(f"✓ Заголовок страницы: {title}")
            
            driver.quit()
            print("✓ Chrome тест пройден успешно")
            return True
            
        except Exception as e:
            print(f"✗ Ошибка Chrome: {e}")
            return False
    
    def test_edge():
        """Тест Edge"""
        try:
            print("\n--- Тест Edge ---")
            edge_options = EdgeOptions()
            edge_options.add_argument("--headless")
            edge_options.add_argument("--no-sandbox")
            edge_options.add_argument("--disable-dev-shm-usage")
            
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=edge_options)
            
            print("✓ Edge WebDriver создан")
            
            driver.get("https://ru.wikipedia.org/wiki/")
            print("✓ Страница загружена")
            
            title = driver.title
            print(f"✓ Заголовок страницы: {title}")
            
            driver.quit()
            print("✓ Edge тест пройден успешно")
            return True
            
        except Exception as e:
            print(f"✗ Ошибка Edge: {e}")
            return False
    
    def main():
        print("Тестирование браузеров...")
        print("=" * 50)
        
        chrome_ok = test_chrome()
        edge_ok = test_edge()
        
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
        print(f"Chrome: {'✓ РАБОТАЕТ' if chrome_ok else '✗ НЕ РАБОТАЕТ'}")
        print(f"Edge:  {'✓ РАБОТАЕТ' if edge_ok else '✗ НЕ РАБОТАЕТ'}")
        
        if chrome_ok or edge_ok:
            print("\n✓ По крайней мере один браузер работает!")
            print("Можете запускать main1.py")
        else:
            print("\n✗ Ни один браузер не работает!")
            print("Проверьте установку браузеров и драйверов")
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"✗ Ошибка импорта: {e}")
    print("Установите зависимости: pip install -r requirements.txt")
except Exception as e:
    print(f"✗ Неожиданная ошибка: {e}")
