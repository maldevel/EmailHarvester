import re
from urllib import parse

from com.core.OptionManager import OptionManager


class MyParser:
    """
    The MyParser class is able to look for emails in a html document.
    """

    @staticmethod
    def generic_clean(results):
        """
        Clean the string containing the results.
        Remove entities that could compromise the results.

        :param results: String containing the result of all queries.
        :return:
        """
        # TODO the whole method should be re-thinked
        # Why use strings instead of lists or sets?
        for e in '''<KW> </KW> </a> <b> </b> </div> <em> </em> <p> </span>
                    <strong> </strong> <title> <wbr> </wbr>'''.split():
            results = results.replace(e, '')

        for e in '%2522 %22 %2f %3a %3A %3C %3D & / : ; < = > \\'.split():
            results = results.replace(e, ' ')

        return results

    @staticmethod
    def emails(results):
        """
        Get a set of the resulting emails.

        :param results: String containing the result of all queries.
        :param word:
        :return:
        """
        results = MyParser.generic_clean(results)
        reg_emails = re.compile(
            '[a-zA-Z0-9.\-_+%#~!$&\',;=:]+' +
            '@' +
            '[a-zA-Z0-9.-]*' +
            OptionManager()["domain"])
        # TODO: build an email object which contains more informations like the site and the search engine
        # which have ben used to find it out

        list_emails_founds = reg_emails.findall(results)
        return set(list_emails_founds)
