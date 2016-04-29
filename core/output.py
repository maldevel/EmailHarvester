__author__ = 'herve.beraud'
from core import colors


def save(filename, all_emails):
    if filename:
        try:
            print(colors.green("\n[+] Saving files..."))
            with open(filename, 'w') as out_file:
                for email in all_emails:
                    try:
                        out_file.write(email + "\n")
                    except:
                        print(colors.red("Exception " + email))
        except Exception as e:
            print(colors.red("Error saving TXT file: " + e))

        try:
            filename = filename.split(".")[0] + ".xml"
            with open(filename, 'w') as out_file:
                out_file.write('<?xml version="1.0" encoding="UTF-8"?><EmailHarvester>')
                for email in all_emails:
                    out_file.write('<email>{}</email>'.format(email))
                out_file.write('</EmailHarvester>')
            print(colors.green("Files saved!"))
        except Exception as er:
            print(colors.red("Error saving XML file: " + er))


def stdout_print(all_emails):
    for emails in all_emails:
        print(emails)
