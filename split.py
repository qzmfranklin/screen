#!/usr/bin/env python3

import math
import subprocess

class ScreenArrayError(Exception):
    pass

class ScreenArray(object):

    def __init__(self, session, *, width = 3, height = 3, quiet = False):
        self.session = session
        self.quiet = quiet
        self.width = width
        self.height = height

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

        if self.height == 1:
            return

        # Make the rest rows.
        for i in range(self.height - 1):
            for j in range(self.width):
                self._do('focus')       #  C-a tab
                self._do('split -v')    #  C-a |
                self._do('screen')      #  C-a c
    
    def visit(self, func, *, mask = None)
        """Visit each window, issue commands for issue window.

        Arguments:
            func: A python function that takes a non-negative integer as
                input and returns a python3 string as output. For example:
                        def foo(index):
                            return 'ls -al /dev/sd{}'.format(index)
                The returned string, @ret is the command issued to the window
                with the @index:
                        screen -S session -X select @index
                        screen -S session -X @ret
                As a final note, @index starts at 0.
            mask: An iterable of indices to visit. Only windows of these indices
                are visited. It is the caller's responsibility to make sure that
                all indices in this @mask are valid. The default value is None,
                which is interprete as 'all'. i.e., all windows are visited.

        Returns:
            By the time this method returns, the last window is active.

        Raises:
            ScreenArrayError: The mask has invalid indices.
        """
        fullmask = set(range(self.width * self.height))
        if mask is None:
            mask = fullmask
        else:
            if not mask <= fullmask:
                raise ScreenArrayError("{} is not a subset of {}.".
                        format(mask, fullmask))

        for i in mask:
            self._do(func(i))

    def _do(self, cmd):
        """Execute screen command in a subshell."""
        cmdstr = 'screen -S {} -X {}'.format(self.session, cmd)
        if not self.quiet:
            print(cmdstr)
        subprocess.check_call(cmdstr, shell = True)

    def __str__(self):
        return '{obj.session}: {obj.height} x {obj.width} >= {obj.capacity}'.format(obj = self)

if __name__ == '__main__':
    g = ScreenArray('beef', width = 5, height = 4, capacity = 20)
    print(g)
    g.set_height(2)
    print(g)
    g.set_height(7)
    print(g)
    g.set_height(2)
    print(g)
    g.set_width(7)
    print(g)
    g.set_width(3)
    g.set_height(3)
