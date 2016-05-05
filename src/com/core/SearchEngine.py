import requests

from com.core.MyParser import MyParser
from com.core.OptionManager import OptionManager
import time
from math import *


from com.utils.ColorPrint import ColorPrint
from com.utils.ProgressBar import ProgressBar


class SearchEngine:
    """
    THis is the super class for all plugins, the code relative to searches has been put here and all engines use it.
    """

    def __init__(self, url_dict):
        self.__url_dict = url_dict
        self.__option_manager = OptionManager()
        self.__results = set([])

    def search(self):
        """
        Perform the research
        :return: set of emails found
        """

        for location in self.__url_dict:

            if location != self.__class__.__name__:
                print(ColorPrint.green("[+] Searching in " + str(self.__class__.__name__) + " + " + str(location)))
            url = self.__url_dict[location]["url"]
            init = self.__url_dict[location]["init"]
            step = self.__url_dict[location]["step"]
            domain = self.__option_manager["domain"]
            limit = self.__option_manager["limit"]
            proxy = self.__option_manager["proxy"]

            bar = ProgressBar(limit, title="", tabs = 1)

            counter = init
            page = init
            while counter < limit:
                counter += step
                page += 1
                bar.update(increase=False, new_step=counter)
                try:
                    if "page" not in self.__url_dict:
                        urly = url.format(counter=str(counter-step), word=domain)
                    else:
                        urly = url.format(page=str(page), word=domain)
                    headers = {'User-Agent': self.__option_manager["userAgent"]}
                    if proxy:
                        proxies = {proxy.scheme: "http://" + self.__option_manager["proxy"].netloc}
                        r = requests.get(urly, headers=headers, proxies=proxies)
                    else:
                        r = requests.get(urly, headers=headers)

                    self.__results.update( MyParser.emails(r.content.decode(r.encoding)))
                    time.sleep(1)

                except Exception as e:
                    print(e)
                    sys.exit(4)
            print()
        return self.__results