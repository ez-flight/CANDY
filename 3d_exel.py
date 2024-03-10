import matplotlib.pyplot as plt
import numpy as np
# Import `xlrd`
import xlrd

name = "KONDOR FKA NO.1"
filename = "DATA/" + name + ".xls"

# Open a workbook 
workbook = xlrd.open_workbook(filename)
# Loads only current sheets to memory
workbook = xlrd.open_workbook(filename, on_demand = True)
print(workbook.sheet_names())
# Загрузите определенный лист по названию
worksheet = workbook.sheet_by_name('90.5')

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

for i in range(0, 6441):
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


fig = plt.figure()
ax = fig.add_subplot(projection="3d")

def f_sin_xy(x, y):
    return np.sin(np.sqrt(x**2 + y**2))

x = lon_s_m
y = lat_s_m
z = Fd_m



ax.scatter3D(x, y, z, c=z)

ax.set(xlabel="$x$", ylabel="$y$", zlabel="$z$");

plt.show()