
# import vim
vim = None
from vimide import utils

class IdeArea(list):
    def __init__(self, init_command=None, windows=[]):
        super(IdeArea, self).__init__(windows)
        self._init_command = init_command
        self.InitArea()

    def InitArea(self):
        if self._init_command:
            vim.command(self._init_command)
            return True
        return False

    def Add(self, commands):
        if not len(self) and not self.InitArea():
            return False

        if vim.current.window not in self:
            self.GoTo()
            if vim.current.window not in self:
                return False

        for com in commands:
            vim.command(com)


    def GoTo(self):
        if len(self):
            utils.JumpToWindow(self[0])



class Sidebar(object):

    """Docstring for Sidebar. """

    def __init__(self, window, tree_enabled=True, sidebar_enabled=True):
        """TODO: to be defined.

        :Docstring for Sidebar.: TODO

        """
        vim.command('NERDTree')
        self.nerd_tree_window = vim.current.window

        pass

class Ide(object):
    """docstring for Ide"""
    def __init__(self):
        code_window = vim.current.window
        vim.command('topleft vertical 30 new')
        sidbar_window = vim.current.window
        self._sidebar = Sidebar(sidbar_window)
        utils.JumpToWindow(code_window)
