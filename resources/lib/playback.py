# -*- coding: utf-8 -*-

import json
import simple_requests as requests

class Playback:

    def __init__(self, data, token_data):
        self.ManifestUrl = ''
        self.LaUrl = ''
        self.LaUrlAuthParam = ''
        self.parse_data(data.get('PlaybackDetails', []), json.loads(token_data))

    def parse_data(self, data, token_data):
        for i in data:
            r = requests.head(i['ManifestUrl'])
            if r.status_code == 200:
                self.ManifestUrl = i['ManifestUrl']
                self.LaUrl = i['LaUrl']
                self.LaUrlAuthParam = '{0}={1}'.format(i['LaUrlAuthParamName'], token_data['mpx'])
                break
