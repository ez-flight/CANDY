# Import `xlwt`
import xlrd

from datetime import date, datetime, timedelta

filename1 = "t_max_semki"

# Open a workbook 
workbook = xlrd.open_workbook(filename1 + ".xls")
# Loads only current sheets to memory
workbook = xlrd.open_workbook(filename1 + ".xls", on_demand = True)
# Получаем количество листов в файле 
len_list = len(workbook.sheet_names())
for k in range(len_list):
    # Получить объект листа по индексу
    sheet1 = workbook.sheet_by_index(k)
    # Загрузите определенный лист по названию
    worksheet = workbook.sheet_by_name(sheet1.name)

    vitok = []
    dt_start = []
    dt_end = []
    t_simki= []

    for i in range(0, 27):
        for j in range(0, 3):
            if j == 0:
                vitok.append(worksheet.cell_value(i, j))
            elif j == 1:
                date1 = datetime.strptime(worksheet.cell_value(i, j), '%Y-%m-%d %H:%M:%S')
                dt_start.append(date1)
            elif j == 2:
                date2= datetime.strptime(worksheet.cell_value(i, j), '%Y-%m-%d %H:%M:%S')
                dt_end.append(date2)
            elif j == 3:
                t_simki.append(worksheet.cell_value(i, j))
print (dt_start)
