__author__ = 'herve'
import sys
import time
import requests
from EmailHarvester.core.parser import Default
from EmailHarvester.core.output import alert
from EmailHarvester.core.output import error
from EmailHarvester.core.output import message


class Plugin:
    results = ""
    limit = 0
    start = 0
    url = None
    step = 0
    word = None
    parser = None

    def __init__(self, url, word, limit, start,
                 step, proxy, user_agent, name=__name__, parser=Default):
        self.name = name
        self.url = url
        self.word = word
        self.limit = limit
        self.start = start
        self.step = step
        self.parser = parser
        self.proxy = proxy
        self.user_agent = user_agent

    def initialize(self, engine):
        self.url = engine['url']
        self.start = 0
        self.step = engine["step"]

    def search(self):
        try:
            url = self.url.format(counter=str(self.start), word=self.word)
            headers = {'User-Agent': self.user_agent}
            if self.proxy:
                proxies = {self.proxy.scheme: "http://" + self.proxy.netloc}
                req = requests.get(url, headers=headers, proxies=proxies)
            else:
                req = requests.get(url, headers=headers)

        except Exception as e:
            error(e)
            sys.exit(4)

        self.results += req.content.decode(req.encoding)

    def process(self):
        alert("\n[+] Searching in {0}..\n".format(self.name))
        while self.start < self.limit:
            self.search()
            time.sleep(1)
            self.start += self.step
            message("\tSearching {0} results...".format(self.start))

    def get_emails(self):
        parser = self.parser(self.results, self.word)
        return parser.extract()

    def run(self):
        raise NotImplementedError
