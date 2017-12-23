# -*- coding: utf-8 -*-

from resources.lib.client import Client
from resources.lib import dazn
from resources.lib.common import *

client = Client()

def router(paramstring):

    args = dict(urlparse.parse_qs(paramstring))
    mode = args.get('mode', ['rails'])[0]
    title = args.get('title', [''])[0]
    id_ = args.get('id', ['home'])[0]
    params = args.get('params', [''])[0]

    if mode == 'rails':
        dazn.rails_items(client.rails(id_, params), id_)
    elif 'rail' in mode:
        dazn.rail_items(client.rail(id_, params), mode)
    elif 'epg' in mode:
        date = params
        if id_ == 'date':
            date = get_date()
        dazn.epg_items(client.epg(date), date, mode)
    elif mode == 'play':
        dazn.playback(client.playback(id_))
    elif mode == 'play_context':
        dazn.playback(client.playback(id_), title, True)
    elif mode == 'is_settings':
        is_settings()

if __name__ == '__main__':
    if addon.getSetting('startup') == 'true':
        device_id = uniq_id()
        if device_id:
            client.startUp(device_id)
            playable = is_helper()
            if client.TOKEN and playable:
                addon.setSetting('startup', 'false')

    if client.TOKEN and client.DEVICE_ID:
        router(sys.argv[2][1:])
