# import openpyxl as xl
# from openpyxl.chart import BarChart, Reference
#
#
# # 加载工作簿
# wb = xl.load_workbook('transactions.xlsx')
# sheet = wb['Sheet1']
#
# # 行号从 1 开始
# for row in range(2, sheet.max_row + 1):
#     cell = sheet.cell(row, 3)
#     print(cell)
#     print(cell.value)
#
#     # 改变数字
#     correct_price = cell.value * 0.9
#     # 规定位置
#     correct_price_cell = sheet.cell(row, 4)
#     # 改变对应位置的值
#     correct_price_cell.value = correct_price
#
# values = Reference(sheet,
#                    min_row=2,
#                    max_row=sheet.max_row,
#                    min_col=4,
#                    max_col=4)
#
# chart = BarChart()
# chart.add_data(values)
# sheet.add_chart(chart, 'e2')
#
# # 保存到新文件防止出错
# wb.save("transactions2.xlsx")