from urllib2 import Request, urlopen, URLError
from urllib import urlencode
import json
import tempfile
import requests

class WoWIApi():
    cookie = None
    login_tried = False

    def __init__(self, username, password):
        self.username = username
        self.password = password
        try:
            f = open('cookie', 'r')
            self.cookie = json.loads(f.read())
            f.close()
        except IOError:
            pass

    def _do_request(self, url, rtype, data=None, files=None, json_res=True):
        if self.cookie is None:
            self._do_login()
        try:
            if rtype == 'get':
                response = requests.get(url, data=data, files=files, cookies=self.cookie)
            else:
                response = requests.post(url, data=data, files=files, cookies=self.cookie)

            response.raise_for_status()
            if json_res:
                return response.json()
        except requests.exceptions.HTTPError, e:
            if e.response.status_code == 403 and not self.login_tried:
                self.login_tried = True
                self._do_login()
                return self._do_request(url, rtype, data, files)
                pass
            else:
                raise e

    def _do_login(self):
        url = 'https://secure.wowinterface.com/forums/login.php'
        data = {'vb_login_username': self.username,
                'vb_login_password': self.password,
                'do': 'login',
                'cookieuser': '1'}

        response = requests.post(url, data=data)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError, e:
            raise e
        #print requests.utils.dict_from_cookiejar(response.cookies)
        self.cookie = requests.utils.dict_from_cookiejar(response.cookies)
        f = open('cookie', 'w')
        json.dump(self.cookie, f)
        f.close()

    def get_addon_list(self):
        url = 'http://api.wowinterface.com/addons/list.json'
        response = self._do_request(url, 'get')
        return response

    def get_addon_details(self, addonid):
        url = 'http://api.wowinterface.com/addons/details/%s.json' % addonid
        response = self._do_request(url, 'get')
        return response


    def update_addon(self, addon_info, update_info):
        url = 'http://api.wowinterface.com/addons/update'
        data = {'id': addon_info['wowi_id'],
                'version': update_info['version'],
                'description': update_info['desc']}
        files = {'updatefile': open(tempfile.gettempdir()+("/%s" % update_info['file_name']), 'rb')}
        self._do_request(url, 'post', files=files, data=data, json_res=False)
