import time
import sys
from math import *

__author__ = 'kristie'


class ProgressBar:
    """
    This class allows you to make easily a progress bar.
    """

    def __init__(self, steps, maxbar=50, title='Loading', tabs=0):
        """

        :param steps: the number of steps in the progress bar (exemple: if you download 100 file and you want a
            progression for each file dowloaded, you have 100 steps)
        :param maxbar: the number of caracters in the bar
        :param title: the title before the progress bar
        :param tabs: the number of tabs before the progress bar
        """
        if steps <= 0 or maxbar <= 0 or maxbar > 200:
            raise ValueError
        self.__steps = steps

        self.__maxbar = maxbar
        self.__title = title
        self.__tabs = tabs

        # the number of completed steps in the progress bar
        self.__completed_steps = 0

        self.update(False)

    def update(self, increase=True, new_step=-1):
        """

        :param increase: default: True - the basical +1 step
        :param new_step: if set, there will be a progressive loop to the specified step
        :return:
        """
        if increase:
            self.__completed_steps += 1
        elif new_step != -1:
            while self.__completed_steps < new_step and self.__completed_steps < self.__steps:
                time.sleep(0.05)
                self.update()

        # the percentage has been modified by the new completed_step value
        perc = floor(self.__completed_steps / self.__steps * 100)

        # There cannot be more completed steps than the maximum of steps
        if self.__completed_steps > self.__steps:
            self.__completed_steps = self.__steps

        # The number of caracters representing the steps done
        steps_bar = floor(perc / 100 * self.__maxbar)

        visual_bar = steps_bar * '#' + (self.__maxbar - steps_bar) * ' '

        sys.stdout.write('\r' + self.__tabs * "\t" + self.__title + ' [' + visual_bar + '] ' + str(perc) + '% '
                         + str(self.__completed_steps) + "/" + str(self.__steps))
        sys.stdout.flush()


if __name__ == '__main__':
    bar = ProgressBar(100)

    i = 0
    while bar.perc != 100:
        bar.update()
        time.sleep(0.5)

        i += 1