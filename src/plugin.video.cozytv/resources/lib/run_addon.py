# -*- coding: utf-8 -*-
"""
    Copyright (C) 2022 tracey-fans (plugin.video.cozytv)

    SPDX-License-Identifier: MIT
    See LICENSES/MIT.md for more information.
"""
import sys
from future.moves.urllib.parse import urlparse, urlencode, urljoin, parse_qsl
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

import requests.api
import json
import re

_url = ""
_handle = 0

def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def list_categories():
    """
    Create the list of video categories in the Kodi interface. Currently only one
    is available, and it is hard-coded.
    """
    
    r = requests.api.get(urljoin('https://api.cozy.tv', 'cache/homepage'))
    j = json.loads(r.text)
    
    for USER in j['users']:
    
        img_lnk = USER['avatarUrl']
        info_txt = USER['displayName']
        list_item = xbmcgui.ListItem(label=info_txt)
        list_item.setArt({'thumb': img_lnk,
                          'icon': img_lnk,
                          'fanart': img_lnk})
        list_item.setInfo('video', {'title': info_txt, 'genre': info_txt})

        url = get_url(action='listing', category="/cache/{0}/replays".format(USER['name']))
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def list_videos(category, page):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    
    if page > 1:
        page_str = ""
    else:
        page_str = ""
    r = requests.api.get(urljoin('https://api.cozy.tv', category + page_str))
    
    j = json.loads(r.text)
    
    for item in j['replays']:
      
        best_title = item['title']
        best_href = "replays/" + item['user'] + "/" + item['id']

        if best_href != None:

            # Create a list item with a text label and a thumbnail image.
            list_item = xbmcgui.ListItem(label=best_title, label2=item['id'])
            # Set additional info for the list item.
            list_item.setInfo('video', {'title': best_title, 'genre': ''})
            # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
            # Here we use the same image for all items for simplicity's sake.
            #list_item.setArt(
            #    {'thumb' : best_img,       # Next to item in list
            #     'icon'  : best_img,       # Not used?
            #     'fanart': bug_img,        # Background.
            #     'poster': best_img        # Main image for vid
            #    })
            # Set 'IsPlayable' property to 'true'.
            # This is mandatory for playable items!
            list_item.setProperty('IsPlayable', 'true')
            # Create a URL for a plugin recursive call.
            url = get_url(action='play', video=best_href)
            # Add the list item to a virtual Kodi folder.
            # is_folder = False means that this item won't open any sub-list.
            is_folder = False
            # Add our item to the Kodi virtual folder listing.
            xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    # Don't add a sort method for the virtual folder items. It seems that the
    # default is to sort in the order they're added, which is fine. Sorting by
    # tracknumber causes a number to appear in front of every label in the list
    # which looks naff.
    #xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_TRACKNUM)
    
    
    # Add a "Next" option if supported
    #if True:
    #  
    #    if soup.find_all(class_="page-link", rel="next"):
    #        # The page has a "Next" button. This will normally be the case, except
    #        # if it's the last page of content

    #        list_item = xbmcgui.ListItem(label=xbmc.getLocalizedString(209))  # "Next"
    #        url = get_url(action='listing', category=category, page=str(page+1))
    #        # is_folder = True means that this item opens a sub-list of lower level items.
    #        is_folder = True
    #        # set a special sort property
    #        list_item.setProperty("SpecialSort", "bottom")
    #        # Add our item to the Kodi virtual folder listing.
    #        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
        
        
    
    
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    
    SEND_1 = urljoin('https://cozycdn.foxtrotstream.xyz', path + '/index.m3u8')

    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=SEND_1)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(params['category'], int(params.get('page', '1')))
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories()


def run(argv):
    global _url
    global _handle
    
    # Get the plugin url in plugin:// notation.
    _url = sys.argv[0]
    # Get the plugin handle as an integer number.
    _handle = int(sys.argv[1])
    
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(argv[2][1:])
