__author__ = 'herve.beraud'

from termcolor import colored


def yellow(text):
    return colored(text, 'yellow', attrs=['bold'])


def green(text):
    return colored(text, 'green', attrs=['bold'])


def red(text):
    return colored(text, 'red', attrs=['bold'])


def white(text):
    return colored(text, 'white')
