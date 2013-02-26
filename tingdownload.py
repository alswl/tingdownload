#!/usr/bin/env python2
#coding=utf-8

# desc: download mp3 from ting.baidu.com
# author: alswl <http://log4d.com>
# date: 2012-01-06

import sys
import os
from urlparse import urlparse
import urllib
import urllib2
import logging
import re
import argparse
import json

from BeautifulSoup import BeautifulSoup

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

reload(sys)
sys.setdefaultencoding(sys.getfilesystemencoding()) # for cross-platform

class DownloadError(Exception):
    """a user defined exception for download error"""
    pass

class NotFoundError(Exception):
    """a user defined exception for not found"""
    pass

class TooMoreFoundError(Exception):
    """a user defined exception for too more result found"""
    pass

class FileExistError(Exception):
    """a user defined exception for file exist"""
    pass

class TingDownloadInfo(object):
    """result info"""
    count = 0
    header = '== %(message)s (%(count)d) ==\n'
    logger_text = ''
    message = ''

    def log(self, text):
        self.logger_text += text + '\n'
        self.count += 1

    def get_result(self):
        if self.count == 0:
            return ''
        result = self.header %{'message': self.message, 'count': self.count}
        for line in self.logger_text:
            result += line
        return result + '\n'

class TingDownloadInfo200(TingDownloadInfo):
    def __init__(self):
        super(TingDownloadInfo200, self).__init__()
        self.message = 'Download success'

class TingDownloadInfo304(TingDownloadInfo):
    def __init__(self):
        super(TingDownloadInfo304, self).__init__()
        self.message = 'Download failed for file exists'

class TingDownloadInfo400(TingDownloadInfo):
    def __init__(self):
        super(TingDownloadInfo400, self).__init__()
        self.message = 'Download failed for too many result'

class TingDownloadInfo404(TingDownloadInfo):
    def __init__(self):
        super(TingDownloadInfo404, self).__init__()
        self.message = 'Download failed for not fount'

class TingDownloadInfo500(TingDownloadInfo):
    def __init__(self):
        super(TingDownloadInfo500, self).__init__()
        self.message = 'Download failed for network error'

class MusicInfo(object):
    """ting music"""

    def __init__(self, id, song_name, artist_name):
        self.id = id
        self.song_name = song_name
        self.artist_name = artist_name

    def __repr__(self):
        return u'%s %s - %s' %(self.id, self.artist_name, self.song_name)

class TingDownload(object):
    """a download helper for ting.baidu.com"""

    SEARCH_URL = u'http://openapi.baidu.com/public/2.0/mp3/info/suggestion?' \
                'format=json&word=%(word)s&callback=window.baidu.sug'
    DOWNLOAD_URL = u'http://ting.baidu.com/song/%s/download'
    TARGET_URL = u'http://ting.baidu.com%s'

    MUSICS_DIR = os.path.abspath('./musics')

    def __init__(self, name, is_auto_match=False):
        self.name = name
        self.is_auto_match = is_auto_match
        if not os.path.exists(self.MUSICS_DIR):
            os.mkdir(self.MUSICS_DIR)

    def download(self):
        try:
            self.music_info = self.search()
        except urllib2.URLError, e:
            logger.info('X Error, please check network.')
            raise DownloadError(e)
        except NotFoundError, e:
            logger.info(e)
            raise e
        except TooMoreFoundError, e:
            logger.info(e)
            raise e

        try:
            if os.path.exists(self.path_name):
                raise FileExistError('# Info, file: "%s" exists.' \
                                     %self.path_name)
            self.target_url = self.fetchMusic()
            self.write_file()
            logger.info('V Info, download complete.')
        except urllib2.URLError, e:
            logger.info(e)
            raise DownloadError(e)
        except FileExistError, e:
            logger.info(e)

    def search(self):
        word = urllib2.quote(self.name.encode('utf-8'))
        url = self.SEARCH_URL %{'word': word}
        handler = urllib2.urlopen(url)
        json_text  = handler.read()
        json_result = json.loads(json_text.strip()[17: -2])
        if len(json_result['song']) < 1:
            raise NotFoundError(u"X Error, can't find song: %s." %self.name)
        if len(json_result['song']) > 1 and not self.is_auto_match:
            raise TooMoreFoundError(
                u"# Error, too more result found for keyword: %s."
                %self.name
                )

        music = MusicInfo(json_result['song'][0]['songid'],
                          json_result['song'][0]['songname'],
                          json_result['song'][0]['artistname'])
        if len(json_result['song']) > 1:
            logger.info(u'# Info, auto match first one song: %s - %s.'
                        %(music.artist_name, music.song_name))
        self.path_name = os.path.join(
            self.MUSICS_DIR,
            music.artist_name + '-' \
            + music.song_name + '.mp3'
            )
        return music

    def fetchMusic(self):
        """get the link of music"""
        page = urllib2.urlopen(self.DOWNLOAD_URL %self.music_info.id).read()
        link = BeautifulSoup(page).a
        return self.TARGET_URL %link['href']

    def write_file(self):
        """save music to disk"""
        urllib.urlretrieve(self.target_url, self.path_name)

def zh2unicode(text):
    """
    Auto converter encodings to unicode
    It will test utf8, gbk, big5, jp, kr to converter"""
    for encoding in ('utf-8', 'gbk', 'big5', 'jp', 'euc_kr','utf16','utf32'):
        try:
            return text.decode(encoding)
        except:
            pass
    return text

def main():
    # prepare args
    parser = argparse.ArgumentParser(
        description='A script to download music from ting.baidu.com.'
    )
    parser.add_argument('-a', '--auto_match', action='store_true',
                        help='auto match first song')
    parser.add_argument('keywords', metavar='Keyword', type=str, nargs='*',)
    parser.add_argument('--input', '-i', help='a list file to input musics',
                        type=argparse.FileType('r'))
    args = parser.parse_args()

    keywords = args.keywords
    if args.input != None:
        keywords = zh2unicode(args.input.read()).splitlines()

    if len(keywords) == 0:
        parser.print_help()
        return
    is_auto_match = args.auto_match

    # prepare loggers
    info200 = TingDownloadInfo200()
    info304 = TingDownloadInfo304()
    info400 = TingDownloadInfo400()
    info404 = TingDownloadInfo404()
    info500 = TingDownloadInfo500()

    for name in keywords:
        try:
            logger.info('> Start search %s...' \
                     %name.strip())
            tingDownload = TingDownload(re.sub(r'\s+', ' ', name.strip()),
                                        is_auto_match=True)
            tingDownload.download()
            info200.log(name)
        except NotFoundError, e:
            info404.log(name)
            continue
        except TooMoreFoundError, e:
            info400.log(name)
            continue
        except DownloadError, e:
            info500.log(name)
            os.remove(tingDownload.path_name) # delte the error file
            continue
        except FileExistError, e:
            info304.log(name)
            continue
        except KeyboardInterrupt:
            os.remove(tingDownload.path_name) # delte the error file
            break

    print_result(info200, info304, info400, info404, info500)

def print_result(info200, info304, *failed_loggers):
    sys.stdout.write('\n')
    sys.stdout.write(info200.get_result())
    sys.stdout.write(info304.get_result())
    for logger in failed_loggers:
        sys.stdout.write(logger.get_result())

if __name__ == '__main__':
    main()
