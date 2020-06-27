#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''Capture pictures from telegram channel
Below parameters need replace to yours
    - api_id
    - api_hash
    - proxy
Notice: 
    First time you may need enter phone number and get login code
'''

import os
import sys
import socks

from telethon import TelegramClient, sync
from telethon.tl.types import InputMessagesFilterPhotos
from telethon.helpers import TotalList


def get_path(channel):
    home_path = os.path.expanduser('~')
    path = os.path.join(home_path, 'Pictures/python/telegram', channel)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def open_client():
    # get api_id and api_hash from https://my.telegram.org/apps
    api_id = None
    api_hash = None

    if not api_id or not api_hash:
        print('Please set api_id and api_hash, you can get it from https://my.telegram.org/apps')
        sys.exit(1)

    # socks5 proxy, can set to be 'None' if no need
    proxy = (socks.SOCKS5, "localhost", 1080)
    return TelegramClient('tg_session', api_id=api_id,
                          api_hash=api_hash, proxy=proxy).start()


def get_photos(client, channel):
    tg_link = "https://t.me/" + channel

    # get photos
    print('Getting photos from ' + tg_link)
    return client.get_messages(tg_link, None, filter=InputMessagesFilterPhotos)


def main():
    tg_client = open_client()
    tg_channel = input('Please input telegram channel name: ')

    photos = get_photos(tg_client, tg_channel)
    total = photos.total

    save_path = get_path(tg_channel)

    print('Start downloading photos...')
    index = 0
    for photo in photos:
        filename = os.path.join(save_path, str(photo.id) + '.jpg')
        index = index + 1
        print("downloading {}/{} : {}".format(index, total, filename))
        tg_client.download_media(photo, filename)

    tg_client.disconnect()
    print("Done.")


if __name__ == "__main__":
    main()
