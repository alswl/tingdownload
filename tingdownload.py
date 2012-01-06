#!/usr/bin/env python2
#coding=utf-8

# desc: download mp3 from ting.baidu.com
# author: alswl <http://log4d.com>
# date: 2012-01-03

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
            log.error(e)
            raise DownloadError(e)
        except NotFoundError, e:
            log.error(e)
            raise e
        except TooMoreFoundError, e:
            log.error(e)
            raise e

        self.target_url = self.fetchMusic()
        self.write_file()

    def search(self):
        word = urllib2.quote(self.name.encode('utf-8'))
        url = self.SEARCH_URL %{'word': word}
        handler = urllib2.urlopen(url)
        json_text  = handler.read()
        json_result = json.loads(json_text.strip()[17: -2])
        if len(json_result['song']) < 1:
            raise NotFoundError(u"can't find song %s" %self.name)
        elif len(json_result['song']) > 1:
            raise TooMoreFoundError(u"too more result found for keyword %s"
                                    %self.name)
        else:
            music = MusicInfo(json_result['song'][0]['songid'],
                              json_result['song'][0]['songname'],
                              json_result['song'][0]['artistname'])
            return music

    def fetchMusic(self):
        """get the link of music"""
        page = urllib2.urlopen(self.DOWNLOAD_URL %self.music_info.id).read()
        link = BeautifulSoup(page).a
        return self.TARGET_URL %link['href']

    def write_file(self):
        """save music to disk"""
        if os.path.exists(os.path.join(self.MUSICS_DIR, self.name)):
            raise FileExistError

        file = open(os.path.join(self.MUSICS_DIR,
                                 self.music_info.artist_name + '-' + \
                                 self.music_info.song_name + '.mp3'
                                ), 'w')
        handler = urllib2.urlopen(self.target_url)
        file.write(handler.read())
        file.close()

def main():
    # prepare args
    parser = argparse.ArgumentParser(
        description='download music from ting.baidu.com'
        )
    parser.add_argument('keywords',
                        metavar='N',
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

    # prepare logs
    log_200 = '== Download success ==\n'
    log_404 = '== Download failed for not fount == n'
    log_400 = '== Download failed for too many result ==\n'
    log_500 = '== Download failed for network error ==\n'
    log_304 = '== Download failed for file exists ==\n'

    for name in keywords:
        #log.debug(name)
        try:
            tingDownload = TingDownload(re.sub(r'\s+', ' ', name.strip()))
            #tingDownload.download() # FIXME
        except NotFoundError, e:
            log_404 += name +'\n'
            continue
        except TooMoreFoundError, e:
            log_400 += name +'\n'
            continue
        except DownloadError, e:
            log_500 += name +'\n'
            continue
        except FileExistError, e:
            log_304 += name +'\n'
            continue
        log_success += name + '\n'

    sys.stdout.write(log_200)
    sys.stderr.write(log_500 + '\n\n')
    sys.stderr.write(log_400 + '\n\n')
    sys.stderr.write(log_404)
    sys.stderr.write(log_304)

if __name__ == '__main__':
    main()
