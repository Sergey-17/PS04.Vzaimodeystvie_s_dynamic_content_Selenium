#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый скрипт для демонстрации работы Wikipedia Navigator
"""

from main import WikipediaNavigator
import time

def test_wikipedia_search():
    """Тестирование поиска в Wikipedia"""
    try:
        print("=== Тест Wikipedia Navigator ===")
        
        # Создаем экземпляр навигатора
        navigator = WikipediaNavigator()
        
        # Тестируем поиск
        print("\nТестирование поиска статьи 'Python (programming language)'...")
        if navigator.search_article("Python (programming language)"):
            print("✓ Поиск выполнен успешно!")
            
            # Получаем заголовок страницы
            try:
                title = navigator.driver.title
                print(f"✓ Заголовок страницы: {title}")
            except Exception as e:
                print(f"✗ Ошибка при получении заголовка: {e}")
            
            # Получаем URL
            current_url = navigator.driver.current_url
            print(f"✓ Текущий URL: {current_url}")
            
        else:
            print("✗ Ошибка при поиске")
            
        # Небольшая пауза для демонстрации
        time.sleep(3)
        
        print("\n=== Тест завершен успешно! ===")
        
    except Exception as e:
        print(f"✗ Ошибка при тестировании: {e}")
    finally:
        # Закрываем браузер
        if 'navigator' in locals():
            navigator.driver.quit()
            print("✓ Браузер закрыт")

if __name__ == "__main__":
    test_wikipedia_search()
