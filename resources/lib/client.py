# -*- coding: utf-8 -*-

import simple_requests as requests
from common import *

class Client:

    def __init__(self):

        self.DEVICE_ID = addon.getSetting('device_id')
        self.TOKEN = addon.getSetting('token')
        self.COUNTRY = addon.getSetting('country')
        self.LANGUAGE = addon.getSetting('language')
        self.POST_DATA = {}
        self.ERRORS = 0

        self.HEADERS = {
            'Content-Type': 'application/json',
            'Referer': api_base
        }

        self.PARAMS = {
            '$format': 'json'
        }

        self.STARTUP = api_base + 'v2/Startup'
        self.RAIL = api_base + 'v2/Rail'
        self.RAILS = api_base + 'v3/Rails'
        self.EPG = api_base + 'v1/Epg'
        self.EVENT = api_base + 'v2/Event'
        self.PLAYBACK = api_base + 'v1/Playback'
        self.SIGNIN = api_base + 'v3/SignIn'
        self.SIGNOUT = api_base + 'v1/SignOut'
        self.REFRESH = api_base + 'v3/RefreshAccessToken'
        self.PROFILE = api_base + 'v1/UserProfile'

    def content_data(self, url):
        data = self.request(url)
        if data.get('odata.error', None):
            self.errorHandler(data)
        return data

    def rails(self, id_, params=''):
        self.PARAMS['groupId'] = id_
        self.PARAMS['params'] = params
        return self.content_data(self.RAILS)

    def rail(self, id_, params=''):
        self.PARAMS['id'] = id_
        self.PARAMS['params'] = params
        return self.content_data(self.RAIL)

    def epg(self, params):
        self.PARAMS['date'] = params
        return self.content_data(self.EPG)

    def event(self, id_):
        self.PARAMS['Id'] = id_
        return self.content_data(self.EVENT)

    def playback_data(self, id_):
        self.POST_DATA = {
            'AssetId': id_,
            'Format': 'MPEG-DASH',
            'PlayerId': 'DAZN-' + self.DEVICE_ID,
            'Secure': 'true',
            'PlayReadyInitiator': 'false',
            'BadManifests': [],
            'LanguageCode': self.LANGUAGE,
        }
        return self.request(self.PLAYBACK)

    def playback(self, id_):
        data = self.playback_data(id_)
        if data.get('odata.error', None):
            self.errorHandler(data)
            if self.TOKEN:
                data = self.playback_data(id_)
        return data
            
    def userProfile(self):
        data = self.request(self.PROFILE)
        if data.get('odata.error', None):
            self.errorHandler(data)
        else:
            addon.setSetting('viewer_id', data['ViewerId'])

    def setToken(self, auth, result):
        log('[{0}] signin: {1}'.format(addon_id, result))
        if auth and result == 'SignedIn':
            self.TOKEN = auth['Token']
        else:
            if result == 'HardOffer':
                dialog.ok(addon_name, getString(30161))
            self.signOut()
        addon.setSetting('token', self.TOKEN)

    def signIn(self):
        email = dialog.input(addon_name + getString(30002), type=xbmcgui.INPUT_ALPHANUM)
        if email:
            password = dialog.input(addon_name + getString(30003), type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
        if '@' in email and len(password) > 4:
            self.POST_DATA = {
                'Email': utfenc(email),
                'Password': utfenc(password),
                'DeviceId': self.DEVICE_ID,
                'Platform': 'web'
            }
            data = self.request(self.SIGNIN)
            if data.get('odata.error', None):
                self.errorHandler(data)
            else:
                self.setToken(data['AuthToken'], data.get('Result', 'SignInError'))
                self.userProfile()
        else:
            dialog.ok(addon_name, getString(30004))

    def signOut(self):
        self.POST_DATA = {
            'DeviceId': self.DEVICE_ID
        }
        r = self.request(self.SIGNOUT)
        self.TOKEN = ''
        addon.setSetting('token', self.TOKEN)

    def refreshToken(self):
        self.POST_DATA = {
            'DeviceId': self.DEVICE_ID
        }
        data = self.request(self.REFRESH)
        if data.get('odata.error', None):
            self.signOut()
            self.errorHandler(data)
        else:
            self.setToken(data['AuthToken'], data.get('Result', 'RefreshAccessTokenError'))

    def startUp(self, device_id=''):
        kodi_language = get_language()
        if device_id:
            self.DEVICE_ID = device_id
        self.POST_DATA = {
            'LandingPageKey': 'generic',
            'Languages': '{0}, {1}'.format(kodi_language, self.LANGUAGE),
            'Platform': 'web',
            'Manufacturer': '',
            'PromoCode': ''
        }
        data = self.request(self.STARTUP)
        region = data.get('Region', {})
        if region.get('isAllowed', False):
            self.COUNTRY = region['Country']
            self.LANGUAGE = region['Language']
            languages = data['SupportedLanguages']
            for i in languages:
                if i == kodi_language:
                    self.LANGUAGE = i
                    break
            addon.setSetting('language', self.LANGUAGE)
            addon.setSetting('country', self.COUNTRY)
            if not self.TOKEN:
                self.signIn()
        else:
            self.TOKEN = ''
            dialog.ok(addon_name, getString(30101))

    def request(self, url):

        self.HEADERS['Authorization'] = 'Bearer ' + self.TOKEN
        self.PARAMS['LanguageCode'] = self.LANGUAGE
        self.PARAMS['Country'] = self.COUNTRY

        if self.POST_DATA:
            r = requests.post(url, headers=self.HEADERS, data=self.POST_DATA, params=self.PARAMS)
            self.POST_DATA  = {}
        else:
            r = requests.get(url, headers=self.HEADERS, params=self.PARAMS)

        if r.headers.get('content-type', '').startswith('application/json'):
            return r.json()
        else:
            if not r.status_code == 204:
                log('[{0}] error: {1} ({2}, {3})'.format(addon_id, url, str(r.status_code), r.headers.get('content-type', '')))
            return {}

    def errorHandler(self, data):
        self.ERRORS += 1
        msg  = data['odata.error']['message']['value']
        code = str(data['odata.error']['code'])
        log('[{0}] version: {1} country: {2} language: {3}'.format(addon_id, addon_version, self.COUNTRY, self.LANGUAGE))
        log('[{0}] error: {1} ({2})'.format(addon_id, msg, code))
        if code == '10000' and self.ERRORS < 3:
            self.refreshToken()
        elif (code == '401' or code == '10033') and self.ERRORS < 3:
            self.signIn()
        elif code == '7':
            dialog.ok(addon_name, getString(30107))
        elif code == '3001':
            self.startUp()
        elif code == '10006':
            dialog.ok(addon_name, getString(30101))
        elif code == '10008':
            dialog.ok(addon_name, getString(30108))
        elif code == '10049':
            dialog.ok(addon_name, getString(30151))
