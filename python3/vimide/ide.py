
import vim
from vimide import utils
from collections import namedtuple

SIDEBAR_DEFAULTS = {
    "layout": {
        "location": "vertical topleft",
        "vertical": True,
        "size": 30
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
            'open_command': 'execute "Tagbar" | wincmd j',
            'size': 50,
            'opens_by_default': 'belowright',
        }
    ]

}

BOTBAR_DEFAULTS = {
    "layout": {
        "location": "belowright",
        "vertical": False,
        "size": 20
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

LayoutWindow = namedtuple('LayoutWindow', ['window', 'buffer', 'tabpage'])

class BaseView(dict):
    def __init__(self, options=None):
        super(BaseView, self).__init__()
        self._layout = options.get('layout') if options else None
        self._plugins = options.get('plugins', []) if options else []
        self._hidden = True
        self._init_area()

    def _init_area(self):
        def is_current():
            location = self._layout.get('location', "")
            return location in ["", "current"]

        command = self._layout.get('custom')
        if not command:
            location = self._layout.get("location", "current")
            location = "" if location == "current" else location + " "

            size = self._layout.get('size', 30)
            command = f"{location}{size} new"

        vim.command(command)

        dim = "height" if "vert" in location else "width"
        size = int(int(vim.eval(f"win{dim}(0)"))/len(self._plugins))

        for p in self._plugins:
            command = p.get('open_command')

            if command:
                vim.command(command)

            self[p['name']] = LayoutWindow(
                vim.current.window,
                vim.current.window.buffer,
                vim.current.window.tabpage)

        if len(self) > 1:
            for v in self.values():
                with utils.LetCurrentWindow(v.window):
                    vim.command(f"{size}wincmd _")
        self._hidden = False


    def GoTo(self, name=None):
        if name:
            if name in self:
                utils.JumpToWindow(self[name].window)
                return True
        elif len(self):
            for v in self.values():
                utils.JumpToWindow(v.window)
                return True

    def Hide(self):
        for k in self.keys():
            with utils.LetCurrentWindow(self[k].window):
                vim.command("quit")
        self._hidden = True

    def Show(self):
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

        vert = "vert" in location
        dim = "height" if is_current() or vert else "width"
        size = int(int(vim.eval(f"win{dim}(0)"))/len(self._plugins))


        for i,p in enumerate(self._plugins):
            window = vim.current.window
            vim.current.buffer = self[p['name']].buffer
            self[p['name']] = LayoutWindow(
                vim.current.window,
                vim.current.window.buffer,
                vim.current.window.tabpage)
            if i < (len(self._plugins) -1):
                vim.command("belowright new")

        if len(self) > 1:
            for v in self.values():
                with utils.LetCurrentWindow(v.window):
                    vim.command(f"{size}wincmd _")
        self._hidden = False


class CodeView(BaseView):

    def __init__(self, window):
        super(CodeView,self).__init__()
        self[0] = LayoutWindow(
                window, window.buffer, window.tabpage)


    def _init_area(self):
        pass




class Ide(dict):
    """docstring for Ide"""

    def SetupUI(self):
        self["code"] = CodeView(vim.current.window)
        self["sidebar"] = BaseView(SIDEBAR_DEFAULTS)
        self["code"].GoTo()
        self["botbar"] = BaseView(BOTBAR_DEFAULTS)
        self["code"].GoTo()

        # for k,v in self.items():
            # print()
            # print(k)
            # print()
            # for kk,vv in v.items():
                # print(kk,vv)

    def Where(self,window=None):
        window = vim.current.window if not window else window
        for k,v in self.items():
            if window in [lw.window for _,lw in v.items()]:
                vim.command(f"let g:return = \"{k}\"")
                return k
        vim.command(f"let g:return = -1")
        return None

    def GoToWindow(self, name):
        for k,v in self.items():
            if name in [p.get('name', '') for p in v._plugins]:
                if v._hidden:
                    v.Show()
                v.GoTo(name)
                break
        else:
            raise KeyError(f"{name} not in current window list")



