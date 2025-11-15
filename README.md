# config-uprav

Этот код реализует:

**Этап 1:**
- Парсинг аргументов командной строки
- Вывод всех параметров в формате ключ-значение
- Обработку ошибок параметров

**Этап 2:**
- Загрузку APKINDEX из репозитория Alpine Linux
- Парсинг формата APKINDEX для извлечения зависимостей
- Вывод прямых зависимостей заданного пакета

Для использования запустите:
```bash
python dependency_visualizer.py --package <имя_пакета> --repository <URL_репозитория>
Например:

bash
python dependency_visualizer.py --package busybox --repository http://dl-cdn.alpinelinux.org/alpine/v3.18/main
