__author__ = 'herve'
import sys
import time
import requests
from core.parser import Default
from core import colors


class Plugin:
    results = ""
    limit = 0
    counter = 0
    url = None
    step = 0
    word = None
    parser = None

    def __init__(self, url, word, limit, start,
                 step, proxy, user_agent, name=__name__, selected_parser=Default):
        self.name = name
        self.url = url
        self.word = word
        self.limit = limit
        self.counter = start
        self.counter_step = step
        self.parser = selected_parser
        self.proxy = proxy
        self.user_agent = user_agent

    def search(self):
        try:
            url = self.url.format(counter=str(self.counter), word=self.word)
            headers = {'User-Agent': self.user_agent}
            if self.proxy:
                proxies = {self.proxy.scheme: "http://" + self.proxy.netloc}
                req = requests.get(url, headers=headers, proxies=proxies)
            else:
                req = requests.get(url, headers=headers)

        except Exception as e:
            print(e)
            sys.exit(4)

        self.results += req.content.decode(req.encoding)

    def process(self):
        self.show_message("\n[+] Searching in {0}..\n".format(self.name))
        while self.counter < self.limit:
            self.search()
            time.sleep(1)
            self.counter += self.step
            print("\tSearching " + str(self.counter) + " results...")

    def get_emails(self):
        parser = self.parser(self.results, self.word)
        return parser.extract()

    def show_message(self, msg):
        print(colors.green(msg))

    def run(self):
        self.process()
        return self.get_emails()