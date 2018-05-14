import pafy
import platform
import os
from pathlib import Path
import re
import urllib.request
import urllib.error
from collections import OrderedDict


def bytes_2_human_readable(number_of_bytes):
    """ Coverts bytes to human readable format"""
    if number_of_bytes < 0:
        raise ValueError("!!! number_of_bytes can't be smaller than 0 !!!")

    step_to_greater_unit = 1024.

    number_of_bytes = float(number_of_bytes)
    unit = 'bytes'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'KB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'MB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'GB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'TB'

    precision = 1
    number_of_bytes = round(number_of_bytes, precision)

    return str(number_of_bytes) + ' ' + unit


def create_location(location):
    """ Creates/Setup the specified location"""
    # TODO: Location for windows
    home = str(Path.home())
    default_location = home + "/Downloads/Videos"
    is_default_location_exist = os.path.exists(default_location)

    if not location:
        location = default_location

    if not os.path.exists(location):
        print("Location does not exits. So, creating one instead.")
        try:
            os.makedirs(location)
        except PermissionError:
            print("Requested path is not valid. Downloading in default location -- " + default_location)
            if not is_default_location_exist:
                os.makedirs(default_location)
            else:
                location = default_location

    return location


def format_resolution(resolution):
    """Formatting the youtube video resolution to readable format
    Example: 4K, 1080, 720, 480, 360"""
    res = (resolution.split('x'))[1]
    if int(res) > 1440:
        res = "4K"

    return str(res)


def validate_video(url):
    try:
        pafy.new(url)
    except ValueError:
        return False

    return True


def fetch_video_playlist(url):
    """ Fetch youtube video links from youtube playlist links """
    sTUBE = ''
    cPL = ''
    amp = 0
    final_url = []

    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]

    else:
        print('Incorrect Playlist.')
        exit(1)

    try:
        yTUBE = urllib.request.urlopen(url).read()
        sTUBE = str(yTUBE)
    except urllib.error.URLError as e:
        print(e.reason)

    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, sTUBE)

    if mat:

        for PL in mat:
            yPL = str(PL)
            if '&' in yPL:
                yPL_amp = yPL.index('&')
            final_url.append('http://www.youtube.com/' + yPL[:yPL_amp])

        all_url = list(OrderedDict.fromkeys(final_url))

        return all_url

    else:
        print('No videos found.')
        exit(1)
