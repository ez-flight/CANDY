# Библиотека графиков
import matplotlib.pyplot as plt
import numpy as np
# Import `xlrd`
import xlrd
from celluloid import Camera

fig = plt.figure()
camera = Camera(fig)
name = "KONDOR FKA NO.1"
filename = "DATA/" + name

# Open a workbook 
workbook = xlrd.open_workbook(filename + ".xls")
# Loads only current sheets to memory
workbook = xlrd.open_workbook(filename + ".xls", on_demand = True)
# Получаем количество листов в файле 
len_list = len(workbook.sheet_names())
for k in range(len_list):
    # Получить объект листа по индексу
    sheet1 = workbook.sheet_by_index(k)
    # Загрузите определенный лист по названию
    worksheet = workbook.sheet_by_name(sheet1.name)

    i_m = []
    dt_m = []
    lon_s_m = []
    lat_s_m = []
    R_s_m = []
    R_e_m = []
    R_0_m = []
    y_grad_m = []
    ay_grad_m = []
    a_m = []
    Wp_m = []
    Fd_m = []

    for i in range(0, 1291):
        for j in range(0, 12):
            if j == 0:
                i_m.append(worksheet.cell_value(i, j))
            elif j == 1:
                dt_m.append(worksheet.cell_value(i, j))
            elif j == 2:
                lon_s_m.append(worksheet.cell_value(i, j))
            elif j == 3:
                lat_s_m.append(worksheet.cell_value(i, j))
            elif j == 4:
                R_s_m.append(worksheet.cell_value(i, j))
            elif j == 5:
                R_e_m.append(worksheet.cell_value(i, j))
            elif j == 6:
                R_0_m.append(worksheet.cell_value(i, j))
            elif j == 7:
                y_grad_m.append(worksheet.cell_value(i, j))
            elif j == 8:
                ay_grad_m.append(worksheet.cell_value(i, j))
            elif j == 9:
                a_m.append(worksheet.cell_value(i, j))
            elif j == 10:
                Fd_m.append(worksheet.cell_value(i, j))
            elif j == 11:            
                Wp_m.append(worksheet.cell_value(i, j))
            # Print the cell values with tab space



    plt.title('Доплеровское смещение частоты отраженного сигнала в зависимости от долготы ИСЗ')
    plt.xlabel('Долгота')
    plt.ylabel('Fd,Гц')
    plt.plot( lon_s_m, Fd_m, 'go', markersize=1)
    camera.snap()
#    plt.plot(Wp_m_2, Fd_m_2, 'bo')
 #   plt.plot(ass1[4], Fd_m[4], 'yo')
#    plt.show()
animation = camera.animate()
animation.save(filename + '.gif', writer = 'imagemagick')