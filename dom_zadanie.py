#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Консольное приложение для работы с Википедией с использованием Selenium
Функции: поиск статей, чтение параграфов, переход по основным статьям
Автор: Создано по техническому заданию
"""

import os
import time
import random
import textwrap
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    WebDriverException
)


class WikipediaNavigator:
    """Основной класс для навигации по Википедии с возможностью перехода по основным статьям"""
    
    def __init__(self):
        """Инициализация драйвера Firefox в headless режиме"""
        try:
            # Настройка Firefox в headless режиме
            firefox_options = Options()
            firefox_options.add_argument("--headless")
            firefox_options.add_argument("--width=1920")
            firefox_options.add_argument("--height=1080")
            
            # Инициализация драйвера Firefox
            self.driver = webdriver.Firefox(options=firefox_options)
            
            # Инициализация переменных
            self.current_paragraph = 0
            self.paragraphs = []
            self.related_links = []
            self.wait = WebDriverWait(self.driver, 15)
            self.last_request_time = 0
            
            print("✓ Драйвер Firefox успешно инициализирован")
            
        except Exception as e:
            print(f"❌ Ошибка инициализации драйвера: {e}")
            raise
    
    def clear_screen(self):
        """Очистка экрана консоли"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def wait_any_key(self, prompt="Нажмите любую клавишу для продолжения..."):
        """Ожидание нажатия любой клавиши (Windows), либо Enter на других ОС"""
        try:
            import msvcrt  # Доступно на Windows
            print(prompt, end="", flush=True)
            msvcrt.getch()
            print()
        except ImportError:
            input(f"{prompt} (Enter)")
    
    def rate_limit(self, min_delay=2, max_delay=4):
        """Ограничение скорости запросов с случайными вариациями"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < min_delay:
            delay = random.uniform(min_delay, max_delay)
            print(f"⏳ Ожидание {delay:.1f} секунд...")
            time.sleep(delay)
        
        self.last_request_time = time.time()
    
    def wait_for_page_load(self):
        """Ожидание загрузки страницы"""
        try:
            # Ждем загрузки основного контента
            self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            # Дополнительная задержка для стабильности
            time.sleep(1)
            return True
        except TimeoutException:
            print("⚠️ Превышено время ожидания загрузки страницы")
            return False
    
    def format_text(self, text, width=80):
        """Форматирование текста для консоли"""
        if not text or text.strip() == "":
            return ""
        
        # Очистка текста от лишних пробелов и переносов
        text = ' '.join(text.split())
        
        # Форматирование с ограничением ширины
        formatted = textwrap.fill(text, width=width)
        return formatted
    
    def search_article(self, query):
        """Поиск статьи по запросу"""
        try:
            self.rate_limit()
            
            print(f"🔍 Поиск статьи: {query}")
            
            # Переход на главную страницу Википедии
            self.driver.get("https://ru.wikipedia.org/wiki/")
            
            # Поиск по запросу
            search_box = self.wait.until(
                EC.presence_of_element_located((By.NAME, "search"))
            )
            search_box.clear()
            search_box.send_keys(query)
            search_box.submit()
            
            # Ожидание загрузки результатов
            if not self.wait_for_page_load():
                return False
            
            # Проверка, что мы на странице статьи
            try:
                # Ищем заголовок статьи
                title = self.driver.find_element(By.ID, "firstHeading")
                if title:
                    print(f"✅ Найдена статья: {title.text}")
                    return True
            except NoSuchElementException:
                pass
            
            # Если не нашли заголовок, возможно это страница результатов поиска
            try:
                # Проверяем, есть ли результаты поиска
                search_results = self.driver.find_elements(By.CSS_SELECTOR, ".mw-search-result-heading a")
                if search_results:
                    print(f"📋 Найдено результатов поиска: {len(search_results)}")
                    # Берем первый результат
                    first_result = search_results[0]
                    print(f"🔗 Переходим к первому результату: {first_result.text}")
                    first_result.click()
                    
                    if self.wait_for_page_load():
                        title = self.driver.find_element(By.ID, "firstHeading")
                        print(f"✅ Перешли к статье: {title.text}")
                        return True
            except Exception as e:
                print(f"⚠️ Ошибка при переходе к результату поиска: {e}")
            
            print("❌ Статья не найдена")
            return False
            
        except (TimeoutException, NoSuchElementException, WebDriverException) as e:
            print(f"❌ Ошибка при поиске: {e}")
            return False
    
    def get_article_paragraphs(self):
        """Получение параграфов текущей статьи"""
        try:
            # Проверяем, что страница загружена
            if not self.wait_for_page_load():
                print("❌ Страница не загружена")
                return False
            
            # Ищем основной контент статьи
            content = self.driver.find_element(By.ID, "mw-content-text")
            
            # Получаем все параграфы
            paragraphs = content.find_elements(By.TAG_NAME, "p")
            
            # Фильтруем пустые параграфы и параграфы с навигацией
            filtered_paragraphs = []
            for p in paragraphs:
                text = p.text.strip()
                if (text and 
                    len(text) > 20 and 
                    not text.startswith("↑") and
                    not text.startswith("↑↑") and
                    "edit" not in text.lower() and
                    "source" not in text.lower()):
                    filtered_paragraphs.append(text)
            
            self.paragraphs = filtered_paragraphs
            return len(filtered_paragraphs) > 0
            
        except NoSuchElementException:
            print("❌ Не удалось найти контент статьи")
            return False
        except Exception as e:
            print(f"❌ Ошибка при получении параграфов: {e}")
            return False
    
    def get_related_links(self):
        """Получение основных статей из текущей страницы через hatnote элементы"""
        try:
            # Проверяем, что страница загружена
            if not self.wait_for_page_load():
                print("❌ Страница не загружена")
                return False
            
            # Ищем все div элементы на странице
            elements = self.driver.find_elements(By.TAG_NAME, "div")
            print(f"🔍 Найдено элементов на странице: {len(elements)}")
            
            # Фильтруем hatnote элементы (основные статьи)
            hatnotes = []
            for element in elements:
                try:
                    cl = element.get_attribute("class")
                    if cl == "hatnote navigation-not-searchable ts-main":
                        hatnotes.append(element)
                except:
                    continue
            
            print(f"📋 Найдено hatnote элементов (основных статей): {len(hatnotes)}")
            
            # Извлекаем ссылки из hatnote элементов
            related_links = []
            for hatnote in hatnotes:
                try:
                    # Ищем ссылку внутри hatnote
                    link_element = hatnote.find_element(By.TAG_NAME, "a")
                    href = link_element.get_attribute("href")
                    text = hatnote.text.strip()
                    
                    # Проверяем, что это валидная ссылка на статью
                    if (href and 
                        href.startswith("https://ru.wikipedia.org/wiki/") and
                        text and
                        len(text) > 5 and
                        not any(skip in href.lower() for skip in ["/edit", "/history", "/talk", "/special", "/user", "/file"])):
                        
                        # Очищаем текст от лишних символов
                        clean_text = text.replace('\n', ' ').strip()
                        if clean_text:
                            related_links.append({
                                'text': clean_text,
                                'url': href
                            })
                            
                except Exception as e:
                    print(f"⚠️ Ошибка при обработке hatnote: {e}")
                    continue
            
            # Убираем дубликаты
            seen = set()
            unique_links = []
            for link in related_links:
                if link['text'] not in seen:
                    seen.add(link['text'])
                    unique_links.append(link)
            
            self.related_links = unique_links  # Показываем все найденные без обрезки
            print(f"✅ Обработано основных статей: {len(self.related_links)}")
            
            return len(self.related_links) > 0
            
        except Exception as e:
            print(f"❌ Ошибка при поиске основных статей: {e}")
            return False
    
    def display_paragraphs(self):
        """Отображение параграфов с форматированием"""
        if not self.get_article_paragraphs():
            print("❌ Не удалось получить параграфы статьи")
            return
        
        if not self.paragraphs:
            print("📄 Статья не содержит параграфов для отображения")
            return
        
        self.current_paragraph = 0
        
        while True:
            self.clear_screen()
            
            if self.current_paragraph >= len(self.paragraphs):
                print("📖 Достигнут конец статьи")
                break
            
            # Получаем заголовок статьи
            try:
                title = self.driver.find_element(By.ID, "firstHeading").text
            except:
                title = "Заголовок не найден"
            
            # Отображаем текущий параграф
            print("╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"║ {title[:76]:^76} ║")
            print("╚══════════════════════════════════════════════════════════════════════════════╝")
            print()
            
            current_text = self.paragraphs[self.current_paragraph]
            formatted_text = self.format_text(current_text, 78)
            
            print(f"📄 Параграф {self.current_paragraph + 1}/{len(self.paragraphs)}:")
            print("─" * 80)
            print(formatted_text)
            print("─" * 80)
            print()
            
            # Навигация
            print("Навигация: [Enter] - следующий, [2] - назад, [3] - меню, [4] - выход")
            choice = input("Ваш выбор: ").strip()
            
            if choice == '4':
                break
            elif choice == '3':
                break
            elif choice == '2':
                if self.current_paragraph > 0:
                    self.current_paragraph -= 1
                else:
                    print("⚠️ Вы уже в начале статьи")
                    time.sleep(2)
            elif choice == '':  # Enter
                self.current_paragraph += 1
            else:  # Любой другой ввод воспринимаем как следующий
                self.current_paragraph += 1
    
    def show_related_pages(self):
        """Показ основных статей (hatnote) текущей страницы"""
        if not self.get_related_links():
            print("❌ Не удалось получить основные статьи")
            self.wait_any_key()
            return
        
        if not self.related_links:
            print("🔗 Основные статьи не найдены")
            self.wait_any_key()
            return
        
        while True:
            self.clear_screen()
            
            # Получаем заголовок текущей статьи
            try:
                current_title = self.driver.find_element(By.ID, "firstHeading").text
            except:
                current_title = "Текущая статья"
            
            # Параметры пагинации
            page_size = 15
            total = len(self.related_links)
            total_pages = max(1, (total + page_size - 1) // page_size)
            if not hasattr(self, '_related_page_index'):
                self._related_page_index = 0
            current_page = max(0, min(self._related_page_index, total_pages - 1))
            start = current_page * page_size
            end = min(start + page_size, total)
            
            print("🔗 Основные статьи:")
            print("─" * 80)
            print(f"📖 Текущая статья: {current_title}")
            print(f"Страницы: {current_page + 1}/{total_pages}  (всего: {total})")
            print("─" * 80)
            print()
            
            # Отображаем текущую страницу
            for i, link in enumerate(self.related_links[start:end], start=1):
                display_text = link['text'][:60] + "..." if len(link['text']) > 60 else link['text']
                print(f"{i:2d}. {display_text}")
            
            print("─" * 80)
            print("Введите номер статьи (1-15) на этой странице, 'д' - далее, 'н' - назад, 'м' - меню, 'в' - выход")
            
            choice = input("Ваш выбор: ").strip().lower()
            
            if choice == 'в':
                return
            elif choice == 'м':
                return
            elif choice == 'д':
                if current_page < total_pages - 1:
                    self._related_page_index = current_page + 1
                else:
                    print("⚠️ Это последняя страница")
                    time.sleep(1)
            elif choice == 'н':
                if current_page > 0:
                    self._related_page_index = current_page - 1
                else:
                    print("⚠️ Это первая страница")
                    time.sleep(1)
            elif choice.isdigit():
                num = int(choice)
                if 1 <= num <= (end - start):
                    selected_link = self.related_links[start + num - 1]
                    print(f"🔗 Переходим к статье: {selected_link['text']}")
                    try:
                        self.rate_limit()
                        self.driver.get(selected_link['url'])
                        if self.wait_for_page_load():
                            print(f"✅ Успешно перешли к статье: {selected_link['text']}")
                            # Сброс состояния для новой статьи
                            self.paragraphs = []
                            self.related_links = []
                            self.current_paragraph = 0
                            self._related_page_index = 0
                            time.sleep(1.2)
                            return
                        else:
                            print("❌ Не удалось загрузить страницу")
                    except Exception as e:
                        print(f"❌ Ошибка при переходе: {e}")
                    time.sleep(1.2)
                else:
                    print("❌ Неверный номер на текущей странице")
                    time.sleep(1)
            else:
                print("❌ Неверный ввод")
                time.sleep(1)
    
    def navigate_menu(self):
        """Основная навигация по меню"""
        # При первом запуске сразу спрашиваем, что искать
        print("🌐 Wikipedia Navigator")
        print("=" * 50)
        print("📝 Добро пожаловать! Что вы хотите найти?")
        
        # Первичный поиск
        while True:
            query = input("\nВведите поисковый запрос: ").strip()
            
            if query.lower() in ['q', 'quit', 'exit', 'выход']:
                print("👋 До свидания!")
                return
            
            if query:
                if self.search_article(query):
                    # Сбрасываем состояние для новой статьи
                    self.paragraphs = []
                    self.related_links = []
                    self.current_paragraph = 0
                    break
                else:
                    print("❌ Статья не найдена. Попробуйте другой запрос.")
                    continue
            else:
                print("❌ Запрос не может быть пустым")
                continue
        
        # Основной цикл меню
        while True:
            self.clear_screen()
            
            print("🌐 Wikipedia Navigator")
            print("=" * 50)
            
            # Показываем текущую статью
            try:
                title = self.driver.find_element(By.ID, "firstHeading").text
                print(f"📖 Текущая статья: {title}")
            except:
                print("📖 Текущая статья: Заголовок не найден")
            
            # Главное меню
            print("\n📋 Главное меню:")
            print("1. 📖 Листать параграфы текущей статьи")
            print("2. 🔗 Показать основные статьи и перейти к одной из них")
            print("3. 🔎 Поиск новой статьи")
            print("4. 🚪 Выйти из программы")
            
            choice = input("\nВыберите действие: ").strip()
            
            if choice == '1':
                self.display_paragraphs()
            elif choice == '2':
                self.show_related_pages()
            elif choice == '3':
                # Новый поиск: вернуться на главную, принять запрос, найти и перейти
                while True:
                    query = input("\nВведите новый поисковый запрос: ").strip()
                    if query.lower() in ['q', 'quit', 'exit', 'выход']:
                        break
                    if not query:
                        print("❌ Запрос не может быть пустым")
                        continue
                    if self.search_article(query):
                        # Сброс состояния для новой статьи
                        self.paragraphs = []
                        self.related_links = []
                        self.current_paragraph = 0
                        # Успешный переход к новой статье — возвращаемся в меню
                        break
                    else:
                        print("❌ Статья не найдена. Попробуйте другой запрос.")
                        continue
            elif choice == '4':
                print("👋 До свидания!")
                break
            else:
                print("❌ Неверный выбор")
                time.sleep(1)
    
    def __del__(self):
        """Закрытие браузера при завершении"""
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
                print("🔒 Браузер Firefox закрыт")
        except:
            pass


def main():
    """Главная функция"""
    print("🚀 Запуск Wikipedia Navigator...")
    
    try:
        navigator = WikipediaNavigator()
        navigator.navigate_menu()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Программа прервана пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        print("Проверьте подключение к интернету и доступность Википедии")
    finally:
        print("\n🧹 Очистка ресурсов...")
        try:
            if 'navigator' in locals():
                del navigator
        except:
            pass
        print("✅ Программа завершена")


if __name__ == "__main__":
    main()

