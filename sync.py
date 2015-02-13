from wowiapi import WoWIApi
from cursescraper import CurseScraper
import argparse
import json
import ConfigParser
import getpass

config = ConfigParser.ConfigParser()
config.read('wowiupdater.cfg')

try:
    username = config.get('Login', 'username')
    password = config.get('Login', 'password')
except ConfigParser.NoSectionError:
    username = raw_input('Enter wowinterface username: ')
    password = getpass.getpass('Enter wowinterface password:')
    config.add_section('Login')
    config.set('Login', 'username', username)
    config.set('Login', 'password', password)

    with open('wowiupdater.cfg', 'wb') as configfile:
        config.write(configfile)

wowiapi = WoWIApi(username, password)

try:
    f = open('addonlist')
    addons = json.loads(f.read(), 'UTF-8')
    f.close()
except IOError, ValueError:
    addons = {}


def sync_addon(args):

    if addons.__contains__(args.addon_name):
        if addons[args.addon_name]['curse_name'] == '':
            curse_name = raw_input('Curse slug addon name missing please enter it (its in the url, e.g. flight-map-enhanced): ')
            addons[args.addon_name]['curse_name'] = curse_name
            f = open('addonlist', 'w')
            json.dump(addons, f)
            f.close()
    else:
        print "Addon not found"
        exit()

    scraper = CurseScraper()
    update_info = scraper.get_addon(addons[args.addon_name])
    wowiapi.update_addon(addons[args.addon_name], update_info)
    addons[args.addon_name]['latest_file'] = update_info['file_name']
    save_addon_list()


def save_addon_list():
    f = open('addonlist', 'w')
    json.dump(addons, f)
    f.close()


#saving latest file to easily compare for new version, also the changelog so the new one can be appended on top
def update_addon_list(args):
    addonlist = wowiapi.get_addon_list()

    for addon in addonlist:
        if not addons.__contains__(addon['title']):
            addon_details = wowiapi.get_addon_details(addon['id'])

            addons[addon['title']] = {'wowi_id': addon['id'], 'curse_name': '', 'latest_file': addon_details[0]['filename'], 'changelog': addon_details[0]['changelog']}
    save_addon_list()


parser = argparse.ArgumentParser(description='Sync your addon on wowinterface with curseforge data')
subparsers = parser.add_subparsers()
parser_addonlist = subparsers.add_parser('fetch')
parser_addonlist.set_defaults(func=update_addon_list)

parser_addonupdate = subparsers.add_parser('update')
parser_addonupdate.add_argument('addon_name', type=str)
parser_addonupdate.set_defaults(func=sync_addon)

args = parser.parse_args()
args.func(args)


