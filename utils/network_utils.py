__author__ = 'abhishekbharadwaj'

import urllib
import logging
import requests
import json
logger = logging.getLogger(__name__)
from  utils.constants import Youtube


def network_request(url, payload_dict):
    url_values = urllib.urlencode(payload_dict)
    request_url = url + "?" + url_values
    logger.error("request_url  "+request_url, exc_info=True)
    response = urllib.urlopen(request_url)
    res = response.read()
    logger.error("response  "+str(res), exc_info=True)
    return res


def get_channel_details(channel_id, page_token=None):
    if page_token is None:
        request_url = "https://www.googleapis.com/youtube/v3/search?key="+Youtube.YOUTUBE_APIS_KEYS+"&channelId="+channel_id+"&part=snippet,id&order=date&maxResults=50"
    else:
        request_url = "https://www.googleapis.com/youtube/v3/search?key="+Youtube.YOUTUBE_APIS_KEYS+"&channelId="+channel_id+"&part=snippet,id&order=date&maxResults=50&pageToken="+page_token
    # logger.error("request_url  "+request_url, exc_info=True)
    # print request_url
    response = urllib.urlopen(request_url)
    # print response
    res = response.read()
    # print json.loads(res)
    return json.loads(res)

    # logger.error("response  "+str(res), exc_info=True)


def get_video_details(video_id):
    request_url = "https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&key="+Youtube.YOUTUBE_APIS_KEYS+"&part=snippet,contentDetails,statistics,status"
    # print request_url
    response = urllib.urlopen(request_url)
    # print response
    res = response.read()
    # print json.loads(res)
    return json.loads(res)