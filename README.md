# PS04. Взаимодействие с динамическим контентом Selenium

Проект для автоматизации работы с Wikipedia с использованием Selenium WebDriver.

## Установка и настройка

### 1. Создание виртуального окружения
```bash
python -m venv venv
```

### 2. Активация виртуального окружения
**Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Запуск проекта
```bash
python main.py
```

### 5. Тестирование
```bash
python test_wikipedia.py
```

## Зависимости

- `selenium==4.15.2` - для автоматизации браузера
- `webdriver-manager==4.0.1` - для автоматического управления драйверами браузера

## Требования к системе

- Python 3.8+
- Google Chrome браузер
- Windows 10/11 (протестировано)

## Структура проекта

- `main.py` - основной файл с классом WikipediaNavigator
- `test_wikipedia.py` - тестовый скрипт для демонстрации функциональности
- `requirements.txt` - список зависимостей Python
- `venv/` - виртуальное окружение Python (не включается в git)
- `.gitignore` - файл для исключения временных файлов из git

## Возможности

- Автоматический поиск статей в Wikipedia
- Навигация по страницам
- Ограничение скорости запросов
- Headless режим браузера Chrome
- Обработка ошибок и исключений
- Автоматическое управление драйверами браузера

## Решение проблем

### Ошибка "не является приложением Win32"
Это нормально для первого запуска. Система автоматически переключится на системный Chrome WebDriver.

### Chrome не найден
Убедитесь, что Google Chrome установлен в стандартной директории:
`C:\Program Files\Google\Chrome\Application\chrome.exe`
