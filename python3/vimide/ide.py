
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

    def SetupUI(self):
        self._loading = True
        self["code"] = CodeView(vim.current.window)
        for bar,layout in defaults.LAYOUT_DEFAULTS.items():
            with utils.RestoreCurrentWindow():
                self[bar] = BarView(options=layout)
        self._loading = False

        # vim.command(f":augroup VimIdeWinEnter")
        # vim.command(":au!")
        # vim.command(f":au WinEnter * py3 _vim_ide.OnWinEnter()")
        # vim.command(":augroup END")

        # for lkey, layout in self.items():
            # if lkey == "code":
                # vim.command(f":augroup {lkey}")
                # vim.command(":au!")
                # for wkey,w in layout.items():
                    # vim.command(f"au BufLeave {w.buffer.name} " +
                        # f"py3 _vim_ide.OnBufLeave(\"{lkey}\", \"{wkey}\")")
                # vim.command(":augroup END")
            # else:
                # vim.command(f":augroup {lkey}")
                # vim.command(":au!")
                # for wkey,w in layout.items():
                    # vim.command(f"au BufLeave {w.buffer.name} " +
                        # f"py3 _vim_ide.OnBufLeave(\"{lkey}\", \"{wkey}\")")
                # vim.command(":augroup END")

    def OnWinEnter(self):
        bufs = []
        for b in vim.buffers:
            modtime = vim.eval(f"getbufinfo({b.number})")[0]['lastused']
            bufs.append([modtime, b])
        if len(bufs) <= 1:
            return

        last_buf = sorted(bufs, reverse=True, key=lambda k: k[0])[1]
        thiskey, thiswin = self.FindWindow()
        lastkey, lastwin = self.FindBuffer(last_buf)

        if lastkey is not None and lastkey != thiskey:
            self[lastkey].OnLayoutLeave()

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
                if name == 'tagbar':
                    vim.command("let w:autoclose = 0")
                break
        else:
            raise KeyError(f"{name} not in current window list")

    def BufferClose(self, name):
        for lkey, layout in self.items():
            if name in layout:
                vim.command(f"bd! {self[lkey][name].buffer.number}")
                return



