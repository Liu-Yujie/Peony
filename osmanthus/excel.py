import openpyxl
import pandas as pd

filePath = r'D:\doc\work\equity\外部权益(2).xlsx'

pd.set_option('display.max_columns', None)   #显示完整的列
pd.set_option('display.max_rows', None) 	 #显示完整的行

def generateJsonSec():
    wb = openpyxl.load_workbook(filePath)
    sheetList = wb.sheetnames
    for item in sheetList[1:5]:
        sheet = wb[item]
        cells = sheet['b5':'e15']
        for c1,c2 in cells:
            print(c1,c2)
    # wb.save('test.xlsx')


def readExcel():
    sheet = pd.read_excel(filePath, sheet_name='外部权益信息表', header=3, usecols='b,d')
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     pass
    print(sheet)
    print(sheet[0])





if __name__ == '__main__':
    readExcel()
