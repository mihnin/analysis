# Как собрать EXE файл приложения

## Пошаговая инструкция для сборки Windows приложения

---

## Шаг 1: Установка Python

1. Скачайте Python 3.12 или новее с официального сайта: https://www.python.org/downloads/

2. Запустите установщик Python

3. **ВАЖНО**: Отметьте галочку "Add Python to PATH" перед установкой!

4. Нажмите "Install Now"

5. После установки откройте командную строку (cmd) и проверьте:
   ```bash
   python --version
   ```
   Должно показать версию Python 3.12+

---

## Шаг 2: Установка зависимостей

1. Откройте командную строку (cmd) **от имени администратора**

2. Перейдите в папку проекта:
   ```bash
   cd C:\dev\analysis
   ```

3. Установите все необходимые библиотеки:
   ```bash
   pip install -r requirements_desktop.txt
   ```

   Это установит:
   - PyQt6 (UI framework)
   - pandas, numpy (обработка данных)
   - statsmodels, scipy (прогнозирование)
   - xlsxwriter, openpyxl (работа с Excel)
   - pyinstaller (создание EXE)

4. Дождитесь завершения установки (2-5 минут)

---

## Шаг 3: Тестовый запуск

Перед сборкой EXE проверьте, что приложение работает:

```bash
python desktop_app.py
```

Должно открыться окно приложения с интерфейсом Норникель Спутник.

Если есть ошибки:
- Проверьте, что все зависимости установлены
- Убедитесь, что вы находитесь в папке `C:\dev\analysis`
- Проверьте, что все файлы модулей присутствуют

---

## Шаг 4: Сборка EXE файла

### Автоматическая сборка (рекомендуется)

Просто запустите скрипт сборки:

```bash
python build_exe.py
```

Скрипт автоматически:
- Проверит наличие PyInstaller
- Соберет все модули
- Создаст единый EXE файл
- Покажет прогресс и результат

Процесс займет 3-5 минут.

### Ручная сборка (альтернатива)

Если автоматическая сборка не работает, используйте команду напрямую:

```bash
pyinstaller --name Nornickel_Inventory_Analysis --onefile --windowed --clean ^
--hidden-import pandas ^
--hidden-import numpy ^
--hidden-import PyQt6 ^
--hidden-import xlsxwriter ^
--hidden-import openpyxl ^
--hidden-import statsmodels ^
--hidden-import scipy ^
--hidden-import historical_analysis ^
--hidden-import forecast_analysis ^
--hidden-import forecasting_models ^
--hidden-import data_validation ^
--hidden-import file_validation ^
--hidden-import desktop_ui_styles ^
--hidden-import desktop_ui_components ^
--hidden-import excel_export_desktop ^
desktop_app.py
```

---

## Шаг 5: Результат

После успешной сборки EXE файл будет находиться в:

```
C:\dev\analysis\dist\Nornickel_Inventory_Analysis.exe
```

Размер файла: примерно 80-150 MB (все зависимости включены)

---

## Шаг 6: Тестирование EXE

1. Перейдите в папку `dist`:
   ```bash
   cd dist
   ```

2. Запустите EXE файл:
   ```bash
   Nornickel_Inventory_Analysis.exe
   ```

3. Проверьте все функции:
   - ✓ Загрузка исторических данных
   - ✓ Валидация файлов
   - ✓ Автоматический прогноз
   - ✓ Выполнение анализа
   - ✓ Сохранение в Excel

4. Если всё работает - готово! 🎉

---

## Шаг 7: Распространение

EXE файл полностью автономный (standalone), включает все зависимости.

**Для передачи пользователям:**

1. Скопируйте файл `Nornickel_Inventory_Analysis.exe`

2. Приложите инструкцию `БЫСТРЫЙ_СТАРТ.txt` или `DESKTOP_APP_README.md`

3. Пользователи могут запускать приложение сразу, без установки Python или библиотек!

**Рекомендации:**

- Протестируйте EXE на чистой Windows машине (без Python)
- Проверьте работу на Windows 10 и Windows 11
- Убедитесь, что антивирус не блокирует приложение

---

## Частые проблемы и решения

### Проблема: "PyInstaller not found"
**Решение:**
```bash
pip install pyinstaller
```

### Проблема: "Module not found" во время сборки
**Решение:**
Установите недостающий модуль:
```bash
pip install <название_модуля>
```

### Проблема: EXE не запускается (ошибка при запуске)
**Решение:**
1. Запустите сборку с `--debug` флагом:
   ```bash
   pyinstaller --debug=all ...
   ```
2. Проверьте логи в `build/` папке
3. Добавьте недостающие модули через `--hidden-import`

### Проблема: EXE слишком большой (>200 MB)
**Решение:**
Это нормально для приложений с научными библиотеками (pandas, statsmodels). Если нужно уменьшить размер:
1. Используйте виртуальное окружение с минимальным набором библиотек
2. Удалите неиспользуемые модули из зависимостей

### Проблема: Антивирус блокирует EXE
**Решение:**
PyInstaller-файлы иногда воспринимаются как потенциально нежелательные программы (PUP). Это ложное срабатывание.
1. Добавьте EXE в исключения антивируса
2. Подпишите EXE цифровой подписью (для корпоративного использования)

---

## Дополнительные опции сборки

### Добавить иконку приложения

1. Создайте или скачайте иконку в формате `.ico`

2. Сохраните как `icon.ico` в папке проекта

3. Добавьте в команду сборки:
   ```bash
   pyinstaller --icon=icon.ico ...
   ```

### Изменить версию и метаданные

Создайте файл `version.txt`:
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        '040904B0',
        [StringStruct('CompanyName', 'Норникель Спутник'),
        StringStruct('FileDescription', 'Анализ и прогнозирование запасов'),
        StringStruct('FileVersion', '1.0.0'),
        StringStruct('ProductName', 'Nornickel Inventory Analysis'),
        StringStruct('ProductVersion', '1.0.0')])
      ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
```

Добавьте в команду:
```bash
pyinstaller --version-file=version.txt ...
```

---

## Структура после сборки

```
C:\dev\analysis\
├── build\                        # Временные файлы сборки (можно удалить)
├── dist\                         # Готовый EXE файл
│   └── Nornickel_Inventory_Analysis.exe
├── Nornickel_Inventory_Analysis.spec  # Спецификация PyInstaller (можно переиспользовать)
├── desktop_app.py                # Исходные файлы
├── desktop_ui_*.py
├── ...
└── build_exe.py                  # Скрипт сборки
```

---

## Команды для очистки

Если нужно пересобрать с нуля:

```bash
# Удалить временные файлы сборки
rmdir /s /q build
rmdir /s /q dist
del Nornickel_Inventory_Analysis.spec

# Пересобрать
python build_exe.py
```

---

## Успешная сборка!

После выполнения всех шагов у вас будет:

✅ Готовый EXE файл `Nornickel_Inventory_Analysis.exe`
✅ Размер: 80-150 MB
✅ Работает на Windows 10/11 без установки Python
✅ Включает все зависимости
✅ Фирменный дизайн Норникель Спутник
✅ Полный функционал анализа и прогнозирования

**Готово к использованию!** 🚀

---

© 2025 Норникель Спутник. НА ОРБИТЕ ДОВЕРИЯ 🛰️
