import importlib

from com.core.OptionManager import OptionManager
from com.core.MyParser import MyParser

import com.plugins.searchEngines as SE
from com.plugins.SocialNetworks import SocialNetworks
from com.utils.ColorPrint import ColorPrint
from com.utils.exceptions.EmailHarvesterException import EmailHarvesterException


class EmailHarvester(object):

    def __init__(self):
        self.__plugins = {}
        self.__option_manager = OptionManager()

        # self.results = ""
        # self.total_results = ""
        # self.limit = -1
        # self.counter = 0
        # self.url = ""
        # self.step = -1
        # self.word = ""

    # def register_plugin(self, search_method, functions):
    #     self.plugins[search_method] = functions

    # def get_plugins(self):
    #     return self.plugins
    #
    # def show_message(self, msg):
    #     print(ColorPrint.green(msg))

    # def init_search(self, url, word, limit, counterInit, counterStep):
    #     self.results = ""
    #     self.total_results = ""
    #     self.limit = int(limit)
    #     self.counter = int(counterInit)
    #     self.url = url
    #     self.step = int(counterStep)
    #     self.word = word

    # def do_search(self):
    #     try:
    #         urly = self.url.format(counter=str(self.counter), word=self.word)
    #         headers = {'User-Agent': self.userAgent}
    #         if(self.proxy):
    #             proxies = {self.proxy.scheme: "http://" + self.proxy.netloc}
    #             r=requests.get(urly, headers=headers, proxies=proxies)
    #         else:
    #             r=requests.get(urly, headers=headers)
    #
    #     except Exception as e:
    #         print(e)
    #         sys.exit(4)
    #
    #     self.results = r.content.decode(r.encoding)
    #     self.totalresults += self.results

    # def process(self):
    #     while (self.counter < self.limit):
    #         self.do_search()
    #         time.sleep(1)
    #         self.counter += self.step
    #         print("\tSearching " + str(self.counter) + " results...")

    def get_emails(self):
        self.parser.extract(self.totalresults, self.word)
        return self.parser.emails()

    def run(self):
        """
        Run the core code of the software

        :return: void
        """

        # If the option for viewing plugins has been asked for, this is the only thing done by the software
        if self.__option_manager["list_plugins"]:
            msg = "[+] Available plugins:"
            print(ColorPrint.green(msg))
            print(ColorPrint.green("-" * len(msg)))
            # Lists the content of the src/com/plugins directory
            # Mean the list of possibly used search engines
            print("Search Engines:")
            # Looking the name of the searchEngines in the plugins/searchEngines/__init__.py file
            for f in SE.__all__:
                print("\t" + f)

            # The static class social networks owns all the names of networks which can be used
            print("Social Networks: ")
            for f in SocialNetworks().get_all():
                print("\t" + f)
            raise EmailHarvesterException(1)

        if not self.__option_manager["domain"]:
            # The domain must be specified
            raise EmailHarvesterException(2)

        print("You are looking for email adress in domain: {}".format(ColorPrint.yellow(self.__option_manager["domain"])))

        print("User-Agent in use: {}".format(ColorPrint.yellow(self.__option_manager["userAgent"])))

        if self.__option_manager["proxy"]:
            print("Proxy server in use: {}".format(ColorPrint.yellow(self.__option_manager["proxy"].scheme + "://" + self.__option_manager["proxy"].netloc)))

        # Calculating the difference between the set of "wanted engines" and the set of "excluded engines
        # gives the engines to run
        used_engines = self.__option_manager["engine"].difference(self.__option_manager["exclude"])
        print("The following search engines will be used: " + ColorPrint.yellow(", ".join(used_engines)))

        # Same for networks
        used_networks = self.__option_manager["network"].difference(self.__option_manager["exclude"])
        print("The following networks will be browsed (if allowed by the search engine): " +
              ColorPrint.yellow(", ".join(used_networks)))

        all_emails = set([])

        for search_engine in used_engines:
            print(ColorPrint.green("[+] Searching in " + str(search_engine)))
            # Import the module containing the engine
            mod = importlib.import_module("com.plugins.searchEngines." + search_engine)
            # Instanciate the engine
            all_emails.update(eval("mod." + search_engine + "()").search())
            for network in used_networks:
                # Re-instanciate
                # TODO optimize this?
                all_emails.update(eval("mod." + search_engine + "('" + network + "')").search())

        if not all_emails:
            raise EmailHarvesterException(3)

        msg = "\n\n[+] {} emails found:".format(len(all_emails))
        print(ColorPrint.green(msg))
        print(ColorPrint.green("-" * len(msg)))

        if not self.__option_manager["noprint"]:
            for emails in all_emails:
                print(emails)

        filename = self.__option_manager["filename"]

        # Raw output file
        if filename:
            try:
                print(ColorPrint.green("\n[+] Saving files..."))
                with open(filename, 'w') as out_file:
                    for email in all_emails:
                        try:
                            out_file.write(email + "\n")
                        except:
                            raise EmailHarvesterException(4, msg=email)
            except Exception as e:
                raise EmailHarvesterException(5, msg=str(e))

            try:
                # Xml Output File
                filename = filename.split(".")[0] + ".xml"
                with open(filename, 'w') as out_file:
                    out_file.write('<?xml version="1.0" encoding="UTF-8"?><EmailHarvester>')
                    for email in all_emails:
                        out_file.write('<email>{}</email>'.format(email))
                    out_file.write('</EmailHarvester>')
                print(ColorPrint.green("[+] Files saved!"))
            except Exception as er:
                raise EmailHarvesterException(6, msg=str(er))

        raise EmailHarvesterException(1)