__author__ = 'herve.beraud'
from EmailHarvester.core.colors import green
from EmailHarvester.core.colors import yellow
from EmailHarvester.core.colors import red
from EmailHarvester.core.colors import white


class File:

    def __init__(self, filename, results):
        self.filename = filename
        self.results = results

    def save(self):
        alert("\n[+] Saving files...")
        write_file(self.filename, self.txt())
        self.filename = self.filename.split('.')[0] + ".xml"
        write_file(self.filename, self.xml())
        alert("Files saved!")

    def txt(self):
        content = ''
        for result in self.results:
            content += '{0}\n'.format(result)
        return content

    def xml(self):
        content = '<?xml version="1.0" encoding="UTF-8"?>\n<EmailHarvester>\n'
        for result in self.results:
            content += '\t<email>{0}</email>\n'.format(result)
        content += '\n</EmailHarvester>'
        return content


def write_file(filename, content):
    try:
        with open(filename, 'w+') as output_file:
            output_file.write(content)
    except Exception as e:
        error("Error saving file {0} : {1}".format(filename, e))


def console(all_emails):
    for emails in all_emails:
        print(emails)


def message(msg, color=white, underline=False):
    if list is type(msg):
        for line in msg:
            print(color(line))
    else:
        print(color(msg))
    if underline:
        print(color("-" * len(msg)))


def alert(msg, underline=False):
    message(msg, color=green, underline=underline)


def warning(msg, underline=False):
    message(msg, color=yellow, underline=underline)


def error(msg, underline=False):
    message(msg, color=red, underline=underline)
