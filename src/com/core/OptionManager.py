from com.utils.Singleton import singleton


@singleton
class OptionManager:
    """
    The OptionManager class contains all the options necessary to run the software.

    It uses the Singleton design-pattern in order to allow every part of the software to get access to the Options
    provided by the user.

    """

    def __init__(self):
        self.__options = {}

    def set_options(self, args):
        """
        Map the args object to the OptionManager

        :param args:
        :return:
        """
        self.__options = {
            "list_plugins": args.listplugins,
            "domain": args.domain,
            "userAgent": args.uagent or "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0",
            "proxy": args.proxy,
            "filename": args.filename or "",
            "limit": args.limit,
            "engine": args.engine,
            "network": args.network,
            "exclude": args.exclude or set([]),
            "noprint": args.noprint
        }

    def __getitem__(self, key):
        """
        Allow the use of syntactic sugar: Optionmanager["key"]

        :param key: a key value as String in the options attribute
        :return: the value of the key
        """
        return self.__options[key]

    def __repr__(self):
        return str(self.__options)