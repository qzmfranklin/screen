#!/usr/bin/env python3

"""An exmple program demonstrating the use ScreenArray.

Create an array of terminal windows, each of which is connected to an sol
session.

This script is *not* with generality, reusability, or even readability in mind.
It serves to test something, period.
"""

from screen_array import ScreenArray

if __name__ == '__main__':
    g = ScreenArray('beef', height = 3, width = 3, quiet = False,)
    # g.make_array()
    def __visitor_ipmi(index):
        # return 'ipmitool -I lanplus -U ADMIN -P ADMIN -H 10.1.0.{} sol activate'.format(index * 2 + 3)
        return 'ping 10.1.0.{}'.format(index * 2 + 3)
    g.visit(__visitor_ipmi, mask = range(8))
