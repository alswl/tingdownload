#!/usr/bin/env python2
#coding=utf-8

# desc: download mp3 from ting.baidu.com
# author: alswl <http://log4d.com>
# date: 2012-01-06

import sys
import os
from urlparse import urlparse
import urllib2
import logging
import re
import argparse

import simplejson as json
from BeautifulSoup import BeautifulSoup

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
#log.setLevel(logging.ERROR)
log.setLevel(logging.DEBUG)

reload(sys)
sys.setdefaultencoding('utf-8')

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
    log_text = ''
    message = ''

    def __init__(self):
        pass

    def log(self, text):
        self.log_text += text + '\n'
        self.count += 1

    def get_result(self):
        if self.count == 0:
            return ''
        result = self.header %{'message': self.message, 'count': self.count}
        for line in self.log_text:
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

    def __init__(self, name):
        self.name = name
        if not os.path.exists(self.MUSICS_DIR):
            os.mkdir(self.MUSICS_DIR)

    def download(self):
        try:
            self.music_info = self.search()
        except urllib2.URLError, e:
            log.info('# Failed: Check network.')
            raise DownloadError(e)
        except NotFoundError, e:
            log.info(e)
            raise e
        except TooMoreFoundError, e:
            log.info(e)
            raise e

        try:
            if os.path.exists(self.path_name):
                raise FileExistError('# Info: File "%s" exists.' \
                                     %self.path_name)
            self.target_url = self.fetchMusic()
            self.write_file()
        except urllib2.URLError, e:
            log.info(e)
            raise DownloadError(e)
        except FileExistError, e:
            log.info(e)

    def search(self):
        word = urllib2.quote(self.name.encode('utf-8'))
        url = self.SEARCH_URL %{'word': word}
        handler = urllib2.urlopen(url)
        json_text  = handler.read()
        json_result = json.loads(json_text.strip()[17: -2])
        if len(json_result['song']) < 1:
            raise NotFoundError(u"#Failed: Can't find song %s." %self.name)
        elif len(json_result['song']) > 1:
            raise TooMoreFoundError(
                u"Failed: Too more result found for keyword %s."
                %self.name
                )
        else:
            music = MusicInfo(json_result['song'][0]['songid'],
                              json_result['song'][0]['songname'],
                              json_result['song'][0]['artistname'])
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
        file = open(self.path_name, 'w')
        handler = urllib2.urlopen(self.target_url)
        file.write(handler.read())
        file.close()

def main():
    # prepare args
    parser = argparse.ArgumentParser(
        description='A script to download music from ting.baidu.com.'
        )
    parser.add_argument('keywords',
                        metavar='Keyword',
                        type=str,
                        nargs='*',
                       )
    parser.add_argument('--input', '-i',
                        help='a list file to input musics',
                        type=argparse.FileType('r'))
    args = parser.parse_args()
    keywords = args.keywords
    if args.input != None:
        keywords += args.input.read().splitlines()
    if len(keywords) == 0:
        parser.print_help()

    # prepare logs
    log200 = TingDownloadInfo200()
    log304 = TingDownloadInfo304()
    log400 = TingDownloadInfo400()
    log404 = TingDownloadInfo404()
    log500 = TingDownloadInfo500()

    for name in keywords:
        #log.debug(name)
        try:
            log.info('> Start download %s...' \
                     %name.strip())
            tingDownload = TingDownload(re.sub(r'\s+', ' ', name.strip()))
            tingDownload.download()
            log200.log(name)
        except NotFoundError, e:
            log404.log(name)
            continue
        except TooMoreFoundError, e:
            log400.log(name)
            continue
        except DownloadError, e:
            log500.log(name)
            os.remove(tingDownload.path_name) # delte the error file
            continue
        except FileExistError, e:
            log304.log(name)
            continue
        except KeyboardInterrupt:
            os.remove(tingDownload.path_name) # delte the error file
            break

    print_result(log200, log304, log400, log404, log500)

def print_result(log200, log304, *failed_logs):
    sys.stdout.write('\n')
    sys.stdout.write(log200.get_result())
    sys.stdout.write(log304.get_result())
    for log in failed_logs:
        sys.stdout.write(log.get_result())

if __name__ == '__main__':
    main()
