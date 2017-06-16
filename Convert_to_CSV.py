import xlrd
import csv
import glob

def csv_from_excel(file):

    wb = xlrd.open_workbook(file)
    sh = wb.sheet_by_name(wb.sheet_names()[0])
    your_csv_file = open(file.replace('.xlsx', '.csv'), 'w', newline='')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

files = glob.glob('.\Test\*')

for file in files:
    if file.split('\\')[-1].split('.')[-1] == 'xlsx':
        csv_from_excel(file)
    else:
        print("File extension unknown.")