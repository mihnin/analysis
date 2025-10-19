import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy import stats
import sys
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.utils import data_validation as dv

def analyze_historical_data(df, date_column, branch_column, material_column, start_quantity_column, end_quantity_column, end_cost_column, interest_rate, consumption_column=None, lead_time_days=30, consumption_convention='AUTO'):
    """
    Анализ исторических данных по запасам

    Parameters:
    -----------
    lead_time_days : int, optional
        Время выполнения заказа в днях (по умолчанию 30)
    consumption_convention : str, optional
        Конвенция знака списания: 'AUTO', 'POSITIVE', 'NEGATIVE', 'ABS' (по умолчанию 'AUTO')
    """
    df = df.copy()  # Создаем копию чтобы не модифицировать оригинал
    df[date_column] = pd.to_datetime(df[date_column])

    # АВТОМАТИЧЕСКАЯ НОРМАЛИЗАЦИЯ СПИСАНИЯ
    arrival_column = None
    # Пытаемся найти колонку прихода для более точной проверки
    for col in df.columns:
        if any(keyword in col.lower() for keyword in ['прих', 'закуп', 'поступ', 'arrival', 'purchase']):
            arrival_column = col
            break

    if consumption_column and consumption_column in df.columns:
        # Нормализуем списание (всегда делаем положительным)
        df, detection = dv.normalize_consumption(
            df, consumption_column,
            convention=consumption_convention,
            start_column=start_quantity_column,
            end_column=end_quantity_column,
            arrival_column=arrival_column
        )
        print(f"[INFO] Нормализация списания: {detection['recommendation']}")

    results = []
    unique_combinations = df.groupby([material_column, branch_column]).groups.keys()

    for material, branch in unique_combinations:
        group = df[(df[material_column] == material) & (df[branch_column] == branch)].sort_values(date_column)

        start_quantity = group[start_quantity_column].iloc[0]
        end_quantity = group[end_quantity_column].iloc[-1]
        growth = end_quantity / start_quantity if start_quantity != 0 else np.inf
        months = (group[date_column].max() - group[date_column].min()).days / 30.44

        # ИСПРАВЛЕНИЕ ОШИБКИ #1: Используем фактическое списание если доступно
        if consumption_column and consumption_column in group.columns:
            average_usage = group[consumption_column].mean()
            total_usage = group[consumption_column].sum()
        else:
            # Fallback: используем abs разницы остатков
            average_usage = abs((group[start_quantity_column] - group[end_quantity_column]).mean())
            total_usage = abs((group[start_quantity_column] - group[end_quantity_column]).sum())
        
        # Расчет среднего запаса
        average_inventory = abs((group[start_quantity_column] + group[end_quantity_column]).mean() / 2)
        
        # Расчет оборачиваемости
        if average_inventory > 0:
            turnover = abs(total_usage) / average_inventory
            turnover_str = f'{turnover:.2f}'
        elif total_usage == 0 and average_inventory == 0:
            turnover_str = 'Нет движения'
        elif total_usage == 0:
            turnover_str = 'Нет использования'
        elif average_inventory == 0:
            turnover_str = 'Нет запаса'
        else:
            turnover_str = 'Ошибка в данных'
        
        if len(group) > 12:
            decomposition = seasonal_decompose(group[end_quantity_column], model='additive', period=12)
            seasonality = decomposition.seasonal.std() / group[end_quantity_column].std()
            trend = stats.linregress(range(len(group)), group[end_quantity_column]).slope
        else:
            seasonality = np.nan
            trend = np.nan
        
        excess_inventory = "Да" if end_quantity > 2 * abs(average_usage) else "Нет"

        # ИСПРАВЛЕНИЕ ОШИБКИ #1: Используем фактическое списание для расчета std
        if consumption_column and consumption_column in group.columns:
            usage_std = group[consumption_column].std()
        else:
            usage_std = abs((group[start_quantity_column] - group[end_quantity_column]).std())
        coefficient_variation = usage_std / abs(average_usage) if average_usage != 0 else np.nan
        
        end_cost = group[end_cost_column].iloc[-1]
        unit_cost = end_cost / end_quantity if end_quantity != 0 else 0
        
        # Рассчет упущенной выгоды
        if excess_inventory == "Да":
            excess_amount = end_quantity - 2 * abs(average_usage)
            lost_profit = excess_amount * unit_cost * interest_rate / 100
        else:
            lost_profit = 0

        # НОВАЯ МЕТРИКА 1: Оборачиваемость в днях
        if turnover_str != 'Нет движения' and turnover_str != 'Нет использования' and turnover_str != 'Нет запаса':
            try:
                turnover_val = float(turnover_str)
                days_of_inventory = 365 / turnover_val if turnover_val > 0 else np.inf
                days_str = f'{days_of_inventory:.0f} дней' if days_of_inventory != np.inf else 'Н/Д'
            except:
                days_str = 'Н/Д'
        else:
            days_str = 'Н/Д'

        # НОВАЯ МЕТРИКА 2: Точка заказа (ROP - Reorder Point)
        # ROP = (Среднее потребление/день × Lead Time) + Страховой запас
        # Страховой запас = Z-score × std_deviation × sqrt(lead_time)
        # Для 95% service level: Z = 1.65
        daily_usage = abs(average_usage) * 12 / 365  # перевод месячного в дневное
        if consumption_column and consumption_column in group.columns:
            daily_std = group[consumption_column].std() / np.sqrt(30)  # Примерная дневная вариация
        else:
            daily_std = usage_std / np.sqrt(30)

        z_score = 1.65  # 95% service level
        safety_stock_rop = z_score * daily_std * np.sqrt(lead_time_days)
        reorder_point = (daily_usage * lead_time_days) + safety_stock_rop
        reorder_point_str = f'{reorder_point:.0f} единиц'

        # НОВАЯ МЕТРИКА 3: Анализ дефицитов
        # Считаем периоды с отрицательным остатком на конец
        deficit_periods = (group[end_quantity_column] < 0).sum()
        total_periods = len(group)
        deficit_percentage = (deficit_periods / total_periods * 100) if total_periods > 0 else 0

        # Средний размер дефицита
        deficits = group[end_quantity_column][group[end_quantity_column] < 0]
        avg_deficit = abs(deficits.mean()) if len(deficits) > 0 else 0

        # Fill Rate (процент удовлетворенного спроса)
        if consumption_column and consumption_column in group.columns:
            total_demand = group[consumption_column].sum()
            # Спрос который не удовлетворили = дефицит
            unsatisfied_demand = abs(deficits.sum()) if len(deficits) > 0 else 0
            fill_rate = ((total_demand - unsatisfied_demand) / total_demand * 100) if total_demand > 0 else 100
        else:
            # Примерный расчет если нет колонки потребления
            fill_rate = 100 - deficit_percentage

        fill_rate_str = f'{fill_rate:.1f}%'
        deficit_str = f'{deficit_periods} из {total_periods} ({deficit_percentage:.1f}%)'

        # НОВАЯ МЕТРИКА 4: Мертвый запас
        # Материалы без движения (когда списание близко к 0)
        if consumption_column and consumption_column in group.columns:
            no_movement_periods = (group[consumption_column] == 0).sum()
        else:
            # Если нет движения: начало = конец
            no_movement_periods = (group[start_quantity_column] == group[end_quantity_column]).sum()

        dead_stock_percentage = (no_movement_periods / total_periods * 100) if total_periods > 0 else 0
        is_dead_stock = "Да" if dead_stock_percentage > 50 else "Нет"  # >50% периодов без движения
        dead_stock_str = f'{is_dead_stock} ({no_movement_periods}/{total_periods})'

        results.append({
            'Материал': material,
            'Филиал': branch,
            'Рост за период': f'{growth:.2f} раз за {months:.1f} месяцев',
            'Среднее списание': f'{average_usage:.0f} единиц в месяц',
            'Оборачиваемость': turnover_str,
            'Оборачиваемость (дни)': days_str,  # НОВАЯ МЕТРИКА
            'Сезонность': f'{seasonality:.2f}' if not np.isnan(seasonality) else 'Н/Д',
            'Тренд': f'{trend:.2f}' if not np.isnan(trend) else 'Н/Д',
            'Признаки накопления излишков': excess_inventory,
            'ABC-класс': get_abc_class(abs(average_usage)),
            'XYZ-класс': get_xyz_class(coefficient_variation),
            'Коэффициент вариации спроса': f'{coefficient_variation:.2f}' if not np.isnan(coefficient_variation) else 'Н/Д',
            'Рекомендуемый уровень запаса': f'{get_recommended_stock_level(abs(average_usage), seasonality, trend):.0f} единиц',
            'Точка заказа (ROP)': reorder_point_str,  # НОВАЯ МЕТРИКА
            'Упущенная выгода': f'{lost_profit:.2f} руб.',
            'Периоды с дефицитом': deficit_str,  # НОВАЯ МЕТРИКА
            'Fill Rate': fill_rate_str,  # НОВАЯ МЕТРИКА
            'Мертвый запас': dead_stock_str  # НОВАЯ МЕТРИКА
        })
    
    results_df = pd.DataFrame(results)
    explanation = get_explanation(results_df.iloc[0])
    
    return results_df, explanation

def get_abc_class(average_usage):
    if average_usage > 100:
        return 'A'
    elif average_usage > 50:
        return 'B'
    else:
        return 'C'

def get_xyz_class(coefficient_of_variation):
    if coefficient_of_variation < 0.1:
        return 'X'
    elif coefficient_of_variation < 0.3:
        return 'Y'
    else:
        return 'Z'

def get_recommended_stock_level(average_usage, seasonality, trend):
    base_level = average_usage * 2
    if not np.isnan(seasonality) and seasonality > 0.5:
        base_level *= 1.2
    if not np.isnan(trend) and trend > 0:
        base_level *= 1.1
    return base_level

def get_explanation(row):
    explanation = f"""
    Пояснение расчетов на примере материала {row['Материал']} в филиале {row['Филиал']}:

    1. Рост за период: {row['Рост за период']}
       - Формула: Рост = Конечный запас / Начальный запас
       - Это показывает, как изменился запас материала за весь период.
       - Если больше 1, запас вырос. Если меньше 1, запас уменьшился.
       - Что делать: Если рост большой, проверьте, не накапливаются ли излишки.

    2. Среднее списание: {row['Среднее списание']}
       - Формула: Среднее списание = Среднее (Начальный запас - Конечный запас) за все месяцы
       - Сколько в среднем материала используется за месяц.
       - Что делать: Используйте это значение для планирования закупок.

    3. Оборачиваемость: {row['Оборачиваемость']}
       - Формула: Оборачиваемость = Общее использование / Средний запас
       - Показывает, сколько раз запас полностью обновляется за период.
       - Чем выше, тем эффективнее используется запас.
       - Что делать: Стремитесь увеличить этот показатель, это сэкономит деньги.

    4. Сезонность: {row['Сезонность']}
       - Формула: Сезонность = Стандартное отклонение сезонной компоненты / Стандартное отклонение запаса
       - Показывает, насколько сильно меняется спрос в разные сезоны.
       - Что делать: Если высокая, планируйте закупки с учетом сезонных колебаний.

    5. Тренд: {row['Тренд']}
       - Формула: Тренд = Наклон линейной регрессии по запасам
       - Показывает общее направление изменения запаса.
       - Положительный - запас растет, отрицательный - уменьшается.
       - Что делать: Учитывайте при долгосрочном планировании.

    6. ABC-класс: {row['ABC-класс']}
       ABC-классификация — это метод разделения материалов на три групы, основанный на их важности для компании. В нашем случае важность измеряется через среднее списание, то есть сколько материала обычно используется каждый месяц.
       
       Группы в ABC-классификации:
       - A: Это самые важные материалы, которых расходуется больше всего (более 100 единиц в месяц). Обычно сюда относятся материалы, на которые тратится много денег или которые часто нужны. Мы должны уделять этим материалам максимум внимания, чтобы они всегда были в наличии и не заканчивались.
       - B: Это материалы средней важности (от 50 до 100 единиц в месяц). Они не так важны, как A, но их тоже часто используют. Мы уделяем им достаточное внимание, но не так много, как материалам категории A.
       - C: Это менее важные материалы, которые используются меньше всех (менее 50 единиц в месяц). Обычно они стоят дешевле или нужны редко, поэтому д��я них не требуется столько внимания.

       Пример:
       Представьте, что вы управляете складом строительных материалов:
       - A: Цемент, который используется почти в каждом проекте и в больших количествах.
       - B: Краска, которая нужна часто, но не в таких больших объемах, как цемент.
       - C: Специальные инструменты, которые нужны редко и в небольших количествах.

       Что делать:
       - Для класса A: Постоянно следите за уровнем запасов, прогнозируйте спрос, оптимизируйте закупки.
       - Для класса B: Регулярно проверяйте запасы, но не так часто, как для A.
       - Для класса C: Можно использовать более простые методы управления запасами, например, пополнять запас, когда он достигает определенного минимума.

    7. XYZ-класс: {row['XYZ-класс']}
       - Формула: XYZ-класс основан на коэффициенте вариации спроса
       - X - стабильный спрос, Y - колеблющийся спрос, Z - непредсказуемый спрос.
       - Что делать: Для Z-класса держите больший страховой запас.

    8. Коэффициент вариации спроса: {row['Коэффициент вариации спроса']}
       - Формула: Коэффициент вариации = Стандартное отклонение списаний / Среднее списание
       - Показывает, насколько сильно колеблется спрос.
       - Что делать: Чем выше, тем больше страховой запас нужен.

    9. Рекомендуемый уровень запаса: {row['Рекомендуемый уровень запаса']}
       - Формула: Уровень запаса = Среднее списание * 2 (скорректированный на сезонность и тренд)
       - Оптимальный уровень запаса с учетом всех факторов.
       - Что делать: Старайтесь поддерживать запас на этом уровне.

    10. Упущенная выгода: {row['Упущенная выгода']}
       - Выявление излишков: Излишки определяются как превышение конечного запаса над удвоенным значением среднего списания. Это дает возможность выявить ситуации, когда запас превышает ожидаемую потребность.
       
       - Расчет упущенной выгоды: Упущенная выгода рассчитывается для излишков на основе стоимости единицы материала и процентной ставки. 
         Формула: Упущенная выгода = (Конечный запас - 2 × Среднее списание) × Стоимость единицы × Процентная ставка / 100
         Этот подход учитывает, сколько денег можно было бы заработать, если бы они были вложены вместо хранения излишков.
       
       - Рекомендации по сокращению излишков: Расчет упущенной выгоды мотивирует уменьшение излишков, что ведет к более эффективному использованию средств и снижению затрат на хранение.
       
       - Что делать: 
         1. Регулярно анализируйте уровень запасов и выявляйте излишки.
         2. Разработайте стратегию по сокращению излишков, например, через акции или специальные предложения.
         3. Оптимизируйте процесс закупок, чтобы избежать накопления излишков в будущем.
         4. Рассмотрите возможность инвестирования средств, высвобожденных от сокращения излишков, в более прибыльные направления бизнеса.



    Бизнес-выгоды от использования этой аналитики:
    1. Снижение затрат на хранение за счет оптимизации уровня запасов.
    2. Уменьшение рисков дефицита благодаря правильному планированию.
    3. Повышение оборачиваемости капитала.
    4. Улучшение качества обслуживания клиентов за счет наличия нужных материалов.
    5. Более эффективное использование складских помещений.
    """
    return explanation