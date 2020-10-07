
import vim
from vimide import (
        utils,
        defaults,
        baseview)

class CodeView(baseview.BaseView):

    def __init__(self, window):
        super(CodeView,self).__init__(options={'hideable': False})
        self[0] = baseview.LayoutWindow(
                window, window.buffer, window.tabpage)

class BarView(baseview.BaseView):
    def _init_area(self):
        command = self._layout.get('custom')
        if not command:
            location = self._layout.get("location", "current")
            location = "" if location == "current" else location + " "

            size = self._layout.get('size', 30)
            command = f"{location}{size} new"

        vim.command(command)

        dim = "height" if "vert" in location else "width"
        size = int(int(vim.eval(f"win{dim}(0)"))/len(self._plugins))
        print(size)

        for name,p in self._plugins.items():
            opens = p.get('opens_by_default')
            command = p.get('open_command')

            if opens and opens != 'current':
                with utils.RestoreCurrentWindow():
                    vim.command(command)
                    buf = vim.current.buffer
                    vim.command("quit")
                pbuf = vim.current.buffer
                vim.current.buffer = buf
                vim.command(f":bd {pbuf.number}")

            elif command:
                print(command)
                vim.command(command)

            self[name] = baseview.LayoutWindow(
                vim.current.window,
                vim.current.window.buffer,
                vim.current.window.tabpage)

            if name == 'terminal':
                self[name].buffer.options['buflisted'] = False

        if len(self) > 1:
            for _,v in self.items():
                with utils.LetCurrentWindow(v.window):
                    vim.command(f"{size}wincmd _")

        super(BarView,self)._init_area()




class Ide(dict):
    """docstring for Ide"""
    def __init__(self):
        super(Ide,self).__init__()
        self._loading = False
        self._prev_state = None

    def SetupUI(self):
        self._loading = True
        self["code"] = CodeView(vim.current.window)
        for bar,layout in defaults.LAYOUT_DEFAULTS.items():
            with utils.RestoreCurrentWindow():
                self[bar] = BarView(options=layout)
        self._loading = False

    def IsLoading(self):
        for _,l in self.items():
            if l._loading:
                return True
        return self._loading

    def OnWinLeave(self):
        if not self.IsLoading():
            lkey, wkey = self.FindWindow(vim.current.window)
            if lkey is not None and self[lkey]._layout.get('autoclose', False):
                self[lkey].Hide()

        self._prev_state = baseview.LayoutWindow(
                vim.current.window,
                vim.current.buffer,
                vim.current.window.tabpage)


    def FindWindow(self,window=None):
        window = vim.current.window if not window else window
        for lkey,layout in self.items():
            wkey = layout.GetWindowPlugin(window)
            if wkey is not None:
                vim.command(f"let g:return = \"{lkey},{wkey}\"")
                return lkey, wkey
        vim.command(f"let g:return = -1")
        return None, None

    def FindBuffer(self,buf=None):
        buf = vim.current.buffer if not buf else buf
        for lkey,layout in self.items():
            wkey = layout.GetBufferPlugin(buf)
            if wkey is not None:
                vim.command(f"let g:return = \"{lkey},{wkey}\"")
                return lkey, wkey
        vim.command(f"let g:return = -1")
        return None, None

    def GoToWindow(self, name):
        for _,v in self.items():
            if name in v._plugins:
                if v._hidden:
                    with utils.RestoreCurrentWindow():
                        v.Show()
                v.GoTo(name)
                break
        else:
            raise KeyError(f"{name} not in current window list")

    def BufferClose(self, name):
        for lkey, layout in self.items():
            if name in layout:
                vim.command(f"bd! {self[lkey][name].buffer.number}")
                return



