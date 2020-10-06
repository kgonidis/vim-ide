import vim
from vimide import utils
from collections import namedtuple

LayoutWindow = namedtuple('LayoutWindow', ['window', 'buffer', 'tabpge'])

class BaseView(dict):
    def __init__(self, *args, options=None, **kwargs):
        super(BaseView, self).__init__(*args, **kwargs)
        self._layout = options.get('layout', {}) if options else {}
        self._plugins = options.get('plugins', {}) if options else {}
        self._hidden = self._layout.get('hidden', False)
        self._autoclose = self._layout.get('autoclose', False)
        self._hideable = self._layout.get('hideable', True)
        autoload = self._layout.get('autoload', True)
        self._loaded = False
        self._loading = False
        if autoload:
            self._loading = True
            self._init_area()

    def _init_area(self):
        if self._hidden:
            self.Hide()
        self._loading = False
        self._loaded = True

    def GoTo(self, name=None):
        if name:
            if name in self:
                utils.JumpToWindow(self[name].window)
                return True
        elif len(self):
            for v in self.values():
                utils.JumpToWindow(v.window)
                return True

    def GetWindowPlugin(self, window=None):
        window = vim.current.window if not window else window
        for wkey, lwin in self.items():
            if lwin.window == window:
                return wkey

    def GetBufferPlugin(self, buf=None):
        buf = vim.current.buffer if not buf else buf
        for wkey, lwin in self.items():
            if lwin.buffer == buf:
                return wkey

    def Hide(self):
        if not self._hideable:
            return
        for _,lwin in self.items():
            try:
                utils.JumpToWindow(lwin.window)
                vim.command("quit")
            except:
                pass
        self._hidden = True

    def _show(self):
        if not self._loaded:
            self._init_area()
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
            buf = vim.current.buffer
            vim.current.buffer = self[p].buffer
            vim.command(f":bd {buf.number}")
            self[p] = LayoutWindow(
                vim.current.window,
                vim.current.window.buffer,
                vim.current.window.tabpage)

            if p == 'terminal':
                buf = self[p].buffer
                buf.options['buflisted'] = False

            if i < (len(self._plugins) -1):
                vim.command(f":belowright new")

        if len(self) > 1:
            for v in self.values():
                with utils.LetCurrentWindow(v.window):
                    vim.command(f"{size}wincmd _")
        self._hidden = False

    def Show(self):
        self._loading = True
        self._show()
        self._loading = False

    def Toggle(self):
        if self._hidden:
            self.Show()
        else:
            self.Hide()

    def OnLayoutLeave(self):
        print("leaving")

