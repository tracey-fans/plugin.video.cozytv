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
from bs4 import BeautifulSoup
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
    Create the list of video categories in the Kodi interface. It does it by looking
    at all the dropdown items in the hamburger on the front page. Currently it
    only recognises AIU as a content creator
    """
    
    
    r = requests.api.get('https://censored.tv')
    
    soup = BeautifulSoup(r.content, 'html.parser')
    
    set_of_hrefs = set()

    for link in soup.find_all("a", class_="dropdown-item"):
        # Look for links that are relative and have an image attached. Those are
        # the shows
        if link.img != None and link.get("href", None) != None:
            if urlparse(link["href"]).netloc == "":

                # Looks for duplicates
                if link["href"] in set_of_hrefs:
                    # Is a duplicate. Do nothing
                    pass
                else:
                    # Not a duplicate

                    set_of_hrefs.add(link["href"])

                    img_lnk = link.img["src"]
                    info_txt = link.text.strip()
                    list_item = xbmcgui.ListItem(label=info_txt)
                    list_item.setArt({'thumb': img_lnk,
                                      'icon': img_lnk,
                                      'fanart': img_lnk})
                    list_item.setInfo('video', {'title': info_txt, 'genre': info_txt})

                    if "UNSTOPPABLE" in info_txt.upper():
                        # Make sure AIU sorts at the top of the list. This is for
                        # my benefit since I like this creator. Could possibly
                        # become an option?
                        list_item.setProperty("SpecialSort", "top")

                    url = get_url(action='listing', category=link["href"])
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
        page_str = "?page={0}".format(page)
    else:
        page_str = ""  # ...or ?page=1 also works.
    r = requests.api.get(urljoin('https://censored.tv', category + page_str))
    
    soup = BeautifulSoup(r.content, 'html.parser')


    for link in soup.find_all("div", class_="card my-3 my-lg-0"):
        
        best_href = None
        best_title = "No title"
        best_img = ""
        bug_img = ""
        
        try:
            bug_img = urljoin("https://censored.tv", link.img["src"])
        except:
            pass
        
        
        # Try to parse the "style" component to get a single-quote-denominated url
        # out of it. Don't worry too much if anything fails, we can always fall back
        # to an empty picture.
        if link.img["style"] != None:
          
            p = re.compile("background-image:.*url\('(.*)'.*")
            m = p.match(link.img["style"])
            
            if m != None:
                try:
                    best_img = m.group(1)
                except:
                    pass
                    
        
                
            for n in link.find_all("div", class_="card-body"):
                for q in n.find_all("a"):
                    best_href = q["href"]
                    for t in q.find_all(class_="card-title"):
                        best_title = t.text
                            
        if best_href != None:

            # Create a list item with a text label and a thumbnail image.
            list_item = xbmcgui.ListItem(label=best_title, label2="XYZ")
            # Set additional info for the list item.
            list_item.setInfo('video', {'title': best_title, 'genre': 'Censored TV'})
            # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
            # Here we use the same image for all items for simplicity's sake.
            list_item.setArt(
                {'thumb' : best_img,       # Next to item in list
                 'icon'  : best_img,       # Not used?
                 'fanart': bug_img,        # Background.
                 'poster': best_img        # Main image for vid
                })
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
    if True:
      
        if soup.find_all(class_="page-link", rel="next"):
            # The page has a "Next" button. This will normally be the case, except
            # if it's the last page of content

            list_item = xbmcgui.ListItem(label=xbmc.getLocalizedString(209))  # "Next"
            url = get_url(action='listing', category=category, page=str(page+1))
            # is_folder = True means that this item opens a sub-list of lower level items.
            is_folder = True
            # set a special sort property
            list_item.setProperty("SpecialSort", "bottom")
            # Add our item to the Kodi virtual folder listing.
            xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
        
        
    
    
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    
    # We have got to this point without signing in. At this stage can just do a sign
    # in and read. The session doesn't need to persist beyond this.
    
    session = requests.Session()
    
    rr = session.get("https://censored.tv/login")

    soup = BeautifulSoup(rr.content, 'html.parser')
    
    
    the_email = xbmcaddon.Addon().getSettingString('email')
    the_password = xbmcaddon.Addon().getSettingString('password')
    the_preferred_resolution = "1920x1080"    # Will make this one a setting later
    

    post = ""

    for m in soup.find_all("form"):
        is_login = False
        try:
            is_login = (m['action'] == '/login')
        except KeyError:
            pass
        if is_login:
            for q in m.find_all("input"):
                if q["name"] == "_token":
                    # Need to have received a token
                    post = m["action"]
                    post_val = {q["name"]: q["value"], "email": the_email, "password": the_password}


    if len(post) > 1:
        r = session.post(urljoin("https://censored.tv", post), post_val)

        # Discard r, we don't need it. All we need are the cookies.
      
    
    ## Now load in the requested file
    #
    
    r3 = session.get(urljoin("https://censored.tv", path))

    soup3 = BeautifulSoup(r3.content, 'html.parser')


    content_links = []

    for link in soup3.find_all(type="application/x-mpegURL"):
        content_links.append(link.get('src'))
        


    if len(content_links) < 1:
        # No content. This tends to happen if the user's password is wrong. Send
        # a message to that extent. TODO: use the translation system!!
        dialog = xbmcgui.Dialog()
        dialog.notification('Password wrong', 'Could not log onto Censored.TV. Check e-mail and password settings in the Configuration of this add-on.', xbmcgui.NOTIFICATION_INFO, 5000)
        xbmc.log("CENSOREDTV: No content links found. Exiting", xbmc.LOGINFO)
        return


    ## Read the first content file
    #
    
    r4 = session.get(content_links[0])
    


    ## Parse the contents to get the right resolution
    #
    f_5 = ""
    f_6 = ""

    found_line_preferred = False
    found_line_other = False

    for line in r4.text.splitlines():
        if line[:18] == "#EXT-X-STREAM-INF:":
            if line.find("RESOLUTION=" + the_preferred_resolution) >= 0:
                found_line_preferred = True
            elif line.find("RESOLUTION=") >= 0:
                found_line_other = True
        else:
            if found_line_preferred:
                f_5 = line
                break
            if found_line_other and f_6 == "":
                f_6 = line
            found_line_preferred = False
            found_line_other = False


    if len(f_5) <= 0 and len(f_6) <= 0:
        xbmc.log("CENSOREDTV: Haven't found the right resolution", xbmc.LOGINFO)
        return



    if f_5 != "":
        f_7 = urljoin(content_links[0], f_5)
    else:
        f_7 = urljoin(content_links[0], f_6)



    ## Read the file
    #
    r_5 = session.get(f_7)
    

    s_7 = set()


    ## Look for any non-empty line that doesn't start "#":
    #
    for line in r_5.text.splitlines():
        if len(line) > 0 and line[0] != '#':
            s_7.add(line)


    if len(s_7) == 0:
        xbmc.log("CENSOREDTV: Did not find content", xbmc.LOGINFO)
        return
    elif len(s_7) == 1:
        # Exactly one piece of content pointed to. Send that piece to Kodi, it works
        # better to do that way
        SEND_1 = urljoin(f_7, next(iter(s_7)))
    else:
        # More than one piece of content. We have no choice but to send the whole thing
        SEND_1 = f_7


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
