import pafy
import argparse

DIR_LOC = "/Users/kishore/Documents/Video/"
# DIR_LOC = None

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


def format_resolution(resolution):
    res = (resolution.split('x'))[1]
    if int(res) > 1440:
        res = "4K"

    return str(res)


class Download():
    def __init__(self, url):
        self.video = pafy.new(url)
        self.title = self.video.title
        self.streams = self.video.videostreams

    def best_resolution(self):
        best = self.video.getbest()
        return best

    def available_version(self):
        res_list = []
        for s in self.streams:
            res = format_resolution(s.resolution)
            size = s.get_filesize()
            ext = s.extension
            human_readable = bytes_2_human_readable(size)
            avl_version = "Resolution - " + res + " | Size - " + human_readable + " | Extension - " + ext
            res_list.append(avl_version)

        return "\n".join(res_list)

    def download_vid(self, location):
        vid_download = self.streams[-1]
        vid_download.download(filepath=location)
        return "Downloaded"


# d = Download("https://www.youtube.com/watch?v=R3GfuzLMPkA")
# DIR_LOC = "/Users/kishore/Documents/Video/"
# print(d.best_resolution())
# print(d.available_version())
# print(d.download_vid(DIR_LOC))

# url = "https://www.instagram.com/p/BikYx5agUBw/"
# a = requests.get(url).text
# insta_link = re.findall('(?<=/)[\w\-\_]+\.mp4', a)
# insta_link = re.findall("https://instagram[\s\S]*?.mp4", a)
# insta_link = list(set(insta_link))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="YouTube Url")
    parser.add_argument("--path", help="Path to store the file")
    parser.add_argument("--operation", help="Options - best, version, download",
                        choices=["best", "version", "download"])

    args = parser.parse_args()

    url = args.url
    DIR_LOC = args.path
    download = Download(url)

    if args.operation == "best":
        print(download.best_resolution())
