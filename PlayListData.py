__author__ = 'abhishekbharadwaj'

import xlsxwriter, logging
import logging
from utils import network_utils, FileWriter
from utils.constants import Youtube

LOG_FILENAME = 'downloader.log'
logger = logging.getLogger(__name__)

YOUTUBE_CHANNEL_ID = 'UCGje2kPIo-0M3fycdAghUsQ'
FILE_NAME = 'playlist_data.xlsx'

def get_playlist_id(channel_id, data):
    channel_resp = network_utils.get_playlist_id(channel_id, page_token=None)
    total_result = channel_resp['pageInfo']['totalResults']
    logger.info("channel "+str(channel_id)+" - - - - total number of video"+str(total_result))
    counter = total_result/50 + 1

    # channel_video_mapping_dict = dict()
    count_already_present = 0
    logger.info("no of Items ----"+str(len(channel_resp['items'])))
    playlist_ids =[]
    while(counter):
        for video in channel_resp['items']:
            if video['kind'] =="youtube#playlist" and video['snippet']['channelId'] == channel_id:
                playlist_ids.append(video['id'])

        counter -= 1

        if counter > 0:
            try:
                logger.info("next page token ----"+channel_resp['nextPageToken'])
                channel_resp = network_utils.get_playlist_id(channel_id, page_token=channel_resp['nextPageToken'])
                logger.info("no of Items ----"+str(len(channel_resp['items'])))

                # sleep(5)
                # logger.warning(channel_resp)
            except Exception as ex:
                logger.warning("exception -- token "+str(ex.message)+"----"+str(ex.args))
                logger.warning(channel_resp)
                print str(ex.args)
                print str(ex.message)
    logger.info("total playlist count"+str(total_result))
    logger.info("total playlists ---"+str(len(playlist_ids)))
    # return playlist_ids
    return get_video_ids(playlist_ids, channel_id)

def get_video_ids(playlist_ids, channel_id):
    video_ids=[]

    # workbook = xlsxwriter.Workbook(FILE_NAME)
    # worksheet = workbook.add_worksheet()
    playlist_video_map = dict()
    for playlist_id in playlist_ids:
        playlist_result = network_utils.get_videoIds_from_playlist(playlist_id, page_token=None)
        total_result = playlist_result['pageInfo']['totalResults']
        logger.info("playlist "+str(playlist_id)+" - - - - total number of video"+str(total_result))

        counter = total_result/50 + 1

        while(counter):
            for video in playlist_result['items']:
                if video['snippet']['resourceId']['kind'] == "youtube#video" and video['snippet']['resourceId']['videoId'] not in video_ids and video['snippet']['channelId'] == channel_id:
                    video_ids.append(video['snippet']['resourceId']['videoId'])
                    playlist_video_map[playlist_id] = video['snippet']['resourceId']['videoId']
            counter -= 1

            if counter > 0:
                try:
                    logger.info("next page token ----"+playlist_result['nextPageToken'])
                    playlist_resp = network_utils.get_videoIds_from_playlist(playlist_id, page_token=playlist_result['nextPageToken'])
                    logger.info("no of Items ----"+str(len(playlist_resp['items'])))
                # sleep(5)
                # logger.warning(channel_resp)
                except Exception as ex:
                    logger.warning("exception -- token "+str(ex.message)+"----"+str(ex.args))
                    print str(ex.args)
                    print str(ex.message)


    logger.info("total playlist count"+str(total_result))
    logger.info("video id present---"+str(len(video_ids)))
    logger.info("video ids--"+str(video_ids))
    return video_ids

if __name__ == "__main__":
    playList_ids = get_playlist_id(YOUTUBE_CHANNEL_ID, "")


