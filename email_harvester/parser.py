import re


class MyParser:

    def __init__(self):
        self.new = None
        self.results = None
        self.temp = []
        self.word = None

    def extract(self, results, word):
        self.results = results
        self.word = word

    def genericClean(self):
        for e in '''<KW> </KW> </a> <b> </b> </div> <em> </em> <p> </span>
                    <strong> </strong> <title> <wbr> </wbr>'''.split():
            self.results = self.results.replace(e, '')
        for e in '%2f %3a %3A %3C %3D & / : ; < = > \\'.split():
            self.results = self.results.replace(e, ' ')

    def emails(self):
        self.genericClean()
        reg_emails = re.compile(
            '[a-zA-Z0-9.\-_+#~!$&\',;=:]+' +
            '@' +
            '[a-zA-Z0-9.-]*' +
            self.word)
        self.temp = reg_emails.findall(self.results)
        emails = self.unique()
        return emails

    def unique(self):
        self.new = list(set(self.temp))
        return self.new
