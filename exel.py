# Import `xlwt`
import xlwt

# Initialize a workbook 
book = xlwt.Workbook(encoding="utf-8")

# Add a sheet to the workbook
sheet1 = book.add_sheet("Sheet1")

# The data
cols = ["A", "B", "C", "D", "E"]
txt = [0,1,2,3,4]

# Loop over the rows and columns and fill in the values
for num in range(5):
      row = sheet1.row(num)
      for index, col in enumerate(cols):
          value = txt[index] + num
          row.write(index, value)

# Save the result
book.save("space/test.xls")
