# -*- coding: utf-8 -*-

from common import *
from resources import resources

class Rails:

    def __init__(self, i):
        self.item = {}
        self.item['mode'] = 'rail'
        self.item['title'] = utfenc(resources(i['Id']))
        self.item['id'] = i['Id']
        self.item['plot'] = i['Id']
        if i.get('Params', ''):
            self.item['params'] = i['Params']
