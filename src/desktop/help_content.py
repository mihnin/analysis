"""Содержимое справочной системы для desktop приложения"""

def get_help_general():
    """Общая информация о работе с приложением"""
    return """
    <h2 style='color: #0077C8;'>📖 Добро пожаловать в систему управления запасами!</h2>

    <h3>🎯 Назначение приложения:</h3>
    <p style='font-size: 14px; line-height: 1.8;'>
    Приложение <b>"Норникель Спутник - Анализ и прогнозирование запасов"</b> предназначено для:
    </p>
    <ul style='font-size: 14px; line-height: 1.8;'>
        <li>📊 Анализа исторических данных по запасам материалов</li>
        <li>🔮 Прогнозирования будущих потребностей</li>
        <li>📦 Расчета рекомендаций по закупкам</li>
        <li>💰 Оптимизации затрат на управление запасами</li>
        <li>📈 Повышения эффективности складской логистики</li>
    </ul>

    <h3>⚡ Быстрый старт (5 шагов):</h3>
    <div style='background-color: #f0f5ff; padding: 15px; border-radius: 5px; border-left: 4px solid #0077C8;'>
        <ol style='font-size: 14px; line-height: 2;'>
            <li><b>Загрузите файл с историческими данными</b> (Excel файл с остатками материалов за 6-24 месяца)</li>
            <li><b>Выберите режим прогнозирования:</b>
                <ul>
                    <li>🤖 <b>Автоматический</b> - приложение само создаст прогноз (рекомендуется)</li>
                    <li>📄 <b>Ручной</b> - загрузите готовый файл с плановым спросом</li>
                </ul>
            </li>
            <li><b>Настройте параметры</b> (страховой запас, время поставки и т.д.) или оставьте по умолчанию</li>
            <li><b>Нажмите "▶ Выполнить анализ"</b> и дождитесь завершения (обычно 2-5 секунд)</li>
            <li><b>Сохраните результаты</b> - получите Excel файл, 2 markdown файла с пояснениями и лог выполнения</li>
        </ol>
    </div>

    <h3>📤 Что вы получите:</h3>
    <table style='width: 100%; border-collapse: collapse; margin: 15px 0;'>
        <tr style='background-color: #004C97; color: white;'>
            <th style='padding: 10px; border: 1px solid #ddd;'>Файл</th>
            <th style='padding: 10px; border: 1px solid #ddd;'>Содержание</th>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>📊 Excel файл</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>
                • Таблица исторического анализа (18 метрик)<br>
                • Таблица прогнозов и рекомендаций по закупкам
            </td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>📄 Markdown файлы (2 шт)</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>
                • Подробные пояснения расчетов исторических метрик<br>
                • Подробные пояснения расчетов прогноза
            </td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>📋 Лог файл</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>
                • Детальная информация о ходе выполнения анализа<br>
                • Обнаруженные колонки, параметры, результаты
            </td>
        </tr>
    </table>

    <h3>💡 Рекомендации:</h3>
    <ul style='font-size: 14px; line-height: 1.8;'>
        <li>Для точного прогноза используйте <b>минимум 12 месяцев</b> исторических данных</li>
        <li>Убедитесь, что в данных есть колонка <b>"Потребление"</b> для более точных расчетов</li>
        <li>При первом запуске используйте <b>автоматический режим</b> с моделью <b>AUTO</b></li>
        <li>Изучите пояснения в markdown файлах для понимания всех расчетов</li>
        <li>Проверьте лог-файл если возникли проблемы</li>
    </ul>

    <h3>📞 Поддержка:</h3>
    <p style='font-size: 14px; line-height: 1.8;'>
    Если у вас возникли вопросы или проблемы, обратитесь к другим вкладкам справки:<br>
    • <b>Структура данных</b> - как должен быть оформлен Excel файл<br>
    • <b>Интерфейс</b> - описание всех кнопок и полей<br>
    • <b>Модели</b> - как работают модели прогнозирования<br>
    • <b>Параметры</b> - что означают настройки анализа
    </p>
    """

def get_help_data_structure():
    """Структура входных данных"""
    return """
    <h2 style='color: #0077C8;'>📊 Структура данных</h2>

    <h3>📋 ИСТОРИЧЕСКИЕ ДАННЫЕ (обязательный файл)</h3>

    <h4 style='color: #004C97;'>✅ Обязательные колонки:</h4>
    <table style='width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 13px;'>
        <tr style='background-color: #004C97; color: white;'>
            <th style='padding: 8px; border: 1px solid #ddd;'>Колонка</th>
            <th style='padding: 8px; border: 1px solid #ddd;'>Варианты названий</th>
            <th style='padding: 8px; border: 1px solid #ddd;'>Формат</th>
            <th style='padding: 8px; border: 1px solid #ddd;'>Пример</th>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Дата</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Дата, Date, Период, Month, Месяц</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Дата (Excel)</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>2024-01-01</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Материал</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Материал, Material, Товар, Артикул, SKU</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Текст</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Цемент М500</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Начальный остаток</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Начальный остаток, Start Balance</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Число</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>485.0</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Конечный остаток</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Конечный остаток, End Balance</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Число</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>520.5</td>
        </tr>
    </table>

    <h4 style='color: #0077C8;'>⭐ Рекомендуемые колонки:</h4>
    <table style='width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 13px;'>
        <tr style='background-color: #0077C8; color: white;'>
            <th style='padding: 8px; border: 1px solid #ddd;'>Колонка</th>
            <th style='padding: 8px; border: 1px solid #ddd;'>Варианты названий</th>
            <th style='padding: 8px; border: 1px solid #ddd;'>Зачем нужна</th>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Филиал</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Филиал, Branch, Склад, Warehouse</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Анализ по подразделениям</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Потребление</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Потребление, Consumption, Расход</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Точный расчет метрик и прогноза</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Стоимость</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Стоимость, Cost, Цена</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Расчет упущенной выгоды</td>
        </tr>
    </table>

    <h4 style='color: #FF9800;'>⚠️ Важные требования:</h4>
    <ul style='font-size: 14px; line-height: 1.8;'>
        <li>Формат файла: <b>.xlsx</b> или <b>.xls</b> (НЕ .csv!)</li>
        <li>Даты должны быть в <b>формате даты Excel</b> (не текст "01.01.2024", а настоящая дата)</li>
        <li>Числа должны быть в <b>числовом формате</b> (не текст "100", а число 100)</li>
        <li>Минимум данных: <b>6-12 месяцев истории</b></li>
        <li>Рекомендуется: <b>12-36 месяцев</b> для точного прогноза и выявления сезонности</li>
        <li>Одна строка = один материал за один период</li>
    </ul>

    <h3>📈 ПРОГНОЗНЫЕ ДАННЫЕ (опционально, для ручного режима)</h3>

    <p style='font-size: 14px;'>Если вы НЕ используете автоматический прогноз, подготовьте файл с плановым спросом:</p>

    <table style='width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 13px;'>
        <tr style='background-color: #004C97; color: white;'>
            <th style='padding: 8px; border: 1px solid #ddd;'>Колонка</th>
            <th style='padding: 8px; border: 1px solid #ddd;'>Варианты названий</th>
            <th style='padding: 8px; border: 1px solid #ddd;'>Формат</th>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Дата</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Дата, Date, Период</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Дата</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Материал</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Материал, Material</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Текст</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Филиал</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Филиал, Branch</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Текст (если есть)</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Плановый спрос</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Плановый спрос, Demand, Forecast, План</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Число</td>
        </tr>
    </table>

    <h3>✨ Автоматическое определение колонок</h3>
    <p style='font-size: 14px; line-height: 1.8;'>
    <b>Вам НЕ нужно переименовывать колонки!</b> Приложение автоматически определит их по ключевым словам
    (поддерживаются русские и английские названия). Просто загружайте ваши файлы как есть.
    </p>
    """

def get_help_interface():
    """Описание элементов интерфейса"""
    return """
    <h2 style='color: #0077C8;'>🖥️ Элементы интерфейса</h2>

    <h3>1️⃣ БЛОК "Исторические данные"</h3>
    <div style='background-color: #f0f5ff; padding: 15px; margin: 10px 0; border-left: 4px solid #0077C8;'>
        <p><b>📁 Кнопка "Выбрать файл"</b></p>
        <ul>
            <li><b>Назначение:</b> Загрузка Excel файла с историческими данными по запасам</li>
            <li><b>Формат:</b> .xlsx или .xls</li>
            <li><b>Что делает:</b> Открывает диалог выбора файла, автоматически определяет колонки</li>
            <li><b>Подсказка:</b> Выбирайте файл с минимум 6-12 месяцами истории</li>
        </ul>
    </div>

    <h3>2️⃣ БЛОК "Прогнозирование"</h3>
    <div style='background-color: #f0fff0; padding: 15px; margin: 10px 0; border-left: 4px solid #00C853;'>

        <p><b>🔘 Радиокнопка "Загрузить файл с прогнозом"</b></p>
        <ul>
            <li><b>Назначение:</b> Ручной режим - вы загружаете готовый файл с плановым спросом</li>
            <li><b>Когда использовать:</b> Если у вас уже есть план закупок от отдела снабжения</li>
        </ul>

        <p><b>📁 Кнопка "Выбрать файл прогноза"</b></p>
        <ul>
            <li><b>Назначение:</b> Загрузка Excel файла с плановым спросом</li>
            <li><b>Активна только:</b> Если выбран ручной режим</li>
        </ul>

        <p><b>🔘 Радиокнопка "Автоматический прогноз"</b></p>
        <ul>
            <li><b>Назначение:</b> Приложение само создаст прогноз на основе истории</li>
            <li><b>Когда использовать:</b> Рекомендуется для первого запуска и когда нет готового плана</li>
            <li><b>Преимущества:</b> Использует 5 профессиональных моделей прогнозирования</li>
        </ul>

        <p><b>🔢 Поле "Количество периодов"</b></p>
        <ul>
            <li><b>Назначение:</b> Сколько месяцев вперед прогнозировать</li>
            <li><b>Диапазон:</b> 1-24 месяца</li>
            <li><b>По умолчанию:</b> 12 месяцев</li>
            <li><b>Рекомендация:</b> 3-6 месяцев для краткосрочного планирования, 12 месяцев для годового</li>
        </ul>

        <p><b>📊 Выпадающий список "Модель прогнозирования"</b></p>
        <ul>
            <li><b>Назначение:</b> Выбор алгоритма для создания прогноза</li>
            <li><b>Варианты:</b>
                <ul>
                    <li><b>AUTO</b> - автоматически выбирает лучшую модель (рекомендуется)</li>
                    <li><b>NAIVE</b> - простой прогноз (последнее значение)</li>
                    <li><b>Moving Average</b> - скользящее среднее</li>
                    <li><b>Exponential Smoothing</b> - экспоненциальное сглаживание</li>
                    <li><b>Holt-Winters</b> - учитывает тренд и сезонность</li>
                    <li><b>SARIMA</b> - продвинутая модель для сложных паттернов</li>
                </ul>
            </li>
            <li><b>Подсказка:</b> Оставьте AUTO, если не знаете что выбрать</li>
        </ul>
    </div>

    <h3>3️⃣ БЛОК "Параметры анализа"</h3>
    <div style='background-color: #fffef0; padding: 15px; margin: 10px 0; border-left: 4px solid #FF9800;'>

        <p><b>📊 Ползунок "Процент страхового запаса"</b></p>
        <ul>
            <li><b>Назначение:</b> Размер буферного запаса для защиты от дефицита</li>
            <li><b>Диапазон:</b> 0-100%</li>
            <li><b>По умолчанию:</b> 20%</li>
            <li><b>Как работает:</b> Страховой запас = Плановая потребность × %</li>
            <li><b>Рекомендации:</b>
                <ul>
                    <li>10-15% для стабильного спроса (XYZ класс X)</li>
                    <li>20-30% для умеренных колебаний (класс Y)</li>
                    <li>30-50% для непредсказуемого спроса (класс Z)</li>
                </ul>
            </li>
        </ul>

        <p><b>💰 Ползунок "Процентная ставка (opportunity cost)"</b></p>
        <ul>
            <li><b>Назначение:</b> Ставка для расчета упущенной выгоды от замороженного капитала</li>
            <li><b>Диапазон:</b> 0.00-20.00%</li>
            <li><b>По умолчанию:</b> 5.00%</li>
            <li><b>Как работает:</b> Упущенная выгода = Излишки × Цена × Ставка</li>
            <li><b>Что использовать:</b> Ключевую ставку ЦБ или доходность альтернативных инвестиций</li>
        </ul>

        <p><b>⏱️ Поле "Время поставки (lead time)"</b></p>
        <ul>
            <li><b>Назначение:</b> Сколько дней требуется от заказа до получения материала</li>
            <li><b>Диапазон:</b> 1-365 дней</li>
            <li><b>По умолчанию:</b> 30 дней</li>
            <li><b>Как работает:</b> Используется для расчета точки заказа (ROP)</li>
            <li><b>Подсказка:</b> Уточните у поставщиков реальное время поставки</li>
        </ul>

        <p><b>☑️ Чекбокс "Вести лог выполнения"</b></p>
        <ul>
            <li><b>Назначение:</b> Управление логированием процесса анализа</li>
            <li><b>Включено:</b> Записывается подробный лог (удаляется при каждом запуске)</li>
            <li><b>Выключено:</b> Логирование отключено (полезно для экономии места)</li>
            <li><b>По умолчанию:</b> Включено</li>
            <li><b>Рекомендация:</b> Оставьте включенным для диагностики проблем</li>
        </ul>
    </div>

    <h3>4️⃣ КНОПКИ УПРАВЛЕНИЯ</h3>
    <div style='background-color: #f0f0f0; padding: 15px; margin: 10px 0; border-left: 4px solid #626262;'>

        <p><b>▶ Кнопка "Выполнить анализ"</b></p>
        <ul>
            <li><b>Назначение:</b> Запуск анализа исторических данных и создание прогноза</li>
            <li><b>Когда активна:</b> После загрузки исторических данных</li>
            <li><b>Что происходит:</b> Анализ (2-5 сек) → показ результатов → предложение сохранить</li>
        </ul>

        <p><b>💾 Кнопка "Сохранить в Excel"</b></p>
        <ul>
            <li><b>Назначение:</b> Экспорт результатов в файлы</li>
            <li><b>Когда активна:</b> После успешного выполнения анализа</li>
            <li><b>Что создается:</b>
                <ul>
                    <li>📊 Excel файл с таблицами</li>
                    <li>📄 2 markdown файла с пояснениями</li>
                    <li>📋 Лог-файл выполнения (если включено логирование)</li>
                </ul>
            </li>
        </ul>

        <p><b>❓ Кнопка "Справка"</b></p>
        <ul>
            <li><b>Назначение:</b> Открытие этого окна справки</li>
            <li><b>Содержание:</b> 5 вкладок с подробной информацией</li>
        </ul>
    </div>

    <h3>5️⃣ ОБЛАСТЬ РЕЗУЛЬТАТОВ</h3>
    <div style='background-color: #e6f7e6; padding: 15px; margin: 10px 0; border-left: 4px solid #00C853;'>
        <p><b>📊 Панель результатов</b></p>
        <ul>
            <li><b>Назначение:</b> Отображение краткой сводки после анализа</li>
            <li><b>Что показывается:</b>
                <ul>
                    <li>Количество проанализированных материалов</li>
                    <li>Количество филиалов</li>
                    <li>Количество сгенерированных прогнозов</li>
                    <li>Объем рекомендуемых закупок</li>
                    <li>Информация о создаваемых файлах</li>
                </ul>
            </li>
            <li><b>Подсказка:</b> Прокручивайте вниз для просмотра всей информации</li>
        </ul>
    </div>
    """

def get_help_models():
    """Описание моделей прогнозирования"""
    return """
    <h2 style='color: #0077C8;'>🤖 Модели прогнозирования</h2>

    <p style='font-size: 14px; line-height: 1.8;'>
    Приложение поддерживает 5 профессиональных моделей прогнозирования временных рядов.
    Каждая модель имеет свои преимущества и лучше всего подходит для определенных типов данных.
    </p>

    <h3>🏆 AUTO (Автоматический выбор) - РЕКОМЕНДУЕТСЯ</h3>
    <div style='background-color: #e8f5e9; padding: 15px; margin: 10px 0; border-left: 4px solid #4CAF50;'>
        <p><b>Как работает:</b></p>
        <ul style='line-height: 1.8;'>
            <li>Тестирует все 5 моделей на ваших данных</li>
            <li>Сравнивает точность по метрике MAPE (средняя абсолютная процентная ошибка)</li>
            <li>Автоматически выбирает модель с наименьшей ошибкой</li>
        </ul>

        <p><b>Преимущества:</b></p>
        <ul style='line-height: 1.8;'>
            <li>✅ Не требует знаний о моделях</li>
            <li>✅ Всегда дает лучший результат</li>
            <li>✅ Адаптируется к особенностям ваших данных</li>
        </ul>

        <p><b>Когда использовать:</b> Всегда, если вы не эксперт в прогнозировании</p>
    </div>

    <h3>1️⃣ NAIVE (Наивный прогноз)</h3>
    <div style='background-color: #f5f5f5; padding: 15px; margin: 10px 0; border-left: 4px solid #9E9E9E;'>
        <p><b>Принцип работы:</b></p>
        <p style='font-family: monospace; background-color: #fff; padding: 10px; border-radius: 5px;'>
        Прогноз = Последнее наблюдаемое значение
        </p>

        <p><b>Пример:</b></p>
        <ul style='line-height: 1.8;'>
            <li>Потребление в декабре 2024: 150 ед</li>
            <li>Прогноз на январь 2025: 150 ед</li>
            <li>Прогноз на февраль 2025: 150 ед (тоже)</li>
        </ul>

        <p><b>Когда использовать:</b></p>
        <ul style='line-height: 1.8;'>
            <li>Очень стабильный спрос без тренда</li>
            <li>Когда нужна базовая линия для сравнения</li>
            <li>Быстрый прогноз для экспериментов</li>
        </ul>

        <p style='color: #FF5722;'><b>⚠️ Недостатки:</b> Не учитывает тренды и сезонность</p>
    </div>

    <h3>2️⃣ Moving Average (Скользящее среднее)</h3>
    <div style='background-color: #e3f2fd; padding: 15px; margin: 10px 0; border-left: 4px solid #2196F3;'>
        <p><b>Принцип работы:</b></p>
        <p style='font-family: monospace; background-color: #fff; padding: 10px; border-radius: 5px;'>
        Прогноз = Среднее(последние N периодов)<br>
        Обычно N = 3 месяца
        </p>

        <p><b>Пример:</b></p>
        <ul style='line-height: 1.8;'>
            <li>Октябрь 2024: 140 ед</li>
            <li>Ноябрь 2024: 150 ед</li>
            <li>Декабрь 2024: 160 ед</li>
            <li>Прогноз на январь 2025: (140+150+160)/3 = 150 ед</li>
        </ul>

        <p><b>Когда использовать:</b></p>
        <ul style='line-height: 1.8;'>
            <li>Сглаживание случайных колебаний</li>
            <li>Стабильный спрос с небольшим шумом</li>
            <li>Когда нужна простая и понятная модель</li>
        </ul>

        <p><b>✅ Преимущества:</b> Сглаживает выбросы, простая интерпретация</p>
        <p style='color: #FF5722;'><b>⚠️ Недостатки:</b> Запаздывает при изменении тренда</p>
    </div>

    <h3>3️⃣ Exponential Smoothing (Экспоненциальное сглаживание)</h3>
    <div style='background-color: #fff3e0; padding: 15px; margin: 10px 0; border-left: 4px solid #FF9800;'>
        <p><b>Принцип работы:</b></p>
        <p style='font-family: monospace; background-color: #fff; padding: 10px; border-radius: 5px;'>
        Прогноз = α × (последнее значение) + (1-α) × (предыдущий прогноз)<br>
        где α = 0.3 (вес свежих данных)
        </p>

        <p><b>Особенности:</b></p>
        <ul style='line-height: 1.8;'>
            <li>Больший вес на свежих данных</li>
            <li>Плавно адаптируется к изменениям</li>
            <li>Хорошо работает для краткосрочного прогноза</li>
        </ul>

        <p><b>Когда использовать:</b></p>
        <ul style='line-height: 1.8;'>
            <li>Постепенно меняющийся спрос</li>
            <li>Нужна быстрая реакция на недавние изменения</li>
            <li>Отсутствует выраженная сезонность</li>
        </ul>

        <p><b>✅ Преимущества:</b> Адаптивность, малая задержка реакции</p>
    </div>

    <h3>4️⃣ Holt-Winters (Тройное экспоненциальное сглаживание)</h3>
    <div style='background-color: #f3e5f5; padding: 15px; margin: 10px 0; border-left: 4px solid #9C27B0;'>
        <p><b>Принцип работы:</b></p>
        <p style='font-family: monospace; background-color: #fff; padding: 10px; border-radius: 5px;'>
        Учитывает три компоненты:<br>
        1. Level (базовый уровень)<br>
        2. Trend (тренд роста/снижения)<br>
        3. Seasonality (сезонные колебания)
        </p>

        <p><b>Пример применения:</b></p>
        <ul style='line-height: 1.8;'>
            <li>Стройматериалы: летом спрос выше, зимой ниже</li>
            <li>Цемент: растущий тренд + сезонность</li>
            <li>Модель учтет и рост, и летний пик</li>
        </ul>

        <p><b>Когда использовать:</b></p>
        <ul style='line-height: 1.8;'>
            <li>Есть выраженная сезонность (зима/лето, кварталы)</li>
            <li>Спрос растет или падает (тренд)</li>
            <li>Минимум 2 полных сезонных цикла в данных (24 месяца)</li>
        </ul>

        <p><b>✅ Преимущества:</b> Учитывает сезонность и тренды одновременно</p>
        <p style='color: #FF5722;'><b>⚠️ Требования:</b> Минимум 24 месяца данных</p>
    </div>

    <h3>5️⃣ SARIMA (Seasonal AutoRegressive Integrated Moving Average)</h3>
    <div style='background-color: #e0f2f1; padding: 15px; margin: 10px 0; border-left: 4px solid #009688;'>
        <p><b>Принцип работы:</b></p>
        <p style='font-family: monospace; background-color: #fff; padding: 10px; border-radius: 5px;'>
        Продвинутая статистическая модель:<br>
        • AR (AutoRegressive) - зависимость от прошлых значений<br>
        • I (Integrated) - учет нестационарности<br>
        • MA (Moving Average) - зависимость от прошлых ошибок<br>
        • S (Seasonal) - сезонные компоненты
        </p>

        <p><b>Особенности:</b></p>
        <ul style='line-height: 1.8;'>
            <li>Самая сложная и точная модель</li>
            <li>Автоматически находит оптимальные параметры</li>
            <li>Может моделировать сложные паттерны</li>
        </ul>

        <p><b>Когда использовать:</b></p>
        <ul style='line-height: 1.8;'>
            <li>Сложные паттерны спроса</li>
            <li>Комбинация трендов, циклов и сезонности</li>
            <li>Когда другие модели дают плохой результат</li>
            <li>Есть достаточно данных (36+ месяцев)</li>
        </ul>

        <p><b>✅ Преимущества:</b> Максимальная точность для сложных данных</p>
        <p style='color: #FF5722;'><b>⚠️ Недостатки:</b> Медленная, требует много данных</p>
    </div>

    <h3>📊 Сравнительная таблица моделей</h3>
    <table style='width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 13px;'>
        <tr style='background-color: #004C97; color: white;'>
            <th style='padding: 8px; border: 1px solid #ddd;'>Модель</th>
            <th style='padding: 8px; border: 1px solid #ddd;'>Скорость</th>
            <th style='padding: 8px; border: 1px solid #ddd;'>Точность</th>
            <th style='padding: 8px; border: 1px solid #ddd;'>Мин. данных</th>
            <th style='padding: 8px; border: 1px solid #ddd;'>Сезонность</th>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>AUTO</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Средняя</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>⭐⭐⭐⭐⭐</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>6 мес</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>✅</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'>NAIVE</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>⚡ Мгновенно</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>⭐⭐</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>1 мес</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>❌</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'>Moving Average</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>⚡ Быстро</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>⭐⭐⭐</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>3 мес</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>❌</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'>Exp. Smoothing</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>⚡ Быстро</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>⭐⭐⭐</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>6 мес</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>⚠️</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'>Holt-Winters</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Средняя</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>⭐⭐⭐⭐</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>24 мес</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>✅</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'>SARIMA</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Медленная</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>⭐⭐⭐⭐⭐</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>36 мес</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>✅</td>
        </tr>
    </table>

    <h3>💡 Рекомендации по выбору:</h3>
    <ul style='font-size: 14px; line-height: 1.8;'>
        <li>🥇 <b>Первый запуск:</b> Используйте AUTO</li>
        <li>📈 <b>Есть рост/падение:</b> AUTO выберет Holt-Winters или SARIMA</li>
        <li>🔄 <b>Сезонные товары:</b> AUTO выберет Holt-Winters или SARIMA</li>
        <li>⚡ <b>Нужна скорость:</b> Moving Average</li>
        <li>🎯 <b>Максимальная точность:</b> AUTO (тестирует все модели)</li>
    </ul>
    """

def get_help_parameters():
    """Описание параметров анализа"""
    return """
    <h2 style='color: #0077C8;'>⚙️ Параметры анализа</h2>

    <h3>1️⃣ Процент страхового запаса (Safety Stock)</h3>
    <div style='background-color: #f0f5ff; padding: 15px; margin: 10px 0; border-left: 4px solid #0077C8;'>
        <p><b>Что это такое:</b></p>
        <p style='line-height: 1.8;'>
        Страховой запас - это дополнительный буфер материала для защиты от непредвиденных ситуаций:
        </p>
        <ul style='line-height: 1.8;'>
            <li>Внезапный рост спроса</li>
            <li>Задержка поставки</li>
            <li>Брак материала</li>
            <li>Сбои в логистике</li>
        </ul>

        <p><b>Как рассчитывается:</b></p>
        <p style='font-family: monospace; background-color: #fff; padding: 10px; border-radius: 5px;'>
        Страховой запас = Плановая потребность × Процент / 100
        </p>

        <p><b>Пример:</b></p>
        <ul style='line-height: 1.8;'>
            <li>Плановая потребность: 100 ед/мес</li>
            <li>Процент страхового запаса: 20%</li>
            <li>Страховой запас: 100 × 0.20 = 20 ед</li>
        </ul>

        <p><b>Как выбрать процент:</b></p>
        <table style='width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 13px;'>
            <tr style='background-color: #004C97; color: white;'>
                <th style='padding: 8px; border: 1px solid #ddd;'>Ситуация</th>
                <th style='padding: 8px; border: 1px solid #ddd;'>Рекомендуемый %</th>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'>Стабильный спрос (XYZ класс X)</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>10-15%</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'>Умеренные колебания (класс Y)</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>20-30%</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'>Непредсказуемый спрос (класс Z)</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>30-50%</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'>Критичный материал (ABC класс A)</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>+10% к базовому</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'>Ненадежный поставщик</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>+15% к базовому</td>
            </tr>
        </table>

        <p><b>⚠️ Баланс:</b></p>
        <ul style='line-height: 1.8;'>
            <li>Слишком малый → риск дефицита и остановки производства</li>
            <li>Слишком большой → замороженные деньги, затраты на хранение</li>
        </ul>
    </div>

    <h3>2️⃣ Процентная ставка (Opportunity Cost)</h3>
    <div style='background-color: #fff3e0; padding: 15px; margin: 10px 0; border-left: 4px solid #FF9800;'>
        <p><b>Что это такое:</b></p>
        <p style='line-height: 1.8;'>
        Это стоимость упущенной выгоды - сколько денег вы могли бы заработать, если бы не держали излишки запасов,
        а инвестировали эти средства (например, в банк под проценты или в другие проекты).
        </p>

        <p><b>Как рассчитывается упущенная выгода:</b></p>
        <p style='font-family: monospace; background-color: #fff; padding: 10px; border-radius: 5px;'>
        Упущенная выгода = Излишки × Цена единицы × Ставка / 100<br>
        <br>
        где Излишки = max(0, Конечный остаток - 2 × Среднее потребление)
        </p>

        <p><b>Пример:</b></p>
        <ul style='line-height: 1.8;'>
            <li>Конечный остаток: 1000 ед</li>
            <li>Среднее потребление: 200 ед/мес</li>
            <li>Норматив (2× среднее): 400 ед</li>
            <li>Излишки: 1000 - 400 = 600 ед</li>
            <li>Цена единицы: 1000 руб</li>
            <li>Ставка: 5%</li>
            <li>Упущенная выгода = 600 × 1000 × 0.05 = 30,000 руб/год</li>
        </ul>

        <p><b>Какую ставку использовать:</b></p>
        <table style='width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 13px;'>
            <tr style='background-color: #FF9800; color: white;'>
                <th style='padding: 8px; border: 1px solid #ddd;'>Вариант</th>
                <th style='padding: 8px; border: 1px solid #ddd;'>Ставка</th>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'>Ключевая ставка ЦБ РФ (2025)</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>~21%</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'>Депозит в банке</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>5-15%</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'>Инвестиции в бизнес</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>10-30%</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'>Консервативная оценка</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>5% (по умолчанию)</td>
            </tr>
        </table>

        <p><b>💡 Применение:</b></p>
        <p>Этот показатель помогает принять решение:</p>
        <ul style='line-height: 1.8;'>
            <li>Сократить излишки и инвестировать деньги</li>
            <li>Провести акцию/распродажу для быстрой реализации</li>
            <li>Оптимизировать закупки в будущем</li>
        </ul>
    </div>

    <h3>3️⃣ Время поставки / Lead Time</h3>
    <div style='background-color: #f0fff0; padding: 15px; margin: 10px 0; border-left: 4px solid #00C853;'>
        <p><b>Что это такое:</b></p>
        <p style='line-height: 1.8;'>
        Время поставки (Lead Time) - это количество дней от момента размещения заказа у поставщика
        до получения материала на склад.
        </p>

        <p><b>Где используется:</b></p>
        <p style='font-family: monospace; background-color: #fff; padding: 10px; border-radius: 5px;'>
        ROP (Reorder Point) = Среднее потребление × Lead Time + Страховой запас
        </p>

        <p><b>Что такое ROP (Точка заказа):</b></p>
        <p style='line-height: 1.8;'>
        Это уровень запаса, при котором нужно разместить заказ. Если запас падает ниже ROP - пора заказывать!
        </p>

        <p><b>Пример:</b></p>
        <ul style='line-height: 1.8;'>
            <li>Среднее потребление: 10 ед/день</li>
            <li>Время поставки: 30 дней</li>
            <li>Страховой запас: 50 ед</li>
            <li>ROP = 10 × 30 + 50 = 350 ед</li>
            <li><b>Вывод:</b> Когда на складе останется 350 ед - размещайте заказ!</li>
        </ul>

        <p><b>Как определить Lead Time:</b></p>
        <ol style='line-height: 1.8;'>
            <li>Узнайте у поставщика сроки поставки</li>
            <li>Добавьте время на оформление документов (1-3 дня)</li>
            <li>Добавьте время на доставку и приемку (1-2 дня)</li>
            <li>Учтите возможные задержки (+10-20%)</li>
        </ol>

        <p><b>Типичные значения:</b></p>
        <table style='width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 13px;'>
            <tr style='background-color: #00C853; color: white;'>
                <th style='padding: 8px; border: 1px solid #ddd;'>Тип поставки</th>
                <th style='padding: 8px; border: 1px solid #ddd;'>Lead Time</th>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'>Местный поставщик (тот же город)</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>3-7 дней</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'>Региональный поставщик</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>7-14 дней</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'>Поставка из другого региона РФ</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>14-30 дней</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'>Импорт из-за рубежа</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>30-90 дней</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'>Производство на заказ</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>30-180 дней</td>
            </tr>
        </table>
    </div>

    <h3>4️⃣ Вести лог выполнения</h3>
    <div style='background-color: #f5f5f5; padding: 15px; margin: 10px 0; border-left: 4px solid #626262;'>
        <p><b>Что это такое:</b></p>
        <p style='line-height: 1.8;'>
        Чекбокс для управления записью детального лога работы приложения.
        </p>

        <p><b>Включено (по умолчанию):</b></p>
        <ul style='line-height: 1.8;'>
            <li>✅ Записывается подробный лог каждого запуска</li>
            <li>✅ При каждом новом запуске старый лог удаляется</li>
            <li>✅ Лог сохраняется вместе с результатами анализа</li>
            <li>✅ Лог-файл: <code>Анализ_запасов_..._Лог_выполнения.log</code></li>
        </ul>

        <p><b>Выключено:</b></p>
        <ul style='line-height: 1.8;'>
            <li>❌ Логирование полностью отключено</li>
            <li>❌ Лог-файл не создается</li>
            <li>✅ Немного быстрее работает (экономия ~0.1 сек)</li>
        </ul>

        <p><b>Что записывается в лог:</b></p>
        <ul style='line-height: 1.8;'>
            <li>Время запуска приложения</li>
            <li>Импорт модулей</li>
            <li>Загрузка файлов</li>
            <li>Автоматически определенные колонки</li>
            <li>Параметры анализа</li>
            <li>Ход выполнения каждого шага</li>
            <li>Результаты расчетов (размеры таблиц, количество записей)</li>
            <li>Ошибки (если возникли)</li>
        </ul>

        <p><b>💡 Рекомендация:</b></p>
        <p style='line-height: 1.8;'>
        <b>Оставьте включенным</b>, особенно если вы используете приложение впервые.
        Лог поможет диагностировать проблемы, если что-то пойдет не так.
        </p>

        <p><b>🔍 Где найти лог:</b></p>
        <ul style='line-height: 1.8;'>
            <li>После сохранения результатов - в той же папке что и Excel</li>
            <li>Во время работы: <code>C:\\Users\\&lt;Пользователь&gt;\\Nornickel_Inventory_Analysis.log</code></li>
        </ul>
    </div>

    <h3>💡 Резюме рекомендаций</h3>
    <table style='width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 13px;'>
        <tr style='background-color: #004C97; color: white;'>
            <th style='padding: 8px; border: 1px solid #ddd;'>Параметр</th>
            <th style='padding: 8px; border: 1px solid #ddd;'>Рекомендуемое значение</th>
            <th style='padding: 8px; border: 1px solid #ddd;'>Когда менять</th>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Страховой запас</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>20%</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Больше для Z-класса, меньше для X-класса</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Процентная ставка</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>5% (консервативно)</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Используйте ключевую ставку ЦБ для точности</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Время поставки</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>30 дней</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Уточните у поставщиков реальные сроки</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Вести лог</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Включено</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Отключайте только если уверены</td>
        </tr>
    </table>
    """

def get_help_forecast_modes():
    """Подробное описание режимов прогнозирования и входных данных"""
    return """
    <h2 style='color: #0077C8;'>🔮 Режимы прогнозирования: Входные данные</h2>

    <p style='font-size: 14px; line-height: 1.8; background-color: #e3f2fd; padding: 15px; border-radius: 5px;'>
    <b>⚡ Ключевое отличие режимов:</b> В автоматическом режиме система <b>прогнозирует 2 показателя</b>
    (плановый спрос и начальный остаток), а в ручном режиме - только 1 (начальный остаток).
    </p>

    <h3>📋 Режим 1: РУЧНОЙ (с файлом прогноза)</h3>
    <div style='background-color: #fff3e0; padding: 20px; margin: 15px 0; border-left: 4px solid #FF9800; border-radius: 5px;'>

        <p><b>📁 Что нужно на входе:</b></p>

        <h4 style='color: #E65100;'>1. Исторический файл (обязательно):</h4>
        <table style='width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 13px;'>
            <tr style='background-color: #FF9800; color: white;'>
                <th style='padding: 8px; border: 1px solid #ddd;'>Колонка</th>
                <th style='padding: 8px; border: 1px solid #ddd;'>Статус</th>
                <th style='padding: 8px; border: 1px solid #ddd;'>Использование</th>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Дата</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>✅ Обязательно</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Группировка данных по периодам</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Материал</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>✅ Обязательно</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Идентификация материалов</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Филиал</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>✅ Обязательно</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Разделение по складам</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Начальный остаток</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>✅ Обязательно</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Исторические метрики (рост, оборачиваемость)</td>
            </tr>
            <tr style='background-color: #fff8e1;'>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Конечный остаток</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>✅ Обязательно</td>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>→ Прогноз НАЧАЛЬНОГО остатка на будущее</b></td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Потребление</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>❌ НЕ используется</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Не нужно (есть файл прогноза)</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Конечная стоимость</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>⭐ Рекомендуется</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Расчет упущенной выгоды</td>
            </tr>
        </table>

        <h4 style='color: #E65100;'>2. Файл прогноза (обязательно):</h4>
        <table style='width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 13px;'>
            <tr style='background-color: #FF9800; color: white;'>
                <th style='padding: 8px; border: 1px solid #ddd;'>Колонка</th>
                <th style='padding: 8px; border: 1px solid #ddd;'>Статус</th>
                <th style='padding: 8px; border: 1px solid #ddd;'>Описание</th>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Дата</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>✅ Обязательно</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Периоды прогноза (будущие даты)</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Материал</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>✅ Обязательно</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Те же материалы что в истории</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Филиал</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>✅ Обязательно</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Те же филиалы что в истории</td>
            </tr>
            <tr style='background-color: #fff8e1;'>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Плановый спрос</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>✅ Обязательно</td>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>ВЫ предоставляете готовый план!</b></td>
            </tr>
        </table>

        <p style='background-color: #fff; padding: 15px; border-radius: 5px; border: 2px solid #FF9800;'>
        <b>🔑 Ключевое:</b> В ручном режиме система прогнозирует <b>ТОЛЬКО ОДИН показатель</b>:<br>
        → <b>Начальный остаток</b> на будущие периоды (на основе конечных остатков из истории)<br>
        <br>
        Плановый спрос <b>НЕ прогнозируется</b> - вы его предоставляете в файле!
        </p>

        <h4 style='color: #E65100;'>🔄 Как это работает:</h4>
        <ol style='line-height: 2;'>
            <li><b>Берём последние конечные остатки</b> из исторического файла</li>
            <li><b>Прогнозируем начальные остатки</b> на будущие периоды (методом Naive/Exponential Smoothing)</li>
            <li><b>Берём плановый спрос</b> из ВАШЕГО файла прогноза</li>
            <li><b>Считаем:</b> Остаток на конец = Остаток на начало - Плановый спрос</li>
            <li><b>Рассчитываем рекомендации</b> по закупкам с учетом страхового запаса</li>
        </ol>

        <p><b>💡 Когда использовать:</b></p>
        <ul style='line-height: 1.8;'>
            <li>У вас есть точный план производства/продаж</li>
            <li>Вы хотите протестировать "что если" сценарии</li>
            <li>Плановый отдел уже подготовил прогноз спроса</li>
            <li>Нужно учесть внешние факторы (маркетинговые акции, сезонность бизнеса)</li>
        </ul>
    </div>

    <h3>🤖 Режим 2: АВТОМАТИЧЕСКИЙ (без файла прогноза)</h3>
    <div style='background-color: #e8f5e9; padding: 20px; margin: 15px 0; border-left: 4px solid #4CAF50; border-radius: 5px;'>

        <p><b>📁 Что нужно на входе:</b></p>

        <h4 style='color: #2E7D32;'>1. Исторический файл (обязательно):</h4>
        <table style='width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 13px;'>
            <tr style='background-color: #4CAF50; color: white;'>
                <th style='padding: 8px; border: 1px solid #ddd;'>Колонка</th>
                <th style='padding: 8px; border: 1px solid #ddd;'>Статус</th>
                <th style='padding: 8px; border: 1px solid #ddd;'>Использование</th>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Дата</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>✅ Обязательно</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Группировка данных по периодам</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Материал</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>✅ Обязательно</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Идентификация материалов</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Филиал</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>✅ Обязательно</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Разделение по складам</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Начальный остаток</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>✅ Обязательно</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Исторические метрики (рост, оборачиваемость)</td>
            </tr>
            <tr style='background-color: #f1f8e9;'>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Конечный остаток</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>✅ Обязательно</td>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>→ Прогноз НАЧАЛЬНОГО остатка на будущее</b></td>
            </tr>
            <tr style='background-color: #c8e6c9;'>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>🔥 Потребление</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>🔥 КРИТИЧЕСКИ ВАЖНО!</td>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>→ Автопрогноз ПЛАНОВОГО СПРОСА!</b></td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Конечная стоимость</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>⭐ Рекомендуется</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Расчет упущенной выгоды</td>
            </tr>
        </table>

        <h4 style='color: #2E7D32;'>2. Файл прогноза:</h4>
        <p style='background-color: #fff; padding: 15px; border-radius: 5px; font-size: 15px;'>
        <b>❌ НЕ НУЖЕН!</b> Система сама создаст прогноз на основе исторических данных!
        </p>

        <p style='background-color: #fff; padding: 15px; border-radius: 5px; border: 2px solid #4CAF50;'>
        <b>🔑 Ключевое:</b> В автоматическом режиме система прогнозирует <b>ДВА показателя</b>:<br>
        <br>
        1️⃣ <b>Плановый спрос</b> (на основе колонки "Потребление" из истории)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;→ Использует модели: Naive, MA, ES, Holt-Winters, SARIMA<br>
        <br>
        2️⃣ <b>Начальный остаток</b> (на основе конечных остатков из истории)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;→ Использует методы: Naive, Exponential Smoothing
        </p>

        <h4 style='color: #2E7D32;'>🔄 Как это работает:</h4>
        <ol style='line-height: 2;'>
            <li><b>Берём колонку "Потребление"</b> из исторического файла</li>
            <li><b>АВТОМАТИЧЕСКИ прогнозируем будущий спрос</b> (5 моделей: Naive, MA, ES, Holt-Winters, SARIMA)</li>
            <li><b>Выбираем лучшую модель</b> (если режим AUTO) по минимальной ошибке MAPE</li>
            <li><b>Прогнозируем начальные остатки</b> на будущие периоды</li>
            <li><b>Считаем:</b> Остаток на конец = Остаток на начало - СПРОГНОЗИРОВАННЫЙ спрос</li>
            <li><b>Рассчитываем рекомендации</b> по закупкам</li>
        </ol>

        <p><b>💡 Когда использовать:</b></p>
        <ul style='line-height: 1.8;'>
            <li><b>Рекомендуется в 90% случаев!</b> Самый простой и быстрый способ</li>
            <li>У вас нет готового плана спроса</li>
            <li>Спрос относительно стабильный и предсказуемый</li>
            <li>Есть история потребления минимум за 6-12 месяцев</li>
            <li>Хотите сэкономить время на подготовке прогнозного файла</li>
        </ul>

        <p><b>⚠️ Важно:</b></p>
        <p style='background-color: #fff3e0; padding: 10px; border-radius: 5px;'>
        Если в историческом файле <b>нет колонки "Потребление"</b>, система попытается вычислить её:<br>
        <code style='background-color: #fff; padding: 5px; border-radius: 3px;'>
        Потребление = Начальный остаток - Конечный остаток
        </code><br>
        <br>
        <b>НО!</b> Это может быть неточно, если были поступления материалов! Крайне рекомендуется иметь колонку "Потребление".
        </p>
    </div>

    <h3>📊 Сравнительная таблица режимов</h3>
    <table style='width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 13px;'>
        <tr style='background-color: #004C97; color: white;'>
            <th style='padding: 10px; border: 1px solid #ddd;'>Параметр</th>
            <th style='padding: 10px; border: 1px solid #ddd;'>Ручной режим</th>
            <th style='padding: 10px; border: 1px solid #ddd;'>Автоматический режим</th>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Файл прогноза</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>✅ Обязательно</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>❌ Не нужен</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Колонка "Потребление"</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>❌ Не используется</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>🔥 Критически важна!</td>
        </tr>
        <tr style='background-color: #fff8e1;'>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Что прогнозируется</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>
                1. Начальный остаток ✅<br>
                (Плановый спрос - из файла)
            </td>
            <td style='padding: 8px; border: 1px solid #ddd;'>
                1. Плановый спрос ✅<br>
                2. Начальный остаток ✅
            </td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Источник планового спроса</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Из файла прогноза (вы даёте)</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Прогнозируется автоматически</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Модели прогнозирования</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Только для начальных остатков</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Для спроса И остатков</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Сложность</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Средняя (нужен файл прогноза)</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Простая (один файл)</td>
        </tr>
        <tr>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Точность</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Зависит от вашего прогноза</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Зависит от качества истории</td>
        </tr>
        <tr style='background-color: #e8f5e9;'>
            <td style='padding: 8px; border: 1px solid #ddd;'><b>Рекомендация</b></td>
            <td style='padding: 8px; border: 1px solid #ddd;'>Для специфических сценариев</td>
            <td style='padding: 8px; border: 1px solid #ddd;'>⭐ Рекомендуется в 90% случаев!</td>
        </tr>
    </table>

    <h3>💡 Резюме</h3>
    <div style='background-color: #e3f2fd; padding: 20px; border-radius: 5px;'>
        <p style='font-size: 15px; line-height: 1.8;'>
        <b>🎯 Главное отличие:</b>
        </p>
        <ul style='font-size: 14px; line-height: 2;'>
            <li><b>Ручной режим:</b> Прогнозирует <b>1 показатель</b> (начальный остаток).
                Плановый спрос вы предоставляете в файле.</li>
            <li><b>Автоматический режим:</b> Прогнозирует <b>2 показателя</b> (плановый спрос + начальный остаток).
                Использует колонку "Потребление" из истории.</li>
        </ul>

        <p style='font-size: 15px; line-height: 1.8; margin-top: 20px;'>
        <b>💡 Наша рекомендация:</b>
        </p>
        <p style='font-size: 14px; line-height: 1.8; background-color: #fff; padding: 15px; border-radius: 5px; border-left: 4px solid #4CAF50;'>
        Используйте <b>автоматический режим</b> для повседневной работы. Он быстрее, проще и даёт хорошие результаты
        при наличии качественных исторических данных. Ручной режим используйте только для специфических сценариев,
        когда у вас есть точный план спроса от планового отдела или маркетинга.
        </p>
    </div>
    """
