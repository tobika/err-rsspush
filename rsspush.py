import re
import os.path
import urllib2
from BeautifulSoup import BeautifulSoup
from errbot import BotPlugin, botcmd, re_botcmd
from feedgen.feed import FeedGenerator


class RssPush(BotPlugin):
    """RssPush plugin for Err"""

    @re_botcmd(pattern=r"^http(|$)", prefixed=False, flags=re.IGNORECASE)
    def listen_for_urls(self, msg, match):
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(msg))

        p = re.compile('\/(.*)')
        user = re.search(p, str(msg.getFrom())).group()[1:]

	if len(url) == 1:
            url = str(url[0])

            filename = '/mnt/extern1/SYSTEM/www/foorss/' + user + '.xml'

            fg = FeedGenerator()

            # Some pages block urllib2 so we need a fake user agent
            header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                   'Accept-Encoding': 'none',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive'}

            req = urllib2.Request(url, headers=header)

            try:
                soup = BeautifulSoup(urllib2.urlopen(req))
            except urllib2.HTTPError, e:
                print e.fp.read()
                yield "Error while parsing the website..."


            if os.path.isfile(filename):
                fg.from_rss(filename)
            else:
                fg.id(user)
                fg.title('Some Testfeed')
                fg.link( href='http://nix.da', rel='alternate' )
                fg.description('This is a cool feed!')

            if soup.title != None:
                title = soup.title.string
            else:
                title = url

            fe = fg.add_entry()
            fe.id(url)
            fe.title(title)
            fe.description('Description')
            fe.link([{'href': url}])

            fg.rss_file(filename)

            yield title + ' from ' + user + ' (rss updated)'

