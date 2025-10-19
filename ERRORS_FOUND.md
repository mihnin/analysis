# Отчет о найденных логических ошибках

## Критические ошибки

### ОШИБКА #1: Неправильный расчет среднего списания в historical_analysis.py

**Расположение:** `historical_analysis.py:19`

**Текущий код:**
```python
average_usage = (group[start_quantity_column] - group[end_quantity_column]).mean()
```

**Проблема:**
1. Формула `(start - end).mean()` дает **отрицательные значения** когда запасы растут (приход > расход)
2. **Игнорирует фактический приход** товара
3. В исходных данных уже есть колонка **'Списано/Использовано (количество)'** с фактическим расходом!

**Пример:**
- Начало периода: 100
- Приход: 70
- Расход: 20
- Конец периода: 150
- Текущая формула: (100 - 150) = **-50** (НЕПРАВИЛЬНО!)
- Фактический расход: **20** (ПРАВИЛЬНО!)

**Исправление:**
```python
# Если в данных есть колонка со списанием
if 'Списано/Использовано (количество)' in group.columns:
    average_usage = group['Списано/Использовано (количество)'].mean()
else:
    # Используем abs только если нет колонки списания
    average_usage = abs((group[start_quantity_column] - group[end_quantity_column]).mean())
```

**Влияние ошибки:**
- Неправильный расчет ABC классификации
- Неправильный расчет коэффициента вариации и XYZ класса
- Неправильный рекомендуемый уровень запаса
- Неправильный расчет излишков и упущенной выгоды

---

### ОШИБКА #2: Rolling sum суммирует прошлые периоды вместо будущих в forecast_analysis.py

**Расположение:** `forecast_analysis.py:101`

**Текущий код:**
```python
future_demand = df[forecast_quantity_column].rolling(window=3, min_periods=1).sum()
```

**Проблема:**
`rolling(window=3)` суммирует **ТЕКУЩИЙ + 2 ПРЕДЫДУЩИХ** периода, но для планирования закупок нужен **ТЕКУЩИЙ + 2 СЛЕДУЮЩИХ** периода!

**Пример:**
Потребность по периодам: [10, 20, 30, 40, 50]

Текущая логика (НЕПРАВИЛЬНО):
- Период 0: 10 (только текущий)
- Период 1: 30 (10+20)
- Период 2: 60 (10+20+30) ← суммирует ПРОШЛОЕ
- Период 3: 90 (20+30+40)
- Период 4: 120 (30+40+50)

Правильная логика:
- Период 0: 60 (10+20+30) ← должна суммировать БУДУЩЕЕ
- Период 1: 90 (20+30+40)
- Период 2: 120 (30+40+50)
- Период 3: 90 (40+50)
- Период 4: 50 (только 50)

**Исправление:**
```python
# Метод 1: Используем shift с отрицательным значением
future_demand = df.groupby([forecast_material_column, forecast_branch_column])[forecast_quantity_column].transform(
    lambda x: x.shift(-1).rolling(window=3, min_periods=1).sum().shift(1)
)

# Метод 2: Используем iloc в цикле (более явно)
def calculate_forward_rolling_sum(series, window=3):
    result = []
    for i in range(len(series)):
        window_sum = series.iloc[i:min(i+window, len(series))].sum()
        result.append(window_sum)
    return pd.Series(result, index=series.index)

future_demand = df.groupby([forecast_material_column, forecast_branch_column])[forecast_quantity_column].transform(
    lambda x: calculate_forward_rolling_sum(x, window=3)
)
```

**Влияние ошибки:**
- Неправильный расчет будущего спроса
- Неправильные рекомендации по закупкам
- Возможен дефицит материалов

---

### ОШИБКА #3: Exponential Smoothing перезаписывает запланированную потребность в forecast_analysis.py

**Расположение:** `forecast_analysis.py:16-21`

**Текущий код:**
```python
for material in analysis_df[material_column].unique():
    for branch in analysis_df[branch_column].unique():
        material_branch_data = analysis_df[(analysis_df[material_column] == material) & (analysis_df[branch_column] == branch)]
        if len(material_branch_data) > 2:
            model = ExponentialSmoothing(material_branch_data[demand_column], trend='add', seasonal=None).fit()
            analysis_df.loc[(analysis_df[material_column] == material) & (analysis_df[branch_column] == branch), demand_column] = model.fittedvalues.round(1)
```

**Проблема:**
1. **Перезаписывает исходные данные** запланированной потребности
2. Применяется **ПОСЛЕ всех расчетов** в app.py, что делает предыдущие расчеты некорректными
3. **Не имеет смысла** применять сглаживание к запланированным данным

**Порядок операций в app.py:**
1. Загружаются прогнозные данные
2. `forecast_start_balance()` - прогноз начального остатка
3. Расчет конечного остатка = начало - **потребность** ← использует исходную потребность
4. `calculate_purchase_recommendations()` - рекомендации на основе **потребности** ← использует исходную потребность
5. `analyze_forecast_data()` - ПЕРЕЗАПИСЫВАЕТ **потребность**! ← все предыдущие расчеты становятся некорректными

**Исправление:**
Полностью **удалить** эту часть кода или применять Exponential Smoothing **только для визуализации**, не перезаписывая исходные данные:

```python
# ВАРИАНТ 1: Удалить полностью (рекомендуется)
def analyze_forecast_data(df, date_column, material_column, branch_column, demand_column,
                          start_balance_column, end_balance_column, recommendation_column,
                          future_demand_column, safety_stock_column):
    analysis_df = df.copy()
    numeric_columns = [demand_column, start_balance_column, end_balance_column,
                       recommendation_column, future_demand_column, safety_stock_column]
    analysis_df[numeric_columns] = analysis_df[numeric_columns].round(1)
    analysis_df = analysis_df.sort_values([date_column, material_column, branch_column])

    # УДАЛИТЬ ЦИКЛ С EXPONENTIAL SMOOTHING

    explanation = get_explanation(...)
    return analysis_df, explanation

# ВАРИАНТ 2: Создать отдельную колонку для сглаженных значений (если нужно)
model = ExponentialSmoothing(material_branch_data[demand_column], trend='add', seasonal=None).fit()
analysis_df.loc[..., 'Сглаженная потребность'] = model.fittedvalues.round(1)
# НЕ перезаписывать demand_column!
```

**Влияние ошибки:**
- Потеря исходных запланированных данных
- Некорректные расчеты остатков и рекомендаций
- Невозможность проверить исходные данные

---

## Дополнительные замечания

### Замечание #1: Расчет общего использования в historical_analysis.py:22

**Текущий код:**
```python
total_usage = abs((group[start_quantity_column] - group[end_quantity_column]).sum())
```

**Проблема:**
Применяется `abs()` к сумме, что может скрывать реальную динамику запасов.

**Рекомендация:**
Если есть колонка фактического списания, использовать её:
```python
if 'Списано/Использовано (количество)' in group.columns:
    total_usage = group['Списано/Использовано (количество)'].sum()
else:
    total_usage = abs((group[start_quantity_column] - group[end_quantity_column]).sum())
```

---

### Замечание #2: Проверка баланса

В исходных данных есть колонки:
- Остаток на начало месяца
- Закуплено (количество)
- Списано/Использовано (количество)
- Остаток на конец месяца

Должен соблюдаться баланс:
```
Остаток на конец = Остаток на начало + Закуплено - Списано
```

Рекомендуется добавить валидацию данных при загрузке.

---

## Приоритет исправлений

1. **Высокий:** ОШИБКА #1 - влияет на все метрики
2. **Высокий:** ОШИБКА #3 - перезаписывает исходные данные
3. **Средний:** ОШИБКА #2 - влияет на рекомендации по закупкам
4. **Низкий:** Замечания #1-2 - улучшение качества кода

---

## Статус тестирования

- ✅ Созданы unit тесты для historical_analysis.py (12 тестов)
- ✅ Созданы unit тесты для forecast_analysis.py (12 тестов)
- ✅ Тесты подтвердили наличие всех выявленных проблем
- ✅ Тесты готовы для проверки исправлений
