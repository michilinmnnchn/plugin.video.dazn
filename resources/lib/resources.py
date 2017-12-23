# -*- coding: utf-8 -*-

from common import *

def resources(string):
    if string == 'CatchUp':
        return getString(30201)
    elif string == 'ComingUp':
        return getString(30202)
    elif string == 'UpComing':
        return getString(30202)
    elif string == 'Editorial':
        return getString(30203)
    elif string == 'Feature':
        return getString(30204)
    elif string == 'Live':
        return getString(30205)
    elif string == 'MostPopular':
        return getString(30206)
    elif string == 'Personal':
        return getString(30207)
    elif string == 'Scheduled':
        return getString(30208)
    elif string == 'Sport':
        return getString(30209)
    elif string == 'Competition':
        return getString(30210)
    elif string == 'Competitor':
        return getString(30211)
    elif string == 'Today':
        return getString(30221)
    elif string == 'Tomorrow':
        return getString(30222)
    elif string == 'Monday':
        return getString(30223)
    elif string == 'Tuesday':
        return getString(30224)
    elif string == 'Wednesday':
        return getString(30225)
    elif string == 'Thursday':
        return getString(30226)
    elif string == 'Friday':
        return getString(30227)
    elif string == 'Saturday':
        return getString(30228)
    elif string == 'Sunday':
        return getString(30229)
    else:
        return string
