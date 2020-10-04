
import vim
from vimide import utils

SIDEBAR_DEFAULTS = {
    "layout": {
        "location": "vertical topleft",
        "size": 30,
    },
    "plugins": [
        {
            'name': 'nerdtree',
            'open_command': 'NERDTree',
            'size': 50,
            'opens_by_default': 'current'
        },
        {
            'name': 'tagbar',
            'open_command': 'Tagbar',
            'size': 50,
            'opens_by_default': 'belowright',
        }
    ]

}

BOTBAR_DEFAULTS = {
    "layout": {
        "location": "belowright",
        "size": 20,
    },
    "plugins": [
        {
            'name': 'terminal',
            'open_command': 'terminal ++curwin',
            'size': 50,
            'opens_by_default': 'current'
        }
    ]
}

class BaseView(dict):
    def __init__(self, options=None):
        super(BaseView, self).__init__()
        self._layout = options.get('layout') if options else None
        self._plugins = options.get('plugins', []) if options else []
        self._init_area()

    def _init_area(self):
        def is_current():
            location = self._layout.get('location', "")
            return location in ["", "current"]

        command = self._layout.get('custom')
        if not command:
            location = self._layout.get("location", "")
            location = "" if location == "current" else location + " "

            size = self._layout.get('size', 30)
            command = f"{location}{size} new"

        vim.command(command)

        dim = "height" if is_current() or "vert" in location else "width"
        size = int(int(vim.eval(f"win{dim}(0)"))/len(self._plugins))

        counter = 0
        for p in self._plugins:
            command = p.get('open_command')
            if command:
                vim.command(command)
            if 'name' in p:
                self[p['name']] = vim.current.window
            elif counter:
                self["no_name"] = vim.current.window
                counter += 1
            else:
                self["no_name" + counter] = vim.current.window
                counter += 1

        if len(self) > 1:
            for v in self.values():
                with utils.LetCurrentWindow(v):
                    vim.command(f"{size}wincmd _")

    def GoTo(self, name=None):
        if name:
            utils.JumpToWindow(self[name])
        elif len(self):
            for v in self.values():
                utils.JumpToWindow(v)
                break

class CodeView(BaseView):
    """docstring for CodeView"""

    def __init__(self, window):
        super(CodeView,self).__init__()
        self["no_name"] = window


    def _init_area(self):
        pass



class Ide(object):
    """docstring for Ide"""
    def __init__(self):
        self._code = CodeView(vim.current.window)
        self._sidebar = BaseView(SIDEBAR_DEFAULTS)
        self._code.GoTo()
        self._botbar = BaseView(BOTBAR_DEFAULTS)
        self._code.GoTo()

