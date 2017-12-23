# -*- coding: utf-8 -*-

from common import *
from items import Items
from rails import Rails
from tiles import Tiles
from playback import Playback
from context import Context
from resources import resources

items = Items()

def rails_items(data, id_):
    if id_ == 'home':
        epg = {
            'mode': 'epg',
            'title': utfenc(getString(30212)),
            'plot': 'Schedule',
            'params': 'today',
        }
        epg['cm'] = Context().highlights(epg, mode='epg_highlights')
        items.add_item(epg)
    for i in data.get('Rails', []):
        item = Rails(i).item
        if item.get('id', '') == 'CatchUp':
            item['cm'] = Context().highlights(item, mode='rail_highlights')
        items.add_item(item)
    items.list_items()

def rail_items(data, mode, list=True):
    highlights = True if 'highlights' in mode else False
    focus = data.get('StartPosition', False)
    for i in data.get('Tiles', []):
        context = Context()
        item = Tiles(i).item
        if highlights:
            if item['type'] == 'Highlights':
                item['cm'] = context.goto(item)
                items.add_item(item)
            elif item.get('related', []):
                for i in item['related']:
                    if i.get('Videos', []) and i.get('Type', None) == 'Highlights':
                        _item = Tiles(i).item
                        _item['cm'] = context.goto(_item)
                        items.add_item(_item)
        else:
            if item.get('related', []):
                cm_items = []
                for i in item['related']:
                    if i.get('Videos', []):
                        cm_items.append(Tiles(i).item)
                context.related(cm_items)
            item['cm'] = context.goto(item)
            items.add_item(item)
    if list:
        items.list_items(focus)

def epg_items(data, params, mode):
    update = False if params == 'today' else True
    if data.get('Date'):
        date = epg_date(data['Date'])
        cm = Context().epg_date()

        def date_item(day):
            return {
                'mode': mode,
                'title': '{0} ({1})'.format(resources(day.strftime('%A')), day.strftime(date_format)),
                'plot': '{0} ({1})'.format(resources(date.strftime('%A')), date.strftime(date_format)),
                'params': day,
                'cm': cm
            }

        items.add_item(date_item(get_prev_day(date)))
        rail_items(data, mode, list=False)
        items.add_item(date_item(get_next_day(date)))
    items.list_items(upd=update)

def playback(data, name=False, context=False):
    items.play_item(Playback(data), name, context)
