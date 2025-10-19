import pandas as pd
import xlsxwriter
from io import BytesIO

def to_excel(df):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Записываем заголовки
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value)

    # Записываем данные
    for row_num, row in enumerate(df.values):
        for col_num, value in enumerate(row):
            if isinstance(value, str):
                worksheet.write(row_num + 1, col_num, value)
            else:
                worksheet.write(row_num + 1, col_num, value)

    workbook.close()
    output.seek(0)
    return output