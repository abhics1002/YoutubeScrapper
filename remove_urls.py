__author__ = 'abhishekbharadwaj'
import xlsxwriter, logging
import re
import xlrd

COLUMN = 4


def open_file(path):
    book = xlrd.open_workbook(path)
    print book.nsheets
    # print sheet names
    print book.sheet_names()
    # get the first worksheet
    first_sheet = book.sheet_by_index(0)
    # read a row
    print first_sheet.row_values(0)
    row =0
    len_row = first_sheet.nrows
    len_col = first_sheet.ncols
    new_file = path + "_new.xlsx"
    workbook = xlsxwriter.Workbook(new_file)
    worksheet = workbook.add_worksheet()
    for row_data in range(len_row):
        for col_data in range(len_col):
            try:
                cell_data = first_sheet.cell(row_data, col_data).value
                # FileWriter.write_file_trim_urls(worksheet, text, row)
                if COLUMN == col_data:
                    test2 = re.sub(r"(?:\@|https?\://)\S+", "", cell_data)
                    test3 = re.sub(r"(?:\@|www?\.)\S+", "",test2)
                    worksheet.write_string(row_data, col_data, str(test3))
                else:
                    worksheet.write_string(row_data, col_data, str(cell_data))
            except Exception as ex:
                print "Exception ---" + str(ex.message)
    workbook.close()


if __name__ == "__main__":
    path = "gurumaaashram_with_playlist_js.xlsx"
    open_file(path)