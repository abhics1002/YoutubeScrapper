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
        request_url = "https://www.googleapis.com/youtube/v3/search?key="+Youtube.YOUTUBE_APIS_KEYS+"&channelId="+channel_id+"&part=snippet,id&order=date&maxResults=50&type=video"
    else:
        request_url = "https://www.googleapis.com/youtube/v3/search?key="+Youtube.YOUTUBE_APIS_KEYS+"&channelId="+channel_id+"&part=snippet,id&order=date&maxResults=50&type=video&pageToken="+page_token
    # logger.error("request_url  "+request_url, exc_info=True)
    # print request_url
    response = urllib.urlopen(request_url)
    # print response
    res = response.read()
    # print json.loads(res)
    return json.loads(res)

    # logger.error("response  "+str(res), exc_info=True)

def get_channel_details_before_time(channel_id, page_token=None, publishedBefore=None):
    if page_token is None:
        request_url = "https://www.googleapis.com/youtube/v3/search?key="+Youtube.YOUTUBE_APIS_KEYS+"&channelId="+channel_id+"&part=snippet,id&order=date&maxResults=50&type=video&publishedBefore="+publishedBefore
    else:
        request_url = "https://www.googleapis.com/youtube/v3/search?key="+Youtube.YOUTUBE_APIS_KEYS+"&channelId="+channel_id+"&part=snippet,id&order=date&maxResults=50&type=video&publishedBefore="+publishedBefore+"&pageToken="+page_token

    response = urllib.urlopen(request_url)
    res = response.read()
    return json.loads(res)


def get_video_details(video_id):
    request_url = "https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&key="+Youtube.YOUTUBE_APIS_KEYS+"&part=snippet,contentDetails,statistics,status"
    # print request_url
    response = urllib.urlopen(request_url)
    # print response
    res = response.read()
    # print json.loads(res)
    return json.loads(res)


def get_channel_details_by_video_count(channel_id, page_token=None):
    if page_token is None:
        request_url = "https://www.googleapis.com/youtube/v3/search?key="+Youtube.YOUTUBE_APIS_KEYS+"&channelId="+channel_id+"&part=snippet,id&order=viewCount&maxResults=50&type=video"
    else:
        request_url = "https://www.googleapis.com/youtube/v3/search?key="+Youtube.YOUTUBE_APIS_KEYS+"&channelId="+channel_id+"&part=snippet,id&order=viewCount&maxResults=50&type=video&pageToken="+page_token
    # logger.error("request_url  "+request_url, exc_info=True)
    # print request_url
    response = urllib.urlopen(request_url)
    # print response
    res = response.read()
    # print json.loads(res)
    return json.loads(res)


def get_channel_details_by_title(channel_id, page_token=None):
    if page_token is None:
        request_url = "https://www.googleapis.com/youtube/v3/search?key="+Youtube.YOUTUBE_APIS_KEYS+"&channelId="+channel_id+"&part=snippet,id&order=title&maxResults=50&type=video"
    else:
        request_url = "https://www.googleapis.com/youtube/v3/search?key="+Youtube.YOUTUBE_APIS_KEYS+"&channelId="+channel_id+"&part=snippet,id&order=title&maxResults=50&type=video&pageToken="+page_token
    # logger.error("request_url  "+request_url, exc_info=True)
    # print request_url
    response = urllib.urlopen(request_url)
    # print response
    res = response.read()
    # print json.loads(res)
    return json.loads(res)


def get_channel_details_by_rating(channel_id, page_token=None):
    if page_token is None:
        request_url = "https://www.googleapis.com/youtube/v3/search?key="+Youtube.YOUTUBE_APIS_KEYS+"&channelId="+channel_id+"&part=snippet,id&order=rating&maxResults=50&type=video"
    else:
        request_url = "https://www.googleapis.com/youtube/v3/search?key="+Youtube.YOUTUBE_APIS_KEYS+"&channelId="+channel_id+"&part=snippet,id&order=rating&maxResults=50&type=video&pageToken="+page_token
    # logger.error("request_url  "+request_url, exc_info=True)
    # print request_url
    response = urllib.urlopen(request_url)
    # print response
    res = response.read()
    # print json.loads(res)
    return json.loads(res)


def get_playlist_id(channel_id, page_token=None):
    if page_token is None:
        request_url = "https://www.googleapis.com/youtube/v3/playlists?key="+Youtube.YOUTUBE_APIS_KEYS+"&channelId="+channel_id+"&part=snippet,contentDetails,id&maxResults=50"
    else:
        request_url = "https://www.googleapis.com/youtube/v3/playlists?key="+Youtube.YOUTUBE_APIS_KEYS+"&channelId="+channel_id+"&part=snippet,contentDetails,id&maxResults=50&pageToken="+page_token
    # logger.error("request_url  "+request_url, exc_info=True)
    # print request_url
    response = urllib.urlopen(request_url)
    # print response
    res = response.read()
    # print json.loads(res)
    return json.loads(res)


def get_videoIds_from_playlist(playlist_id, page_token=None):

    if page_token is None:
        request_url = "https://www.googleapis.com/youtube/v3/playlistItems?key="+Youtube.YOUTUBE_APIS_KEYS+"&playlistId="+playlist_id+"&part=snippet,contentDetails,id&maxResults=50"
    else:
        request_url = "https://www.googleapis.com/youtube/v3/playlistItems?key="+Youtube.YOUTUBE_APIS_KEYS+"&playlistId="+playlist_id+"&part=snippet,contentDetails,id&maxResults=50&pageToken="+page_token
    # logger.error("request_url  "+request_url, exc_info=True)
    # print request_url
    response = urllib.urlopen(request_url)
    # print response
    res = response.read()
    # print json.loads(res)
    return json.loads(res)