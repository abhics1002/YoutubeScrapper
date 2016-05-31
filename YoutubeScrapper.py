__author__ = 'abhishekbharadwaj'

from utils import network_utils, FileWriter
from utils.constants import Youtube
import xlsxwriter, logging
import logging
from time import sleep

LOG_FILENAME = 'downloader.log'
logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

# YOUTUBE_CHANNEL_ID = 'UCV0DVncZjaudmyfZRrLZXVg'  # sacredverses - 1549
# YOUTUBE_CHANNEL_ID = 'UCDF_Bb6LDhHbJDassMsZ68Q'  # anandmurtigurumaa - 723
# YOUTUBE_CHANNEL_ID = 'UCbsVNxLVgkSRCYs49xa8W0w'  # gurumaaashram - 2150
# YOUTUBE_CHANNEL_ID = 'UCPqYEzL1g3s4g_N_Np42Xdw'  # Mystica Music - 702
# YOUTUBE_CHANNEL_ID = 'UCuVP4Q6LoWmSyl3d9xSxaEA'  # GIANI SANT SINGH JI MASKEEN 1296
YOUTUBE_CHANNEL_ID = 'UCGje2kPIo-0M3fycdAghUsQ'    # Endedhaivam

FILE_NAME = 'Endedhaivam.xlsx'
DOWNLOADED_VIDEO_IDS = "video_ids_file_Endedhaivam"
PLAYLIST_FILE_NAME = "play_list_Endedhaivam.xlsx"

def start_scrapping(channel_ids):

    channel_video_mapping_dict = dict()
    for channel_id in channel_ids:
        # network_utils.network_request(Youtube.YOUTUBE_APIS_ENDPOINT, )
        channel_resp = network_utils.get_channel_details(channel_id)
        total_result = channel_resp['pageInfo']['totalResults']
        logger.info("channel "+str(channel_id)+" ---- total number of video"+str(total_result))
        counter = total_result/50 + 1
        invalid_video_count = 0
        while(counter):
            for video in channel_resp['items']:
                if video['id']['kind'] == "youtube#video":
                    # print video['id']['videoId']
                    if channel_id in channel_video_mapping_dict:
                        channel_video_mapping_dict[channel_id].append(video['id']['videoId'])
                        last_publish_date = video['snippet']['publishedAt']
                    else:
                        channel_video_mapping_dict[channel_id] = [video['id']['videoId']]
                        last_publish_date = video['snippet']['publishedAt']
                else:
                    logger.info("this item is not video")
                    invalid_video_count += 1

            counter -= 1

            if counter > 0:
                try:
                    logger.info("next page token ----"+channel_resp['nextPageToken'])
                    channel_resp = network_utils.get_channel_details(channel_id, channel_resp['nextPageToken'])
                    logger.info("no of Items ----"+str(len(channel_resp['items'])))

                    # sleep(5)
                    # logger.warning(channel_resp)
                except Exception as ex:
                    logger.warning("exception -- token "+str(ex.message)+"----"+str(ex.args))
                    logger.warning(channel_resp)
                    print str(ex.args)
                    print str(ex.message)

    logger.info("total video count"+str(total_result))
    logger.info("invalid video count"+str(invalid_video_count))
    logger.info("total video retrived "+str(len(channel_video_mapping_dict[YOUTUBE_CHANNEL_ID])))
    logger.info("finding video before publish date"+str(last_publish_date))
    # scrap_before_published_date("UCV0DVncZjaudmyfZRrLZXVg", last_publish_date)
    channel_data = scrap_before_published_date(channel_id, last_publish_date, channel_video_mapping_dict)
    data = scrap_using_viewCount(channel_id, channel_data)
    title_result = scrap_using_title(channel_id, data)
    rating_result = scrap_using_rating(channel_id, title_result)
    return rating_result



def scrap_before_published_date(channel_id, publish_date, channel_video_mapping_dict):
    logger.info("last publish date"+str(publish_date))
    print str(publish_date)
    channel_resp = network_utils.get_channel_details_before_time(channel_id, page_token=None, publishedBefore=publish_date)
    total_result = channel_resp['pageInfo']['totalResults']
    logger.info("channel "+str(channel_id)+" - - - - total number of video"+str(total_result))
    counter = total_result/50 + 1

    # channel_video_mapping_dict = dict()
    count_already_present = 0
    logger.info("no of Items ----"+str(len(channel_resp['items'])))
    while(counter):
        for video in channel_resp['items']:
            if video['id']['videoId'] not in channel_video_mapping_dict[channel_id]:
                channel_video_mapping_dict[channel_id].append(video['id']['videoId'])
            else:
                count_already_present +=1

        counter -= 1

        if counter > 0:
            try:
                logger.info("next page token ----"+channel_resp['nextPageToken'])
                channel_resp = network_utils.get_channel_details_before_time(channel_id, page_token=channel_resp['nextPageToken'], publishedBefore=publish_date)
                logger.info("no of Items ----"+str(len(channel_resp['items'])))

                # sleep(5)
                # logger.warning(channel_resp)
            except Exception as ex:
                logger.warning("exception -- token "+str(ex.message)+"----"+str(ex.args))
                logger.warning(channel_resp)
                print str(ex.args)
                print str(ex.message)

    logger.info("total video count"+str(total_result))
    logger.info("total video retrived "+str(len(channel_video_mapping_dict[channel_id])))
    logger.info("count_already_present---"+str(count_already_present))
    return channel_video_mapping_dict


def scrap_using_rating(channel_id,channel_video_mapping_dict):
    channel_resp = network_utils.get_channel_details_by_rating(channel_id, page_token=None)
    total_result = channel_resp['pageInfo']['totalResults']
    logger.info("channel "+str(channel_id)+" - - - - total number of video"+str(total_result))
    counter = total_result/50 + 1

    # channel_video_mapping_dict = dict()
    count_already_present = 0
    logger.info("no of Items ----"+str(len(channel_resp['items'])))
    while(counter):
        for video in channel_resp['items']:
            if video['id']['videoId'] not in channel_video_mapping_dict[channel_id]:
                channel_video_mapping_dict[channel_id].append(video['id']['videoId'])
            else:
                count_already_present +=1

        counter -= 1

        if counter > 0:
            try:
                logger.info("next page token ----"+channel_resp['nextPageToken'])
                channel_resp = network_utils.get_channel_details_by_rating(channel_id, page_token=channel_resp['nextPageToken'])
                logger.info("no of Items ----"+str(len(channel_resp['items'])))

                # sleep(5)
                # logger.warning(channel_resp)
            except Exception as ex:
                logger.warning("exception -- token "+str(ex.message)+"----"+str(ex.args))
                logger.warning(channel_resp)
                print str(ex.args)
                print str(ex.message)

    logger.info("total video count"+str(total_result))
    logger.info("total video retrived "+str(len(channel_video_mapping_dict[channel_id])))
    logger.info("count_already_present---"+str(count_already_present))
    return channel_video_mapping_dict


def scrap_using_title(channel_id,channel_video_mapping_dict):
    channel_resp = network_utils.get_channel_details_by_title(channel_id, page_token=None)
    total_result = channel_resp['pageInfo']['totalResults']
    logger.info("channel "+str(channel_id)+" - - - - total number of video"+str(total_result))
    counter = total_result/50 + 1

    # channel_video_mapping_dict = dict()
    count_already_present = 0
    logger.info("no of Items ----"+str(len(channel_resp['items'])))
    while(counter):
        for video in channel_resp['items']:
            if video['id']['videoId'] not in channel_video_mapping_dict[channel_id]:
                channel_video_mapping_dict[channel_id].append(video['id']['videoId'])
            else:
                count_already_present +=1

        counter -= 1

        if counter > 0:
            try:
                logger.info("next page token ----"+channel_resp['nextPageToken'])
                channel_resp = network_utils.get_channel_details_by_title(channel_id, page_token=channel_resp['nextPageToken'])
                logger.info("no of Items ----"+str(len(channel_resp['items'])))

                # sleep(5)
                # logger.warning(channel_resp)
            except Exception as ex:
                logger.warning("exception -- token "+str(ex.message)+"----"+str(ex.args))
                logger.warning(channel_resp)
                print str(ex.args)
                print str(ex.message)

    logger.info("total video count"+str(total_result))
    logger.info("total video retrived "+str(len(channel_video_mapping_dict[channel_id])))
    logger.info("count_already_present---"+str(count_already_present))
    return channel_video_mapping_dict


def scrap_using_videoCount():
    pass

def scrap_using_viewCount(channel_id,channel_video_mapping_dict):
    channel_resp = network_utils.get_channel_details_by_video_count(channel_id, page_token=None)
    total_result = channel_resp['pageInfo']['totalResults']
    logger.info("channel "+str(channel_id)+" - - - - total number of video"+str(total_result))
    counter = total_result/50 + 1

    # channel_video_mapping_dict = dict()
    count_already_present = 0
    logger.info("no of Items ----"+str(len(channel_resp['items'])))
    while(counter):
        for video in channel_resp['items']:
            if video['id']['videoId'] not in channel_video_mapping_dict[channel_id]:
                channel_video_mapping_dict[channel_id].append(video['id']['videoId'])
            else:
                count_already_present +=1

        counter -= 1

        if counter > 0:
            try:
                logger.info("next page token ----"+channel_resp['nextPageToken'])
                channel_resp = network_utils.get_channel_details_by_video_count(channel_id, page_token=channel_resp['nextPageToken'])
                logger.info("no of Items ----"+str(len(channel_resp['items'])))

                # sleep(5)
                # logger.warning(channel_resp)
            except Exception as ex:
                logger.warning("exception -- token "+str(ex.message)+"----"+str(ex.args))
                logger.warning(channel_resp)
                print str(ex.args)
                print str(ex.message)

    logger.info("total video count"+str(total_result))
    logger.info("total video retrived "+str(len(channel_video_mapping_dict[channel_id])))
    logger.info("count_already_present---"+str(count_already_present))
    return channel_video_mapping_dict




def scrap_video_data(video_ids):
    # video_resp = network_utils.get_video_details(video_ids)
    # print video_resp
    workbook = xlsxwriter.Workbook(FILE_NAME)
    worksheet = workbook.add_worksheet()
    row =1
    logger.info("writing into file " + str(len(video_ids)))
    for v_id in video_ids:
        video_resp = network_utils.get_video_details(v_id)
        # print video_resp
        try:
            if YOUTUBE_CHANNEL_ID == video_resp['items'][0]['snippet']['channelId']:
                FileWriter.write_file(video_resp, workbook, worksheet, row=row)
                row = row + 1
        except Exception as ex:
            logger.exception("exception ========")
    workbook.close()
    logger.info("writing into file completed.")
    return video_resp



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

    return get_video_ids(playlist_ids, channel_id)


def get_video_ids(playlist_ids, channel_id):
    video_ids=[]

    for playlist_id in playlist_ids:
        playlist_result = network_utils.get_videoIds_from_playlist(playlist_id, page_token=None)
        total_result = playlist_result['pageInfo']['totalResults']
        logger.info("playlist "+str(playlist_id)+" - - - - total number of video"+str(total_result))

        counter = total_result/50 + 1

        while(counter):
            for video in playlist_result['items']:
                if video['snippet']['resourceId']['kind'] == "youtube#video" and video['snippet']['resourceId']['videoId'] not in video_ids and video['snippet']['channelId'] == channel_id:
                    video_ids.append(video['snippet']['resourceId']['videoId'])

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
    print "Inside main"
    logger.info("inside main")
    # channel_ids = ['UCNJcSUSzUeFm8W9P7UUlSeQ'] #TVF
    channel_ids =[YOUTUBE_CHANNEL_ID] # sacredverses - 1549
    # channel_ids = ['UCDF_Bb6LDhHbJDassMsZ68Q'] # anandmurtigurumaa - 723
    # channel_ids = ['UCbsVNxLVgkSRCYs49xa8W0w']  # gurumaaashram - 2150
    # channel_ids = ['UCPqYEzL1g3s4g_N_Np42Xdw'] # Mystica Music - 702
    # channel_ids = ['UCuVP4Q6LoWmSyl3d9xSxaEA'] # GIANI SANT SINGH JI MASKEEN 1296
    video = start_scrapping(channel_ids)
    playlist_video_ids = get_playlist_id(YOUTUBE_CHANNEL_ID,"")

    video_ids = video[YOUTUBE_CHANNEL_ID]
    already_present = 0
    for i in playlist_video_ids:
        if i in video_ids:
            already_present +=1
        else:
            video_ids.append(i)

    logger.info("already_present count"+str(already_present))
    logger.info("video ids count"+str(len(video_ids)))

    duplicate_count=0
    new_count =0
    with open(DOWNLOADED_VIDEO_IDS) as data_file:
        for i in data_file:
            if i.rstrip() in video_ids:
                duplicate_count += 1
            else:
                new_count += 1
                logger.info("new Ids -"+i.rstrip())
                video_ids.append(i)

    logger.info("already_present count"+str(duplicate_count))
    logger.info("new_count count"+str(new_count))
    logger.info("video ids count"+str(len(video_ids)))
    video_resp = scrap_video_data(video_ids)
