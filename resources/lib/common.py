# -*- coding: utf-8 -*-

import sys
import urllib
import urlparse
import time
import datetime
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import uuid
from hashlib import md5
from inputstreamhelper import Helper

addon_handle = int(sys.argv[1])
addon = xbmcaddon.Addon()
dialog = xbmcgui.Dialog()
addon_id = addon.getAddonInfo('id')
addon_name = addon.getAddonInfo('name')
addon_version = addon.getAddonInfo('version')
icon = addon.getAddonInfo('icon')
fanart = addon.getAddonInfo('fanart')
content = addon.getSetting('content')
view_id = addon.getSetting('view_id')
force_view = addon.getSetting('force_view') == 'true'

api_base = 'https://isl.dazn.com/misl/'

time_format = '%Y-%m-%dT%H:%M:%SZ'
date_format = '%Y-%m-%d'

def log(msg):
    xbmc.log(str(msg), xbmc.LOGNOTICE)

def build_url(query):
    return sys.argv[0] + '?' + urllib.urlencode(query)

def get_language():
    language = xbmc.getLanguage().split(' (')[0]
    return xbmc.convertLanguage(language, xbmc.ISO_639_1)

def utfenc(text):
    result = text
    if isinstance(text, unicode):
        result = text.encode('utf-8')
    return result

def getString(id_):
    return addon.getLocalizedString(id_)

def time_stamp(str_date):
    return datetime.datetime.fromtimestamp(time.mktime(time.strptime(str_date,time_format)))

def timedelta_total_seconds(timedelta):
    return (
        timedelta.microseconds + 0.0 +
        (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6

def utc2local(date_string):
    if str(date_string).startswith('2'):
        utc = datetime.datetime(*(time.strptime(date_string, time_format)[0:6]))
        epoch = time.mktime(utc.timetuple())
        offset = datetime.datetime.fromtimestamp(epoch) - datetime.datetime.utcfromtimestamp(epoch)
        return (utc + offset).strftime(time_format)

def uniq_id():
    device_id = ''
    mac_addr = xbmc.getInfoLabel('Network.MacAddress')
    if not ":" in mac_addr: mac_addr = xbmc.getInfoLabel('Network.MacAddress')
    # hack response busy
    i = 0
    while not ":" in mac_addr and i < 3:
        i += 1
        time.sleep(1)
        mac_addr = xbmc.getInfoLabel('Network.MacAddress')
    if ":" in mac_addr:
        device_id = str(uuid.UUID(md5(str(mac_addr.decode("utf-8"))).hexdigest()))
    else:
        log("[{0}] error: failed to get device id ({1})".format(addon_id, str(mac_addr)))
        dialog.ok(addon_name, getString(30051))
    addon.setSetting('device_id', device_id)
    return device_id

def is_settings():
    xbmcaddon.Addon(id='inputstream.adaptive').openSettings()

def is_helper():
    helper = Helper(protocol='mpd', drm='widevine')
    return helper.check_inputstream()

def days(title, now, start):
    today = datetime.date.today()
    if start and not title == 'Live':
        if now[:10] == start[:10]:
            return 'Today'
        elif str(today + datetime.timedelta(days=1)) == start[:10]:
            return 'Tomorrow'
        for i in range(2,8):
            if str(today + datetime.timedelta(days=i)) == start[:10]:
                return (today + datetime.timedelta(days=i)).strftime('%A')
    return title

def epg_date(date):
    return datetime.datetime.fromtimestamp(time.mktime(time.strptime(date, date_format)))

def get_prev_day(date):
    return (date - datetime.timedelta(days=1))

def get_next_day(date):
    return (date + datetime.timedelta(days=1))

def get_date():
    date = 'today'
    dlg = dialog.numeric(1, getString(30230))
    if dlg:
        spl = dlg.split('/')
        date = '%s-%s-%s' % (spl[2], spl[1], spl[0])
    return date
