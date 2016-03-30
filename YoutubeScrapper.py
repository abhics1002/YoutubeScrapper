__author__ = 'abhishekbharadwaj'

from utils import network_utils, FileWriter
from utils.constants import Youtube
import xlsxwriter


def start_scrapping(channel_ids):

    channel_video_mapping_dict = dict()
    for channel_id in channel_ids:
        # network_utils.network_request(Youtube.YOUTUBE_APIS_ENDPOINT, )
        channel_resp = network_utils.get_channel_details(channel_id)
        total_result = channel_resp['pageInfo']['totalResults']
        counter = total_result/50
        while(counter):
            for video in channel_resp['items']:
                if video['id']['kind'] == "youtube#video":
                    # print video['id']['videoId']
                    if channel_id in channel_video_mapping_dict:
                        channel_video_mapping_dict[channel_id].append(video['id']['videoId'])
                    else:
                        channel_video_mapping_dict[channel_id] = [video['id']['videoId']]
            counter = counter -1
            if counter>0:
                channel_resp = network_utils.get_channel_details(channel_id, page_token=channel_resp['nextPageToken'])
    # print channel_video_mapping_dict
    return channel_video_mapping_dict


def scrap_video_data(video_ids):

    # video_resp = network_utils.get_video_details(video_ids)
    # print video_resp
    workbook = xlsxwriter.Workbook('youtube_data.xlsx')
    worksheet = workbook.add_worksheet()
    row =1
    for video_id in video_ids:
        video_resp = network_utils.get_video_details(video_id)
        # print video_resp
        FileWriter.write_file(video_resp, workbook, worksheet, row=row)
        row = row + 1
    workbook.close()
    return video_resp


if __name__ == "__main__":
    print "Inside main"
    channel_ids = ['UCNJcSUSzUeFm8W9P7UUlSeQ']
    video = start_scrapping(channel_ids)
    # print video['UCNJcSUSzUeFm8W9P7UUlSeQ']
    video_resp = scrap_video_data(video['UCNJcSUSzUeFm8W9P7UUlSeQ'])
    # FileWriter.write_file(video_resp)
