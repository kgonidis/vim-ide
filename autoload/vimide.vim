
function vimide#load()
py3 << EOF
_vim_ide = __import__('vimide', fromlist = ['ide']).ide.Ide()
_vim_ide.SetupUI()
EOF
call airline#extensions#tabline#buflist#invalidate()
augroup vimide#autoclose
    au!
    au WinLeave * py3 _vim_ide.OnWinLeave()
    au BufEnter __Tagbar__* :let w:autoclose=0
augroup END
endfunction

function vimide#where()
py3 << EOF
_vim_ide.Where()
EOF
    return g:return
endfunction

function vimide#goto(name)
py3 << EOF
_vim_ide.GoToWindow(vim.eval("a:name"))
EOF
endfunction

function vimide#hide(layout)
py3 << EOF
_vim_ide[vim.eval("a:layout")].Hide()
EOF
endfunction

function vimide#show(layout)
py3 << EOF
_vim_ide[vim.eval("a:layout")].Show()
EOF
endfunction

function vimide#toggle(layout)
py3 << EOF
_vim_ide[vim.eval("a:layout")].Toggle()
EOF
endfunction

function vimide#delbuf(name)
py3 << EOF
_vim_ide.BufferClose(vim.eval("a:name"))
EOF
endfunction

function vimide#autoload()
    let g:vimide_autoload = 1
endfunction

function vimide#debugpy()
    py3 __import__("vimspector", fromlist=["developer"])
        \.developer.SetUpDebugpy()
endfunction

