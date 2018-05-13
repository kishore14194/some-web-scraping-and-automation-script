import pafy
import argparse
import sys

from video_dl_utils import format_resolution, bytes_2_human_readable, create_location,\
    validate_video

WEBM_FORMAT = 'webm'
DEFAULT_VERSION = 9


class Download:
    def __init__(self, url):
        self.video = pafy.new(url)
        self.title = self.video.title.encode('ascii', 'ignore').decode('ascii')
        self.streams = self.video.videostreams

    @property
    def best_resolution(self):
        best = self.video.getbest()
        best = format_resolution(best.resolution)
        return "Best Resolution - " + best

    @property
    def available_version(self):
        res_list = []
        for ind, s in enumerate(self.streams):
            res = format_resolution(s.resolution)
            size = s.get_filesize()
            ext = s.extension
            if ext == WEBM_FORMAT:
                continue

            human_readable = bytes_2_human_readable(size)
            avl_version = str(ind) + " - Resolution - " + res + " | Size - " + human_readable + " | Extension - " + ext
            res_list.append(avl_version)

        return "\n".join(res_list)

    def download_vid(self, location=None, version=None):
        location = create_location(location)
        if not version:
            version = DEFAULT_VERSION

        version = int(version)

        vid_download = self.streams[version]
        vid_download.download(filepath=location)
        return "Downloaded -- \"" + self.title + "\""

    def __str__(self):
        return self.title


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="YouTube Url")
    parser.add_argument("--path", help="Path to store the file")
    parser.add_argument("operation", help="best - Displays the best version, available_version - List of avaliable "
                                          "Version, download - Download the video",
                        choices=["best", "available_version", "download"])
    parser.add_argument("--version", help="Version to download")

    args = parser.parse_args()

    url = args.url
    DIR_LOC = args.path

    is_valid_video = validate_video(url)

    if not is_valid_video:
        print("-- Entered video is not valid - " + url + " --")
        sys.exit()

    download = Download(url)
    version = args.version

    if args.operation == "best":
        print(download.best_resolution)
    if args.operation == "available_version":
        print(download.available_version)
    if args.operation == "download":
        print(download.download_vid(DIR_LOC, version))

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
