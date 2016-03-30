__author__ = 'abhishekbharadwaj'


from datetime import datetime
import xlsxwriter


def write_file(video_data, workbook, worksheet, row):
    # Create a workbook and add a worksheet.
    # workbook = xlsxwriter.Workbook('youtube_data.xlsx')
    # worksheet = workbook.add_worksheet()

    # worksheet.sheet_name(video_data['items'][0]['snippet']['channelTitle'])
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})

    # Add a number format for cells with money.
    money_format = workbook.add_format({'num_format': '$#,##0'})

    # Add an Excel date format.
    date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})

    # Adjust the column width.
    worksheet.set_column(1, 1, 15)

    # Write some data headers.
    worksheet.write('A1', 'id', bold)
    worksheet.write('B1', 'publishedAt', bold)
    worksheet.write('C1', 'channelId', bold)
    worksheet.write('D1', 'title', bold)
    worksheet.write('E1', 'description', bold)

    worksheet.write('F1', 'tags', bold)
    worksheet.write('G1', 'categoryId', bold)
    worksheet.write('H1', 'viewCount', bold)
    worksheet.write('I1', 'likeCount', bold)
    worksheet.write('J1', 'dislikeCount', bold)
    worksheet.write('K1', 'favoriteCount', bold)
    worksheet.write('L1', 'commentCount', bold)
    worksheet.write('M1', 'videoUrl', bold)

    # Some data we want to write to the worksheet.

    # Start from the first cell below the headers.
    # row = 1
    col = 0



    try:
        worksheet.write_string  (row, col,     video_data['items'][0]['id'])
        worksheet.write_string(row, col + 1, video_data['items'][0]['snippet']['publishedAt'])
        worksheet.write_string  (row, col + 2, video_data['items'][0]['snippet']['channelId'])
        worksheet.write_string  (row, col + 3, video_data['items'][0]['snippet']['title'])
        worksheet.write_string  (row, col + 4, video_data['items'][0]['snippet']['description'])
        worksheet.write_string  (row, col + 5, ",".join(str(x) for x in video_data['items'][0]['snippet']['tags']))
        worksheet.write_string  (row, col + 6, video_data['items'][0]['snippet']['categoryId'])
        worksheet.write_string  (row, col + 7, video_data['items'][0]['statistics']['viewCount'])
        worksheet.write_string  (row, col + 8, video_data['items'][0]['statistics']['likeCount'])
        worksheet.write_string  (row, col + 9, video_data['items'][0]['statistics']['dislikeCount'])
        worksheet.write_string  (row, col + 10, video_data['items'][0]['statistics']['favoriteCount'])
        worksheet.write_string  (row, col + 11, video_data['items'][0]['statistics']['commentCount'])
        worksheet.write_string  (row, col + 12, "https://www.youtube.com/watch?v="+video_data['items'][0]['id'])
        # row += 1
        # workbook.close()
    except Exception as ex:
        print "exception not able to write "+video_data['items'][0]['id'] + " , "+video_data['items'][0]['snippet']['title']
        print video_data
        print str(ex.message)




if __name__ == "__main__":
    print "Inside main"
    channel_ids = ['UCNJcSUSzUeFm8W9P7UUlSeQ']
    write_file()


