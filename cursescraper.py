from urllib2 import Request, urlopen, URLError
import urllib
import re
from html2bbcode.parser import HTML2BBCode
import tempfile

class CurseScraper():

    def __init__(self):
        self.files_url = 'http://wow.curseforge.com/addons/%s/files/'
        self.main_url = 'http://wow.curseforge.com/addons/%s/'
        self.base_url = 'http://wow.curseforge.com%s'

    def get_addon(self, addon_info):

        try:
            request = Request(self.files_url % addon_info['curse_name'])
            response = urlopen(request).read().replace('\n', '')
            #get the table holding the file releases
            files_table_re = re.compile('<table class="listing">.*?<tbody>(.*?)</table>')
            files_table = re.search(files_table_re, response)
            #get all files releases
            file_releases_re = re.compile('<tr(.*?)</tr>')
            file_releases = re.findall(file_releases_re, files_table.group(1))
            #looking for a release
            for file_release in file_releases:
                if "Release" in file_release:
                    file_details_re = re.compile('href="([^"]+).*?>([^<]+).*?col\-filename">([^<]+)')
                    file_details = re.search(file_details_re, file_release)

                    file_url = file_details.group(1)
                    file_version = file_details.group(2)
                    file_name = file_details.group(3).strip()
                    break

            if file_name == addon_info['latest_file']:
                print 'No new version found, stopping'
                exit()

            request = Request(self.main_url % addon_info['curse_name'])
            response = urlopen(request).read().replace('\n', '')
            description_re = re.compile('<div class="content-box"><div class="content-box-inner">(.*?)</div></div>')
            description = re.search(description_re, response)
            #strip out the default image if there is one
            if 'project-default-image' in description.group(1):
                strip_image_re = re.compile('</a>(.*)')
                description = re.search(strip_image_re, description.group(1))

            parser = HTML2BBCode()
            desc = str(parser.feed(description.group(1).strip()))
            request = Request(self.base_url % file_url)
            response = urlopen(request).read().replace('\n', '')
            download_url_re = re.compile('<li class="user-action user-action-download"><span><a href="(.*?)"')
            download_url = re.search(download_url_re, response)
            urllib.urlretrieve(download_url.group(1), tempfile.gettempdir()+("/%s" % file_name))
            update_info = {'version': file_version, 'desc': desc, 'file_name': file_name}
            return update_info
        except URLError, e:

            raise e

