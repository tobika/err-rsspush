import re
import os.path
import urllib2
from BeautifulSoup import BeautifulSoup
from errbot import BotPlugin, botcmd, re_botcmd
from feedgen.feed import FeedGenerator


class RssPush(BotPlugin):
    """RssPush plugin for Err"""

    @botcmd
    def add(self, msg, args):
        """Say hello to the world"""
        return "Hello, world!\n"

    @re_botcmd(pattern=r"^http(|$)", prefixed=False, flags=re.IGNORECASE)
    def listen_for_urls(self, msg, match):
        """Talk of cookies gives Err a craving..."""
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(msg))

        p = re.compile('\/(.*)')
        user = re.search(p, str(msg.getFrom())).group()[1:]

	if len(url) == 1:
            url = str(url[0])

            filename = '/mnt/extern1/SYSTEM/www/foorss/' + user + '.xml'

            fg = FeedGenerator()

            soup = BeautifulSoup(urllib2.urlopen(url))

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

            yield url + ' from ' + user + ' (rss updated)'

