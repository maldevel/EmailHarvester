import importlib

from com.core.OptionManager import OptionManager

import com.plugins.searchEngines as SE
from com.plugins.SocialNetworks import SocialNetworks
from com.utils.ColorPrint import ColorPrint
from com.utils.exceptions.EmailHarvesterException import EmailHarvesterException


class Manager(object):
    """
    The class EmailHarvester manage the whole process within its run method
    """

    def run(self):
        """
        Run the core code of the software

        :return: void
        """

        # If the option for viewing plugins has been asked for, this is the only thing done by the software
        if OptionManager()["list_plugins"]:
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

        if not OptionManager()["domain"]:
            # The domain must be specified
            raise EmailHarvesterException(2)

        print("You are looking for email adress in domain: {}".format(ColorPrint.yellow(OptionManager()["domain"])))

        print("User-Agent in use: {}".format(ColorPrint.yellow(OptionManager()["userAgent"])))

        if OptionManager()["proxy"]:
            print("Proxy server in use: {}".format(ColorPrint.yellow(OptionManager()["proxy"].scheme + "://" + OptionManager()["proxy"].netloc)))

        # Calculating the difference between the set of "wanted engines" and the set of "excluded engines
        # gives the engines to run
        used_engines = OptionManager()["engine"].difference(OptionManager()["exclude"])
        print("The following search engines will be used: " + ColorPrint.yellow(", ".join(used_engines)))

        # Same for networks
        # TODO: do not display networks if the used search engine do not allow to look in specific sites
        used_networks = OptionManager()["network"].difference(OptionManager()["exclude"])
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
                # TODO: optimize this?
                # I don't think that the process is well thinked here
                all_emails.update(eval("mod." + search_engine + "('" + network + "')").search())

        # Check if the email list is empy
        if not all_emails:
            raise EmailHarvesterException(3)

        msg = "\n\n[+] {} emails found:".format(len(all_emails))
        print(ColorPrint.green(msg))
        print(ColorPrint.green("-" * len(msg)))

        if not OptionManager()["noprint"]:
            for emails in all_emails:
                print(emails)

        filename = OptionManager()["filename"]

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