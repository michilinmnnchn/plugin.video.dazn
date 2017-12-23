# -*- coding: utf-8 -*-

from common import *
from resources import resources

class Context:

    def __init__(self):
        self.cm = []

    def epg_date(self):
        d = {
            'mode': 'epg',
            'id': 'date'
        }
        self.cm.append((utfenc(getString(30230)), 'ActivateWindow(Videos, {0})'.format(build_url(d))))
        return self.cm

    def highlights(self, item, mode):
        d = {
            'mode': mode,
            'title': utfenc(item['title']),
            'id': item.get('id', ''),
            'params': item.get('params','')
        }
        self.cm.append((utfenc(getString(30231)), 'ActivateWindow(Videos, {0})'.format(build_url(d))))
        return self.cm

    def related(self, cm_items): 
        for i in cm_items:
            if i['type'] == 'Highlights':
                d = {
                    'mode': 'play_context',
                    'title': utfenc(i['title']),
                    'id': i.get('id', ''),
                    'params': i.get('params','')
                }
                self.cm.append((utfenc(getString(30213)), 'XBMC.RunPlugin({0})'.format(build_url(d))))
                break
        return self.cm

    def goto(self, item):
        if item.get('sport', None):
            i = item['sport']
            d = {
                'mode': 'rails',
                'title': utfenc(i['Title']),
                'id': 'sport',
                'params': i['Id']
            }
            self.cm.append((utfenc(getString(30214)), 'ActivateWindow(Videos, {0})'.format(build_url(d))))

        if item.get('competition', None):
            i = item['competition']
            d = {
                'mode': 'rails',
                'title': utfenc(i['Title']),
                'id': 'competition',
                'params': i['Id']
            }
            self.cm.append((utfenc(getString(30215)), 'ActivateWindow(Videos, {0})'.format(build_url(d))))

        return self.cm
