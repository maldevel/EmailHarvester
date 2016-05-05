from com.utils.ColorPrint import ColorPrint


class EmailHarvesterException(Exception):
    def __init__(self, value, msg=""):
        super().__init__()
        self.__value = value
        self.__message = msg

    def __str__(self):
        if self.__value == 1:
            return ColorPrint.green("[+] Good bye")

        elif self.__value == 2:
            return ColorPrint.red("[-] Please specify a domain name to search.")

        elif self.__value == 3:
            return ColorPrint.red("[-] No emails found!")

        elif self.__value == 4:
            return ColorPrint.red("[-] Error while writing the email: " + str(self.__message))

        elif self.__value == 5:
            return ColorPrint.red("[-] Error while writing the output file:\n" + str(self.__message))

        elif self.__value == 6:
            return ColorPrint.red("[-] Error while writing the XML file:\n" + str(self.__message))