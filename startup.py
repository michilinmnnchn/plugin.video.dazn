# -*- coding: utf-8 -*-

import xbmcaddon

addon = xbmcaddon.Addon(id='plugin.video.dazn')

if __name__ == '__main__':
    addon.setSetting('startup', 'true')
