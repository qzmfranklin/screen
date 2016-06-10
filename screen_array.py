#!/usr/bin/env python3

"""Create an array of terminal windows.

The cli does not provide visitor interface as the python API does.
"""

import argparse
import math
import subprocess
import sys

class ScreenArrayError(Exception):
    pass

class ScreenArray(object):

    def __init__(self, session, *, height = 3, width = 3, quiet = False):
        if height <= 0:
            raise ScreenArrayError("height ({}) <= 0.".format(height))
        if width <= 0:
            raise ScreenArrayError("width ({}) <= 0.".format(width))
        self.session = session
        self.quiet = quiet
        self.width = width
        self.height = height

    @property
    def capacity(self):
        return self.width * self.height

    def make_array(self):
        """Make array in the screen session.

        The screen commands are documented in great detail in the manpage of the
        'screen' program.
        """
        # Vertically split to have the correct height.
        for i in range(self.height - 1):
            self._do('split')       # C-a S

        # Make the first row.
        # The first row does not need to create the screen for the first window.
        for i in range(self.width - 1):
            self._do('split -v')    #  C-a |
            self._do('focus')       #  C-a tab
            self._do('screen')      #  C-a c

        # Make the rest rows.
        for i in range(self.height - 1):
            self._do('focus')       #  C-a tab
            self._do('screen')      #  C-a c
            for j in range(self.width - 1):
                self._do('split -v')    #  C-a |
                self._do('focus')       #  C-a tab
                self._do('screen')      #  C-a c

    def visit(self, func, *, mask = None):
        """Visit and issue commands in each window.

        Arguments:
            func: A python function that takes a non-negative integer as
                input and returns a python3 string as output. For example:
                        def foo(index):
                            return 'ls -al /dev/sd{}'.format(index)
                The returned string, @ret is the command issued to the window
                with the @index:
                        screen -S session -X select @index
                        screen -S session -X exec @ret
                As a final note, @index starts at 0, if it is in the @mask.
                The traversal happens in creasing order of indices.
            mask: An iterable of indices to visit. Only windows of these indices
                are visited. It is the caller's responsibility to make sure that
                all indices in this @mask are valid. The default value is None,
                which is interprete as 'all'. i.e., all windows are visited.

        Returns:
            By the time this method returns, the last window is active.

        Raises:
            ScreenArrayError: The mask has invalid indices.
        """
        fullmask = set(range(self.capacity))
        if mask is None:
            mask = fullmask
        else:
            if not set(mask) <= fullmask:
                raise ScreenArrayError("{} is not a subset of {}.".
                        format(mask, fullmask))

        for i in sorted(mask):
            self._do('select {}'.format(i))
            self._do('exec ' + func(i))

        self._do('select {}'.format(self.capacity))

    def _do(self, cmd):
        """Execute screen command in a subshell.

        If self.quiet if True, print the command to stdout in additional to
        issuing it in a subshell.
        """
        cmdstr = 'screen -S {} -X {}'.format(self.session, cmd)
        if not self.quiet:
            print(cmdstr)
        subprocess.check_call(cmdstr, shell = True)

    def __str__(self):
        return '{obj.session}: {obj.height} x {obj.width}'.format(obj = self)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__,
            formatter_class = argparse.RawDescriptionHelpFormatter)

    parser.add_argument('session',
            metavar = 'SESSION',
            type = str,
            help = 'session name to attach to')
    parser.add_argument('height',
            metavar = 'HEIGHT',
            type = int,
            default = 3,
            nargs = '?',
            help = 'height of the table, default = 3')
    parser.add_argument('width',
            metavar = 'WIDTH',
            type = int,
            default = 3,
            nargs = '?',
            help = 'width of the table, default = 3')
    parser.add_argument('-q', '--quiet',
            action = 'store_true',
            help = 'do not print the commands used to make the screen array')

    args = parser.parse_args()
    if args.height <= 0:
        print('HEIGHT ({}) must be a positive integer.'.format(args.height))
        sys.exit(1)
    if args.width <= 0:
        print('WIDTH ({}) must be a positive integer.'.format(args.width))
        sys.exit(1)

    g = ScreenArray(args.session,
            height = args.height,
            width = args.width,
            quiet = args.quiet,
    )
    g.make_array()
